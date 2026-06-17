# CLI Commands Reference

Siyarix v3.0.0 is a CLI-first security operations platform built on **Typer**. All functionality is accessible via the `siyarix` binary with subcommands and command groups.

---

## Global Options

```bash
siyarix [OPTIONS] COMMAND [ARGS]...
```

| Option | Description |
|--------|-------------|
| `--config`, `-c` | Path to custom config file |
| `--batch`, `-b` | Path to batch script file to execute |
| `--mode`, `-m` | Execution mode: `autonomous`, `integrated`, `registry` |
| `--target`, `-t` | Set initial target for the session |
| `--session` | Resume a previous session by ID |
| `--resume` | Resume the last existing session |
| `--version` | Show version information |
| `--help` | Show help message |

---

## Usage Modes

1. **Interactive REPL**: `siyarix` (no subcommand) — launches the context-aware chat interface with 40+ slash commands
2. **Direct Command**: `siyarix scan 10.0.0.1` — executes and exits
3. **Pipe Mode**: `echo "scan 10.0.0.1" \| siyarix` — batch commands via stdin
4. **Batch File**: `siyarix --batch script.txt` — execute a script file
5. **Goal-Driven Agent**: `siyarix agent "enumerate services"` — autonomous Observe-Reason-Act loop
6. **REST API Server**: `siyarix serve` — start the HTTP/WebSocket API server

---

## Core Commands

### `init`

Interactive 12-step onboarding wizard — ethics pledge, requirements check, provider setup, and persona configuration:

```bash
siyarix init [--force] [--skip-requirements]
```

### `scan`

Run security scans against one or more targets using discovered tools on `PATH`. Supports `@targets.txt` multi-target mode.

```bash
siyarix scan <targets...> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--tool`, `-t` | Specific tool to use |
| `--mode`, `-m` | Execution mode (`autonomous`, `integrated`, `registry`) |
| `--output`, `-o` | Output format (`table`, `json`, `yaml`, `csv`, `html`, `xml`, `raw`, `quiet`) |
| `--parallel`, `-p` | Number of parallel workers |
| `--timeout` | Timeout per tool in seconds |
| `--save`, `-s` | Save results to database |
| `--dry-run` | Plan only, do not execute |
| `--profile` | Use specific command profile |
| `--cloud` | Run cloud provider scan (`aws`, `azure`, `gcp`, `kubernetes`, `docker`, `all`) |

Scan subcommands for specialized workflows:

| Subcommand | Description |
|------------|-------------|
| `siyarix scan quick <target>` | Fast reconnaissance scan |
| `siyarix scan full <target>` | Comprehensive scan with all tools |
| `siyarix scan web <target>` | Web application security scan |
| `siyarix scan network <target>` | Network infrastructure scan |
| `siyarix scan cloud <provider>` | Cloud configuration scan |
| `siyarix scan mobile <apk>` | Mobile APK analysis |
| `siyarix scan iot <target>` | IoT device/firmware scan |

### `discover`

Asset and service discovery for specified targets:

```bash
siyarix discover <target>
```

### `run`

Convert natural language into structured execution plans:

```bash
siyarix run "scan my network for open ports"
siyarix run "check SOC 2 compliance on the infrastructure"
```

### `agent`

Goal-driven autonomous agent with Observe-Reason-Act loop:

```bash
siyarix agent "find all vulnerabilities on our web server"
```

| Option | Description |
|--------|-------------|
| `--mode` | Agent mode: `registry` (deterministic), `autonomous` (full AI), `hybrid`, `interactive` |

### `health`

Comprehensive system health check — model providers, tools, resources, and component status:

```bash
siyarix health
```

### `metrics`

Session performance metrics — scan counts, durations, tool usage, cache hit rates:

```bash
siyarix metrics
```

### `ci-gate`

CI/CD pipeline compliance gate — fails the build if security thresholds are not met:

```bash
siyarix ci-gate
```

### `report`

Generate assessment reports from the KnowledgeGraph:

```bash
siyarix report generate [--format html|json|markdown|pdf] [--output file]
```

### `serve`

Start the REST API + WebSocket server for programmatic access:

```bash
siyarix serve [--host 0.0.0.0] [--port 8000]
```

### `version`

Display installed version and build information:

```bash
siyarix version
```

### `palette`

Open interactive command palette (requires `prompt_toolkit`):

```bash
siyarix palette
```

### `render-cmd`

Render a saved command profile with key=value substitution:

```bash
siyarix render-cmd <name> [key=value ...]
```

---

## Sub-Command Groups

### `auth`

API key management for AI providers. Supported providers: openai, gemini, anthropic, groq, together, openrouter, deepseek, xai, mistral, perplexity, cerebras, fireworks, zai, minimax, moonshot, nvidia, huggingface, azure.

```bash
siyarix auth set-key <provider>
siyarix auth list-keys
siyarix auth remove-key <provider>
```

### `profile`

Command profile management for reusable command templates:

| Command | Description |
|---------|-------------|
| `siyarix profile list-cmds` | List saved command profiles |
| `siyarix profile save-cmd <name> <command>` | Save a reusable command profile |
| `siyarix profile rm-cmd <name>` | Remove a saved command profile |

### `audit`

Tamper-evident audit trail management using SHA-256 hash chaining:

| Command | Description |
|---------|-------------|
| `siyarix audit report` | View audit trail report |
| `siyarix audit logs` | View detailed audit logs |
| `siyarix audit verify` | Verify audit chain integrity |

### `config`

CLI configuration and settings management:

| Command | Description |
|---------|-------------|
| `siyarix config list` | Show all settings |
| `siyarix config get <key>` | Get a single setting |
| `siyarix config set <key> <value>` | Set a setting |
| `siyarix config reset` | Reset to defaults |
| `siyarix config edit` | Open config in default editor |
| `siyarix config backup` | Backup current configuration |
| `siyarix config restore` | Restore configuration from backup |

### `completions`

Generate and install shell completions:

```bash
siyarix completions [bash|zsh|fish|powershell]
```

### `theme`

Terminal color theme customization. 12 built-in themes:

| Command | Description |
|---------|-------------|
| `siyarix theme list` | List available color themes |
| `siyarix theme set <name>` | Set default color theme |
| `siyarix theme preview [name]` | Preview a theme |

Available themes: `CYBER_NOIR`, `MATRIX`, `BLOODMOON`, `ARCTIC`, `GOLDENROD`, `ECLIPSE`, `SYNTHWAVE`, `DARK`, `LIGHT`, `NEON`, `MINIMAL`, `DEFAULT`.

### `cache`

Manage the LRU cache:

| Command | Description |
|---------|-------------|
| `siyarix cache status` | Show cache statistics |
| `siyarix cache clear` | Clear all cached data |

### `tool-registry`

Manage and inspect discovered tools and providers:

| Command | Description |
|---------|-------------|
| `siyarix tool-registry list` | List all discovered tools on PATH (80+ parsers) |
| `siyarix tool-registry providers` | List configured model providers with preference order |
| `siyarix tool-registry update-metadata` | Refresh tool metadata cache |

### `compliance`

Run compliance assessments against security frameworks:

```bash
siyarix compliance run --framework soc-2
siyarix compliance run --framework all
```

### `playbook`

Execute, list, and validate incident response playbooks:

| Command | Description |
|---------|-------------|
| `siyarix playbook run <name>` | Execute a saved playbook |
| `siyarix playbook list` | List available playbooks |
| `siyarix playbook validate <path>` | Validate a playbook file |

---

## Additional Commands

| Command | Description |
|---------|-------------|
| `siyarix session-log` | View structured session log |
| `siyarix session branch` | Create or switch session branches |

---

## Output Formats

All commands support the `--output` / `-o` flag with these formats:

| Format | Description |
|--------|-------------|
| `TABLE` | Rich formatted table (default) |
| `JSON` | Machine-readable JSON |
| `YAML` | YAML structured output |
| `CSV` | Comma-separated values |
| `HTML` | HTML report |
| `XML` | XML structured output |
| `RAW` | Raw unformatted output |
| `QUIET` | Minimal output |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error / unknown command / target missing |
| 2 | Validation error |
| 3 | Permission denied / file missing |
| 4 | Timeout |
| 5 | Safety gate denied |
