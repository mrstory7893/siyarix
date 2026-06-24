# Safety, Security & Hallucination Resistance

Siyarix implements a multi-layered safety architecture that protects the host system, operator data, and audit trail integrity. Every command passes through staged validation, danger classification, secret redaction, and interactive review before execution, with comprehensive audit logging for compliance and forensic analysis.

---

## Safety Pipeline

Every tool command flows through these stages:

```
User input → InputValidator → PermissionGate → DangerAnalyzer → DLPEngine → ShellReview → AuditLogger
```

---

## 1. InputValidator

Located in `src/siyarix/security_hardening.py`, validates and sanitises user-supplied targets before they reach the executor.

### Target Validation

Auto-detects and validates target format:

```python
from siyarix.security_hardening import validator

# Validates IP, hostname, or URL
valid, msg = validator.validate_target("10.0.0.1")
valid, msg = validator.validate_ip("192.168.1.0/24")
valid, msg = validator.validate_hostname("example.com")
valid, msg = validator.validate_url("https://example.com")
```

### Injection Detection

Checks for shell injection patterns:

| Pattern | Example | Severity |
|---------|---------|----------|
| Shell pipe/redirection | `|`, `;`, `&`, `` ` `` | Blocked |
| Command substitution | `$(...)` | Blocked |
| Path traversal | `../`, `..\\`, `%2e%2e` | Blocked |
| Null byte | `\x00` | Blocked |
| Newline injection | `\r\n` | Blocked |
| Format string | `%x`, `%n` | Blocked |
| SQL injection keywords | `SELECT`, `DROP`, `UNION` + `'` or `"` | Blocked |
| Backtick execution | `` `cmd` `` | Blocked |

### Argument Sanitisation

```python
safe = validator.sanitize_arg("target; rm -rf /")
# Returns: "target rm -rf " (shell metacharacters stripped)
```

Removes null bytes, carriage returns, newlines, ANSI escape sequences, backticks, `$()`, `${}`, `|`, `;`, `&`, `<`, `>`, and collapses `../` traversals.

---

## 2. DangerAnalyzer

Also in `security_hardening.py`, classifies commands by destructiveness before execution.

### Danger Levels

| Severity | Recommendation | Example Patterns |
|----------|---------------|------------------|
| **Critical** | Blocked | `sudo rm -rf /`, `mkfs`, `dd if=`, fork bombs, format drive, `chmod 777 /`, credential exfiltration |
| **High** | Confirm | `shutdown`, `reboot`, `halt`, pipe curl/wget to shell, SQL DROP/DELETE without WHERE, `Remove-Item -Recurse` |
| **Medium** | Caution | `rm`, `killall`, `iptables -F`, netcat listener, crontab edit, PowerShell encoded command |
| **Low** | Info | `chmod`, `chown`, `crontab` |
| **Info** | Note | `sudo` |
| **Safe** | — | No patterns matched |

### Usage

```python
from siyarix.security_hardening import danger_analyzer

report = danger_analyzer.analyze("rm -rf /tmp")
print(report.severity)        # "medium"
print(report.is_dangerous)    # True
print(report.recommendation)  # "⚡ CAUTION — Review this command before execution."
```

The analyzer covers both Linux and Windows destructive patterns, including registry manipulation, shadow copy deletion, event log clearing, and scheduled task abuse.

### Formatted Warning

```python
from rich.console import Console
danger_analyzer.format_warning(report, Console())
```

Renders a colour-coded Rich panel with severity, reasons, and recommendation.

---

## 3. PermissionGate

Located in `src/siyarix/permission_gate.py`, provides two-stage runtime safety enforcement.

### Two-Stage Check

**Stage 1 — Syntax check**: Validates the command is non-empty and syntactically valid.

**Stage 2 — Danger analysis**: Delegates to `DangerAnalyzer` and maps severity to enforcement action:

| Danger Severity | Gate Result | Action |
|----------------|-------------|--------|
| `critical` | `FORBIDDEN` | Blocked with reason |
| `high` / `medium` | `REVIEW` | Allowed with `requires_review=True` |
| `low` / `info` / `safe` | `APPROVED` | Allowed |

### Rate Limiting

Tracks call frequency with configurable limits:

```python
gate = PermissionGate(rate_limit_calls=100, rate_limit_period=60.0)
```

- Default: 100 calls per 60 seconds
- State persisted to `rate_limit.json` in config directory
- Rate limit exceeded → `FORBIDDEN` result

### Restricted Payload Detection

When `context={"restricted_payload": True}` is passed, checks for destructive patterns (`rm -rf`, `mkfs`, `dd if=`) before rate limiting.

### GateResult

```python
@dataclass
class GateResult:
    allowed: bool             # True if command passes
    stage: GateStage          # Which stage the result originates from
    reason: str               # Human-readable explanation
    tool: str                 # Tool name
    command: str              # Original command
    requires_review: bool     # True if user confirmation needed
```

### Gate Stages

| Stage | Meaning |
|-------|---------|
| `SYNTAX` | Failed basic syntax validation |
| `FORBIDDEN` | Blocked by danger or rate limit |
| `PERMISSION` | Under permission evaluation |
| `REVIEW` | Passed syntax check but requires user review |
| `APPROVED` | Fully approved for execution |

---

## 4. DLPEngine

Located in `src/siyarix/dlp.py`, scans and redacts sensitive information from tool outputs.

### Redaction Patterns

| Category | Patterns |
|----------|----------|
| **Secrets** | AWS keys (`AKIA...`), GCP keys (`AIza...`), Slack tokens (`xoxb-...`), GitHub tokens (`ghp_...`), Bearer tokens, Private keys (PEM) |
| **PII** (optional) | Email addresses, US Social Security numbers |

### Usage

```python
from siyarix.dlp import DLPEngine

dlp = DLPEngine(redact_secrets=True, redact_pii=False)

safe_output = dlp.redact("API key: AKIAIOSFODNN7EXAMPLE")
# Returns: "API key: [REDACTED AWS_KEY]"

safe_dict = dlp.redact_dict({"token": "ghp_xxxxxxxxxxxxxxxxxxxx"})
```

Secrets are redacted with their category name: `[REDACTED AWS_KEY]`, `[REDACTED GITHUB_TOKEN]`, etc.

### SecretRedactor (security_hardening.py)

A more comprehensive redactor in `security_hardening.py` covers 20+ patterns including:

- OpenAI (`sk-...`), Anthropic (`sk-ant-...`), DeepSeek (`sk-ds...`), xAI (`xai-...`), Mistral API keys
- AWS access/secret keys, GCP service accounts, Azure connection strings
- JWTs, GitHub tokens, GitLab tokens, Slack tokens, Google API keys
- Bearer/Basic auth, passwords in URLs, private key markers
- Generic `secret=value`, `password=value` key-value pairs

```python
from siyarix.security_hardening import redactor

safe = redactor.redact("Key: sk-ant-xxxxxxxxxxxxxxxxxxxx")
safe_dict = redactor.redact_dict({"credentials": {"password": "hunter2"}})
safe_env = redactor.redact_env()  # os.environ with secrets masked
```

---

## 5. ShellReview

Located in `src/siyarix/shell_review.py`, provides interactive command review with four decisions.

### Review Prompt

```
╭──────────────── Command Execution Review ─────────────────╮
│ Tool: raw                                                 │
│ Reason: Raw shell command from LLM plan                   │
│                                                           │
│ nmap -sS -sV -O -Pn example.com                           │
╰───────────────────────────────────────────────────────────╯
Review command [edit/run/step/cancel] (run):
```

### Review Decisions

| Decision | Behavior |
|----------|----------|
| `run` | Execute the command as-is |
| `edit` | Edit the command interactively, then execute modified version |
| `step` | Execute but step through commands one at a time |
| `cancel` | Skip/cancel this command entirely |

### Non-TTY / CI Mode

Auto-approves all commands when stdin/stdout are not TTYs (CI pipelines, non-interactive shells):

```python
if not _is_interactive():
    return ReviewResult(decision=ReviewDecision.RUN, edited_command=original)
```

### Integration

Importable by all executors:

```python
from siyarix.shell_review import review_and_confirm, review_command

reviewed = review_and_confirm("nmap -sV target", "nmap", "Port scan")
if reviewed is None:
    return  # Cancelled
# Execute reviewed command
```

---

## 6. AuditLogger

Located in `src/siyarix/audit_log.py`, provides enterprise-grade audit trail with tamper-evident chain of custody.

### Event System

```python
from siyarix.audit_log import AuditEventType, AuditSeverity, AuditEvent, AuditLogger
```

Every event is a structured dataclass:

```python
@dataclass
class AuditEvent:
    event_id: str               # UUID hex
    timestamp: datetime         # UTC timestamp
    event_type: str             # Event category
    severity: str               # info / low / medium / high / critical
    user: str                   # Attributed user
    session_id: str             # Session identifier
    source_ip: str              # Originating IP
    target: str                 # Target resource
    action: str                 # Action performed
    result: str                 # success / failure / denied
    details: dict               # Arbitrary structured data
    hash_prev: str | None       # Previous event's hash (chain link)
    hash_current: str | None    # This event's hash
```

### Tamper-Evident Chain

Each event's hash incorporates the previous event's hash:

```python
def compute_hash(self, prev_hash: str | None = None) -> str:
    data = (
        f"{self.timestamp.isoformat()}{self.event_type}{self.severity}"
        f"{self.user}{self.session_id}{self.source_ip}{self.target}"
        f"{self.action}{self.result}{details_str}{prev_hash or ''}"
    )
    return hashlib.sha256(data.encode()).hexdigest()[:16]
```

### Chain Verification

```python
audit = AuditLogger()
result = audit.verify_chain()

# Returns:
# {
#     "valid": True,
#     "total_events": 142,
#     "broken_at": None,
#     "errors": [],
#     "chain_integrity": "intact",
# }
```

### Event Types (87 defined)

| Category | Events |
|----------|--------|
| **Authentication** | `auth_login`, `auth_logout`, `auth_failed` |
| **Scanning** | `scan_start`, `scan_complete`, `scan_failed` |
| **Incidents** | `incident_create`, `incident_update`, `incident_close` |
| **Vulnerabilities** | `vuln_create`, `vuln_update` |
| **Security** | `security_approval`, `security_denial`, `dlp_violation`, `rate_limit_hit` |
| **System** | `system_start`, `system_error`, `config_change`, `credential_rotated` |
| **Plugins** | `plugin_install`, `plugin_remove` |
| **API** | `api_key_create`, `api_key_revoke` |
| **Compliance** | `compliance_check`, `permission_change` |
| **Containers** | `container_check`, `file_integrity` |

### Session Tracking

```python
session_id = audit.start_session(user="alice")
# ... perform operations ...
audit.end_session(session_id)
```

### Logging Events

```python
from siyarix.audit_log import audit, log_event

# Via module-level singleton
audit.log(
    event_type=AuditEventType.SCAN_START,
    severity=AuditSeverity.INFO,
    user="alice",
    action="port_scan",
    result="success",
    target="10.0.0.1",
    session_id=session_id,
    details={"ports": "1-1000", "tool": "nmap"},
)

# Via convenience function
log_event(
    event_type=AuditEventType.SECURITY_DENIAL,
    severity=AuditSeverity.HIGH,
    user="alice",
    action="command_blocked",
    result="denied",
    details={"command": "rm -rf /", "reason": "critical destructive pattern"},
)
```

### Export

```python
# Export to JSON (returns string)
json_data = audit.export(export_format="json", days=30)

# Export to file (returns None)
audit.export(export_format="json", filepath="audit_export.json", days=30)

# Export to CSV
csv_data = audit.export(export_format="csv", days=7)
```

### CLI Commands

| Command | Purpose |
|---------|---------|
| `/audit status` | Show audit statistics and chain integrity |
| `/audit export` | Export audit logs (JSON or CSV) |
| `/audit verify` | Verify tamper-evident chain integrity |

### Retention and Cleanup

- Default retention: 365 days (configurable via `audit.toml`)
- `cleanup_old_events()` removes events older than retention period and rewrites the audit file
- In-memory limit: last 1000 events loaded from disk; full persistence via JSONL with SHA-256 chain

### OpSec Integration

In memory-only mode (via `opsec_manager`), events are tracked in memory but never written to disk:

```python
if opsec_manager.status.memory_only:
    self._unflushed_events.clear()
    self._dirty = False
    return
```

---

## 7. SeccompProfile

Located in `security_hardening.py`, generates Docker-compatible seccomp profiles for sandboxed execution.

### Restricted Syscalls

Blocks 50+ dangerous syscalls while allowing normal tool execution:

```
acct, add_key, bpf, clock_adjtime, clock_settime, create_module,
delete_module, finit_module, init_module, ioperm, iopl, kexec_*, mount,
open_by_handle_at, perf_event_open, pivot_root, ptrace, reboot, setns,
swapoff, swapon, umount, unshare, userfaultfd, ...
```

### Usage

```python
from siyarix.security_hardening import SeccompProfile

profile_path = SeccompProfile.generate_docker_seccomp()
# Returns path to cached JSON profile: /tmp/siyarix/seccomp/docker_seccomp.json
```

---

## 8. Validator

Located in `src/siyarix/validators.py`, provides input format validators separate from the injection-detection focused `InputValidator`.

### Validated Types

| Function | Validates |
|----------|-----------|
| `validate_target` | Auto-detect IP, CIDR, hostname, or URL |
| `validate_hostname` | RFC 1123 hostname (supports single-label, localhost, numeric TLDs) |
| `validate_url` | HTTP/HTTPS URLs with required dot in host |
| `validate_ip` | IPv4/IPv6 address |
| `validate_cidr` | CIDR notation with `ipaddress.ip_network` |
| `validate_port` | Single port 1–65535 |
| `validate_port_range` | Dash-separated range (`80-443`) or single port |
| `validate_email` | Simplified RFC 5321 email |
| `validate_not_empty` | Non-blank string |
| `validate_min_length` | Minimum character length |

### PlanStep Validation

The `Validator` class validates `PlanStep` objects before execution:

```python
from siyarix.validators import Validator

v = Validator()
results = await v.validate_plan(steps)  # List[ValidationResult]
```

Checks:
- Step has a tool specified
- Step has arguments (except report/summary tools)
- Step timeout is positive

### Recovery Planning

When validation fails, `plan_recovery()` suggests corrective actions:

| Error | Recovery |
|-------|----------|
| `nmap` filtered ports | Add `-Pn` flag |
| `nikto` / `nuclei` refused | Try alternative tool |
| `gobuster` / `ffuf` all 404s | Add more extensions |
| Max retries exceeded | Skip step |

```python
recovery = await v.plan_recovery(failed_step, "filtered")
# RecoveryPlan(action=RETRY, modified_step=..., message="Adding -Pn flag")
```

---

## Related Modules

| Module | Path | Purpose |
|--------|------|---------|
| `InputValidator` | `src/siyarix/security_hardening.py:88` | Target validation, injection detection, sanitisation |
| `DangerAnalyzer` | `src/siyarix/security_hardening.py:650` | Command danger classification (6 severity levels) |
| `SecretRedactor` | `src/siyarix/security_hardening.py:328` | Comprehensive secret redaction (20+ patterns) |
| `PermissionGate` | `src/siyarix/permission_gate.py:49` | Two-stage gate: syntax check + danger analysis |
| `DLPEngine` | `src/siyarix/dlp.py:29` | Data loss prevention for tool outputs |
| `ShellReview` | `src/siyarix/shell_review.py:48` | Interactive command review (edit/run/step/cancel) |
| `AuditLogger` | `src/siyarix/audit_log.py:194` | Enterprise audit with SHA-256 tamper-evident chain |
| `Validator` | `src/siyarix/validators.py:598` | PlanStep validation with recovery planning |
| `SeccompProfile` | `src/siyarix/security_hardening.py:771` | Docker-compatible syscall restriction profiles |
