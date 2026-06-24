# Interactive Chat (REPL) Mode

The Siyarix REPL is the primary interaction interface — a full-featured interactive shell with AI-assisted planning, 54+ slash commands, split-pane layout, and SmartAutocomplete via `prompt_toolkit`.

---

## Launching

```bash
siyarix        # Opens the REPL directly (default when no subcommand given)
```

---

## Slash Commands

All available slash commands in the REPL:

| Command | Description |
|---------|-------------|
| `/help` | Show all slash commands (or `/help <cmd>` for details) |
| `/exit` | Exit the session |
| `/clear` | Clear conversation history |
| `/new` | Start a new conversation thread |
| `/history` | Show command history |
| `/tools` | List available tools from the registry |
| `/platform` | Show platform information |
| `/status` | Show session status |
| `/session` | Session management details |
| `/uptime` | Show session uptime |
| `/env` | Show environment variables |
| `/intents` | Show parsed intent history |
| `/shells` | List available shell tools |
| `/search` | Search through findings and history |
| `/examples` | Show usage examples |
| `/reset` | Reset session state |
| `/key` | Set or rotate API keys |
| `/theme` | Change terminal color theme |
| `/mode` | Switch interaction mode |
| `/model` | Switch AI provider model |
| `/provider` | Show/switch AI provider |
| `/report` | Generate a session report |
| `/split` | Toggle split-pane layout |
| `/batch` | Execute batch commands |
| `/opsec` | Operational security checks |
| `/siem` | SIEM integration commands |
| `/intel` | Threat intelligence operations |
| `/performance` | Show performance metrics |
| `/cache` | Cache management |
| `/campaign` | Campaign management for red team ops |
| `/kb` | Knowledge base queries |
| `/ticket` | Ticket/issue management |
| `/retest` | Re-run previous tests |
| `/stealth` | Toggle stealth mode |
| `/audit` | Audit trail commands |
| `/queue` | View execution queue |
| `/diff` | Diff between scan results |
| `/log` | View session logs |
| `/save` | Save current session |
| `/review` | Review session context |
| `/persona` | Set active persona |
| `/scan` | Quick scan command |
| `/savecmd` | Save a command profile |
| `/cmds` | List saved command profiles |
| `/cmd` | Run a saved command profile |
| `/context` | Show session context |
| `/version` | Show Siyarix version |
| `/config` | View/change configuration |
| `/agent` | Launch an autonomous agent |
| `/cancel` | Cancel current operation |
| `/esc` | Alias for /cancel |
| `/security-cmds` | List security commands for shell |
| `/run` | Run a command or tool |
| `/translate` | Translate intent to shell command |
| `/target` | Set or show current target |
| `/load` | Load a session from file |
| `/fork` | Fork the current session |
| `/export` | Export session data |
| `/plugins` | List available plugins |
| `/alias` | Manage command aliases |
| `/language` | Set interface language |
| `/learn` | Learn from session context |
| `/feedback` | Submit feedback |
| `/redteam` | Switch to red team mode |
| `/blueteam` | Switch to blue team mode |
| `/benchmark` | Run performance benchmarks |
| `/upgrade` | Check for upgrades |
| `/docs` | Open documentation |
| `/tutorial` | Start an interactive tutorial |
| `/bug` | Report a bug |
| `/suggest` | Suggest a feature |
| `/playbook` | Execute a playbook |
| `/stats` | Show session statistics |
| `/skills` | List available skills |

---

## Natural Language Input

Type any natural language command and the AI interprets it via the execution engine:

```
> scan 192.168.1.1
> find all open ports on example.com
> run a vulnerability scan against the web server
> what tools do I have available?
```

---

## Split-Pane Layout

Toggle a vertical split-pane view with `/split`:

- **Left pane**: Input area with conversation
- **Right pane**: Live output, logs, or status information

Change the right-pane view with `/split <timeline|metrics|cheatsheet|attack_map>`.

---

## SmartAutocomplete

The REPL includes `SmartAutocomplete` with:

- Tab completion for commands, targets, and file paths
- Context-aware suggestions based on conversation history
- Slash command discovery (type `/` to see all commands)

---

## Session Management

Sessions are persisted to SQLite (`~/.siyarix/sessions.db`):

- Commands executed with timestamps
- AI conversation history (multi-turn context)
- Findings and results
- Session duration and metadata

---

## Credential Store

API keys and secrets are stored with **AES-256-GCM** encryption in the local credential store. Manage keys via `/key` or the `auth` CLI command group.

---

## Pipe and Batch Mode

Commands can be piped via stdin:

```powershell
echo "scan 10.0.0.1" | siyarix
```

Or loaded from a batch file:

```bash
siyarix --batch commands.txt
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Auto-complete |
| `Up` / `Down` | Navigate command history |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+L` | Clear screen |
| `Ctrl+D` | Exit REPL |
