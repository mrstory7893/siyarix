# Installation Guide

Welcome! Let's get Siyarix installed on your machine so you can start orchestrating your security tasks with AI. Siyarix is built with modern Python and designed to run seamlessly across all major platforms.

---

## What You Need

Before we start, make sure your system meets these basic requirements:

- **Python**: version 3.11 or later.
- **Operating System**: Windows, macOS, or Linux (including WSL2).
- **Memory**: At least 512 MB (though we recommend 4 GB+ to handle heavy AI operations smoothly).
- **Storage**: About 500 MB for various tool dependencies.

---

## The Fastest Way: PyPI

If you already have Python set up, the easiest way to install Siyarix is via `pip`:

```bash
pip install siyarix
```

### Power Up with Extras

Siyarix is highly modular. You can install optional packages depending on which AI providers and features you plan to use:

```bash
# Bring your favorite AI providers
pip install "siyarix[openai,gemini,anthropic]"

# Supercharge the terminal experience (Rich + Textual TUI)
pip install "siyarix[cli]"

# Hook up to your SIEM (Splunk, ELK)
pip install "siyarix[siem]"

# Or, just install absolutely everything!
pip install "siyarix[all]"
```

**Here’s the full list of available extras:**

| Tag | What You Get |
|-----|--------------|
| `openai` | OpenAI Python SDK |
| `gemini` | Google Generative AI SDK |
| `anthropic` | Anthropic SDK |
| `groq` | Groq SDK |
| `together` | Together AI SDK |
| `ollama` | Ollama Python library for local models |
| `autonomous` | The big three: OpenAI, Gemini, and Anthropic |
| `cli` | Rich-enhanced CLI experience + Textual TUI |
| `siem` | Splunk/ELK SIEM forwarders |
| `api` | FastAPI REST server with JWT auth |
| `all` | The whole kitchen sink! |

---

## Native Package Managers

Prefer using your OS's package manager? We’ve got you covered.

### 🍏 macOS (Homebrew)

```bash
brew install mufthakherul/siyarix/siyarix
```

### 🪟 Windows (Winget)

```bash
winget install Mufthakherul.Siyarix
```

### 🌐 Node.js (npx launcher)

If you live in the JS ecosystem, you can run Siyarix instantly without installing it globally:

```bash
npx @mufthakherul/siyarix --help
```

---

## Building from Source

Are you a developer looking to contribute, or just someone who loves the cutting edge? Here’s how to build Siyarix straight from the source:

```bash
# 1. Grab the code
git clone https://github.com/mufthakherul/siyarix.git
cd siyarix

# 2. Set up a pristine virtual environment
python -m venv .venv

# 3. Activate the environment
# On macOS / Linux:
source .venv/bin/activate
# On Windows:
# .\.venv\Scripts\Activate.ps1

# 4. Install Siyarix in editable mode with all the bells and whistles
pip install -e ".[all,cli,siem]"
```

---

## Let's Make Sure It Works

Once installed, let’s verify everything is ready to go:

```bash
siyarix --version
siyarix --help
```

If you see the awesome Siyarix banner and help menu, you’re in business! 🎉

---

## What's Next?

Now that Siyarix is installed, let's configure your AI keys and customize your environment.

- 👉 **[Setup & Configuration](setup.md)** — Launch the interactive wizard and get your API keys ready.
- 👉 **[First Run](first-run.md)** — Fire off your first AI-orchestrated command!
