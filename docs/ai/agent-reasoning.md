# Agent Reasoning Pipeline

The agent reasoning pipeline transforms user objectives into executed actions through a **Planner Router** architecture that dispatches requests to either an LLM-driven planner or a heuristic registry planner depending on the execution mode. The system supports an **Observe–Reason–Act–Reflect** loop in autonomous mode and deterministic template-based planning in registry/offline mode.

---

## Planner Architecture

Siyarix uses a two-planner system coordinated by a unified `Planner` router:

```
User Request
    │
    ▼
┌─────────────────────────────────────────┐
│            Planner Router               │
│  (src/siyarix/planner.py)              │
│                                         │
│  mode == "autonomous" ──► AutonomousPlanner │
│  mode == "registry"   ──► RegistryPlanner   │
│  mode == "offline"    ──► RegistryPlanner   │
│  mode == "integrated" ──► try Autonomous →   │
│                            fallback Registry  │
└─────────────────────────────────────────┘
```

### AutonomousPlanner

`AutonomousPlanner` (in `planner_autonomous.py`) is a pure LLM-driven planner with no heuristic fallback. The LLM is responsible for verifying tool availability, installing missing tools, and constructing correct shell commands.

Key design features:

- **Session-aware token optimisation**: Tool schemas are sent only on the first call of a session. Subsequent calls use a compact prompt.
- **Multi-format response parsing**: The planner parses LLM responses from JSON, YAML, Markdown code blocks, XML tags, and raw text with heuristic conversational filtering.
- **OpenAI tool calling support**: When available, structured tool calls (`tool_calls`) are preferred over free-form text responses.
- **`execute_plan` function schema**: A structured function definition is passed to the LLM to constrain output to a validated format.

```python
plan = await autonomous_planner.plan(
    goal="scan 10.0.0.1",
    llm_call=llm_call_fn,
    tool_schemas=tool_dicts,
    available_tools=tool_names,
    history=conversation_history,
    is_first_call=True,
)
```

### RegistryPlanner

`RegistryPlanner` (in `planner_registry.py`) is a deterministic heuristic planner that operates with no LLM dependency. It uses:

- **Inverted keyword index** — maps user request keywords to tool names
- **Template-based workflow generation** — 25+ predefined DAG templates (recon_full, web_audit, network_scan, cloud_audit, vuln_scan, dns_recon, ad_assessment, linux_privesc, etc.)
- **Intent extraction** — `NaturalLanguageParser` extracts intent and target from natural language
- **Tool alternatives** — fallback chains when a tool is unavailable (e.g., nmap → masscan → rustscan)

```python
plan = registry_planner.plan(
    goal="scan 10.0.0.1",
    available_tools=tool_names,
)
```

---

## Execution Modes

`AgentCore` (in `core/__init__.py`) supports four execution modes:

| Mode | Planner | Executor | LLM Required |
|------|---------|----------|-------------|
| `REGISTRY` | RegistryPlanner | RegistryExecutor | No |
| `AUTONOMOUS` | AutonomousPlanner | AutonomousExecutor | Yes |
| `HYBRID` | AutonomousPlanner → RegistryPlanner | Both | Optional |
| `INTERACTIVE` | RegistryPlanner | RegistryExecutor with user approval | No |

### Observe–Reason–Act–Reflect Loop (Autonomous Mode)

The `LLMEngineMixin._execute_agent()` method implements a multi-turn reasoning loop with the AutonomousPlanner:

```
while objective_incomplete and iterations < max_waves:
    # Observe
    state = collect_environment_state()
    findings = previous_execution_results

    # Reason
    analysis = llm_analyses_results(wave_outputs)
    next_plan = autonomous_planner.plan(analysis)

    # Act
    result = executor_autonomous.execute_plan(next_plan)
    context.add_history(result)

    # Reflect
    if result.indicates_new_targets:
        objectives.add(result.new_targets)
```

### 1. Observe

The agent collects all available context:

- **Environment state**: OS, shell type, available tools, current working directory
- **Session state**: conversation history, execution results from previous waves
- **Target context**: user-specified target (IP, domain, URL) injected into instructions
- **Tool availability**: results from `ToolRegistry` scan, checked via `ToolAvailabilityContext`
- **CLS pre-execution**: High-confidence cached skills may be executed before the LLM call to provide rich base context

### 2. Reason

The LLM receives a structured prompt containing:

```
Persona Preamble (optional) + System Prompt + Platform Context +
Conversation History + Tool Schemas + User Goal
```

It returns a structured plan via JSON or tool calls:

```python
{
    "needs_tools": True,
    "reasoning": "Step-by-step analysis of the request",
    "response": "Direct answer when needs_tools=false, or synthesis post-execution",
    "steps": [
        {
            "tool": "",
            "command": "nmap -sV -p 1-1000 10.0.0.1",
            "description": "Port scan target with service detection"
        }
    ]
}
```

The AutonomousPlanner's `_parse_llm_response()` method supports multiple response formats:

1. Native `tool_calls` (structured function arguments)
2. JSON with `needs_tools` / `steps` fields
3. YAML with matching fields
4. Markdown code blocks (extracted as raw commands)
5. XML tags (`<function=name>...</function>`)
6. Direct raw text (filtered heuristically for conversational vs. command content)

### 3. Act

Commands from the LLM plan are executed per wave:

```python
for wave in range(max_waves):
    if not plan or not plan.steps:
        break
    plan = await executor_autonomous.execute_plan(plan, live_display=True)
```

Each command passes through:

1. **PermissionGate** — two-stage review: syntax validation → danger analysis
2. **Input validation** — `InputValidator` checks injection patterns (shell metacharacters, path traversal, null bytes)
3. **Shell review** — `review_and_confirm()` interactive prompt (edit/run/step/cancel) when enabled
4. **Execution** — via `safe_run_async_stream` with timeout, line-by-line output capture, and orphan process tracking
5. **DLP redaction** — `DLPEngine` strips secrets, API keys, tokens from output
6. **Secret redaction** — `SecretRedactor` handles 25+ credential patterns

### 4. Reflect

After each wave, the LLM receives all command outputs and decides whether to:

- **Continue** (`needs_tools=true`): Generate a new plan for the next wave
- **Conclude** (`needs_tools=false`): Synthesize findings into a final response

Up to **12 waves** execute per instruction by default (configurable via `max_waves` setting).

---

## Tool Call Repair

When an LLM outputs tool calls as plain text instead of structured JSON, `ToolCallRepair` parses and promotes them to native format:

```python
from siyarix.tool_call_repair import (
    promote_to_native_tool_calls,
    parse_plain_text_tool_calls,
    has_plain_text_tool_calls,
)
```

### Supported Syntaxes

| Syntax | Example |
|--------|---------|
| Bracket | `[nmap]{"target": "10.0.0.1", "flags": "-sV"}` |
| XML | `<function=nmap><parameter=target>10.0.0.1</parameter></function>` |
| Function call | `function_call: {"name": "nmap", "args": {...}}` |
| Closing markers | `[END_TOOL_REQUEST]`, `[/tool]`, `[/function]`, `<\|call\|>` |

### Fuzzy Name Matching

When `fuzzy=True`, tool names are matched with Levenshtein distance ≤ 2, supporting:

- Exact match
- Case-insensitive match
- Substring match
- Typo tolerance (edit distance ≤ 2)

---

## Shell Review

`shell_review.py` provides interactive review of LLM-generated shell commands:

```python
from siyarix.shell_review import review_and_confirm, review_command, ReviewDecision

# Returns edited command or None if cancelled
result = review_and_confirm("nmap -sV 10.0.0.1", tool="nmap", reason="Port scan")
```

The review prompt:

```
╭──────────────── Command Execution Review ─────────────────╮
│ Tool: raw                                                 │
│ Reason: Raw shell command from LLM plan                   │
│                                                           │
│ nmap -sS -sV -O -Pn example.com                           │
╰───────────────────────────────────────────────────────────╯
Review command [edit/run/step/cancel] (run):
```

| Choice | Effect |
|--------|--------|
| `run` | Execute the command as-is |
| `edit` | Edit the command before execution |
| `step` | Execute but step through one at a time |
| `cancel` | Skip/cancel this command |

Auto-approves all commands in non-TTY/CI mode to prevent blocking.

---

## Heuristic Fallback (Registry Mode)

When no LLM provider is available, the `RegistryPlanner` engine provides deterministic planning using templates and keyword matching:

```
Input: "scan 10.0.0.1"
  → Extract intent: "scan"
  → Extract target: "10.0.0.1"
  → Match template: "recon_full" or "network_scan"
  → Build multi-step plan with nmap, whatweb, gobuster, subfinder, amass, nuclei
  → Return structured ExecutionPlan
```

Patterns are defined with 400+ multi-word intent matches across red team, blue team, forensics, cloud, container, and compliance domains.

### Template-Based Workflows

Pre-built workflow templates include:

| Template | Steps |
|----------|-------|
| `recon_full` | nmap → whatweb → gobuster → subfinder → amass → nuclei |
| `web_audit` | curl → whatweb → nuclei → ffuf → wpscan → nikto |
| `network_scan` | nmap full TCP → nmap service → dig → whois → masscan |
| `vuln_scan` | nuclei → nikto → wpscan → sqlmap |
| `ad_assessment` | nmap DC ports → smb-protocols → ldap-rootdse → krb5-enum-users |
| `linux_privesc` | uname → find SUID → find writable → cat cron |
| `dns_recon` | dig ANY → subfinder → amass → whois |
| `cloud_audit` | curl → whatweb → dig ANY → openssl |

---

## Dependency Resolution & Parallel Execution

Steps are organized into layers for execution:

```
Layer 1: Recon (no dependencies)
Layer 2: Scan (depends on recon results)
Layer 3: Enumerate (depends on scan results)
Layer 4: Vuln Scan (depends on enumerate results)
Layer 5: Report (depends on all previous)
```

Independent steps within the same layer execute concurrently via `asyncio.gather`. Dependency ordering is determined by the plan type (`SEQUENTIAL` or `DAG`).

---

## Result Synthesis

After all waves complete, the agent:

1. **Deduplicates findings** — MD5-hash based on (target, port, CVE, severity)
2. **Correlates related findings** across tools
3. **Assigns severity** (Critical/High/Medium/Low/Info)
4. **Generates summary** with completion statistics
5. **Ingests findings** into the knowledge graph for persistent analysis

---

## Validation & Recovery

The `Validator` class (`validators.py`) provides step-level validation and recovery planning:

```python
from siyarix.validators import Validator, RecoveryAction, RecoveryPlan

validator = Validator()
results = await validator.validate_plan(plan.steps)
# If a step fails:
recovery = await validator.plan_recovery(failed_step, error)
```

Recovery actions include:

| Action | Behavior |
|--------|----------|
| `RETRY` | Retry with modified arguments (e.g., add `-Pn` for filtered ports) |
| `RETRY_ALTERNATIVE` | Try an alternative tool (e.g., nuclei → nikto) |
| `SKIP` | Skip the step |
| `ABORT` | Abort entire plan |
| `DEGRADE` | Degrade execution mode |

---

## Related Modules

| Module | Path | Purpose |
|--------|------|---------|
| `Planner` | `src/siyarix/planner.py` | Unified planner router — dispatches by mode |
| `AutonomousPlanner` | `src/siyarix/planner_autonomous.py` | LLM-driven planner with session-aware optimisation |
| `RegistryPlanner` | `src/siyarix/planner_registry.py` | Heuristic planner with templates and keyword index |
| `AgentCore` | `src/siyarix/core/__init__.py` | Central orchestrator with mode-aware execution |
| `LLMEngineMixin` | `src/siyarix/chat/engine.py` | Agent loop with multi-wave LLM-driven planning |
| `ToolCallRepair` | `src/siyarix/tool_call_repair.py` | Plain-text tool call parsing and promotion |
| `ShellReview` | `src/siyarix/shell_review.py` | Interactive command review before execution |
| `Validator` | `src/siyarix/validators.py` | Step validation and recovery planning |
| `ToolRegistry` | `src/siyarix/registry.py` | Tool discovery and capability indexing |
| `ToolCapabilityGraph` | `src/siyarix/tool_graph.py` | Tool chaining and similarity graph |
| `ToolAvailability` | `src/siyarix/tool_availability.py` | Pre-execution availability evaluation |
| `DangerAnalyzer` | `src/siyarix/security_hardening.py` | Command danger classification |
| `CompactionEngine` | `src/siyarix/compaction.py` | Context window compaction for long histories |
