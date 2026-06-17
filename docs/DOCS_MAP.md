# Documentation Map

Guide to navigating the Siyarix documentation.

## Documentation tree

```
docs/
├── getting-started/       # Installation, onboarding, configuration
│   ├── installation.md    # Multi-platform install (pip, brew, winget, docker)
│   ├── onboarding.md      # Interactive 12-step wizard
│   ├── setup.md           # API keys, credentials, settings
│   ├── first-run.md       # First session walkthrough
│   ├── configuration.md   # Settings deep-dive
│   └── troubleshooting.md # Common fixes
│
├── user/                  # Daily operations
│   ├── cli-commands.md    # 50+ CLI commands
│   ├── interactive-chat.md# AI REPL & slash commands
│   ├── security-workflows.md  # Recon, vuln assessment, IR
│   ├── cloud-scanning.md  # Multi-cloud security
│   ├── compliance-frameworks.md # SOC2, NIST, GDPR, etc.
│   ├── threat-intelligence.md  # MITRE ATT&CK, MISP/STIX
│   ├── playbooks.md       # IR workflows
│   ├── workflow-files.md  # YAML/JSON DAG reference
│   └── ...                # Additional user guides
│
├── developer/             # Building & extending Siyarix
│   ├── codebase-overview.md   # Module structure
│   ├── contribution-guide.md  # Workflow & standards
│   ├── module-architecture.md # Component design
│   ├── testing.md             # pytest, coverage, CI
│   └── building.md            # Packaging & distribution
│
├── architecture/          # System design & internals
│   ├── overview.md        # High-level data flow
│   ├── ai-agent-pipeline.md   # Reasoning & execution
│   ├── provider-abstraction.md # 24-provider interface
│   ├── execution-engine.md    # Step orchestration
│   ├── memory-and-state.md    # Knowledge graph & caching
│   ├── security-model.md      # Permission gate & audit
│   ├── interaction-modes.md   # 9 interaction ways
│   └── intent-routing.md      # Semantic routing pipeline
│
├── ai/                    # AI provider & agent systems
│   ├── multi-provider-routing.md # Failover & load balancing
│   ├── persona-system.md       # 10 security mindsets
│   ├── agent-reasoning.md      # Goal decomposition
│   ├── tool-execution.md       # Discovery & parsing
│   └── multi-model-ensemble.md # LLM voting strategies
│
├── security/              # Safety, ethics & threat models
│   ├── vulnerability-reporting.md  # How to report vulns
│   ├── threat-model.md         # System threat model
│   ├── operational-security.md # TOR, stealth, evasion
│   ├── hsm-integration.md      # HSM (stub-aware)
│   ├── ethical-hacking-policy.md    # Rules of engagement
│   └── abuse-prevention.md     # 7-layer safety system
│
└── legal/                 # Licensing & governance
    ├── agpl-license-guide.md   # AGPL-3.0 overview
    ├── why-agpl.md             # License rationale
    ├── trademark-policy.md     # Branding guidelines
    ├── responsible-ai-usage.md # AI ethics
    ├── disclaimer.md           # Legal disclaimer
    ├── note-file-explained.md  # NOTICE file
    └── plugin-exception.md     # Plugin license exception
```

## Quick navigation

### New users
1. [Installation](getting-started/installation.md)
2. [Onboarding Wizard](getting-started/onboarding.md)
3. [Setup & Configuration](getting-started/setup.md)
4. [First Run](getting-started/first-run.md)

### Security operators
- [Interactive Chat](../user/interactive-chat.md)
- [Security Workflows](../user/security-workflows.md)
- [Cloud & IaC Scanning](../user/cloud-scanning.md)
- [Compliance Frameworks](../user/compliance-frameworks.md)

### Developers
- [Contribution Guide](developer/contribution-guide.md)
- [Codebase Overview](developer/codebase-overview.md)
- [Testing](developer/testing.md)
- [Module Architecture](developer/module-architecture.md)

## Conventions

| Term | Definition |
|------|------------|
| **Provider** | An AI backend (e.g., OpenAI, Ollama) |
| **Tool** | A security executable on PATH (e.g., nmap) |
| **Plan** | An AI-generated sequence of commands |
| **Workflow** | A predefined YAML/JSON DAG execution |
| **Persona** | A specialized behavioral framing for the AI |
