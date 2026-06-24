# 🎯 Siyarix Threat Model

In Siyarix, security isn't an afterthought or a bolted-on feature—it is the foundation of the platform. This document outlines our threat model, detailing the assets we protect, our trust boundaries, potential threats, and the rigorous mitigations we've engineered into the system.

## 💎 Critical Assets

Here is what we are protecting. If these assets are compromised, the system fails.

| Asset | Description | Sensitivity |
|-------|-------------|-------------|
| **AI Provider API Keys** | Your tokens for OpenAI, Anthropic, Gemini, etc. | 🔴 CRITICAL |
| **Credential Store** | The AES-256-GCM encrypted vault holding your secrets. | 🔴 CRITICAL |
| **Scan Results** | Discovered target data, open ports, and vulnerabilities. | 🟠 HIGH |
| **Knowledge Graph** | The mapped relationships of hosts and network topologies. | 🟠 HIGH |
| **Session Logs** | Your command history and raw tool outputs. | 🟠 HIGH |
| **Audit Log** | The SHA-256 tamper-evident trail of actions. | 🟠 HIGH |
| **Config File** | Provider settings and network proxy configurations. | 🟡 MEDIUM |

## 🚧 Trust Boundaries

Understanding where data flows helps us identify where attacks might happen.

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
- **The Threat:** Malicious input from a compromised user account (e.g., shell or command injection).
- **Our Defense:** The `InputValidator` strictly enforces syntax rules, length limits, and scans for SSRF and shell injection patterns before processing anything.

### Boundary 2: Siyarix → AI Provider
- **The Threat:** Accidentally sending highly sensitive data (like your company's AWS keys or client IPs) to a third-party AI cloud.
- **Our Defense:** Our powerful **DLP Engine** redacts over 40+ secret patterns *before* the data leaves your machine. It uses session-scoped bidirectional masking to ensure you can still read the output locally!

### Boundary 3: Siyarix → External Tools
- **The Threat:** An external tool (like `nmap` or `nuclei`) acts unpredictably, or a vulnerability in the tool is exploited.
- **Our Defense:** Siyarix isolates subprocesses, enforces strict timeouts, limits output sizes, and uses the `PermissionGate` to validate every single command before it is passed to the OS.

---

## ⚔️ Threats and Mitigations

Here is exactly how Siyarix defends against specific attack vectors:

### T1: API Key Exfiltration
- **Impact:** 🔴 CRITICAL (Financial loss from unauthorized AI usage).
- **Defense:** The `CredentialStore` encrypts your keys at rest using AES-256-GCM. The DLP engine actively redacts these keys from all network traffic. Keys are never logged to console or debug files.

### T2: LLM Prompt Injection
- **Impact:** 🟠 HIGH (Tricking the AI into executing unauthorized commands).
- **Defense:** The AI does not have direct access to your shell. Everything the AI suggests must pass through the `PermissionGate` (syntax + danger analysis). The `DangerAnalyzer` actively blocks 38+ dangerous command patterns, and the user must manually confirm hybrid commands.

### T3: Data Leakage to the Cloud
- **Impact:** 🟠 HIGH (Exposing client data to AI training sets).
- **Defense:** Bidirectional masking replaces IPs, hostnames, passwords, JWTs, and API keys with safe placeholders (e.g., `[REDACTED_IP_1]`).

### T4: Unauthorized Tool Execution
- **Impact:** 🔴 CRITICAL (Accidental system damage).
- **Defense:** Strict Permission Gates prevent commands like `rm -rf /` or `dd`. Role-based personas and `Safe Mode` can completely lock down the system to reconnaissance-only tools.

### T5: Audit Log Tampering
- **Impact:** 🟠 HIGH (Loss of forensic accountability).
- **Defense:** Siyarix uses a cryptographic SHA-256 hash chain for audit logs. If an attacker deletes or alters a past log entry, the chain breaks, and `siyarix audit-log verify` will immediately flag the tampering.

### T6: Credential Store Compromise
- **Impact:** 🔴 CRITICAL (Total exposure of stored secrets).
- **Defense:** We use AES-256-GCM with a 32-byte key and 12-byte nonce, derived via PBKDF2 (600,000 iterations). Keys are preferably stored in the secure OS keyring. We also support AWS KMS envelope encryption for enterprise setups.

### T7: AI Provider Compromise
- **Impact:** 🟠 HIGH (The cloud AI goes rogue and sends malicious commands).
- **Defense:** Even if the AI provider is hacked, the `PermissionGate` blocks malformed or dangerous commands. Furthermore, our `ProviderStateManager` circuit breaker will automatically cut off a compromised or failing provider and failover to a local or offline model.

## 🛡️ Core Security Assumptions

To maintain this security posture, Siyarix assumes the following:
1. Your local terminal environment and OS user account are relatively secure.
2. The OS protects the file permissions of the `~/.siyarix/` directory.
3. AI providers are treated as **untrusted** third parties.
4. External tools execute as standard subprocesses without requiring raw `root` access unless explicitly authorized.
