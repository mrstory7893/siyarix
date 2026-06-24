# Playbook Engine

The playbook engine provides reusable, multi-step incident response and assessment workflows using YAML playbooks with variable substitution and DAG-based step execution.

---

## Step Types

| Step Type | Description |
|-----------|-------------|
| `tool` | Execute a security tool via the tool registry |
| `agent` | Delegate a sub-goal to the autonomous agent |

> **Note:** The step type system currently supports `tool` (default) and `agent` step types. Additional step types such as conditional branching, loops, and delays are on the roadmap for future releases.

---

## Creating Playbooks

Playbooks are defined as **YAML files** (not JSON). The engine uses `yaml.safe_load` for parsing:

```yaml
name: web-vuln-scan
description: Standard web vulnerability scan workflow
vars:
  target: "example.com"
  port_range: "1-1000"
steps:
  - id: recon
    type: tool
    tool: nmap
    args:
      flags: "-sn"
    depends_on: []

  - id: port-scan
    type: tool
    tool: nmap
    args:
      flags: "-p {{port_range}} -sV"
    depends_on: [recon]

  - id: vuln-scan
    type: tool
    tool: nuclei
    args:
      severity: "high,critical"
    depends_on: [port-scan]
```

### Programmatic Usage

```python
from siyarix.playbook import PlaybookEngine
from siyarix.workflow import WorkflowEngine

engine = PlaybookEngine(WorkflowEngine())
engine.load("my-playbook.yml")
```

---

## Variables

Playbooks support `{{variable}}` substitution using `_resolve_vars()`:

```yaml
vars:
  target: "example.com"
  port_range: "1-1000"
steps:
  - id: scan
    tool: nmap
    args:
      flags: "-p {{port_range}} {{target}}"
```

Variables can be provided at runtime via the `--var` flag:

```bash
siyarix playbook run my-playbook.yml --var target=10.0.0.1 --var port_range=1-5000
```

Environment variables are accessible as `{{env.HOME}}`, `{{env.PATH}}`, and other allowlisted variables.

---

## Running Playbooks

```bash
# Run a playbook from a file path
siyarix playbook run my-playbook.yml

# Run with variable overrides
siyarix playbook run assessment.yml --var target=example.com

# List available playbooks in a directory
siyarix playbook list --dir playbooks/

# Validate a playbook file
siyarix playbook validate my-playbook.yml
```

---

## Error Handling

Each step supports a `retries` field to configure automatic retry on failure:

```yaml
steps:
  - id: vuln-scan
    tool: nuclei
    retries: 2
    timeout: 300
```

The playbook engine runs within the `WorkflowEngine`, which handles DAG scheduling, parallel execution (via `asyncio.Semaphore(4)`), and per-step timeout enforcement.

---

## Use Cases

- **Standardized assessments**: Ensure every scan follows the same process
- **Incident response**: Pre-defined containment and analysis workflows
- **Onboarding**: Automate the setup process for new team members
- **Compliance**: Repeatable evidence collection for audit cycles
