# Configuration Guide

Siyarix uses a layered configuration system with four tiers (lowest to highest priority): code defaults, settings file, environment variables, and CLI flags.

## Configuration layers

1. **Code defaults** — Defined in `config.py` `DEFAULTS` dict
2. **Settings file** — `~/.siyarix/settings.toml`
3. **Environment variables** — Prefixed with `SIYARIX_`
4. **CLI flags** — Per-command overrides

## Environment variables

| Variable | Config key | Description |
|----------|------------|-------------|
| `SIYARIX_CONFIG` | `_config_path` | Path to custom config file |
| `SIYARIX_HOME` | `_home_dir` | Override `~/.siyarix/` directory |
| `SIYARIX_DEBUG` | `log_level` | Enable debug logging |
| `SIYARIX_PROVIDER` | `model_provider` | AI provider override |
| `SIYARIX_TIMEOUT` | `scan_timeout` | Tool timeout in seconds |
| `SIYARIX_LOG_LEVEL` | `log_level` | Logging level |
| `SIYARIX_NO_TELEMETRY` | `_no_telemetry` | Disable telemetry |
| `SIYARIX_SAFE_MODE` | `_safe_mode` | Restrict to reconnaissance only |

## AI provider models

Each provider has a configurable model name in `settings.toml`:

```toml
model_provider = "auto"
openai_model = "gpt-4o"
gemini_model = "gemini-2.0-flash"
anthropic_model = "claude-3-5-sonnet-20241022"
deepseek_model = "deepseek-chat"
groq_model = "llama3-70b-8192"
together_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
ollama_url = "http://localhost:11434"
ollama_model = "llama3.1"
lmstudio_url = "http://localhost:1234"
llamacpp_url = "http://localhost:8080"
vllm_url = "http://localhost:8000"
localai_url = "http://localhost:8080"
```

## Local-only providers

| Provider | Endpoint | Setup |
|----------|----------|-------|
| Ollama | `http://localhost:11434` | `ollama pull llama3.1 && ollama serve` |
| LM Studio | `http://localhost:1234` | Enable API server in settings |
| llama.cpp | `http://localhost:8080` | `./server -m model.gguf` |
| vLLM | `http://localhost:8000` | `vllm serve model` |
| LocalAI | `http://localhost:8080` | `local-ai run` |
| Registry | Built-in | Heuristic planner, no external calls |

## Proxy configuration

```toml
proxy = "http://proxy.example.com:8080"
proxy_pool = "http://proxy1:8080,http://proxy2:8080"
```

The proxy pool rotates through the list for each connection.

## Client profile

Controls HTTP fingerprint:

```toml
client_profile = "desktop_chrome"
# Options: desktop_chrome, desktop_firefox, android_mobile, ios_safari
```

## Color themes

```toml
color_theme = "dark"
# Options: system, default, dark, light, minimal, neon
```

Preview themes: `siyarix themes`

## Config commands

```bash
siyarix config list           # Show all settings
siyarix config get <key>      # Get a single value
siyarix config set <key> <value>  # Set a value
siyarix config reset           # Reset to defaults
siyarix config edit            # Open in $EDITOR
```

## Credential management

```bash
siyarix creds list                    # List stored credentials
siyarix creds set <provider> <key>    # Store a credential
siyarix creds get <provider> <key>    # Retrieve (masked)
siyarix creds delete <provider> <key> # Remove
siyarix creds rotate                  # Rotate encryption key
```

## Next steps

- [Troubleshooting](troubleshooting.md)
- [CLI Commands](../user/cli-commands.md)
