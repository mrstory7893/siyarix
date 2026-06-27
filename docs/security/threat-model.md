# 🎯 Siyarix Threat Model

As a security tool, it's important to understand the risks and protections built into Siyarix. This document outlines the basic threat model and the mitigations I've tried to engineer into the system.

## 💎 Critical Assets

Here is what Siyarix tries to protect locally:

| Asset | Description |
|-------|-------------|
| **AI Provider API Keys** | Your tokens for OpenAI, Anthropic, Gemini, etc. |
| **Credential Store** | The encrypted vault holding your secrets. |
| **Scan Results** | Discovered target data and vulnerabilities. |
| **Session & Audit Logs** | Your command history and local trails. |

## 🚧 Trust Boundaries

```text
┌──────────────┐     ┌──────────────┐     ┌───────────────┐
│   User TTY   │────▶│   Siyarix    │────▶│  AI Provider  │
│  (Terminal)  │     │ CLI Process  │     │    (Cloud)    │
└──────────────┘     └──────┬───────┘     └───────────────┘
                            │
                    ┌───────▼───────┐
                    │   External    │
                    │    Tools      │
                    │ (nmap, etc.)  │
                    └───────────────┘
```

### Boundary 1: User → Siyarix
- **The Threat:** Shell or command injection.
- **Our Defense:** The `InputValidator` enforces syntax rules and the `PermissionGate` validates commands before passing them to the OS.

### Boundary 2: Siyarix → AI Provider
- **The Threat:** Accidentally sending local secrets to a third-party AI cloud.
- **Our Defense:** The **DLP Engine** tries to redact common secret patterns *before* data leaves your machine.

### Boundary 3: Siyarix → External Tools
- **The Threat:** An external tool acts unpredictably.
- **Our Defense:** Subprocess isolation and strict command validation.

---

## ⚔️ Threats and Mitigations

### T1: API Key Exfiltration
- **Defense:** The `CredentialStore` encrypts your keys locally. The DLP engine attempts to redact them from prompts.

### T2: LLM Prompt Injection
- **Defense:** The AI does not have direct access to your shell. Everything the AI suggests must pass through the `PermissionGate` and you must manually confirm hybrid commands.

### T3: Data Leakage to the Cloud
- **Defense:** Masking replaces IPs, passwords, and API keys with safe placeholders (e.g., `[REDACTED_IP_1]`).

### T4: Unauthorized Tool Execution
- **Defense:** The Permission Gate blocks known dangerous commands like `rm -rf /`. `Safe Mode` can lock the system to reconnaissance-only tools.

### T5: Audit Log Tampering
- **Defense:** Siyarix uses a hash chain for audit logs to help detect local tampering.

## 🛡️ Core Security Assumptions

To maintain this security posture, Siyarix assumes:
1. Your local terminal environment and OS user account are reasonably secure.
2. The OS protects the file permissions of the `~/.siyarix/` directory.
3. AI providers are treated as untrusted third parties.
4. External tools execute as standard subprocesses without requiring raw `root` access unless explicitly authorized.
