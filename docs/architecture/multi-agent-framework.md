# Multi-Agent Framework

Siyarix v3.0.0 includes a full multi-agent swarm framework for collaborative autonomous security operations. The **Swarm** orchestrator manages specialized agents (Recon, Scan, Exploit, Report) that communicate via the **EventBus**, share context through the **KnowledgeGraph**, and execute under the **PermissionGate** and **DLP Engine**. The **AgentCore** dispatches to single or multi-agent modes depending on the goal complexity.

---

## Architecture

```
                     ┌──────────────────┐
                     │   User Goal      │
                     │ "enumerate +     │
                     │  exploit network"│
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   AgentCore      │
                     │  (mode dispatch) │
                     └────────┬─────────┘
                              │
                    ┌─────────┴──────────┐
                    │                    │
                    ▼                    ▼
           ┌────────────────┐  ┌──────────────────┐
           │ Single-Agent   │  │ Swarm Orchestrator│
           │ (AUTONOMOUS)   │  │ (multi-agent)     │
           └────────────────┘  └────────┬─────────┘
                                        │
                          ┌─────────────┼─────────────┐
                          │             │             │
                          ▼             ▼             ▼
                   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
                   │ Recon    │  │ Scan     │  │ Exploit  │  │ Report   │
                   │ Agent    │  │ Agent    │  │ Agent    │  │ Agent    │
                   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
                        │             │             │             │
                        └─────────────┼─────────────┼─────────────┘
                                      │             │
                                      ▼             ▼
                              ┌────────────────────────┐
                              │     ExecutionEngine    │
                              │  (per-agent execution) │
                              └────────────────────────┘
                                      │
                                      ▼
                              ┌────────────────────────┐
                              │    KnowledgeGraph      │
                              │  (shared context)      │
                              └────────────────────────┘
```

---

## Agent Roles

| Role | Codename | Primary Tools | Output |
|------|----------|---------------|--------|
| `RECON` | ReconAgent | subfinder, httpx, gowitness, whois, dnsx | Domains, subdomains, screenshots, WHOIS |
| `SCANNER` | ScanAgent | nmap, masscan, naabu | Open ports, service versions, banners |
| `ENUMERATOR` | EnumAgent | dirsearch, wpscan, whatweb, ffuf | Directories, CMS, tech stack |
| `EXPLOITER` | ExploitAgent | searchsploit, metasploit, nuclei | CVEs, exploits, proof-of-concept |
| `REPORTER` | ReportAgent | ReportEngine | Aggregated findings, SARIF, HTML |
| `SOC` | SOCAgent | log parser, alert correlator | Alert triage, incident summary |
| `DFIR` | DFIRAgent | forensic collector, timeline | Evidence, timeline, IoCs |

---

## Swarm Orchestrator

The `Swarm` orchestrator manages the multi-agent lifecycle:

```python
swarm = Swarm(goal="enumerate services and find vulnerabilities on 10.0.0.1")

# Swarm auto-selects required agents
swarm.add_agent(ReconAgent("recon-1"))
swarm.add_agent(ScanAgent("scan-1"))
swarm.add_agent(ExploitAgent("exploit-1"))
swarm.add_agent(ReportAgent("report-1"))

# Execute with coordination
result = await swarm.execute()
```

### Orchestration Flow

```
1. Goal Decomposition
   └── "enumerate + exploit 10.0.0.1"
       ├── ReconAgent: "discover subdomains, technologies"
       ├── ScanAgent: "port scan 10.0.0.1"
       ├── ExploitAgent: "check vulnerabilities on discovered services"
       └── ReportAgent: "generate SARIF report"

2. Dependency Ordering
   Layer 0: ReconAgent (no dependencies)
   Layer 1: ScanAgent (depends on recon results)
   Layer 2: ExploitAgent (depends on scan findings)
   Layer 3: ReportAgent (depends on all findings)

3. Execution
   Each agent executes its sub-plan via ExecutionEngine
   Agents within the same layer run in parallel

4. Context Sharing
   Findings → KnowledgeGraph (shared across all agents)
   Agent communication → EventBus (pub/sub)

5. Result Aggregation
   ReportAgent collects all findings
   Generates final output via ReportEngine
```

---

## Agent Lifecycle

```
                ┌──────────┐
                │  IDLE    │
                └────┬─────┘
                     │
                     ▼
              ┌──────────────┐
              │ INITIALIZING │──→ Load sub-plan → Setup tools
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
         ┌───│   WORKING    │──→ Execute steps via Engine
         │   └──────┬───────┘
         │          │
         │    ┌─────┴─────┐
         │    │           │
         │    ▼           ▼
         │ ┌──────┐  ┌────────┐
         │ │DONE  │  │WAITING │──→ Waiting for dependency
         │ └──────┘  └────────┘
         │    │
         │    ▼
         │ ┌────────┐
         └─│ FAILED │──→ Error recovery → retry or abort
           └────────┘
```

---

## Agent Communication Protocol

Agents communicate via the internal messaging system routed through EventBus:

```python
@dataclass
class AgentMessage:
    sender: str                       # Agent ID (e.g., "recon-1")
    recipient: str                    # Agent ID or "swarm" or "broadcast"
    content: str                      # Message body
    msg_type: MessageType             # task | result | query | broadcast | error
    payload: dict                     # Structured data
    correlation_id: str               # For request/response matching
```

### Message Types

| Type | Direction | Purpose |
|------|-----------|---------|
| `task` | Swarm → Agent | Assignment of a sub-task |
| `result` | Agent → Swarm | Return of findings |
| `query` | Agent → Agent | Request for specific information |
| `broadcast` | Any → All | Team-wide notification |
| `error` | Agent → Swarm | Error reporting |

### Example Flow

```
Swarm → ReconAgent: task("scan example.com subdomains")
ReconAgent → Swarm:  result({"subdomains": ["www", "api", "admin"]})
ReconAgent → Swarm:  broadcast("recon complete for example.com")
ScanAgent → Swarm:   query("target IPs for example.com")
Swarm → ScanAgent:   result({"targets": ["10.0.0.1", "10.0.0.2"]})
Swarm → ScanAgent:   task("port scan 10.0.0.1, 10.0.0.2")
```

---

## Agent Memory

Each agent maintains working memory:

```python
@dataclass
class AgentMemory:
    findings: list[Finding]            # Discovered items
    commands_run: list[CommandRecord]  # Executed commands
    messages_received: deque           # Incoming messages (maxlen=100)
    messages_sent: deque               # Outgoing messages (maxlen=100)
    context: dict                      # Current agent state
```

Memory is:
- Scoped to the agent's lifecycle
- Cleared on agent completion
- Shared via KnowledgeGraph (persistent across session)
- Summarized for context window via Compact system

---

## AgentCore Integration

The `AgentCore` decides single vs. multi-agent execution:

```python
async def dispatch_goal(goal: str):
    route = await intent_router.route(goal)
    
    # Assess complexity
    if requires_swarm(route):
        # Multi-agent: decompose goal into sub-tasks
        swarm = Swarm(goal=goal)
        sub_goals = await decompose_goal(goal)
        for sub_goal in sub_goals:
            agent = create_agent_for_goal(sub_goal)
            swarm.add_agent(agent)
        return await swarm.execute()
    else:
        # Single-agent: use autonomous mode
        return await autonomous_executor.execute(goal)
```

### Complexity Assessment

| Factor | Single-Agent | Multi-Agent (Swarm) |
|--------|-------------|-------------------|
| Tools required | 1–3 tools | 4+ tools |
| Target scope | Single target | Multiple targets / network |
| Operations | RECON only | RECON + SCAN + EXPLOIT |
| Duration | < 5 steps | 10+ steps with dependencies |
| Parallelism | Not needed | Multiple independent tasks |

---

## Sub-Agent Framework

Internal agents use the same framework as top-level agents:

```python
# Internal tools framework
class InternalToolAgent(Agent):
    """Agent that uses internal security tools directly."""

class SecurityCommandsAgent(Agent):
    """Agent that executes security command chains."""

class PipelineAgent(Agent):
    """Agent that executes a CommandPipeline as its sub-plan."""
```

---

## Component Relationships

```
         ┌───────────────────────────────────────────────┐
         │                   AgentCore                    │
         │  (decides single vs. swarm based on goal)     │
         └─────────────────────┬─────────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
    ┌──────────────────┐              ┌──────────────────┐
    │ Autonomous       │              │ Swarm            │
    │ Executor         │              │ Orchestrator     │
    │ (single agent)   │              │                  │
    └──────────────────┘              │ • Goal decompose │
                                      │ • Agent dispatch │
                                      │ • Dependency     │
                                      │   ordering       │
                                      │ • Result aggregate│
                                      └────────┬─────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │             ┌────────────┴────────────┐             │
                    │             │                         │             │
                    ▼             ▼                         ▼             ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ Recon    │  │ Scan     │  │ Enum     │  │ Exploit  │  │ Report   │
              │ Agent    │  │ Agent    │  │ Agent    │  │ Agent    │  │ Agent    │
              └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
                   │             │             │             │             │
                   ▼             ▼             ▼             ▼             ▼
              ┌─────────────────────────────────────────────────────────────────┐
              │                     ExecutionEngine                            │
              │  (each agent gets its own ExecutionPlan, executed via WorkerPool)│
              └─────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
              ┌─────────────────────────────────────────────────────────────────┐
              │                      KnowledgeGraph                            │
              │  (shared across all agents, real-time updates)                 │
              └─────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
              ┌─────────────────────────────────────────────────────────────────┐
              │                    ReportEngine                                 │
              │  (final aggregation: MARKDOWN, HTML, JSON, SARIF + CVSS)       │
              └─────────────────────────────────────────────────────────────────┘
```

---

## Stub Components (Not Fully Implemented)

The following multi-agent components exist as placeholders for future development:

| Component | Status | Expected Capability |
|-----------|--------|---------------------|
| `CanaryTokenManager` | Stub | Canary token deployment and monitoring |
| `CoderBridge` | Stub | Integration with code analysis tools |
| `CloudScanner` | Stub | Cloud infrastructure scanning (AWS, Azure, GCP) |
| `IaCScanner` | Stub | Infrastructure-as-Code scanning |
| `MobileScanner` | Stub | Mobile application security testing |
| `IoTScanner` | Stub | IoT device security assessment |
| `AdversarialTester` | Stub | Adversarial attack simulation |
| `ThreatIntelFeed` | Stub | External threat intelligence ingestion |
| `MITREAttackDB` | Basic | MITRE ATT&CK framework mapping |
