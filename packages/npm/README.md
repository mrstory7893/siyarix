# @mufthakherul/siyarix-agent-cli

Official npm launcher for the CosmicSec Python CLI agent.

## Install

```bash
npm install -g @mufthakherul/siyarix-agent-cli
```

## Usage

```bash
# Auto-installs Python package when needed and runs the CLI
siyarix-agent --help

# Alias
siyarix --version

# Explicit installer command
siyarix-agent-install
```

## How it works

- Detects Python 3.11+.
- Installs `siyarix-agent` via `pipx` (preferred) or `pip --user`.
- Runs `python -m siyarix_agent.main` with your CLI arguments.

## Requirements

- Node.js 20+
- Python 3.11+
