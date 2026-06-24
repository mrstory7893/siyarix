# CLI Commands Reference

Siyarix is a CLI-first security operations platform built on **Typer**. All functionality is accessible via the `siyarix` binary with subcommands and command groups.

---

## Global Options

```bash
siyarix [OPTIONS] COMMAND [ARGS]...
```

| Option | Description |
|--------|-------------|
| `--config`, `-c` | Path to custom config file (YAML/JSON) |
| `--batch`, `-b` | Path to batch script file to execute |
| `--mode`, `-m` | Execution mode: `autonomous`, `integrated`, `offline`, `registry` |
| `--target`, `-t` | Set initial target for the session |
| `--session` | Resume a previous session by ID |
| `--resume` | Resume the last existing session |
| `--version` | Show version information |
| `--help` | Show help message |

---

## Usage Modes

1. **Interactive REPL**: `siyarix` (no subcommand) — launches the context-aware chat interface with 54+ slash commands
2. **Direct Command**: `siyarix scan 10.0.0.1` — executes and exits
3. **Pipe Mode**: `echo "scan 10.0.0.1" | siyarix` — batch commands via stdin
4. **Batch File**: `siyarix --batch script.txt` — execute a script file
5. **Goal-Driven Agent**: `siyarix agent "enumerate services"` — autonomous Observe-Reason-Act loop

---

## Core Commands

### `init`

Interactive setup wizard — ethics pledge, requirements check, provider setup, and persona configuration:

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
| `--mode`, `-m` | Execution mode (`autonomous`, `integrated`, `offline`, `registry`) |
| `--output`, `-o` | Output format (`table`, `json`, `yaml`, `csv`, `html`, `quiet`) |
| `--parallel`, `-p` | Number of parallel workers |
| `--timeout` | Timeout per tool in seconds |
| `--save`, `-s` | Save results to database |
| `--dry-run` | Plan only, do not execute |
| `--notify` | Send notification on completion |
| `--no-banner` | Suppress ASCII banner |
| `--profile` | Use specific command profile |

Scan presets for specialized workflows:

| Subcommand | Description |
|------------|-------------|
| `siyarix scan-quick <target>` | Fast port discovery (top 100 ports, no service detection) |
| `siyarix scan-full <target>` | All ports, service + OS detection, default scripts |
| `siyarix scan-deep <target>` | Multi-pass deep scan (4 progressive phases) |
| `siyarix scan-web <target>` | Web application security scan (whatweb, nikto, nuclei) |

> **Note:** Cloud provider scanning, mobile APK analysis, and IoT device scanning are under active development and not yet available as dedicated subcommands. These capabilities are on the Siyarix roadmap.

### `discover`

Asset and service discovery for specified targets:

```bash
siyarix discover <target> [--deep] [--export file]
```

| Option | Description |
|--------|-------------|
| `--deep`, `-d` | Deep discovery (OS, services, vulnerabilities) |
| `--export`, `-e` | Export to file (JSON/YAML) |

### `run`

Convert natural language into structured execution plans:

```bash
siyarix run "scan my network for open ports" [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--target`, `-t` | Target for the command |
| `--mode`, `-m` | Execution mode |
| `--dry-run` | Plan only, do not execute |
| `--save`, `-s` | Persist workflow execution |
| `--resume`, `-r` | Resume a persisted plan by ID (or `latest`) |

### `agent`

Goal-driven autonomous agent with Observe-Reason-Act loop:

```bash
siyarix agent "find all vulnerabilities on our web server" [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--target`, `-t` | Target host/IP/URL |
| `--max-iter`, `-n` | Maximum agent iterations (default: 10) |
| `--mode`, `-m` | Agent mode: `registry` (deterministic), `autonomous` (full AI), `integrated` (hybrid) |
| `--stealth`, `-s` | Enable stealth mode |

### `health`

Comprehensive system health check — model providers, tools, resources, and component status:

```bash
siyarix health [--output table|json]
```

### `metrics`

Session performance metrics — scan counts, durations, tool usage, cache hit rates:

```bash
siyarix metrics [--output table|json|prometheus] [--export file]
```

### `ci-gate`

CI/CD pipeline compliance gate — fails the build if security thresholds are not met:

```bash
siyarix ci-gate [--allow-degraded]
```

### `report`

Generate assessment reports from the knowledge graph:

```bash
siyarix report generate [--format html|markdown|json|sarif] [--output file]
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

API key management for AI providers:

```bash
siyarix auth set-key <provider> --key <api_key>
siyarix auth show
```

Supported providers: openai, gemini, anthropic, groq, together, openrouter.

### `profile`

Command profile management for reusable command templates:

| Command | Description |
|---------|-------------|
| `siyarix profile save-cmd <name> <command>` | Save a reusable command profile |
| `siyarix profile list-cmds` | List saved command profiles |
| `siyarix profile rm-cmd <name>` | Remove a saved command profile |

### `audit`

Tamper-evident audit trail management using SHA-256 hash chaining:

| Command | Description |
|---------|-------------|
| `siyarix audit report <framework>` | Generate compliance audit report |
| `siyarix audit logs` | View detailed audit logs |
| `siyarix audit verify` | Verify audit chain integrity |

### `config`

CLI configuration and settings management:

| Command | Description |
|---------|-------------|
| `siyarix config list` | Show all settings |
| `siyarix config get <key>` | Get a single setting |
| `siyarix config set <key> <value>` | Set a setting |
| `siyarix config reset [key]` | Reset a setting (or all) to defaults |

### `completions`

Generate and install shell completions:

```bash
siyarix completions install [bash|zsh|fish|powershell]
```

### `theme`

Terminal color theme customization:

| Command | Description |
|---------|-------------|
| `siyarix theme list` | List available color themes |
| `siyarix theme set <name>` | Set default color theme |
| `siyarix theme preview [name]` | Preview a theme |
| `siyarix theme appearance [name]` | Alias for theme preview |

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
| `siyarix tool-registry list` | List all discovered tools on PATH |
| `siyarix tool-registry providers` | List configured model providers with preference order |
| `siyarix tool-registry update-metadata <path>` | Regenerate tool metadata file |

### `security`

Security operations commands — incident management, vulnerability tracking, threat hunting, MITRE ATT&CK coverage, and dashboards:

| Command | Description |
|---------|-------------|
| `siyarix security dashboard` | Show security operations dashboard |
| `siyarix security incidents` | List security incidents |
| `siyarix security incident <id>` | Show incident details |
| `siyarix security incident-create` | Create a new security incident |
| `siyarix security vulnerabilities` | List vulnerabilities with CVSS scores |
| `siyarix security remediation-plan` | Generate prioritized remediation plan |
| `siyarix security hunt <query_id>` | Execute a threat hunt query |
| `siyarix security queries` | List available threat hunting queries |
| `siyarix security mitre-coverage` | Show MITRE ATT&CK technique coverage |
| `siyarix security playbooks` | List incident response playbooks |

### `compliance`

Run compliance assessments against security frameworks:

```bash
siyarix compliance run <framework> <target>
```

Supported frameworks: SOC2, NIST, GDPR, PCI-DSS, ISO-27001, HIPAA.

### `playbook`

Execute, list, and validate YAML playbooks:

| Command | Description |
|---------|-------------|
| `siyarix playbook run <path>` | Execute a YAML playbook file |
| `siyarix playbook list` | List playbooks in a directory |
| `siyarix playbook validate <path>` | Validate a playbook file |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error / unknown command / target missing |
| 2 | Health check failure / validation error |
| 3 | Critical findings detected / file missing |
