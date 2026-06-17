# First Run

This guide walks through your first Siyarix session.

## Launch the CLI

```bash
siyarix
```

You will see the banner and available commands grouped by category.

## Check help

```bash
siyarix --help
```

Command groups include:

| Group / Command | Purpose |
|----------------|---------|
| `scan` | Network/service scanning against targets |
| `run` | Natural language → execution engine |
| `agent` | Goal-driven autonomous agent |
| `discover` | Asset/service/vulnerability discovery |
| `init` | Interactive setup wizard |
| `config` | Configuration management |
| `auth` | API key management |
| `security` | Security operations (incidents, playbooks, hunt, mitre) |
| `report` | Report generation (HTML, JSON, Markdown, PDF) |
| `health` | System health check |
| `metrics` | Performance metrics |
| `audit` | Audit trail management and verification |
| `theme` | Terminal theme customization |
| `workflow` | DAG workflow file execution |
| `palette` | Interactive command palette |

## Run a health check

```bash
siyarix health
```

Reports component status, Python version, platform info, and system state.

## Run a basic scan

```bash
siyarix scan quick example.com
```

This runs a quick port scan against the target using default tools.

## Interactive chat mode

Start an AI-powered interactive session:

```bash
siyarix chat
```

This opens the REPL with slash commands, auto-complete, and multi-turn conversation. Type `/help` inside the chat for available commands.

## Check discovered tools

```bash
siyarix scan --list-tools
```

Lists all security tools discovered on your system (100+ supported tools).

## What happens on first run

The first time you run `siyarix`, the **onboarding wizard** starts automatically. See the [full guide](onboarding.md) for a detailed walkthrough of all 12 steps.

```bash
siyarix
```

If the terminal is non-interactive (CI/pipe), you'll need to run `siyarix init` explicitly.

## Next steps

- [Onboarding Wizard](onboarding.md) — detailed setup walkthrough
- [Configuration Guide](configuration.md)
- [CLI Commands Reference](../user/cli-commands.md)
