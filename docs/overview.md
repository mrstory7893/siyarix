# NexSec — Overview

NexSec (by CosmicSec-Lab) is a lightweight, autonomous security agent designed for fast, repeatable security operations from the terminal. It blends dynamic task planning with deterministic tooling to support scanning, threat hunting, incident management, and CI/CD automation.

Typing `siyarix` by itself now opens a richer assistant-style command center instead of a plain prompt. The landing screen highlights your current mode, theme, session, and model provider, while surfacing the most important actions up front.

Key principles:
- **Minimal cognitive load**: intuitive commands and streamlined names (primary CLI: `siyarix`, legacy alias: `siyarix-agent`).
- **Assistant-first UX**: the no-subcommand launch path shows quick actions, model/theme status, and a more polished landing screen.
- **Integrated execution**: use model-driven planning to orchestrate and combine classic tools (nmap, nuclei, ffuf) with internal analyzers.
- **Extensible**: plugin system and parsers for third-party security tools.
- **Scriptable**: outputs machine-readable JSON/YAML for automated pipelines.

Primary capabilities:
- Interactive AI Assistant (NexSec Chat)
- Polished command-center landing screen when launching `siyarix`
- Network & web scanning
- Threat hunting and enrichment (Autonomous assistance)
- Incident management and enterprise audit trail
- Enterprise Credential Vault (encrypted secrets & KMS)
- Integrated plans combining multiple security tools
- Cross-platform shell intelligence (bash/zsh/sh, PowerShell/CMD, fish, nushell, xonsh)
- Infra-aware tooling (Docker, Kubernetes, Terraform, cloud CLIs)
