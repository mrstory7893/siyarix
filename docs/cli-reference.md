# CLI Reference

This document lists primary subcommands and flags. The CLI is implemented with Typer; use `siyarix --help` for live help.

Top-level commands (examples):

- `scan` — run preconfigured scanning workflows (nmap, nuclei, ffuf)
  - `--profile <name>`: use a saved profile
  - `--format json|yaml`: output format

- `threat hunt` — AI-assisted hunting
  - `--target <target>`: domain, IP range, or CIDR
  - `--ai`: enable AI enrichment

- `plan` — create/run hybrid plans
  - `create`, `list`, `run`, `show` subcommands

- `incident` — incident lifecycle
  - `list`, `show`, `resolve`, `annotate`

Configuration files:
- `~/.siyarix/config.yaml` or project `.siyarix.yml` — stores API keys and defaults.
