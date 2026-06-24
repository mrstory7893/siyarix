# 🛡️ Abuse Prevention

Siyarix is a powerful cybersecurity tool, which means it must be handled with care. To prevent malicious use or accidental damage, we've implemented multiple layers of abuse prevention. These layers work together to provide **Defense in Depth**—protecting everything from input validation to comprehensive audit logging.

## 🍰 The Layers of Prevention

Think of our security model like a multi-layered cake. Every layer adds a new level of protection!

```text
┌─────────────────────────────────────────┐
│        Command-Level Prevention         │
│  ┌──────────┐            ┌──────────┐   │
│  │  Danger  │            │  Syntax  │   │
│  │ Analysis │            │  Check   │   │
│  └──────────┘            └──────────┘   │
├─────────────────────────────────────────┤
│        System-Level Prevention          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Kill Sw.  │ │   Safe   │ │  OPSEC   │ │
│  │(emer-    │ │   Mode   │ │  Evade   │ │
│  │ gency)   │ │          │ │          │ │
│  └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────┤
│        Audit-Level Prevention           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Audit Log │ │ Session  │ │   SIEM   │ │
│  │(chain)   │ │   Log    │ │ Forward  │ │
│  └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────┘
```

> [!TIP]
> Each of these layers operates automatically. You don't need to configure them for them to protect you, though advanced users can fine-tune their behavior.

## 1. 🛑 Danger Analysis

Before any command is executed, it passes through `permission_gate.py`, where it is checked against **38+ dangerous command patterns**. 

```python
PATTERNS = {
    "destructive_disk": r"\b(dd|mkfs|format|mkswap|parted)\b.*(if=|/dev/)",
    "recursive_delete": r"\brm\b.*\s(-rf|/\s*\*)",
    "network_flood": r"\b(ping|hping3|nping)\b.*(-f|--flood)",
    "fork_bomb": r":\(\)\s*\{.*:\|:&\};:",
    "priv_escalation": r"\bsudo\b.*(\!\!|su\s*-)",
}
```

**What does it block?** Everything from accidental disk destruction and recursive file deletion, to network floods, fork bombs, and unintended privilege escalation. 

## 2. 🚧 The Permission Gate

Every command faces a strict two-stage review process:

`Command → Syntax Gate → Danger Analysis → Result`

The gate will return one of three results: `ALLOW`, `FLAG` (prompting the user), or `DENY`.

- **Syntax Gate:** Checks the overall structure, limits length, and scans for shell injection attempts.
- **Danger Analysis:** Checks against the specific destructive patterns mentioned above.
- **Input Validator:** Provides an extra layer of protection against SQL injection, path traversal, SSRF, and null-byte attacks.

## 3. 🤐 Data Loss Prevention (DLP) Engine

To ensure you never accidentally leak sensitive data to third-party cloud AI providers, our **DLP Engine** (`dlp.py`) uses bidirectional token masking.

- **Masks 40+ Patterns:** Redacts IPs, hostnames, emails, passwords, SSH keys, credit cards, and API keys (AWS, GCP, GitHub, Slack, etc.) before the data leaves your machine.
- **Bidirectional:** Data is masked going to the cloud, but unmasked when displayed on your local terminal so you can still read it.
- **Session-Scoped:** Masks remain consistent throughout your session, so the AI doesn't get confused.

> [!IMPORTANT]
> Your secrets belong to you. Siyarix ensures they never end up in a cloud provider's training data.

## 4. 🚨 Emergency Stop (Kill Switch)

Things getting out of hand? You're always in control.

- **Press `Ctrl+C` once:** Cancels the current task gracefully.
- **Press `Ctrl+C` twice:** Instantly halts Siyarix, killing all active subprocesses and cleaning up the environment.

## 5. 🦺 Safe Mode

Need to run Siyarix in a highly restricted environment? Turn on Safe Mode:

```bash
export SIYARIX_SAFE_MODE=1
```

**In Safe Mode:**
- Only reconnaissance is allowed (e.g., `nmap`, passive `nuclei`).
- Exploitation tools (e.g., `metasploit`, active `sqlmap`) are disabled.
- Destructive commands are hard-blocked.
- The Permission Gate operates at maximum strictness.

## 6. 🥷 OPSEC Controls

Siyarix respects your operational security. The `opsec.py` module provides robust evasion controls:

| Control | What it does |
|---------|-------------|
| **TOR Routing** | Routes all outbound traffic through the TOR network. |
| **DNS over HTTPS** | Prevents DNS leakage by encrypting your lookups. |
| **Session Burning** | Securely wipes all artifacts and logs when you're done. |
| **Request Jitter** | Adds random delays to connections to defeat pattern detection. |
| **Proxy Rotation** | Continuously shifts traffic through a pool of proxies. |

## 7. 🔒 System-Level Security Hardening

For advanced deployments, `security_hardening.py` provides OS-level protections:
- **File Integrity Monitoring:** Uses SHA-256 to ensure Siyarix hasn't been tampered with.
- **Seccomp-BPF:** Generates strict sandbox profiles for Docker deployments.
- **Privilege Checking:** Ensures Siyarix is never inadvertently run with dangerous excessive permissions.

## 8. 📜 The Audit Trail

Transparency is key. Every safety-related event is logged in a tamper-evident, SHA-256 hash-chained log (`audit_log.py`).

| Event Type | What gets logged |
|-------|-------------|
| **Blocked Command** | The command, the reason it was blocked, and the matched pattern. |
| **Emergency Stop** | The trigger reason and the exact timestamp. |
| **Safe Mode Violation** | The attempted command, the active persona, and the target. |
| **DLP Redaction** | The *type* of pattern redacted (e.g., "AWS Key"), but **never** the actual key. |

> [!NOTE]
> The audit log is mathematically linked. Modifying a past entry breaks the cryptographic chain, immediately alerting administrators to tampering.
