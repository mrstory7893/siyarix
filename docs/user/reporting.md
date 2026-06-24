# Reporting and Output

Siyarix provides structured output in multiple formats, comprehensive report generation from the knowledge graph, audit logging with tamper-evident SHA-256 chaining, and system health/metrics monitoring.

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
| `JSONL` | JSON lines format |
| `YAML` | YAML structured output |
| `CSV` | Comma-separated values |
| `HTML` | HTML report |
| `XML` | XML structured output |
| `MARKDOWN` | Markdown-formatted output |
| `RAW` | Raw unformatted output |
| `QUIET` | Minimal output |

### Scan Output Validation

The `siyarix scan` command validates `--output` against: `table`, `json`, `yaml`, `csv`, `html`, `quiet`.

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
| SARIF | Static Analysis Results Interchange Format |

### Report Sections

- **Executive Summary**: High-level findings overview
- **Methodology**: Approach and tools used
- **Findings**: Detailed vulnerability descriptions with severity
- **Evidence**: Command outputs, data collected
- **Remediation**: Suggested fixes for each finding
- **Appendix**: Additional technical details

---

## Audit Logging

All actions are logged to an enterprise-grade audit trail:

```bash
siyarix audit report soc2 -o audit-report.md
siyarix audit logs
siyarix audit verify
```

### Audit System Features

- **Tamper evidence**: SHA-256 hash chain linking entries
- **Session tracking**: Every command tied to a session ID
- **Export**: Logs in JSON or CSV
- **Filtering**: By event type, user, severity, or date range

### Audit Record Fields

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 timestamp |
| `session_id` | Unique session identifier |
| `event_type` | Type of event (command, auth, scan, etc.) |
| `severity` | INFO, WARNING, ERROR, CRITICAL |
| `user` | User identity |
| `target` | Target of the action |
| `result` | Outcome (success, failed, started) |

---

## Metrics

```bash
siyarix metrics
```

Performance statistics:

- Total scans performed
- Successful/failed scans
- Average scan duration
- Total findings
- Plans generated
- Model call counts and errors

Supports `--output table|json|prometheus` and `--export` for file output.

---

## Health Check

```bash
siyarix health
```

Comprehensive system health report:

- Component status (Python, core modules, AI providers)
- Platform information (OS, Python version, shell)
- System state (initialized, configured)
- Storage usage
- Model provider reachability
- Tool availability on PATH

Supports `--output table|json` for different display formats.
