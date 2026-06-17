# Security Model

Siyarix v3.0.0 implements a defense-in-depth security model with multiple layers controlling command execution, data handling, credential storage, operational security, and audit integrity. All commands pass through a **PermissionGate** with two-stage review (BLOCK / REVIEW / ALLOW), are inspected by the **DLP Engine**, logged in a tamper-evident **AuditLogger**, and executed under **OPSECManager** controls.

---

## Security Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     Input Security                                │
│  ┌────────────────────┐  ┌──────────────────────────────────┐   │
│  │ Security Hardening │  │ Input Validation                 │   │
│  │ • Shell injection  │  │ • Length limits                  │   │
│  │ • Null bytes       │  │ • Character restrictions         │   │
│  │ • Control chars    │  │ • Target format validation       │   │
│  └────────────────────┘  └──────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────────┤
│                      Permission Gate                             │
│  ┌─────────────────────────────┐  ┌─────────────────────────┐   │
│  │ Stage 1: Syntax Check       │  │ Stage 2: Danger Analysis │   │
│  │ • Command structure         │  │ • 38+ danger signatures │   │
│  │ • Argument validation       │  │ • Destructive ops       │   │
│  │ • Shell pattern detection   │  │ • Exfiltration patterns │   │
│  └─────────────┬───────────────┘  │ • Escalation patterns   │   │
│                │                   │ • Fork bomb detection   │   │
│                ▼                   └─────────────┬───────────┘   │
│         ┌──────────────┐                        │               │
│         │  BLOCK /     │◀───────────────────────┘               │
│         │  REVIEW /    │                                         │
│         │  ALLOW       │                                         │
│         └──────┬───────┘                                         │
├────────────────┼─────────────────────────────────────────────────┤
│                ▼                                                  │
│          DLP Engine                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ • Credential pattern detection (24 regex signatures)     │   │
│  │ • API key / token / secret leak prevention               │   │
│  │ • PII / internal hostname exposure detection             │   │
│  │ • Request/response content scanning                     │   │
│  └──────────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────────┤
│                   Data Protection                                │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ CredentialStore │  │ MaskingEngine  │  │ Secret Redactor  │  │
│  │ AES-256-GCM    │  │ Bidirectional  │  │ 24 regex         │  │
│  │ System keyring │  │ token masking  │  │ patterns         │  │
│  │ Auto-clear     │  │ session-scoped │  │ output filter    │  │
│  └────────────────┘  └────────────────┘  └──────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│              Audit & Operational Security                        │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ AuditLogger    │  │ StealthEngine  │  │ OPSECManager     │  │
│  │ SHA-256 chain  │  │ TOR routing    │  │ Traffic jitter   │  │
│  │ Tamper-evident │  │ DNS over HTTPS │  │ User-agent rot.  │  │
│  │ SIEM forward   │  │ Session burn   │  │ Request timing   │  │
│  └────────────────┘  └────────────────┘  └──────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 1. Input Security & Validation

### Security Hardening

Pre-processing applied to all user input before command construction:

| Check | Examples | Action |
|-------|----------|--------|
| Shell injection | `;`, `\|`, `` ` ``, `$()`, `&&` | Reject input |
| Null bytes | `\0`, `\x00` | Reject input |
| Control characters | `\x01`–`\x1f` (except `\t`, `\n`) | Reject input |
| Path traversal | `../`, `..\\`, `~` | Reject input |
| Length limits | Command > 4096 chars, arg > 1024 chars | Truncate or reject |
| Target validation | IP, CIDR, hostname, URL format | Reject malformed |

### Tool Call Repair

The `ToolCallRepair` system fixes malformed tool calls from AI providers before execution:

- Fixes missing/extra quotes
- Corrects argument names
- Normalizes flag formats (`--flag value` vs `--flag=value`)
- Validates tool existence in ToolRegistry

---

## 2. Permission Gate

Two-stage review producing BLOCK / REVIEW / ALLOW decisions:

### Stage 1: Syntax Check

Validates command structure before any execution:

- Command length limits
- Argument count limits
- Flag format validation (known vs unknown flags)
- Target format enforcement
- Tool-specific argument rules

### Stage 2: Danger Analysis

Pattern-matches against 38+ dangerous command signatures:

| Category | Patterns | Default Action |
|----------|----------|----------------|
| **Destructive disk ops** | `dd`, `format`, `mkfs`, `mkswap`, `parted` | BLOCK |
| **Recursive deletion** | `rm -rf /`, `rm -rf ~`, `rm -rf .`, `rm -rf /*` | BLOCK |
| **System modification** | `chmod 0 /`, `mknod`, `chown 0`, `mount --bind` | BLOCK |
| **Network flooding** | `ping -f`, `hping3 --flood`, `slowloris` | REVIEW |
| **Privilege escalation** | `sudo !!`, `su -`, `pkexec` | REVIEW |
| **Data exfiltration** | `nc -e`, `curl --data @/etc`, `scp -r /` | REVIEW |
| **Fork bomb** | `:(){ :\|:& };:`, `while true fork` | BLOCK |
| **Data destruction** | `shred -z`, `wipe`, `srm`, `sfill` | REVIEW |
| **Crypto mining** | `minerd`, `xmrig`, `cpuminer` | BLOCK |
| **Reverse shell** | `bash -i >& /dev/tcp/`, `nc -e /bin/sh` | BLOCK |

### Gate Results

| Result | Behavior | Audit |
|--------|----------|-------|
| `ALLOW` | Command proceeds | Logged with ALLOW status |
| `REVIEW` | User confirmation required | Logged with REVIEW status |
| `BLOCK` | Command permanently denied | Logged with BLOCK status + reason |

### Safe Mode

```bash
export SIYARIX_SAFE_MODE=1
```

In safe mode:
- All exploitation commands are BLOCKed
- Only RECON and SCAN operations allowed
- Danger analysis applies stricter heuristics
- Kill switch pre-armed (Ctrl+C x2 exits immediately)

---

## 3. DLP Engine

Data Leak Prevention inspects all data flowing to/from AI providers:

| Pattern | Detection | Action |
|---------|-----------|--------|
| AWS access keys | `AKIA[0-9A-Z]{16}` | Redact + log |
| SSH private keys | `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----` | Redact + log |
| JWT tokens | `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` | Redact + log |
| API keys | `sk-[a-zA-Z0-9]{20,}` | Redact + log |
| Database URLs | `(postgres|mysql|mongodb)://[^@]+@` | Redact + log |
| OAuth tokens | `ya29\.[A-Za-z0-9_-]+`, `ghp_[A-Za-z0-9]{36}` | Redact + log |
| Internal hostnames | Resolved from `*.internal`, `*.local`, `10.x.x.x` | Mask + log |

The DLP Engine operates at two points:
1. **Before provider call**: Scans outgoing data, redacts secrets (permanent), masks IPs/hostnames (reversible)
2. **After provider response**: Scans incoming data for any leaked sensitive content

---

## 4. Data Protection

### CredentialStore

Encrypted vault for API keys, tokens, and secrets:

```python
store = CredentialStore(
    encryption="aes-256-gcm",   # Primary cipher
    key_storage="system",       # System keychain via `keyring`
    auto_clear=True             # Clear on session end
)

await store.set("openai_api_key", "sk-...")
key = await store.get("openai_api_key")  # Decrypted at runtime only
```

| Feature | Detail |
|---------|--------|
| **Encryption** | AES-256-GCM (primary), Fernet (fallback) |
| **Key storage** | System keychain via `keyring` library |
| **Key rotation** | Re-encrypt all credentials with new master key |
| **Auto-clear** | Keys cleared from memory at session end |
| **Runtime only** | Keys decrypted for single request, never persisted |

### MaskingEngine

Bidirectional token masking for sensitive data sent to providers:

| Data Type | Masked Form | Reversible |
|-----------|-------------|------------|
| IP addresses | `10.x.x.x` | Yes (session-scoped) |
| Internal hostnames | `example.com` | Yes (session-scoped) |
| Credentials | `[REDACTED]` | No (permanent) |
| API keys | `[REDACTED]` | No (permanent) |
| JWTs | `[REDACTED]` | No (permanent) |
| Database URLs | `[REDACTED]` | No (permanent) |

### SecretRedactor

24 regex patterns for automatic secret detection in tool output:

- AWS keys (`AKIA...`, `ASIA...`)
- SSH private keys (RSA, EC, Ed25519, DSA)
- JWT tokens
- Generic API keys (`sk-...`, `pk-...`)
- OAuth tokens (Google, GitHub, Azure)
- Database connection strings
- Slack webhooks, Stripe keys, Twilio tokens

---

## 5. AuditLogger

Tamper-evident audit log with SHA-256 hash chain:

```python
logger = AuditLogger()

await logger.log(
    event_type="command.execution",
    data={
        "command": "nmap -sV 10.0.0.1",
        "exit_code": 0,
        "user": "operator-1",
        "session_id": "sess-123"
    }
)
```

### Chain Structure

```
Entry 1: {event, timestamp, hash_prev="0000...", hash_self="a1b2..."}
Entry 2: {event, timestamp, hash_prev="a1b2...", hash_self="c3d4..."}
Entry 3: {event, timestamp, hash_prev="c3d4...", hash_self="e5f6..."}
```

- Each entry contains SHA-256 of the previous entry
- Tampering with any entry breaks the chain for all subsequent entries
- Chain integrity can be verified at any time

### SIEM Forwarding

| Destination | Format | Protocol |
|-------------|--------|----------|
| Splunk | JSON | HTTP Event Collector |
| ELK Stack | JSON | Logstash TCP input |
| Azure Sentinel | CEF | Syslog TCP |
| Standard | JSONL | File output |

---

## 6. StealthEngine

Covert operations capability:

```python
stealth = StealthEngine()
await stealth.enable_tor()        # Route traffic through TOR
await stealth.enable_doh()        # DNS over HTTPS (prevent DNS leakage)
await stealth.set_jitter(500)     # Random delay between requests (ms)
await stealth.rotate_ua()         # Rotate User-Agent per request
```

| Feature | Description |
|---------|-------------|
| **TOR routing** | Route all HTTP traffic through TOR SOCKS proxy |
| **DNS over HTTPS** | Prevent DNS leakage via encrypted DNS |
| **Traffic jitter** | Random delay between outgoing requests |
| **User-Agent rotation** | Cycle through browser/OS user-agent strings |
| **Session burning** | Secure cleanup of session artifacts on exit |

---

## 7. OPSECManager

Operational security controls:

```python
opsec = OPSECManager()
await opsec.apply_policy("stealth")   # Maximum covertness
await opsec.apply_policy("standard")  # Normal operations
await opsec.apply_policy("audit")     # Enhanced logging
```

| Policy | TOR | DoH | Jitter | Rotation | Logging |
|--------|-----|-----|--------|----------|---------|
| `standard` | Off | Off | None | Off | Normal |
| `stealth` | On | On | 500ms | On | Minimal |
| `audit` | Off | Off | None | Off | Maximum |

---

## Component Relationships

```
User Input
    │
    ▼
SecurityHardening ──→ Input Validation ──→ ToolCallRepair
    │
    ▼
PermissionGate
    │
    ├── Stage 1: Syntax Check
    │       │
    │       └── Pass → Stage 2
    │       └── Fail → BLOCK
    │
    ├── Stage 2: Danger Analysis
    │       │
    │       └── Safe → ALLOW
    │       └── Flagged → REVIEW (user confirmation)
    │       └── Dangerous → BLOCK
    │
    ▼
DLP Engine
    │
    ├── Check outgoing data → MaskingEngine
    │       └── Secrets → [REDACTED] (permanent)
    │       └── IPs/Hosts → mask (reversible)
    │
    └── Check incoming data → SecretRedactor
            └── Leaked secrets → log + alert
    │
    ▼
CredentialStore ──→ AES-256-GCM decrypt
    │
    ▼
StealthEngine ──→ OPSECManager
    │
    ▼
Execution ──→ AuditLogger (tamper-evident chain)
```
