# Interaction Modes

Siyarix v3.0.0 supports multiple interaction modes selected automatically by the **ModeDispatcher** based on the `LaunchContext`. Each mode provides a different level of autonomy, interactivity, and output formatting. The **OutputEngine** supports 8 output formats with 12 built-in themes, the **Branding** system applies consistent visual identity, and **Webhooks** enable external integration.

---

## Mode Dispatcher

The `ModeDispatcher` evaluates a `LaunchContext` to select the appropriate mode:

| Context Trigger | Mode | Description |
|----------------|------|-------------|
| No arguments, TTY available | `InteractiveShell` | CLI REPL with chat |
| No arguments, piped stdin | `AIConversational` | Non-interactive chat from pipe |
| Command + arguments | `DirectCommand` | One-shot NL execution |
| `--goal` flag | `AutonomousAgent` | Goal-driven autonomous loop |
| `--workflow` flag | `WorkflowAutomation` | DAG pipeline execution |
| `--mode autonomous` | `AutonomousAgent` | Force autonomous mode |
| `--mode registry` | `RegistryMode` | Force deterministic mode |
| `--mode hybrid` | `HybridMode` | Force AI + confirmation mode |
| `--mode interactive` | `InteractiveShell` | Force interactive mode |
| `--wizard` flag | `GuidedWizard` | 12-step onboarding wizard |
| `--dashboard` flag | `TUIDashboard` | Real-time TUI dashboard |
| `--team` flag | `TeamCollaboration` | Multi-user shared session |
| `--batch` flag | `HeadlessAPI` | Batch/non-interactive execution |

### Selection Priority

```
1. No TTY → HeadlessAPI
2. --wizard → GuidedWizard
3. --goal → AutonomousAgent
4. --mode → Force specified mode
5. --workflow → WorkflowAutomation
6. --dashboard → TUIDashboard
7. --team → TeamCollaboration
8. --batch → HeadlessAPI
9. Single instruction → DirectCommand
10. TTY available → InteractiveShell
11. Fallback → AIConversational
```

---

## Mode Reference

### 1. InteractiveShell

Full-featured CLI with REPL, command history, tab completion, and themed output.

```bash
siyarix                          # Launches REPL
siyarix scan 10.0.0.1          # One-shot command (DirectCommand)
```

- Command history via SessionKernel
- Tab completion for tools, flags, targets
- Slash commands (`/help`, `/mode`, `/session`, `/export`)
- Real-time streaming output
- Ctrl+C cancellation, Ctrl+C x2 emergency exit

### 2. AIConversational

Multi-turn chat assistant with context retention, branching, and AI planning.

```bash
echo "scan my network" | siyarix   # Piped input
siyarix                            # Default: chat REPL
```

- Multi-turn context via Conversation History (deque maxlen=100)
- Slash commands for session management
- Branching support via ChatSession (JSONL tree)
- AI-driven planning with user confirmation
- Context window optimization via Compact system

### 3. DirectCommand

Natural language one-shot execution. Converts input to structured plan and executes immediately.

```bash
siyarix run "scan 10.0.0.1 for open ports"
siyarix "enumerate services on example.com"
```

- IntentRouter classifies input
- Mode determined by risk tier (MEDIUM/HIGH → confirmation)
- Results displayed via OutputEngine

### 4. AutonomousAgent

Goal-driven reasoning loop with full autonomy.

```bash
siyarix agent "enumerate the network and find vulnerabilities"
siyarix --goal "compromise the target and extract flags"
```

- Observe-Reason-Act loop (max iterations configurable)
- AutonomousPlanner with LLM-driven decision making
- Swarm multi-agent orchestration for complex goals
- PermissionGate in minimal mode (BLOCK only, no REVIEW)
- Continuous progress reporting via EventBus streaming

### 5. RegistryMode

Deterministic, template-driven execution with no AI dependency.

```bash
siyarix --mode registry scan 10.0.0.1
```

- Uses RegistryPlanner + PlannerRegistry
- No AI provider required — fully offline capable
- PermissionGate in full mode (BLOCK + REVIEW + ALLOW)
- Output via OutputEngine with structured formatting

### 6. HybridMode

AI-guided planning with user confirmation at each step.

```bash
siyarix --mode hybrid "scan and exploit 10.0.0.1"
```

- AutonomousPlanner suggests plan
- PermissionGate in full mode (every step reviewed)
- User can modify/approve/reject each step
- Falls back to RegistryPlanner if AI unavailable

### 7. WorkflowAutomation

DAG pipeline execution from a YAML/JSON workflow file.

```bash
siyarix workflow run assessment.yaml
siyarix --workflow pipeline.json
```

- CommandPipeline executor
- Step chaining with dependency resolution
- Variable interpolation (`$target`, `{step.output}`)
- Conditional execution
- Parallel step execution within layers

### 8. TUIDashboard

Rich terminal dashboard showing real-time security status.

```bash
siyarix dashboard
siyarix security dashboard
```

### 9. GuidedWizard

12-step interactive onboarding wizard for new users.

```bash
siyarix --wizard
```

- Provider configuration
- Tool discovery and installation
- Credential setup
- Theme and branding selection
- Workflow template creation

### 10. TeamCollaboration

Multi-user session with shared context.

```bash
siyarix --team session-123
```

- Shared ChatSession with branching
- Webhook-based event broadcasting
- Shared KnowledgeGraph

### 11. HeadlessAPI

Non-interactive mode for CI/CD pipelines and programmatic access.

```bash
siyarix --batch commands.txt
echo "scan target" | siyarix
curl -X POST -d '{"command":"scan 10.0.0.1"}' http://localhost:8080/api/execute
```

- All output via JSON/JSONL (machine-parseable)
- JWT authentication for API mode
- HealthChecker endpoint for monitoring

---

## OutputEngine

8 output formats with 12 built-in themes:

### Output Formats

| Format | Use Case | Command |
|--------|----------|---------|
| `table` | Terminal display (default) | `--output table` |
| `json` | Machine parsing, API responses | `--output json` |
| `jsonl` | Streaming, log processing | `--output jsonl` |
| `yaml` | Configuration, human-readable data | `--output yaml` |
| `csv` | Spreadsheet import | `--output csv` |
| `markdown` | Documentation, reports | `--output markdown` |
| `html` | Web reports, dashboards | `--output html` |
| `quiet` | Minimal output (exit code only) | `--output quiet` |

### Themes

12 themes controlling color, typography, and layout:

| Theme | Style | Best For |
|-------|-------|----------|
| `default` | Siyarix brand colors | General use |
| `dark` | High-contrast dark | Night ops |
| `light` | Clean light theme | Documentation |
| `matrix` | Green-on-black | Aesthetic |
| `cyber` | Neon cyan/pink | Demos |
| `minimal` | Monochrome, minimal | Logging |
| `dracula` | Dracula palette | Dark mode users |
| `nord` | Nord palette | Arctic theme |
| `solarized` | Solarized light/dark | Readability |
| `monokai` | Monokai palette | Code-heavy output |
| `github` | GitHub-style | Sharing |
| `none` | No styling | Piped output |

### Branding

The Branding system applies consistent visual identity:

```python
brand = Branding(theme="cyber")
brand.apply(output)  # Applies colors, logos, headers, footers
```

- Session header with logo, version, timestamp
- Themed progress bars and spinners
- Consistent color coding (info/success/warning/error/danger)
- Output footer with summary statistics

### ShellReview

The `ShellReview` system provides command safety review with colored output:

- Syntax highlighting for commands
- Danger level indicators (🟢 ALLOW / 🟡 REVIEW / 🔴 BLOCK)
- Suggested alternatives for BLOCKed commands
- Before-execution summary with estimated impact

### PluginLoader

Dynamic plugin discovery for custom commands and modes:

```python
plugin = PluginLoader.discover("custom_mode")
plugin.register(dispatcher)  # Adds new mode to ModeDispatcher
```

- Scan `~/.siyarix/plugins/` for Python plugins
- Register new modes, tools, output formats
- Hook into EventBus for lifecycle events

---

## CommandPipeline

Chaining commands in DAG pipelines:

```yaml
# pipeline.yaml
name: "Full Assessment"
steps:
  - id: recon
    tool: nmap
    target: ${TARGET}
    flags: -sV -sC
    output: nmap.xml

  - id: vuln_scan
    tool: nuclei
    depends_on: [recon]
    input: ${recon.output}
    flags: -severity critical,high

  - id: web_scan
    tool: nikto
    depends_on: [recon]
    target: http://${TARGET}
    flags: -ssl

  - id: report
    tool: report
    depends_on: [vuln_scan, web_scan]
    format: html
    output: assessment.html
```

---

## Webhooks

Webhook system for external integration:

| Event | Payload | Trigger |
|-------|---------|---------|
| `session.started` | Session metadata | Session begins |
| `step.completed` | Step result | Each execution step |
| `finding.discovered` | Finding object | New finding added to KG |
| `objective.complete` | Goal + results | Autonomous agent completes |
| `gate.blocked` | Blocked command + reason | PermissionGate blocks command |
| `error` | Error details | Any unhandled error |
| `pipeline.complete` | Pipeline results | Workflow automation finishes |

```json
POST /webhook/endpoint
{
  "event": "finding.discovered",
  "data": {
    "cve": "CVE-2024-1234",
    "severity": "critical",
    "host": "10.0.0.1",
    "service": "Apache 2.4.41"
  },
  "session_id": "sess-123",
  "timestamp": "2026-06-17T12:00:00Z"
}
```

---

## Component Relationships

```
LaunchContext
    │
    ▼
ModeDispatcher
    │
    ├── InteractiveShell ──→ EventBus ──→ Streaming Event System
    ├── AIConversational  ──→ ChatSession (branching, JSONL tree)
    ├── DirectCommand     ──→ IntentRouter → Planner → Gate → Engine
    ├── AutonomousAgent   ──→ Observe-Reason-Act Loop → Swarm
    ├── RegistryMode      ──→ RegistryPlanner → RegistryExecutor
    ├── HybridMode        ──→ AutonomousPlanner + Gate review
    ├── WorkflowAutomation──→ CommandPipeline → Engine
    ├── TUIDashboard      ──→ HealthChecker + MetricsCollector
    ├── GuidedWizard      ──→ 12-step onboarding
    ├── TeamCollaboration ──→ Webhooks + shared Session
    └── HeadlessAPI       ──→ REST API + JWT + JSON output
           │
           ▼
    OutputEngine
       │
       ├── Formats: table, json, jsonl, yaml, csv, markdown, html, quiet
       ├── Themes: default, dark, light, matrix, cyber, minimal, ...
       └── Branding: logo, colors, headers, footers
```
