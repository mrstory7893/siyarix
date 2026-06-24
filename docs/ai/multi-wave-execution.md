# Multi-Wave Execution & Live Streaming

Siyarix uses a multi-wave execution loop that enables iterative, LLM-driven workflows. Rather than executing a single batch of commands, the system runs multiple waves — each wave's results are analysed by the LLM to determine the next set of commands — enabling autonomous multi-step security operations. Context is carried over between waves, allowing the LLM to build on previous findings progressively.

---

## Execution Flow

```
User request → LLM analyses & plans → Wave 1 executes →
  LLM analyses wave results → Wave 2 (if needed) → ...
  → Final response (up to configurable max waves)
```

---

## Multi-Wave Loop

### LLM-Driven Wave Orchestration (Integrated/Autonomous Modes)

The `LLMEngineMixin._execute_agent()` method in `chat/engine.py` orchestrates the multi-wave loop:

```python
max_waves = self._settings.get("max_waves") or 12
plan = llm_plan

for wave in range(max_waves):
    if not plan or not plan.steps:
        break

    # Execute via AutonomousExecutor with live display
    plan = await agent.executor_autonomous.execute_plan(plan, live_display=True)

    # If cancelled by user, stop
    if plan.status.name == "CANCELLED":
        break

    # Collect outputs for next wave context
    for s in plan.steps:
        result = s.result or {}
        output = (result.get("output") or "").strip()
        all_outputs.append(f"• {cmd_label}:\n{output}\n")

    # Ask LLM: are we done or more work needed?
    if llm_connected:
        wave_goal = (
            f"Original request: {instruction}\n\n"
            f"Completed execution wave {wave + 1}. Results so far:\n\n"
            f"{''.join(all_outputs)}\n\n"
            "Analyse these results. Decide: is the original request fully satisfied?\n"
            "- If YES → set needs_tools=false and provide a final response.\n"
            "- If NO and only 1-2 more commands → set needs_tools=true.\n"
            "- Prefer stopping early with a good summary over endless waves."
        )
        plan = await agent.planner_autonomous.plan(
            wave_goal,
            system_prompt=wave_sys_prompt,
            llm_call=llm_call_fn,
            is_first_call=False,
        )
    else:
        plan = None
```

### Context Carry-Over Between Waves

Each wave's output is collected and fed into the next wave's LLM analysis prompt. The carry-over includes:

- **Original user request** — preserved across all waves
- **All prior command outputs** — accumulated results from every executed wave
- **Execution metadata** — tool used, command run, exit status
- **Wave number** — enables the LLM to gauge progress

The accumulated context helps the LLM make informed decisions about whether to continue, refine, or conclude.

### Wave Decision

The LLM receives the original request plus all outputs from completed waves and produces a new plan:

- **`needs_tools=false`**: Present the final response to the user (done)
- **`needs_tools=true`**: Generate a new plan for the next wave (e.g., found open ports → now scan for vulnerabilities)

The prompt explicitly instructs the LLM to prefer early summarisation over endless probing.

---

### AgentCore Multi-Wave (Core Mode)

`AgentCore.execute_multi_wave()` in `core/__init__.py` provides a structured multi-wave interface for programmatic use:

```python
async def execute_multi_wave(self, goal: AgentGoal, max_waves: int = 5) -> AgentResult:
    all_findings = []
    plan = None
    for wave in range(max_waves):
        wave_context = {
            "wave": wave,
            "previous_findings": all_findings[-20:],
            "goal": goal.description,
        }
        wave_goal = AgentGoal(
            description=goal.description,
            constraints={**goal.constraints, "context": wave_context},
        )
        wave_result = await self.execute_goal(wave_goal, plan)
        all_findings.extend(wave_result.findings)
        if not wave_result.findings:
            break
        if hasattr(self._planner, "plan_next_wave"):
            plan = self._planner.plan_next_wave(wave_result.findings, goal)
        else:
            plan = None
    return AgentResult(goal=goal.description, findings=all_findings, success=True)
```

Key aspects:

- **Context carry-over**: Previous findings (up to 20) are injected into each wave's goal context
- **Early termination**: Breaks if a wave produces no new findings
- **Findings accumulation**: All findings across waves are merged and deduplicated

---

## Live Streaming Display

During execution, command output is streamed line-by-line in real time using the `AutonomousExecutor` with live display enabled.

### Display Behavior

- A single Live panel shows output of the currently focused command
- The display auto-cycles through running commands as they complete
- Coloured borders indicate status:
  - **Cyan**: Still running
  - **Green**: Completed successfully
  - **Red**: Failed (non-zero exit code)
- Panel title shows the command and a status indicator

### Per-Wave Output Display

After each wave completes, summary panels are shown for each command:

```
╭─ ✓ $ nmap -sS -sV -O -Pn example.com ───────────────────╮
│ PORT     STATE  SERVICE    VERSION                       │
│ 22/tcp   open   ssh        OpenSSH 8.9p1                 │
│ 80/tcp   open   http       nginx 1.24.0                  │
│ 443/tcp  open   https      nginx 1.24.0                  │
╰──────────────────────────────────────────────────────────╯
```

---

## Command Review

Before execution begins, each shell command can be reviewed interactively via the permission gate.

### Review Prompt

When command review is enabled (default: on), each command shows a review panel:

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

### Toggle Review

```bash
/command on     # Show review prompt before each command
/command off     # Skip review, run all commands immediately
/command         # Show current review state
```

---

## Wave Summary & Stats

After each wave completes, a bottom stats line shows relevant information:

```
Time: 12.3s | Mode: integrated | Persona: redteam | LLM: connected
```

---

## Safety Integration

Each command in every wave passes through the full safety pipeline:

1. **PermissionGate** — two-stage review: syntax validation followed by danger analysis (blocks critical, flags high/medium for review)
2. **InputValidator** — rejects injection patterns (shell metacharacters, path traversal, null bytes)
3. **DLPEngine** — strips secrets and PII from output
4. **ShellReview** — interactive prompt before execution (edit/run/step/cancel)
5. **Orphan process tracking** — ensures cleanup on timeout or user interrupt

---

## CLS Pre-Execution (Integrated Mode)

Before the LLM planning phase in integrated mode, the `LearningSystem` (CLS) may execute high-confidence cached skills (≥ 80% confidence) to provide rich base context. Results from these pre-executed steps are fed into the LLM's first-wave prompt, potentially reducing the number of waves needed.

---

## Adversarial Review

Before execution, the plan is reviewed by the `AdversarialTester` (via `chat/stubs.py`) which flags potentially dangerous or suspicious patterns:

```
┌──────────────────────────────────────────────────────┐
│ 🔍 Adversarial Review (3 findings) — 1 critical      │
│                                                      │
│ 🔴 [CRITICAL] Command uses full disk wipe patterns   │
│    Suggestion: Consider using safe alternatives       │
│ ⚠ [HIGH] Command may expose sensitive data           │
│    Suggestion: Review command parameters              │
└──────────────────────────────────────────────────────┘
```

---

## Related Modules

| Module | Path | Purpose |
|--------|------|---------|
| `LLMEngineMixin._execute_agent` | `src/siyarix/chat/engine.py:619` | Multi-wave execution orchestrator with context carry-over |
| `AgentCore.execute_multi_wave` | `src/siyarix/core/__init__.py:286` | Structured multi-wave execution for programmatic use |
| `AutonomousExecutor.execute_plan` | `src/siyarix/executor_autonomous.py` | Live-display execution engine |
| `AutonomousPlanner.plan` | `src/siyarix/planner_autonomous.py` | LLM-driven planner for wave analysis and planning |
| `safe_run_async_stream` | `src/siyarix/subprocess_utils.py` | Async subprocess with line-by-line streaming |
| `ShellReview` | `src/siyarix/shell_review.py` | Interactive command review (edit/run/step/cancel) |
| `PermissionGate` | `src/siyarix/permission_gate.py` | Two-stage syntax + danger check |
