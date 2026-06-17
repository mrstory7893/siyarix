# Onboarding Wizard

Siyarix includes a comprehensive interactive setup wizard that guides you through configuration, provider selection, tool discovery, and security hardening on first launch.

## Quick start

```bash
siyarix
```

If the `~/.siyarix/.initialized` marker is absent, the wizard starts automatically. You can also launch it explicitly:

```bash
siyarix init
siyarix init --force   # re-run even if already configured
```

## Wizard steps

| Step | Section | Description |
|------|---------|-------------|
| 0 | Welcome & ethics pledge | ASCII logo, welcome panel, ethical use pledge (must type `c` to continue) |
| 1 | Platform detection | OS, architecture, CPU, RAM, GPU, shell, terminal, package managers, proxy, WSL, container, virtual env, disk space |
| 2 | Requirements check | Python >= 3.12, pip, git, curl, PATH issues, config directory writability |
| 3 | Dependencies | Core Python packages (pydantic, rich, httpx, cryptography, etc.) with auto-install option |
| 4 | Tool discovery | 9 essential security tools (nmap, openssl, dig, whois, tcpdump, tshark, etc.) with guided install |
| 5 | Credential storage | Initialize encrypted credential store (AES-256-GCM / Fernet) |
| 6 | Provider selection | Choose your AI provider (see below) |
| 7 | Mode configuration | Autonomous, Integrated (default), Registry-only |
| 8 | Persona & system message | Select behavior persona, view/customize system prompt |
| 9 | Preferences | Theme, output format, notifications, log level, history retention, command review, stealth mode, auto-update |
| 10 | Network diagnostics | Internet connectivity (1.1.1.1 / 8.8.8.8), DNS resolution, provider API connectivity |
| 11 | Finalize | Summary review, health check, .env migration, shell completions, PATH setup, restart |

## Provider selection options

At step 6, the wizard presents five paths:

### 0 — Recommended (auto-detect)

Analyzes free RAM and suggests a local provider with a security-tuned LLM:

| Tier | RAM | Example models |
|------|-----|----------------|
| Light | <= 4 GB | `drana-infinity-3b`, `qwen3.5:4b`, `gemma4-e4b-secops` |
| Balanced | 4-8 GB | `drana-infinity-7b`, `qwen3.5-9b-red-team`, `mythos-sec:8b` |
| Capable | 8-16 GB | `mythos-sec:8b`, `qwen3:14b`, `qwen3.5-9b-red-team` |
| High-end | 16+ GB | `mythos-sec:24b`, `gemma4:26b`, `qwen3.5-9b-red-team` |

Supports **Ollama** (convenient, ~200 MB daemon) or **llama.cpp** (zero idle RAM, manual) — with model download, GGUF extraction from Ollama cache, and optional Ollama uninstall.

### 1 — Online provider

Choose from 11 cloud providers and enter an API key (stored encrypted):

- OpenAI, Anthropic, Google Gemini, Groq, Together AI, OpenRouter, DeepSeek, xAI/Grok, Mistral AI, Perplexity, Azure OpenAI

### 2 — Offline provider

Choose a local inference engine and configure endpoint URL + model name:

- Ollama, LM Studio, llama.cpp, vLLM, LocalAI

### 3 — Custom provider

Free-form: provider name, base URL, API key, and model name.

### 4 — Skip

Configure a provider later via `siyarix config set model_provider <name>` and `siyarix auth set-key <provider>`.

## Post-wizard setup

After completing the wizard, the following is in place:

- **~/.siyarix/** directory with full subdirectory structure (17+ directories)
- **~/.siyarix/.initialized** marker with version, timestamp, platform, and choices metadata
- **~/.siyarix/settings.toml** with your selected preferences
- **Encrypted credential store** with any API keys provided
- **Shell completions** installed (bash, zsh, fish, PowerShell)
- **Siyarix added to PATH** (via shell profile)
- **Selected persona tools** installed for your persona (appsec, network_security, red_team, blue_team, dfir)

## Unattended / CI setup

For non-TTY environments, the wizard prints:

```
Siyarix needs initial setup. Run siyarix init to start the setup wizard.
```

You can configure Siyarix programmatically:

```bash
export MODEL_PROVIDER=openai
export OPENAI_API_KEY=sk-...
siyarix config set model_provider openai
siyarix auth set-key openai
```

## Directory structure created

```
~/.siyarix/
├── personas/           # Personality definitions
├── personas/custom/    # User-defined personas
├── profiles/           # Active profile
├── memory/             # Knowledge graph persistence
├── logs/sessions/      # Session logs
├── logs/audit/         # Tamper-evident audit trail
├── cache/tool_outputs/ # Cached tool results
├── cache/ai_plans/    # AI-generated plans
├── cache/dns/          # DNS resolution cache
├── cache/intel/        # Threat intelligence cache
├── cache/scan_results/ # Scan result cache
├── cache/user_data/    # User data cache
├── templates/reports/  # Report templates
├── templates/playbooks/ # Playbook templates
├── playbooks/          # Custom playbooks
├── achievements/       # User achievements
├── sessions/           # Session snapshots
├── masking/            # Data masking rules
├── bin/                # Installed binaries (auto-added to PATH)
├── models/             # Downloaded GGUF models
├── .initialized        # Marker file
├── settings.toml       # User settings
└── config.yaml         # Config alias (→ settings.toml)
```

## Next steps

- [Configuration Guide](configuration.md) — detailed settings reference
- [First Run](first-run.md) — run your first commands
- [CLI Commands](../user/cli-commands.md) — full command reference
