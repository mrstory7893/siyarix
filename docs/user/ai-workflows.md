# AI-Powered Workflows

Siyarix uses AI providers for natural language planning, tool selection, and autonomous execution. The execution engine converts user intent into structured execution plans with dependency resolution.

---

## Natural Language Command Interpretation

```bash
siyarix run "scan the network 10.0.0.0/24 for open ports and service versions"
```

The execution engine processes input through:

1. **Intent parsing**: Extract target, parameters, and desired action
2. **Tool selection**: Match intent against tool capabilities in the registry
3. **Plan construction**: Build an execution DAG with parallel dependencies
4. **Execution**: Run steps in topological order
5. **Result aggregation**: Collect and present structured findings

---

## Goal-Driven Autonomous Agent

```bash
siyarix agent "enumerate all subdomains, find live hosts, scan for vulns, and report"
```

The agent uses an Observe-Reason-Act loop to decompose complex objectives.

### Agent Modes

| Mode | CLI Flag | Description |
|------|----------|-------------|
| `REGISTRY` | `--mode offline` | Deterministic planning using tool registry metadata (no AI) |
| `AUTONOMOUS` | `--mode autonomous` | Full AI autonomy — plans and executes without confirmation |
| `HYBRID` | `--mode integrated` | AI proposes plans with integrated execution |

---

## Multi-Provider Failover

If the primary AI provider fails:

1. **Circuit breaker** opens after 3 failures in 60 seconds
2. **Next provider** in the preference chain is tried
3. **All remote providers fail** → heuristic fallback via RegistryPlanner activates
4. **Graceful degradation** — commands still execute without AI planning

Configure provider preference order:

```bash
siyarix config set provider_preference '["openai", "anthropic", "gemini"]'
```

---

## Prompt Architecture

AI prompts are constructed from:

- **System context**: Platform, available tools, session state
- **User input**: Natural language or structured command
- **Conversation history**: Multi-turn context management
- **Safety constraints**: Permission gates, forbidden commands
- **Persona instructions**: Behavior profile (red team, blue team, etc.)

---

## Tool Selection

The AI selects tools based on:

1. **Capability**: What the tool does (port scan, vulnerability check, etc.)
2. **Availability**: Is the tool installed on PATH?
3. **Platform**: Does it work on the current OS?
4. **Safety**: Is the tool appropriate for the current persona/safe mode?

The `ToolRegistry` maintains metadata for discovered security tools including capabilities, platforms, and invocation patterns. Auto-discovery scans PATH on startup.

---

## Execution Modes

| Mode | Description |
|------|-------------|
| `integrated` (default) | AI plans, selects tools, executes, and parses results automatically |
| `offline` / `registry` | Uses tool registry metadata for deterministic planning (no AI) |
| `autonomous` | Full AI autonomy — plans and executes without user confirmation |

---

## Context Management

The AI context window is managed to prevent overflow:

- Conversation history is truncated oldest-first when it exceeds limits
- Tool outputs are summarized rather than included verbatim
- Large result sets are stored in the offline store and referenced by ID

---

## Offline Operation

When no AI provider is available or `--mode offline` is used:

- The `RegistryPlanner` handles command parsing via heuristic and pattern matching
- The `OfflineStore` provides contextual responses in REPL mode
- All existing tools remain fully usable
- `offline_instruction_hint()` and `no_provider_message()` provide user guidance

---

## Supported AI Providers

| Provider | Configuration |
|----------|--------------|
| OpenAI | `siyarix auth set-key openai --key sk-...` |
| Anthropic | `siyarix auth set-key anthropic --key sk-ant-...` |
| Gemini | `siyarix auth set-key gemini --key AIz...` |
| Groq | `siyarix auth set-key groq --key ...` |
| Together | `siyarix auth set-key together --key ...` |
| OpenRouter | `siyarix auth set-key openrouter --key ...` |
