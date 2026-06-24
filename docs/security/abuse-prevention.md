# Abuse Prevention

Siyarix implements multiple layers of abuse prevention to stop malicious or accidental misuse. These layers work together to provide defense in depth — from input validation to audit logging.

## Prevention Layers

```
┌─────────────────────────────────────────┐
│    Command-level prevention             │
│  ┌──────────┐  ┌──────────┐            │
│  │  Danger  │  │  Syntax  │            │
│  │ Analysis │  │  Check   │            │
│  └──────────┘  └──────────┘            │
├─────────────────────────────────────────┤
│    System-level prevention              │
│  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │Kill Sw.  │  │ Safe     │  │OPSEC │ │
│  │(emer-    │  │ Mode     │  │Evade │ │
│  │ gency)   │  │          │  │     │ │
│  └──────────┘  └──────────┘  └──────┘ │
├─────────────────────────────────────────┤
│    Audit-level prevention              │
│  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │Audit Log │  │ Session  │  │SIEM  │ │
│  │(chain)   │  │   Log    │  │Fwd   │ │
│  └──────────┘  └──────────┘  └──────┘ │
└─────────────────────────────────────────┘
```

## 1. Danger Analysis

38+ dangerous command patterns are checked pre-execution in `permission_gate.py`:

```python
PATTERNS = {
    "destructive_disk": r"\b(dd|mkfs|format|mkswap|parted)\b.*(if=|/dev/)",
    "recursive_delete": r"\brm\b.*\s(-rf|/\s*\*)",
    "network_flood": r"\b(ping|hping3|nping)\b.*(-f|--flood)",
    "fork_bomb": r":\(\)\s*\{.*:\|:&\};:",
    "priv_escalation": r"\bsudo\b.*(\!\!|su\s*-)",
}
```

Categories include: disk destruction, recursive deletion, network floods, fork bombs, privilege escalation, credential exfiltration, crypto mining, reverse shells, and more.

## 2. Permission Gate

Two-stage gate per command in `permission_gate.py`:

```
Command → Syntax Gate → Danger Analysis → Result
```

Each stage returns `ALLOW`, `FLAG`, or `DENY`:

- **Syntax Gate**: Validates command structure, length limits, character restrictions, shell injection patterns
- **Danger Analysis**: Pattern-matches against 38+ dangerous command categories
- **InputValidator**: Additional injection prevention (shell, SQL, path traversal, null byte, format string, SSRF)

## 3. DLP Engine

Data Loss Prevention in `dlp.py` with bidirectional token masking:

- Masks sensitive data before sending to cloud AI providers (40+ regex patterns)
- Session-scoped: masks are consistent within a session
- Bidirectional: can reverse masks for local display
- Pattern types: IP addresses, hostnames, email addresses, API keys (OpenAI, AWS, GCP, Azure, GitHub, GitLab, Slack, Stripe), JWT tokens, SSH keys, passwords, credit cards

## 4. Emergency Stop

- Press **Ctrl+C** once to cancel the current task
- Press **Ctrl+C** twice to exit Siyarix entirely
- The execution engine halts all subprocesses and cleans up

## 5. Safe Mode

```bash
export SIYARIX_SAFE_MODE=1
```

Restricts to reconnaissance only:
- Scanning tools only (nmap, masscan, nuclei passive)
- No exploitation (metasploit, sqlmap active)
- No destructive commands (dd, rm, format)
- Permission gate at maximum strictness

## 6. OPSEC Controls

`opsec.py` implements operational security:

| Control | Description |
|---------|-------------|
| TOR routing | Route all outbound traffic through TOR |
| DNS over HTTPS | Prevent DNS leakage |
| Session burning | Secure cleanup of artifacts |
| Request jitter | Random delays between connections |
| Proxy rotation | Rotate through proxy pool |
| Request pacing | Rate-limit outbound requests |
| DNS staggering | Stagger queries across multiple resolvers |

## 7. Security Hardening

`security_hardening.py` provides system-level hardening:

- File integrity monitoring (SHA-256 based)
- Container security configuration checks
- Seccomp-BPF profile generation for Docker sandboxing
- Privilege escalation prevention
- Configuration file integrity verification

## 8. Audit Trail

All safety events are logged to the tamper-evident audit log (`audit_log.py`):

| Event | Logged data |
|-------|-------------|
| Command blocked | command, reason, pattern matched |
| Emergency stop | trigger reason, timestamp |
| Safe mode violation | command, persona, target |
| Permission gate | gate stage, result, user action |
| DLP redaction | pattern type, occurrence count (not actual data) |
| Credential access | provider name, timestamp (not key value) |
