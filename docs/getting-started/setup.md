# Setup & Configuration

After installing Siyarix, configure your AI provider credentials and workspace preferences.

## First-run wizard

The easiest way to configure Siyarix is to launch it — the interactive wizard runs automatically:

```bash
siyarix
```

Re-run the wizard at any time:

```bash
siyarix init
siyarix init --force
```

## API keys

Set at least one AI provider API key as an environment variable:

```bash
export OPENAI_API_KEY="sk-..."           # OpenAI
export GEMINI_API_KEY="..."              # Google Gemini
export ANTHROPIC_API_KEY="sk-ant-..."    # Anthropic Claude
export GROQ_API_KEY="gsk_..."            # Groq
export TOGETHER_API_KEY="..."            # Together AI
export DEEPSEEK_API_KEY="sk-..."         # DeepSeek
```

### .env file

Place a `.env` file in the current directory or `~/.siyarix/.env`:

```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
```

Siyarix loads it automatically on startup.

## Credential vault

For encrypted storage of API keys and secrets using AES-256-GCM with OS keyring integration:

```bash
siyarix auth set-key openai          # Prompts for key (input hidden)
siyarix auth show                    # List configured providers
```

Credentials are stored encrypted at rest via the system keyring with AES-256-GCM file fallback, and auto-cleared on session end.

## Settings management

Settings are persisted in `~/.siyarix/settings.toml` (TOML format). Manage via CLI:

```bash
siyarix config list                  # View all settings
siyarix config get model_provider    # Get single value
siyarix config set model_provider gemini  # Set value
siyarix config edit                  # Open in $EDITOR
siyarix config reset                 # Restore defaults
```

## Key settings

| Setting | Default | Description |
|---------|---------|-------------|
| `model_provider` | `auto` | AI provider: `auto`, `openai`, `gemini`, `anthropic`, `ollama`, etc. |
| `default_output_format` | `table` | Output style: `table`, `json`, `yaml`, `csv`, `html`, `xml`, `raw`, `quiet` |
| `default_parallel` | `3` | Concurrent tool execution limit |
| `scan_timeout` | `300` | Tool timeout in seconds |
| `log_level` | `info` | Logging verbosity |
| `color_theme` | `default` | Theme: `cyber_noir`, `matrix`, `bloodmoon`, `arctic`, `goldenrod`, `eclipse`, `synthwave`, `dark`, `light`, `neon`, `minimal`, `default` |
| `stealth_mode` | `false` | Enable OPSEC features (TOR, jitter, proxy rotation) |
| `persona` | `auto` | AI mindset: `redteam`, `blueteam`, `dfir`, `appsec`, `network`, `malware`, `osint`, `compliance`, `cloud`, `ics` |

## Next steps

- [First Run](first-run.md) — Execute your first command
- [Configuration Deep-Dive](configuration.md) — Full settings reference
