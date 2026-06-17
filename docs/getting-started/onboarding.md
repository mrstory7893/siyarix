# Onboarding Wizard

Siyarix includes a 12-step interactive wizard that configures providers, themes, security defaults, and notifications on first launch.

## Launching the wizard

```bash
siyarix                    # Auto-starts if not initialized
siyarix init               # Manual start
siyarix init --force       # Re-run even if configured
```

## The 12 steps

| Step | Action | Purpose |
|------|--------|---------|
| 0 | Welcome & Ethics Pledge | Acceptable use acknowledgment |
| 1-2 | System & Requirements | Detects OS, RAM, Python version |
| 3 | Dependencies | Installs missing core packages |
| 4 | Tool Discovery | Scans PATH for 80+ security tools |
| 5 | Credential Vault | Initializes AES-256-GCM encrypted store |
| 6 | AI Provider Selection | Cloud (OpenAI, Gemini, Anthropic, etc.) or local (Ollama, LM Studio) |
| 7 | Execution Mode | Autonomous, Integrated, or Registry-only |
| 8 | Persona Selection | Security mindset: redteam, blueteam, dfir, etc. |
| 9 | User Preferences | Theme, output format, log level |
| 10 | Network Diagnostics | Tests internet and API connectivity |
| 11 | Finalize | Creates workspace, configures PATH |

## AI provider selection (Step 6)

**Cloud providers**: OpenAI, Anthropic, Google Gemini, Groq, Together AI, DeepSeek, xAI, Mistral, Perplexity, OpenRouter, and more.

**Local engines**: Ollama, LM Studio, llama.cpp, vLLM, LocalAI — run fully offline with no API key required.

**Auto-detect**: Siyarix analyzes available RAM and suggests a model:
- <=4 GB: Lightweight (e.g., `drana-infinity-3b`)
- 4-8 GB: Balanced (e.g., `drana-infinity-7b`)
- 8-16 GB: High-performance (e.g., `mythos-sec:8b`)
- 16+ GB: Maximum (e.g., `mythos-sec:24b`)

## Workspace layout

```text
~/.siyarix/
├── personas/           # AI personality definitions
├── memory/             # Knowledge graph persistence
├── logs/audit/         # Tamper-evident audit trail
├── cache/tool_outputs/ # Cached tool results
├── templates/reports/  # Custom report templates
└── settings.toml       # Central configuration
```

## Unattended / CI setup

```bash
export MODEL_PROVIDER=openai
export OPENAI_API_KEY=sk-...
siyarix config set model_provider openai
siyarix auth set-key openai
```

## Next steps

- [First Run](first-run.md) — Launch your first scan
- [CLI Commands Reference](../user/cli-commands.md) — Complete command manual
