# Playbook Engine

The playbook engine provides reusable, multi-step incident response and assessment workflows with support for variables, branching, nesting, and error handling strategies.

---

## Step Types

| Step Type | Description |
|-----------|-------------|
| `command` | Execute a shell or scan command |
| `playbook` | Include another playbook (nesting) |
| `conditional` | Branch based on a condition |
| `loop` | Iterate over a list of items |
| `delay` | Wait for a specified duration |
| `prompt` | Ask the user for input |
| `export` | Export results to a file |

---

## Built-in Playbooks

### `bugbounty-recon`

Standard reconnaissance workflow for bug bounty hunting:

1. Subdomain enumeration
2. Port scanning
3. Technology fingerprinting
4. Directory brute-forcing
5. Screenshot capture

### `incident-response`

Security incident containment and analysis:

1. Isolate affected host
2. Capture memory/image
3. Analyze IOCs
4. Collect logs
5. Generate initial report

---

## Creating Playbooks

### Via CLI

```bash
siyarix run "save this workflow as a playbook called 'my-scan'"
```

### Via YAML

Playbooks are stored as JSON but can be created programmatically:

```python
from siyarix.playbook_engine import Playbook, PlaybookStep, PlaybookStepType

playbook = Playbook(
    name="web-vuln-scan",
    description="Standard web vulnerability scan workflow",
    steps=[
        PlaybookStep(name="recon", step_type=PlaybookStepType.COMMAND,
                     command="scan subdomains of {{target}}"),
        PlaybookStep(name="scan", step_type=PlaybookStepType.COMMAND,
                     command="nmap -sV {{target}}"),
        PlaybookStep(name="report", step_type=PlaybookStepType.COMMAND,
                     command="generate report from findings"),
    ]
)
```

---

## Running Playbooks

```bash
# Run a saved playbook
siyarix playbook run bugbounty-recon
siyarix playbook run incident-response

# List available playbooks
siyarix playbook list

# Validate a playbook file
siyarix playbook validate my-playbook.yaml
```

---

## Variables

Playbooks support `{{variable}}` substitution:

```yaml
variables:
  target: "example.com"
  port_range: "1-1000"
steps:
  - command: "nmap -p {{port_range}} {{target}}"
```

Variables can be provided at runtime via the CLI or set in the playbook definition.

---

## Error Handling

| Strategy | Behavior |
|----------|----------|
| `abort` (default) | Stop playbook execution on failure |
| `skip` | Log error and continue with next step |
| `retry` | Retry up to `max_retries` times |

---

## Use Cases

- **Standardized assessments**: Ensure every scan follows the same process
- **Incident response**: Pre-defined containment and analysis workflows
- **Onboarding**: Automate the setup process for new team members
- **Compliance**: Repeatable evidence collection for audit cycles
