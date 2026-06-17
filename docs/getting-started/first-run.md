# First Run

Your first Siyarix session walks through onboarding, health verification, and executing a live command.

## Step 1: Launch and onboard

```bash
siyarix
```

If Siyarix has not been initialized, the 12-step onboarding wizard launches automatically. Follow the prompts to configure your AI provider, credentials, and preferences.

See the [Onboarding Wizard](onboarding.md) for a detailed walkthrough of each step.

## Step 2: Verify health

Ensure everything is operational:

```bash
siyarix health
```

This checks Python version, installed tools, credential store status, provider connectivity, and disk space.

## Step 3: Run a scan

Execute a quick port scan against a domain:

```bash
siyarix scan quick example.com
```

Siyarix will plan the operation, route it through the permission gate, execute the tools, parse the output, and display structured results.

## Step 4: Enter the REPL

Launch the interactive REPL for multi-turn conversations:

```bash
siyarix
```

From the REPL you can run slash commands (`/scan`, `/run`, `/persona`), switch providers mid-session, and chain multiple operations.

## Step 5: Natural language execution

```bash
siyarix run "enumerate services on 10.0.0.1"
```

Siyarix interprets the request, selects appropriate tools, builds an execution plan, and presents the results.

## Getting help

```bash
siyarix --help              # Top-level help
siyarix scan --help         # Subcommand help
siyarix                     # /help lists all slash commands in REPL
```

## What's next

- [Interactive Chat](../user/interactive-chat.md) — Master the REPL
- [Security Workflows](../user/security-workflows.md) — Real-world scenarios
- [CLI Commands](../user/cli-commands.md) — Full command reference
