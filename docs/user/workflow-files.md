# Workflow Files

Siyarix supports DAG-native workflow execution through its `WorkflowEngine`. Workflows define a directed acyclic graph of steps with explicit dependency ordering, enabling parallel execution of independent tasks.

> **Note:** Workflow files are executed programmatically via the `WorkflowEngine` API or through `siyarix playbook run` (the primary CLI entry point). There is no dedicated `siyarix workflow run` CLI command.

---

## Workflow Format

### YAML Example

```yaml
name: network-assessment
description: Standard network security assessment
steps:
  - id: recon
    instruction: "scan subdomains of {{target}}"
    mode: integrated
    depends_on: []

  - id: port-scan
    instruction: "nmap -sV -p 1-1000 {{target}}"
    mode: registry
    depends_on: [recon]

  - id: vuln-scan
    instruction: "run vulnerability scan on {{target}}"
    mode: integrated
    depends_on: [port-scan]

  - id: report
    instruction: "generate report from findings"
    mode: integrated
    depends_on: [vuln-scan]
    retries: 2
    timeout: 600
```

---

## Step Specification

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `id` | Yes | — | Unique step identifier |
| `instruction` | Yes | — | Command or natural language instruction |
| `mode` | No | `integrated` | Execution mode (`registry`, `autonomous`, `integrated`) |
| `depends_on` | No | `[]` | List of step IDs this step depends on |
| `retries` | No | `0` | Number of retries on failure |
| `timeout` | No | `300` | Step timeout in seconds |
| `persist` | No | `true` | Whether to persist results to offline store |

---

## Execution

```bash
# Run a workflow via playbook command (primary CLI access)
siyarix playbook run network-assessment.yaml

# Run with variable overrides
siyarix playbook run assessment.yml --var target=example.com
```

### Programmatic API

```python
from siyarix.workflow import WorkflowEngine

engine = WorkflowEngine()
workflow = engine.create_workflow(
    name="my-workflow",
    nodes=[
        {"id": "scan", "name": "Port Scan", "step_fn": "nmap", "args": {"target": "10.0.0.1"}},
    ],
    edges=[],
)
await engine.run_workflow(workflow)
```

---

## Step States

Each step progresses through these states:

```
PENDING → RUNNING → COMPLETED
               ↓
            FAILED
               ↓
           SKIPPED
```

---

## Dependency Resolution

Steps are executed in topological order. Steps with no dependencies run first (in parallel where possible), followed by their dependents. The runtime uses `asyncio.Semaphore(4)` to bound concurrency.

---

## Retries

The `WorkflowNode` supports `max_retries` (default: 3) and tracks `retry_count` for automatic retry on failure. Configured via the `retries` field in workflow definitions.

---

## Persistence

Workflow results are persisted to the `OfflineStore`:

- Each step's output (findings, errors, duration)
- Overall workflow status and timing
- Plan ID for later retrieval

---

## Validation

The playbook system validates:

- All step IDs are unique
- All dependency references resolve
- No circular dependencies
- Required fields are present
