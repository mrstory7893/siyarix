# AI Agent Pipeline

The AI agent pipeline in Siyarix v3.0.0 processes user input through a structured lifecycle of **Plan → Execute → Reflect**, orchestrated by the `AgentCore`. The pipeline supports four operational modes and an autonomous **Observe-Reason-Act** loop for goal-driven operation.

---

## Agent Lifecycle

```
                     ┌──────────────────┐
                     │   User Input     │
                     └────────┬─────────┘
                              ▼
                     ┌──────────────────┐
                     │  IntentRouter    │
                     │  (4-stage:       │
                     │   exact → regex  │
                     │   → keyword → LLM)│
                     └────────┬─────────┘
                              ▼
                     ┌──────────────────┐
                     │  Context Manager │
                     │  (build/compress  │
                     │   context window) │
                     └────────┬─────────┘
                              ▼
                     ┌──────────────────┐
          ┌──────────│  Planner Router  │──────────┐
          ▼          └──────────────────┘          ▼
   ┌─────────────┐                       ┌─────────────────┐
   │ Registry    │                       │ Autonomous      │
   │ Planner     │                       │ Planner (LLM)   │
   │ (template)  │                       │ (dynamic)       │
   └──────┬──────┘                       └────────┬────────┘
          │                                       │
          └──────────────┬────────────────────────┘
                         ▼
                ┌──────────────────┐
                │  PermissionGate  │──→ DLP Engine
                │  (BLOCK/REVIEW/  │
                │   ALLOW)         │
                └────────┬─────────┘
                         ▼
                ┌──────────────────┐
                │  ExecutionEngine │
                │  (plan → steps)  │
                └────────┬─────────┘
                         ▼
                ┌──────────────────┐
                │  Observe-Reason- │
                │  Act Loop        │
                │  (autonomous)    │
                └──────────────────┘
```

---

## Stage 1: Intent Routing

The `IntentRouter` classifies input through four ordered stages:

| Stage | Method | Latency | Description |
|-------|--------|---------|-------------|
| 1 | Exact match | ~0ms | Prefix regex matching against 7+ command patterns |
| 2 | Heuristic | ~1ms | RuleInterpreter with 60+ intent categories |
| 3 | Keyword | ~5ms | Semantic keyword matching with scoring |
| 4 | LLM fallback | ~500ms | AI provider classifies semantically |

Produces an `IntentRoute` with:
- `instruction`: Original input
- `mode`: REGISTRY / AUTONOMOUS / HYBRID / INTERACTIVE
- `category`: TaskCategory value
- `confidence`: 0.0–1.0
- `risk_tier`: LOW / MEDIUM / HIGH
- `requires_confirmation`: Boolean
- `routing_stage`: 1–4
- `metadata`: Extracted targets, tools, flags

---

## Stage 2: Context Building

The **Context Manager** constructs the LLM context window:

- Conversation history (deque, max 100 per agent)
- Knowledge Graph entity summaries
- Current operational phase
- Tool availability from ToolRegistry
- Session metadata (target, mode, findings)
- **Compact** system optimizes context for LLM token limits

Output: A compressed, structured context passed to the planner.

---

## Stage 3: Planning

### Planner Router

Selects the planning strategy based on mode:

```python
if route.mode == "REGISTRY":
    plan = RegistryPlanner.build(intent, target)
elif route.mode == "AUTONOMOUS":
    plan = await AutonomousPlanner.build(intent, context)
elif route.mode == "HYBRID":
    plan = await HybridPlanner.build(intent, context, registry)
elif route.mode == "INTERACTIVE":
    plan = await InteractivePlanner.build(intent, user_input)
```

### RegistryPlanner (Template-Based)

- Uses **PlannerRegistry** to map intents → plan templates
- Looks up tool chains by intent category
- Deterministic, no AI dependency
- Always available as fallback in offline/air-gapped environments

### AutonomousPlanner (LLM-Driven)

- Receives intent + compressed context
- Returns structured `ExecutionPlan` with tool names, ordering, arguments
- Driven by configured AI provider via the ProviderManager
- Supports tool call repair for malformed LLM output

### PlannerRegistry

Maps intents to plan templates:

| Intent Category | Default Plan Template |
|----------------|----------------------|
| `SCAN` | nmap → nuclei → nikto |
| `RECON` | subfinder → httpx → gowitness |
| `EXPLOIT` | searchsploit → metasploit |
| `REPORT` | Aggregate findings → generate report |
| `ENUMERATE` | dirsearch → wpscan → whatweb |

---

## Stage 4: Permission Gating

Every planned step passes through the permission gate:

1. **Syntax Validation**: Length limits, null bytes, shell injection patterns, target format
2. **Danger Analysis**: 38+ signatures for destructive/recon/exploit patterns
3. **DLP Inspection**: Data leak prevention pattern detection

Returns one of:
- `ALLOW` — proceeds without input
- `REVIEW` — requires user confirmation
- `BLOCK` — permanently denied and logged

---

## Stage 5: Execution

The **ExecutionEngine** builds an execution plan from goals:

1. **Validate** plan structure and dependencies
2. **Resolve** dependency ordering into parallel layers
3. **Execute** steps via WorkerPool (bounded async concurrency)
4. **Route** output through tool-specific parsers
5. **Extract** findings into KnowledgeGraph
6. **Handle** errors with exponential backoff + jitter

Three executor types based on mode:

| Executor | Mode | Behavior |
|----------|------|----------|
| `BaseExecutor` | INTERACTIVE | Per-step user confirmation, incremental |
| `RegistryExecutor` | REGISTRY | Deterministic, template-driven, no AI |
| `AutonomousExecutor` | AUTONOMOUS | Full autonomy, loop until objective met |

---

## Stage 6: Observe-Reason-Act Loop (Autonomous Mode)

For `AUTONOMOUS` mode, the system runs an autonomous loop:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Observe    │────▶│    Reason    │────▶│     Act      │
│              │     │              │     │              │
│ • Tool output│     │ • Analyze    │     │ • Execute    │
│ • Env state  │     │ • Update KG  │     │   commands   │
│ • Scan res.  │     │ • Select     │     │ • Run tools  │
│ • Errors     │     │   next action│     │ • Invoke     │
│              │     │ • Check      │     │   sub-agents │
│              │     │   completion │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
        ▲                                         │
        └─────────────────────────────────────────┘
                     (feedback loop)
```

- **Observe**: Collect environment state, tool outputs, scan results, errors
- **Reason**: Analyze findings, update KnowledgeGraph, select next action via LLM
- **Act**: Execute selected commands, run tools, invoke sub-agents via Swarm

Loop terminates when:
- Objective is achieved (verified by LLM reflection)
- Max iteration limit is reached
- User interrupts with Ctrl+C
- Safety gate blocks critical action

---

## Stage 7: Reflection & Results

After execution, the pipeline produces:

| Output | Destination | Format |
|--------|-------------|--------|
| Findings | KnowledgeGraph | In-memory directed graph |
| Report | ReportEngine | MARKDOWN, HTML, JSON, SARIF + CVSS |
| Audit Trail | AuditLogger | Tamper-evident SHA-256 chain |
| Session Log | ChatSession | JSONL tree format |
| Metrics | MetricsCollector | Prometheus-compatible |
| Offline Backup | OfflineStore | SQLite WAL mode |

---

## Streaming Event System

During execution, all pipeline stages emit events through the **EventBus**:

```
EventBus topics:
  intent.routed       → IntentRoute
  context.built       → CompressedContext
  plan.created        → ExecutionPlan
  step.permission     → GateResult
  step.executing      → ExecutionStep
  step.completed      → StepResult
  step.failed         → StepError
  loop.iteration      → ORAIteration
  objective.complete  → FinalResult
```

---

## Autonomous Agent Loop Configuration

```python
loop_config = {
    "max_iterations": 25,
    "max_tokens_per_step": 4096,
    "confirmation_threshold": 0.7,  # confidence below this requires confirmation
    "safety_mode": "strict",         # strict | permissive
    "observation_window": 10,        # recent tool outputs to include
    "reflection_frequency": 5,        # reflect every N iterations
    "stop_conditions": ["objective_achieved", "max_iterations", "safety_trigger"]
}
```
