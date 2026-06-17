# Reporting and Output

Siyarix provides structured output in multiple formats, comprehensive report generation from the KnowledgeGraph, audit logging with tamper-evident SHA-256 chaining, and system health/metrics monitoring.

---

## Output Formats

Set the default output format:

```bash
siyarix config set default_output_format json
```

| Format | Description |
|--------|-------------|
| `TABLE` | Rich formatted table (default) |
| `JSON` | Machine-readable JSON |
| `YAML` | YAML structured output |
| `CSV` | Comma-separated values |
| `HTML` | HTML report |
| `XML` | XML structured output |
| `RAW` | Raw unformatted output |
| `QUIET` | Minimal output |

---

## Report Generation

```bash
siyarix report generate --format html --output report.html
```

### Report Formats

| Format | Use Case |
|--------|----------|
| HTML | Client-ready reports with formatting |
| JSON | Machine-readable, pipeline integration |
| Markdown | Quick documentation, issue tracking |
| PDF | Formal documentation (requires `wkhtmltopdf`) |

### Report Sections

- **Executive Summary**: High-level findings overview
- **Scope**: Targets scanned and tools used
- **Findings**: Detailed vulnerability descriptions with severity
- **Evidence**: Command outputs, screenshots (if captured)
- **Remediation**: Suggested fixes for each finding
- **Timeline**: Session chronology

---

## Audit Logging

All actions are logged to an enterprise-grade audit trail:

```bash
siyarix audit report
siyarix audit logs
siyarix audit verify
```

### Audit System Features

- **Tamper evidence**: SHA-256 hash chain linking entries
- **SIEM forwarding**: Send logs to Splunk, ELK, or Azure Sentinel
- **Session tracking**: Every command tied to a session ID
- **Export**: Logs in JSON or CSV

### Audit Record Fields

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 timestamp |
| `session_id` | Unique session identifier |
| `event_type` | Type of event (command, auth, safety, tool) |
| `severity` | INFO, WARNING, ERROR, CRITICAL |
| `command` | The executed command |
| `user` | User identity (if auth is configured) |
| `provider` | AI provider used (if applicable) |
| `hash` | SHA-256 of previous entry |

---

## Session Logs

```bash
siyarix session-log
```

Each session log entry includes:

- Command text and parsed intent
- Execution duration
- Exit code and output summary
- Safety events triggered (if any)
- AI provider used for planning

---

## Metrics

```bash
siyarix metrics
```

Performance statistics:

- Total scans performed
- Average scan duration
- Tools used (counts)
- Planner invocation stats
- AI provider usage distribution
- Cache hit/miss rates

---

## Health Check

```bash
siyarix health
```

Comprehensive system health report:

- Component status (Python, core modules, AI providers)
- Platform information (OS, Python version, shell)
- System state (initialized, configured)
- Storage usage (database size, cache size)
- Model provider reachability
- Tool availability on PATH
- Resource utilization
