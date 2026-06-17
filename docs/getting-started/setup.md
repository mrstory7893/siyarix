# Setup & Configuration

## First-run wizard

On first launch, Siyarix runs the [interactive onboarding wizard](onboarding.md) that guides you through 12 steps — platform detection, requirements, tool discovery, provider selection, mode, persona, preferences, and more.

```bash
siyarix
```

If this is your first run, the wizard starts automatically. You can also launch it explicitly:

```bash
siyarix init
siyarix init --force   # re-run even if already configured
```

## API keys

Siyarix supports multiple AI providers. Set at least one API key:

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

### Google Gemini

```bash
export GEMINI_API_KEY="..."
```

### Anthropic Claude

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Groq

```bash
export GROQ_API_KEY="gsk_..."
```

### Together AI

```bash
export TOGETHER_API_KEY="..."
```

### Environment file

Create a `.env` file in `~/.siyarix/.env` or in the current directory:

```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
```

The environment module (`environment.py`) auto-loads `.env` files and maps provider names to expected environment variable names.

## Configuration file

Settings are stored in `~/.siyarix/settings.toml` (TOML format, human-editable).

### Key settings

| Setting | Default | Description |
|---------|---------|-------------|
| `model_provider` | `auto` | Preferred AI provider: `auto`, `openai`, `gemini`, `openrouter`, `anthropic`, `groq`, `together`, `deepseek`, `xai`, `mistral`, `perplexity`, `cerebras`, `fireworks`, `ollama`, `lmstudio`, `llamacpp`, `vllm`, `localai` |
| `default_output_format` | `table` | Output format: `table`, `json`, `yaml`, `csv` |
| `default_parallel` | `3` | Max parallel tool executions |
| `scan_timeout` | `300` | Seconds before a tool is killed |
| `log_level` | `info` | Logging verbosity |
| `color_theme` | `default` | Terminal theme: `system`, `default`, `dark`, `light`, `minimal`, `neon` |
| `stealth_mode` | `false` | Enable stealth/evasion features |
| `persona` | `auto` | Active behavior persona (`auto`, `redteam`, `blueteam`, `dfir`, etc.) |
| `proxy` | `""` | HTTP proxy for outbound connections |
| `stealth_mode` | `false` | Enable stealth/evasion features |
| `persona` | `none` | Active behavior persona |
| `history_retention_days` | `90` | Days to keep scan history |

### View settings

```bash
siyarix config list
```

### Get a setting

```bash
siyarix config get model_provider
```

### Set a setting

```bash
siyarix config set model_provider gemini
siyarix config set default_output_format json
```

### Reset to defaults

```bash
siyarix config reset
```

### Edit config file directly

```bash
siyarix config edit
```

## Credential store

API keys and secrets can be stored in an encrypted vault:

```bash
siyarix creds set openai api_key
# Prompts for the key value (input hidden)
```

The vault uses AES-256-GCM encryption (or Fernet as fallback) and supports key rotation, import, and export.

## Next steps

- [First Run](first-run.md) — run your first commands
- [Configuration Reference](../user/cli-commands.md#config-commands)
