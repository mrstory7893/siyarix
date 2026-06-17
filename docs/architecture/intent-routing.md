# Intent Routing

The `IntentRouter` is a 4-stage semantic routing pipeline that classifies user input, determines risk level, selects the appropriate execution mode, and extracts structured parameters. It works in conjunction with the **NLP Engine** for zero-dependency semantic parsing and the **PlannerRegistry** for intent-to-template mapping.

---

## Architecture

```
User Input
    │
    ▼
┌────────────────────────────────────────────┐
│              IntentRouter                   │
│                                            │
│  Stage 1: Exact Pattern Match  ──→ Route   │
│  Stage 2: Heuristic           ──→ Route   │
│  Stage 3: Keyword Similarity  ──→ Route   │
│  Stage 4: LLM Fallback        ──→ Route   │
│             │                              │
│             ▼                              │
│       IntentRoute                          │
│  (mode, category, confidence, risk_tier,   │
│   requires_confirmation, routing_stage,    │
│   metadata)                                │
└────────────────────────────────────────────┘
    │
    ├──→ Mode Dispatcher (selects REGISTRY / AUTONOMOUS / HYBRID / INTERACTIVE)
    ├──→ NLP Engine (semantic parsing, entity extraction)
    └──→ PlannerRegistry (intent → plan template)
```

---

## Routing Stages

### Stage 1: Exact Pattern Match (~0ms)

Predefined regex patterns matched against the beginning of user input:

| Pattern | Category | Intent | Example |
|---------|----------|--------|---------|
| `^scan\s+(.+)$` | SCAN | `scan_target` | `scan 10.0.0.0/24` |
| `^recon\s+(.+)$` | RECON | `reconnaissance` | `recon example.com` |
| `^exploit\s+(.+)$` | EXPLOIT | `exploit_target` | `exploit 10.0.0.1` |
| `^analyze\s+(.+)$` | ANALYZE | `analyze_findings` | `analyze results` |
| `^report\s*(.*)$` | REPORT | `generate_report` | `report --format html` |
| `^dashboard\s*(.*)$` | MONITOR | `dashboard_view` | `dashboard` |
| `^wizard\s*(.*)$` | CONFIG | `onboarding_wizard` | `wizard` |
| `^agent\s+(.+)$` | AGENT | `autonomous_agent` | `agent "enumerate network"` |
| `^workflow\s+(.+)$` | WORKFLOW | `workflow_execute` | `workflow run pipeline.yaml` |
| `^chat\s*(.*)$` | CHAT | `conversational` | `chat` |

Confidence: `1.0` — immediate route without further stages.

### Stage 2: Heuristic Interpretation (~1ms)

The `RuleInterpreter` applies 60+ intent patterns across 6 shell/command types to match natural language input against known command categories:

- Pattern matching against common security operations phrasing
- Shell type detection (cmd, powershell, sh, bash, zsh, fish)
- Extraction of implicit targets, ports, and flags
- Context-aware disambiguation based on session state

Confidence: `0.7–0.95` depending on pattern specificity.

### Stage 3: Keyword Similarity (~5ms)

Semantic keyword matching with scoring:

1. Tokenize input into significant keywords
2. Score against known intent category keyword vectors
3. Apply TF-IDF-like weighting for rare vs common terms
4. Return highest-scoring intent above `SIMILARITY_THRESHOLD`

```python
@dataclass
class KeywordMatch:
    intent: str
    confidence: float          # 0.0–1.0
    matched_keywords: list[str]
    extracted_targets: list[str]
```

Confidence: `0.5–0.85` depending on term overlap.

### Stage 4: LLM Fallback (~500ms)

When stages 1–3 fail to produce a confident match (below `CONFIDENCE_THRESHOLD=0.5`), the configured AI provider classifies the instruction semantically:

1. Send input + available intent categories to LLM
2. LLM returns structured classification (intent, parameters, confidence)
3. Validate response structure via `ToolCallRepair` if malformed

Confidence: `0.3–0.95` depending on LLM performance.

---

## IntentRoute Output

```python
@dataclass
class IntentRoute:
    instruction: str                    # Original user input
    mode: str                           # REGISTRY | AUTONOMOUS | HYBRID | INTERACTIVE
    category: TaskCategory              # SCAN | RECON | EXPLOIT | REPORT | etc.
    confidence: float                   # 0.0–1.0
    risk_tier: RiskTier                 # LOW | MEDIUM | HIGH | CRITICAL
    requires_confirmation: bool         # Whether user must confirm
    routing_stage: int                  # 1 | 2 | 3 | 4
    metadata: dict                      # Extracted targets, tools, flags, params
```

---

## NLP Engine

The **NLP Engine** provides zero-dependency semantic parsing for intent extraction:

```python
nlp = NPLEngine()
parse_result = nlp.parse("scan 10.0.0.1 for open ports and run vulnerability scan")
# ParseResult(
#     entities=["10.0.0.1"],
#     actions=["scan", "vulnerability_scan"],
#     targets=["10.0.0.1"],
#     modifiers={"port_scan": True, "vuln_scan": True}
# )
```

- **Zero-dependency**: No external ML libraries required
- **Grammar-based**: Pattern grammar for security operations language
- **Entity extraction**: IP addresses, domains, URLs, CIDR ranges, ports
- **Intent disambiguation**: Resolves ambiguous phrasing using context
- **Slash command parsing**: Handles `/` prefixed internal commands

---

## PlannerRegistry

Maps classified intents to plan templates:

```python
@dataclass
class PlanTemplate:
    intent: str
    tool_chain: list[str]               # Ordered tool list
    default_args: dict                  # Default tool arguments
    risk_tier: RiskTier                 # Associated risk
    requires_confirmation: bool

# Registry entries
registry = PlannerRegistry()
registry.register(PlanTemplate(
    intent="scan_target",
    tool_chain=["nmap", "nuclei", "nikto"],
    risk_tier=RiskTier.MEDIUM,
    requires_confirmation=True
))
```

| Intent | Default Tool Chain | Risk Tier |
|--------|-------------------|-----------|
| `scan_target` | nmap → nuclei → nikto | MEDIUM |
| `reconnaissance` | subfinder → httpx → gowitness | LOW |
| `exploit_target` | searchsploit → metasploit | HIGH |
| `generate_report` | Aggregate findings → report engine | LOW |
| `enumerate_services` | nmap → enum4linux → smbclient | MEDIUM |
| `analyze_findings` | Aggregate → analyze | LOW |

---

## Risk Tiers & Confirmation

| Tier | Category Examples | Requires Confirmation | Confidence Requirement |
|------|-------------------|----------------------|----------------------|
| `LOW` | CONFIG, REPORT, MONITOR, CHAT | No | ≥ 0.3 |
| `MEDIUM` | SCAN, RECON, ENUMERATE | Yes | ≥ 0.5 |
| `HIGH` | EXPLOIT, BRUTE-FORCE | Yes (explicit) | ≥ 0.7 |
| `CRITICAL` | DESTRUCTIVE, DATA_EXFIL | Always blocked | N/A |

---

## Mode Selection

Based on the IntentRoute, the system selects an execution mode:

```
┌───────────────────────────────────────────────────────────┐
│ IntentRoute                                          │
│   mode = "autonomous" (from LLM suggestion)           │
│   category = "scan_target"                            │
│   risk_tier = MEDIUM                                  │
│   routing_stage = 2                                   │
└───────────────────────┬───────────────────────────────┘
                        ▼
┌───────────────────────────────────────────────────────────┐
│ ModeDispatcher                                            │
│                                                           │
│   route["mode"] == "autonomous"  →  AutonomousAgent       │
│   route["mode"] == "registry"    →  DirectCommand         │
│   route["mode"] == "hybrid"      →  HybridAgent           │
│   route["mode"] == "interactive" →  InteractiveShell      │
│   route["mode"] == "chat"        →  AIConversational      │
│   route["category"] == "workflow" → WorkflowAutomation    │
└───────────────────────────────────────────────────────────┘
```

---

## Integration Points

| Component | Role |
|-----------|------|
| **AgentCore** | Receives IntentRoute, dispatches to correct mode |
| **NLP Engine** | Provides semantic parsing for stage 3 |
| **PlannerRegistry** | Maps intent to plan template for REGISTRY mode |
| **ModeDispatcher** | Selects interaction mode from route |
| **Context Manager** | Receives route metadata for context building |
| **PermissionGate** | Evaluates route risk tier for gating decisions |
| **EventBus** | Emits `intent.routed` event with full IntentRoute |
