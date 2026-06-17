# Security Policy

**Effective Date:** June 2026  
**Version:** 3.0.0  
**Applies to:** Siyarix v3.0.x and all earlier supported versions

Siyarix is built by security professionals for security professionals. The platform handles sensitive operations, API credentials, target data, and privileged command execution. The security of the platform itself is our highest priority. We deeply value the role of the security community in keeping Siyarix robust and trustworthy.

---

## Supported Versions

We actively provide security patches for the following versions:

| Version | Status | Security Patches | Recommended Action |
|---------|--------|------------------|--------------------|
| **v3.0.x (Latest)** | Active | Full priority support | Run latest patch |
| **v2.0.x** | Maintenance | Critical patches only (until 2026-12-17) | Upgrade to v3.0 |
| **< v2.0** | End of Life | No patches | Upgrade immediately |

We recommend always running the latest available release to benefit from the most up-to-date security features and patches.

---

## Reporting a Vulnerability

### Private Disclosure Process

If you discover a security vulnerability, **do not open a public GitHub issue.** We operate a coordinated disclosure process to ensure vulnerabilities are fixed before public awareness.

1. **GitHub Security Advisories (Preferred)**

   Navigate to: `https://github.com/mufthakherul/siyarix/security/advisories`

   Click "New advisory" and provide the details requested. This is the most secure and efficient method for coordinating with the maintainer team and automatically enables CVE assignment through GitHub.

2. **Private Email (Alternative)**

   Send encrypted details to the security contact listed on the maintainer's GitHub profile. We strongly recommend GPG encryption for any sensitive information, exploit code, or proof-of-concept data.

### What to Include

To help us respond quickly and effectively, please include:

| Element | Description |
|---------|-------------|
| **Vulnerability type** | Command injection, credential leak, RCE, privilege escalation, etc. |
| **Affected components** | Specific modules, files, or features affected |
| **Affected versions** | Which versions are vulnerable |
| **Steps to reproduce** | Clear, minimal, actionable reproduction steps |
| **Impact assessment** | What an attacker could achieve (access level, data exposure, etc.) |
| **Proof of Concept** | PoC code or demonstration (optional but helpful) |
| **Suggested fix** | If you have a proposed patch or mitigation |

---

## Scope

### In-Scope (We Want These Reports)

- Privilege escalation within the Siyarix execution environment
- Weaknesses in the **Credential Store** (AES-256-GCM encryption, key derivation, memory handling)
- Bypassing the **Safety Resolver**, **Permission Gate**, or **Danger Analysis** engine
- Failures in the **Masking Engine** leading to data leakage to AI providers
- Remote code execution (RCE) or command injection through crafted inputs
- Audit log manipulation or cryptographic chain integrity failures
- Authentication or authorization bypass in the REST API
- Plugin sandbox escape or file system traversal

### Out-of-Scope (Tracked Elsewhere)

- Publicly known CVEs in upstream dependencies (tracked via automated Dependabot and pip-audit)
- Theoretical attacks requiring physical access or local administrative privileges
- UI/UX issues without direct security impact
- Self-inflicted denial of service (user running destructive commands on their own systems)
- Features listed as stubs/not-yet-implemented in the codebase

---

## Our Commitment to You

| Milestone | Target |
|-----------|--------|
| **Acknowledgement** | Within 48 hours of report submission |
| **Triage & Assessment** | Within 5 business days |
| **Fix Development** | Priority-based, typically within 14 days for critical issues |
| **Embargo Period** | 90 days from report date before public disclosure |
| **CVE Assignment** | Coordinated through GitHub Security Advisories and MITRE |
| **Credit** | Reporter credited in release notes and security acknowledgments (with permission) |

We will coordinate the disclosure timeline with you, keep you informed of progress, and ensure proper attribution for your contribution to Siyarix's security.

---

## Built-in Security Features

Siyarix is hardened by design with the following security layers:

| Feature | Description |
|---------|-------------|
| **Encrypted Credential Store** | All API keys, tokens, and secrets encrypted with AES-256-GCM using a locally derived master key |
| **Safety Resolver** | Two-stage AI-powered and heuristic danger analysis for every generated command before execution |
| **Permission Gate** | Risk-tiered classification (SAFE, LOW, MEDIUM, HIGH, CRITICAL) with configurable action policies |
| **Masking Engine** | Bidirectional redaction of IPs, domains, credentials, and custom patterns before data leaves the host |
| **Tamper-Evident Audit Log** | Every action recorded in a SHA-256 cryptographically chained trail with `verify` command |
| **Event Bus Security** | Internal event system with access controls for inter-component communication |
| **Plugin Sandbox** | Plugins loaded from dedicated restricted user directory (`~/.siyarix/plugins/`) |
| **DLP Engine** | Pattern-based detection and prevention of sensitive data leakage |
| **Stealth Engine** | TOR routing support and honeypot detection for operational security |
| **Metrics Isolation** | Performance and usage metrics collected without exposing operational data |

---

## Safe Harbor

We encourage good-faith security research. If you follow this coordinated disclosure policy:

- We will **not** pursue legal action against you for your research
- We consider your research **authorized** under applicable computer fraud and abuse laws (including the U.S. CFAA and similar international statutes)
- We will work with you to understand and resolve the reported issue promptly
- We will provide public credit for verified and accepted vulnerability reports, with your permission

---

*Thank you for helping keep Siyarix and its users secure. Together, we can build a safer open-source security ecosystem.*

---

*SPDX-License-Identifier: AGPL-3.0-or-later*
