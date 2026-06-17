# Interactive Chat (REPL) Mode

The Siyarix REPL is the primary interaction interface — a full-featured interactive shell with AI-assisted planning, 40+ slash commands, split-pane layout, and SmartAutocomplete via `prompt_toolkit`.

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
| `/help` | Show all slash commands |
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
| `/mode` | Switch interaction mode (integrated/registry/autonomous) |
| `/model` | Switch AI provider model |
| `/provider` | Switch AI provider |
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

---

## Natural Language Input

Type any natural language command and the AI interprets it via `TaskPlanner`:

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

### Session Branching

Create divergent session branches with `/branch`:

```
> /branch investigation-v2
> /branch list
> /branch switch investigation-v1
```

Each branch maintains independent conversation history and findings.

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
