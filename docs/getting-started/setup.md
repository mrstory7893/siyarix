# Setup & Configuration

Awesome, you've got Siyarix installed! Now let's get it configured so it knows how you like to work. Siyarix is highly customizable, and we've built an intuitive setup process to make it as painless as possible.

---

## The First-Run Wizard

The absolute easiest way to get started is to let Siyarix guide you. The first time you launch the CLI, it will automatically start an interactive onboarding wizard. This wizard takes you through 12 quick steps, including platform detection, discovering installed security tools, selecting your preferred AI provider, and picking a persona.

```bash
siyarix
```

Need to change your initial choices later? You can manually trigger the setup wizard at any time:

```bash
siyarix init
siyarix init --force   # Force the wizard to run even if you're already configured
```

---

## Hooking up the Brain: API Keys

Siyarix needs access to an AI provider to do its heavy lifting. It supports a massive roster of 24 providers. To get started, you just need to set at least one API key.

Here are some common ones:

### 🧠 OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

### 🌌 Google Gemini
```bash
export GEMINI_API_KEY="..."
```

### 🎭 Anthropic Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### ⚡ Groq
```bash
export GROQ_API_KEY="gsk_..."
```

### 🤝 Together AI
```bash
export TOGETHER_API_KEY="..."
```

### Don't Like Environment Variables? Use a `.env` File!

You can also drop a `.env` file either in the current directory or in `~/.siyarix/.env`. Siyarix will automatically load it:

```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Fine-Tuning Your Settings

Siyarix saves all your preferences in a human-readable TOML file located at `~/.siyarix/settings.toml`. 

### Key Settings at a Glance

| Setting | Default | What it Does |
|---------|---------|--------------|
| `model_provider` | `auto` | Choose your brain: `auto`, `openai`, `gemini`, `openrouter`, `anthropic`, `groq`, `together`, `deepseek`, `xai`, `mistral`, `perplexity`, `ollama`, `lmstudio` (and many more!) |
| `default_output_format` | `table` | How do you like your data? `table`, `json`, `yaml`, or `csv`. |
| `default_parallel` | `3` | How many tools should run at once? |
| `scan_timeout` | `300` | Max seconds a tool is allowed to run before Siyarix kills it. |
| `log_level` | `info` | How chatty should the logs be? |
| `color_theme` | `default` | Make it yours: `system`, `default`, `dark`, `light`, `minimal`, `neon`. |
| `stealth_mode` | `false` | Enable OPSEC features to fly under the radar. |
| `persona` | `auto` | Define Siyarix's personality (`auto`, `redteam`, `blueteam`, `dfir`, etc.). |

### Managing Settings via CLI

You don't even have to open the file to change things. The built-in config commands have you covered:

```bash
# See everything
siyarix config list

# Get a specific value
siyarix config get model_provider

# Change a value
siyarix config set model_provider gemini
siyarix config set default_output_format json

# Open the config file in your default editor
siyarix config edit

# Messed up? Reset to defaults!
siyarix config reset
```

---

## Keeping Secrets Safe: Credential Vault

Tired of leaving API keys in plain text? Siyarix features an encrypted credential store built right in.

```bash
siyarix creds set openai api_key
# Siyarix will prompt you for the key, and input will be hidden!
```

This vault uses robust AES-256-GCM encryption (with a Fernet fallback) and fully supports key rotation, import, and export.

---

## What's Next?

You are all set! Let’s get our hands dirty and run some commands.

- 👉 **[First Run](first-run.md)** — Learn how to fire off your first AI-orchestrated command!
- 👉 **[CLI Commands Reference](../user/cli-commands.md)** — Explore the full power of Siyarix.
