# Threat Model

This document identifies assets, trust boundaries, threats, and mitigations for Siyarix. Security is not an afterthought in this platform — it is foundational. Every component, from the credential store to the permission gate, is designed with defense in mind.

## Assets

| Asset | Description | Sensitivity |
|-------|-------------|-------------|
| AI provider API keys | Keys for OpenAI, Gemini, Anthropic, etc. | CRITICAL |
| Scan results | Target data, open ports, vulnerabilities | HIGH |
| Knowledge graph | Mapped relationships (hosts, credentials) | HIGH |
| Session logs | Command history, tool outputs | HIGH |
| Config file | Provider settings, proxy settings | MEDIUM |
| Credential store | AES-256-GCM encrypted vault of stored credentials | CRITICAL |
| Audit log | SHA-256 chained tamper-evident action trail | HIGH |

## Trust Boundaries

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   User TTY   │────▶│  Siyarix    │────▶│  AI Provider │
│  (terminal)  │     │  CLI Process│     │  (cloud)     │
└──────────────┘     └──────┬───────┘     └──────────────┘
                            │
                    ┌───────▼───────┐
                    │  External     │
                    │  Tools       │
                    │  (nmap, etc.)│
                    └───────────────┘
```

### Boundary 1: User → Siyarix
- **Threat**: Malicious input (shell injection, command injection)
- **Mitigation**: `InputValidator` with syntax validation, length limits, character restrictions, shell injection pattern detection, SSRF protection

### Boundary 2: Siyarix → AI Provider
- **Threat**: Sensitive data sent to third-party API
- **Mitigation**: `DLP Engine` redacts 40+ secret patterns (credentials, IPs, hostnames, API keys, JWTs). Bidirectional masking ensures consistency within a session

### Boundary 3: Siyarix → External Tools
- **Threat**: Tool vulnerability or unexpected behavior
- **Mitigation**: Subprocess isolation, timeouts, output size limits, `PermissionGate` validates all commands before execution

## Threats and Mitigations

### T1: API Key Exfiltration
- **Impact**: CRITICAL — unauthorized AI usage, cost
- **Mitigation**: `CredentialStore` encrypts at rest with AES-256-GCM. `DLP Engine` redacts keys from AI provider traffic. Keys never logged, never in debug output. `AuditLogger` records all access

### T2: Prompt Injection
- **Impact**: HIGH — unauthorized command execution
- **Mitigation**: `PermissionGate` two-stage gate (syntax + danger analysis) validates all commands. `DangerAnalyzer` blocks 38+ dangerous patterns. `ResponseGenerator` validates AI output for safety

### T3: Data Leakage to AI Provider
- **Impact**: HIGH — data exposure
- **Mitigation**: `DLP` bidirectional masking replaces IPs, hostnames, credentials. Session-scoped masking ensures consistency. Pattern types include API keys (OpenAI, AWS, GCP, Azure, GitHub, GitLab, Slack, Stripe), JWTs, SSH keys, passwords

### T4: Unauthorized Tool Execution
- **Impact**: CRITICAL — system damage
- **Mitigation**: Two-stage `PermissionGate` (syntax + danger). 38 dangerous pattern checks (disk destruction, fork bombs, network floods, privilege escalation). Persona-based ACLs. `Safe Mode` blocks all exploitation. `SecurityHardening` for system-level controls

### T5: Audit Log Tampering
- **Impact**: HIGH — loss of accountability
- **Mitigation**: SHA-256 hash chain links entries. Any modification breaks the chain. `siyarix audit-log verify` command validates chain integrity. SIEM forwarding provides off-system copy. Event bus integration for real-time monitoring

### T6: Credential Store Compromise
- **Impact**: CRITICAL — all stored credentials exposed
- **Mitigation**: AES-256-GCM encryption with 32-byte key, 12-byte nonce. Keys stored in OS keyring (preferred) with encrypted file fallback. PBKDF2 key derivation with 600,000 iterations. Optional KMS envelope encryption. Key rotation support. Rate-limited access (10 req/s)

### T7: AI Provider Compromise
- **Impact**: HIGH — command injection, data exfiltration
- **Mitigation**: `PermissionGate` blocks malformed commands. Registry fallback (heuristic planner) always available. `ProviderStateManager` circuit breaker prevents repeated retries to compromised providers

### T8: System Hardening Bypass
- **Impact**: MEDIUM — reduced security posture
- **Mitigation**: `SecurityHardening` module provides system-level hardening, file integrity monitoring, and container security checks. `StealthEngine` for covert operations with TOR routing, user-agent rotation, request jitter

## Security Assumptions

- The user's terminal environment is trusted
- Host OS file permissions protect `~/.siyarix/`
- AI providers are untrusted third parties
- External tools execute as subprocesses with standard OS isolation
- Network traffic to AI providers uses TLS
- The `cryptography` library is available for credential encryption
