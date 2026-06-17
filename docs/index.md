# Welcome to Siyarix v3

**Siyarix** is an AI-native cybersecurity operations platform that acts as your personal AI orchestration agent. It bridges the gap between natural language security objectives and deterministic tool execution.

Describe what you need in plain English — *"scan this subnet for open ports"* — and Siyarix routes it through a robust multi-provider AI abstraction layer, generates an execution plan, and runs local open-source tools to deliver precise results safely.

---

## Why Siyarix?

> Human oversight with machine speed.

We believe AI shouldn't replace security operators — it should take over the repetitive scripting, tool parsing, and workflow glue so you can focus on what matters.

Siyarix is built on four design pillars:

- **CLI-First** — Everything works in your terminal. No bloated dashboards required.
- **Provider Agnostic** — Use OpenAI, Anthropic, Gemini, or run completely offline with local models. If one fails, automatic failover keeps you moving.
- **Safe & Deterministic** — Every AI-generated command passes through a two-stage permission gate before execution. 38 dangerous patterns are blocked by default.
- **Extreme Parsing** — 114+ tool output parsers transform raw security tool output into structured, actionable findings.

---

## Capabilities at a Glance

| Domain | What Siyarix Does |
|--------|-------------------|
| **AI Orchestration** | Routes tasks across 24 AI providers with automatic failover, circuit breakers, multi-model ensemble voting, and offline heuristic fallback |
| **Security Tooling** | Discovers 100+ tools on your PATH, executes them with intelligent planning, and parses outputs into structured findings |
| **Workflow Automation** | YAML/JSON DAG pipelines, reusable playbooks, goal-driven autonomous agents with Observe-Reason-Act loop |
| **Compliance & Intel** | Maps findings to MITRE ATT&CK, ingests MISP/STIX feeds, assesses against SOC2, ISO27001, NIST, PCI-DSS, GDPR, HIPAA |
| **Cloud & Infrastructure** | Scans AWS, Azure, GCP, Kubernetes, Docker, Terraform, CloudFormation, Helm for misconfigurations |
| **Mobile & IoT** | Android APK static analysis, firmware inspection, serial port enumeration, device identification |
| **Safety & OPSEC** | Two-stage permission gate, encrypted credential vault, tamper-evident audit trail, TOR routing, stealth mode |

---

## Quick Links

<div class="grid cards" markdown>

-   :material-rocket-launch: **Getting Started**

    ---

    Install Siyarix and set up your environment in minutes.

    [Installation Guide](getting-started/installation.md)

-   :material-console: **User Guide**

    ---

    Learn about available commands, interactive chat, and specific workflows.

    [CLI Reference](user/cli-commands.md)

-   :material-brain: **AI Internals**

    ---

    Understand multi-provider routing, agent reasoning, and multi-wave execution.

    [AI Agent Pipeline](architecture/ai-agent-pipeline.md)

-   :material-security: **Security Model**

    ---

    Review how Siyarix handles safe execution, threat models, and OPSEC.

    [Security Architecture](architecture/security-model.md)

</div>

---

## Quick Start

```bash
# Launch interactive session
siyarix

# Quick scan
siyarix scan quick example.com

# Natural language
siyarix run "enumerate services on 10.0.0.1"

# Autonomous agent
siyarix agent "find all vulnerabilities on the web server"

# Health check
siyarix health
```

---

## Who Is It For?

| Role | What Siyarix Offers |
|------|---------------------|
| **Penetration Testers** | Automated reconnaissance, intelligent tool chaining, structured reporting |
| **Security Engineers** | Custom playbooks, CI/CD integration, compliance automation |
| **SOC Analysts** | Incident response workflows, threat hunting, MITRE ATT&CK mapping |
| **Cloud Architects** | Multi-cloud posture scanning, IaC security validation |
| **Researchers** | AI-assisted analysis, extensible parser framework, plugin system |
| **Students** | Learn security tool orchestration, AI-assisted education, CTF automation |

---

## Project Status

**Stable release** — v3.0.0 is the current stable version, suitable for production assessments. Breaking changes follow semantic versioning and are documented in the [changelog](../CHANGELOG.md).

---

> **Disclaimer & Ethical Use**: Siyarix is designed for authorized security testing, research, and defensive operations only. Unauthorized access or exploitation without explicit consent is strictly prohibited. Please read our [Ethical Hacking Policy](security/ethical-hacking-policy.md) before use.
