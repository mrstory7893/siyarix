# Installation Guide

Siyarix v3.0.0 requires **Python 3.11 or later** and supports Linux, macOS, Windows (PowerShell 5.1+), and HarmonyOS. Minimum 512 MB RAM (4 GB+ recommended for AI operations), ~500 MB disk for tool dependencies.

## PyPI (recommended)

```bash
pip install siyarix
```

### Optional extras

| Extra | Provides |
|-------|----------|
| `openai` | OpenAI SDK |
| `gemini` | Google Generative AI SDK |
| `anthropic` | Anthropic SDK |
| `groq` | Groq SDK |
| `together` | Together AI SDK |
| `ollama` | Ollama Python library |
| `autonomous` | OpenAI + Gemini + Anthropic |
| `cli` | Rich + Textual TUI |
| `siem` | Splunk/ELK forwarders |
| `api` | FastAPI REST server with JWT auth |
| `all` | All extras |

```bash
pip install "siyarix[openai,gemini,anthropic]"
pip install "siyarix[cli]"
pip install "siyarix[all]"
```

## Package managers

**macOS (Homebrew)**
```bash
brew install mufthakherul/siyarix/siyarix
```

**Windows (Winget)**
```bash
winget install Mufthakherul.Siyarix
```

**Windows (Chocolatey)**
```bash
choco install siyarix
```

**Node.js (npx)**
```bash
npx @mufthakherul/siyarix --help
```

**Debian/Ubuntu**
```bash
sudo dpkg -i siyarix_3.0.0-1_all.deb
```

**Docker**
```bash
docker pull siyarix:latest
docker run siyarix:latest --help
```

## Build from source

```bash
git clone https://github.com/mufthakherul/siyarix.git
cd siyarix
python -m venv .venv
# source .venv/bin/activate  (Linux/macOS)
# .\.venv\Scripts\Activate.ps1  (Windows)
pip install -e ".[all,cli,siem]"
```

## Verify installation

```bash
siyarix --version
siyarix --help
```

## Next steps

- [Onboarding Wizard](onboarding.md) — Interactive 12-step setup
- [Setup & Configuration](setup.md) — API keys, credentials, settings
- [First Run](first-run.md) — Your first session
