# Documentation Map

## Navigation Guide

```
docs/
├── getting-started/     → New user onboarding
├── user/                → Daily usage & workflows
├── developer/           → Codebase & contributions
├── architecture/        → System design & internals
├── ai/                  → AI provider & agent docs
├── security/            → Ethics, safety, threat model
└── legal/               → Licensing & governance
```

---

## Who Should Read What

### New Users

Start here:

1. [Installation](getting-started/installation.md) — install Siyarix on your platform
2. [Onboarding Wizard](getting-started/onboarding.md) — interactive setup walkthrough
3. [Setup & Configuration](getting-started/setup.md) — configure API keys and settings
4. [First Run](getting-started/first-run.md) — run your first commands
5. [Configuration Reference](getting-started/configuration.md) — detailed configuration guide
6. [CLI Commands](user/cli-commands.md) — command reference

### Daily Users

- [Interactive Chat](user/interactive-chat.md) — using the REPL and slash commands
- [Security Workflows](user/security-workflows.md) — common security testing workflows
- [AI Workflows](user/ai-workflows.md) — AI-powered operations and autonomous agents
- [Reporting & Output](user/reporting.md) — output formats, audit logs, metrics
- [Cloud Scanning](user/cloud-scanning.md) — AWS, Azure, GCP, K8s, Docker scanning
- [Compliance Frameworks](user/compliance-frameworks.md) — SOC2, ISO27001, NIST, GDPR, HIPAA, PCI-DSS
- [Threat Intelligence](user/threat-intelligence.md) — MITRE ATT&CK, MISP, STIX feeds
- [Playbooks](user/playbooks.md) — reusable incident response workflows
- [Workflow Files](user/workflow-files.md) — YAML/JSON DAG workflow reference
- [Deception & Canary Tokens](user/deception-and-canary-tokens.md) — honeypot detection, canary tokens
- [Importing Findings](user/importing-findings.md) — import Nessus, Burp, Metasploit, STIX results
- [Offline Registry](user/offline-registry.md) — offline response system and registry packs
- [IaC Scanning](user/iac-scanning.md) — Terraform, CloudFormation, Helm, Dockerfile scanning
- [Mobile Scanning](user/mobile-scanning.md) — Android APK security analysis
- [IoT Scanning](user/iot-scanning.md) — firmware analysis, serial port scanning

### Developers

- [Contribution Guide](developer/contribution-guide.md) — how to contribute to Siyarix
- [Codebase Overview](developer/codebase-overview.md) — module structure and key subsystems
- [Module Architecture](developer/module-architecture.md) — execution engine, planner, gate, agents
- [Testing](developer/testing.md) — test framework, writing tests, coverage targets
- [Building & Packaging](developer/building.md) — build, package, publish

### Architects

- [System Overview](architecture/overview.md) — high-level system design
- [AI Agent Pipeline](architecture/ai-agent-pipeline.md) — AI processing pipeline
- [Provider Abstraction](architecture/provider-abstraction.md) — 24-provider design
- [Execution Engine](architecture/execution-engine.md) — plan execution and tool orchestration
- [Memory & State](architecture/memory-and-state.md) — persistence and caching
- [Security Model](architecture/security-model.md) — security architecture
- [Experience Intelligence](architecture/experience-intelligence.md) — context tracking, skill profiling, predictions
- [Interaction Modes](architecture/interaction-modes.md) — 9 interaction modes reference
- [Intent Routing](architecture/intent-routing.md) — 4-stage semantic routing pipeline

### AI Engineers

- [Multi-Provider Routing](ai/multi-provider-routing.md) — provider registration, failover, session-disabled providers
- [Persona System](ai/persona-system.md) — persona switching, system prompts, available personas
- [Multi-Wave Execution](ai/multi-wave-execution.md) — iterative execution, live streaming, command review
- [Prompt Architecture](ai/prompt-architecture.md) — prompt construction and context management
- [Agent Reasoning](ai/agent-reasoning.md) — planning and reasoning pipeline
- [Tool Execution](ai/tool-execution.md) — tool lifecycle and parsing
- [Safety & Hallucination](ai/safety-and-hallucination.md) — safety constraints and hallucination detection
- [Multi-Model Ensemble](ai/multi-model-ensemble.md) — parallel LLM voting strategies

### Security Researchers

- [Ethical Hacking Policy](security/ethical-hacking-policy.md) — authorized use and boundaries
- [Abuse Prevention](security/abuse-prevention.md) — safety controls and prevention layers
- [Threat Model](security/threat-model.md) — security analysis and mitigations
- [Vulnerability Reporting](security/vulnerability-reporting.md) — how to report issues
- [Operational Security](security/operational-security.md) — OPSEC features and stealth
- [HSM Integration](security/hsm-integration.md) — YubiKey, PKCS#11, TPM support

### Legal & Compliance

- [AGPL-3.0 License Guide](legal/agpl-license-guide.md) — what the license means
- [Why AGPL?](legal/why-agpl.md) — rationale behind the license choice
- [Plugin Exception](legal/plugin-exception.md) — AGPL exception for third-party plugins
- [NOTICE File Explained](legal/note-file-explained.md) — NOTICE structure and purpose
- [Disclaimer](legal/disclaimer.md) — warranty and liability
- [Trademark Policy](legal/trademark-policy.md) — trademark usage guidelines
- [Responsible AI Usage](legal/responsible-ai-usage.md) — AI governance and transparency

---

## Documentation Tree

```
docs/
├── getting-started/
│   ├── installation.md          # pip, brew, winget, npm, source installs
│   ├── onboarding.md            # Interactive setup wizard (12-step walkthrough)
│   ├── setup.md                 # API keys, env vars, config, credential store
│   ├── first-run.md             # Health check, scan, chat, first commands
│   ├── configuration.md         # Settings reference, env var mapping
│   └── troubleshooting.md       # Common issues and solutions
│
├── user/
│   ├── cli-commands.md          # Full command reference (50+ commands)
│   ├── interactive-chat.md      # REPL, slash commands, multi-turn chat
│   ├── security-workflows.md    # Recon, vuln assessment, exploitation, IR
│   ├── ai-workflows.md          # AI planning, multi-agent, failover
│   ├── reporting.md             # Report formats, audit logging, metrics
│   ├── cloud-scanning.md        # AWS, Azure, GCP, K8s, Docker scanning
│   ├── compliance-frameworks.md # SOC2, ISO27001, NIST, GDPR, HIPAA, PCI-DSS
│   ├── threat-intelligence.md   # MITRE ATT&CK, MISP, STIX feed ingestion
│   ├── playbooks.md             # Reusable incident response workflows
│   ├── workflow-files.md        # YAML/JSON DAG workflow format reference
│   ├── deception-and-canary-tokens.md  # Honeypot detection, canary tokens
│   ├── importing-findings.md    # Nessus, Burp, Metasploit, STIX import
│   ├── offline-registry.md      # Offline response registry packs
│   ├── iac-scanning.md          # Terraform, CloudFormation, Helm, Dockerfile
│   ├── mobile-scanning.md       # Android APK static analysis
│   └── iot-scanning.md          # Firmware analysis, serial port scanning
│
├── developer/
│   ├── codebase-overview.md     # Module structure and key subsystems
│   ├── contribution-guide.md    # Setup, workflow, conventions, PR process
│   ├── module-architecture.md   # Execution engine, planner, gate, agents
│   ├── testing.md               # Test framework, writing tests, coverage
│   └── building.md              # Build, package, publish
│
├── architecture/
│   ├── overview.md              # High-level system design and data flow
│   ├── ai-agent-pipeline.md     # Intent routing, planning, execution
│   ├── provider-abstraction.md  # 24-provider manager, interface, failover
│   ├── execution-engine.md      # Step execution, dependency resolution
│   ├── memory-and-state.md      # Knowledge graph, persistence, caching
│   ├── security-model.md        # Permission gate, masking, audit
│   ├── experience-intelligence.md  # XI subsystem — context, skills, predictions
│   ├── interaction-modes.md     # 9 interaction modes reference
│   └── intent-routing.md        # 4-stage semantic routing pipeline
│
├── ai/
│   ├── multi-provider-routing.md  # 24 providers, preference chains, CB
│   ├── persona-system.md          # Persona switching, system prompts
│   ├── multi-wave-execution.md    # Iterative execution, live streaming
│   ├── prompt-architecture.md     # System context, safety constraints
│   ├── agent-reasoning.md         # Goal decomposition, multi-agent
│   ├── tool-execution.md          # Tool discovery, parsing, errors
│   ├── safety-and-hallucination.md  # Response sensor, danger analysis
│   └── multi-model-ensemble.md    # Parallel LLM voting strategies
│
├── security/
│   ├── ethical-hacking-policy.md   # Authorized use, scope, compliance
│   ├── abuse-prevention.md         # Danger analysis, emergency stop, OPSEC
│   ├── threat-model.md             # Assets, boundaries, mitigations
│   ├── vulnerability-reporting.md  # Reporting process, disclosure
│   ├── operational-security.md     # TOR, proxy rotation, stealth
│   └── hsm-integration.md          # YubiKey, PKCS#11, TPM support
│
└── legal/
    ├── agpl-license-guide.md       # AGPL-3.0-or-later explained
    ├── why-agpl.md                 # Rationale for choosing AGPL
    ├── plugin-exception.md         # AGPL exception for third-party plugins
    ├── note-file-explained.md      # NOTICE structure and purpose
    ├── disclaimer.md               # Warranty and liability disclaimer
    ├── trademark-policy.md         # Name/logo usage guidelines
    └── responsible-ai-usage.md     # AI governance and transparency
```

---

## Section Purposes

| Section | Purpose | Primary Audience |
|---------|---------|-----------------|
| `getting-started/` | First-time setup, configuration, troubleshooting | All users |
| `user/` | Daily CLI usage, command reference, workflows | Operators |
| `developer/` | Codebase internals, contribution guide | Contributors |
| `architecture/` | System design, data flow, security model | Architects |
| `ai/` | AI provider system, agent reasoning | AI engineers |
| `security/` | Ethics, safety, threat model, OPSEC | Security team |
| `legal/` | Licensing, trademark, governance | Legal/compliance |

---

## Future Expansion

The current structure supports expansion as the project grows:

```
docs/
├── plugins/       → Plugin system (sandboxing, lifecycle, SDK)
├── api/           → REST/gRPC API (auth, endpoints, SDK)
├── operations/    → Monitoring, logging, performance tuning
├── governance/    → Additional governance beyond legal
└── contributing/  → Expanded contributor guides
```

Each new section can be added without breaking the existing structure.

---

## Conventions

- **Filenames**: lowercase with hyphens (`multi-provider-routing.md`)
- **Cross-references**: relative paths (`../security/threat-model.md`)
- **Code examples**: fenced with language tag (` ```bash `, ` ```python `)
- **Tables**: Used for structured reference data
- **Consistent terminology**: "provider" not "LLM", "tool" not "binary", "plan" not "script"
