# AI-Powered Workflows

Siyarix uses AI providers for natural language planning, tool selection, and autonomous execution. The `TaskPlanner` converts user intent into structured execution plans with dependency resolution.

---

## Natural Language Command Interpretation

```bash
siyarix run "scan the network 10.0.0.0/24 for open ports and service versions"
```

The AI planner processes input through:

1. **Intent parsing**: Extract target, parameters, and desired action
2. **Tool selection**: Match intent against 80+ tool capabilities in the registry
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

| Mode | Description |
|------|-------------|
| `registry` | Deterministic planning using tool registry metadata (no AI) |
| `autonomous` | Full AI autonomy — plans and executes without confirmation |
| `hybrid` | AI proposes plans, user approves before execution |
| `interactive` | AI guides interactively, user confirms each step |

---

## Multi-Provider Failover

If the primary AI provider fails:

1. **Circuit breaker** opens after 3 failures in 60 seconds
2. **Next provider** in the preference chain is tried
3. **All remote providers fail** → heuristic fallback activates
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

The `ToolRegistry` maintains metadata for 100+ security tools including capabilities, platforms, and invocation patterns. Auto-discovery scans PATH on startup.

---

## Execution Modes

| Mode | Description |
|------|-------------|
| `integrated` (default) | AI plans, selects tools, executes, and parses results automatically |
| `registry` | Uses tool registry metadata for deterministic planning (no AI) |
| `autonomous` | Full AI autonomy — plans and executes without user confirmation |

---

## Context Management

The AI context window is managed to prevent overflow:

- Conversation history is truncated oldest-first when it exceeds limits
- Tool outputs are summarized rather than included verbatim
- Large result sets are stored in the offline store and referenced by ID

---

## Offline Operation

When no AI provider is available:

- The `NoopProvider` activates automatically
- `RuleInterpreter` handles command parsing via heuristic fallback
- Pattern matching and keyword extraction replace AI-driven planning
- All existing tools remain fully usable
- The Offline Registry provides contextual responses in REPL mode

---

## Supported AI Providers

| Provider | Configuration |
|----------|--------------|
| OpenAI | `siyarix auth set-key openai` |
| Anthropic | `siyarix auth set-key anthropic` |
| Gemini | `siyarix auth set-key gemini` |
| Groq | `siyarix auth set-key groq` |
| Together | `siyarix auth set-key together` |
| OpenRouter | `siyarix auth set-key openrouter` |
| DeepSeek | `siyarix auth set-key deepseek` |
| xAI | `siyarix auth set-key xai` |
| Mistral | `siyarix auth set-key mistral` |
| Perplexity | `siyarix auth set-key perplexity` |
| Cerebras | `siyarix auth set-key cerebras` |
| Fireworks | `siyarix auth set-key fireworks` |
| Azure OpenAI | `siyarix auth set-key azure` |
| HuggingFace | `siyarix auth set-key huggingface` |
| NVIDIA | `siyarix auth set-key nvidia` |
| Moonshot | `siyarix auth set-key moonshot` |
| Minimax | `siyarix auth set-key minimax` |
| ZAI | `siyarix auth set-key zai` |
