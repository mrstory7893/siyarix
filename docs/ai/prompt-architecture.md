# Prompt Architecture

Siyarix constructs prompts dynamically from system context, user input, session state, persona configuration, and safety constraints. All prompts are defined in `src/siyarix/chat/prompts.py` and assembled at call time by `LLMEngineMixin._build_system_prompt()` in `chat/engine.py`.

---

## Prompt Structure

Every LLM request follows a layered structure:

```
[Persona Preamble] (optional — from persona system)
[System Prompt]    (SIYARIX_SYSTEM_PROMPT or NEUTRAL_SYSTEM_PROMPT)
[Custom Instructions] (optional — from additional_system_message setting)
[Workspace Context] (optional — AGENTS.md / SOUL.md)
[Execution Environment] (dynamically injected — OS, Shell)
[Conversation History] (truncated oldest-first to fit context window)
[User Input]       (natural language or structured command)
```

---

## Core System Prompts

### SIYARIX_SYSTEM_PROMPT

The full-spectrum system prompt (~60 lines) used with all named personas and universal mode:

```
You are Siyarix, an elite cybersecurity professional operating in a
terminal-driven environment.

- Platform Context (OS, shell, Windows-specific warnings)
- Operational Framework (Intent, Scope, Depth, Risk)
- Decision Logic (needs_tools=true/false)
- Output Format (JSON with needs_tools, reasoning, response, steps)
- Tool Execution Steps (shell command construction)
- Shell Quoting Rules (bash compatibility)
- Available Tool Categories (recon, exploitation, web, etc.)
- Output Analysis (post-execution synthesis)
- Communication Standards (MITRE ATT&CK, CVEs, remediation)
```

```python
SIYARIX_SYSTEM_PROMPT = f"""You are Siyarix, an elite cybersecurity professional operating in a terminal-driven environment.

{_platform_context()}

## Operational Framework
Analyse every request across four dimensions:
1. **Intent** — Chat/explanation, security operation, or tool analysis?
2. **Scope** — Network, web, cloud, endpoint, identity, mobile, etc.
3. **Depth** — Quick question, multi-step assessment, or deep research?
4. **Risk** — Could any proposed command cause harm?

## Decision Logic
- **needs_tools=true**: Security operation → construct shell commands
- **needs_tools=false**: General chat → respond directly

## Output Format — Always Return Valid JSON
{{ "needs_tools": true/false, "reasoning": "...", "response": "...", "steps": [] }}

## Tool Execution Steps (needs_tools=true)
Each step is a raw shell command. Use the `command` field.

## Shell Quoting Rules
Avoid patterns that break bash quoting. Prefer grep -E over grep -P.

## Output Analysis (post-execution)
Analyse findings like a pentest report. Identify exposures, correlate tools, assign severity.

## Communication Standards
Be technical and precise. Reference CVEs, ATT&CK techniques. Use Markdown."""
```

### NEUTRAL_SYSTEM_PROMPT

A minimal system prompt (~30 lines) for `persona = none`:

```python
NEUTRAL_SYSTEM_PROMPT = f"""You are Siyarix, a cybersecurity professional in a terminal-driven environment.

{_platform_context()}

## Approach
Analyse every request within cybersecurity. Determine needs_tools vs direct response.

## Output Format — Always Return Valid JSON
{{ "needs_tools": true/false, "reasoning": "...", "response": "...", "steps": [] }}

## Tool Execution Steps (needs_tools=true)
Each step is a raw shell command.

## Communication Standards
Be technical and precise. Explain reasoning. Use Markdown."""
```

### Compact Variants

Used for follow-up calls within the same interaction to reduce token usage:

| Variant | Purpose |
|---------|---------|
| `COMPACT_PROMPT` | Continue as active persona with full instructions previously provided |
| `COMPACT_NEUTRAL` | Continue as neutral Siyarix with minimal JSON output instruction |

```python
COMPACT_PROMPT = """Continue as Siyarix in your active persona. Follow the full system instructions previously provided.

When a security operation is described, output JSON: { "needs_tools": true, ... }
For general chat or after tool execution, output JSON: { "needs_tools": false, ... }"""

COMPACT_NEUTRAL = """Continue as Siyarix following the system instructions previously provided.
Output JSON: { "needs_tools", "reasoning", "response", "steps" } when tools are needed."""
```

---

## Platform Context

Injected dynamically at the top of every system prompt via `_platform_context()` in `prompts.py:139`:

```
## Platform Context
- OS: Windows 10 (AMD64)
- Shell: cmd /c
- WARNING: Windows system detected — commands must use Windows-compatible flags:
  * nmap: use -sT (TCP connect) instead of -sS (SYN scan); omit -O
  * Use forward slashes or escaped backslashes in paths
  * For DNS: use nslookup if dig is unavailable
  * Find binaries with `where` instead of `which`
```

On Unix-like systems, it provides appropriate guidance for the platform.

---

## Persona Preamble

When a persona is active, the preamble is prepended to the system prompt:

```
## Active Persona: Red Team / Offensive Security
[Persona-specific expertise paragraph with methodology, tools, and mindset]
```

For `auto` mode, the preamble lists all available personas and instructs the LLM to select the best fit:

```
## Active Persona: Auto (Smart Select)
Analyse the user's request below and automatically adopt the persona
that best fits the task. Available personas:
  - **Red Team / Offensive Security**: Adversary emulation, penetration testing...
  - **Blue Team / Defensive Security**: Detection engineering, SOC operations...
  ...
```

---

## Custom Instructions & Workspace Context

The `_build_system_prompt()` method injects additional context when available:

```python
# Custom instructions from settings
extra = self._settings.get("additional_system_message", "").strip()
if extra:
    prompt += "\n\n## Custom Instructions\n" + extra

# Workspace context files
for filename in ("AGENTS.md", "SOUL.md"):
    ctx_file = Path.cwd() / filename
    if ctx_file.exists():
        content = ctx_file.read_text(encoding="utf-8").strip()
        if content:
            label = filename.replace(".md", "")
            prompt += f"\n\n## {label}\n{content}"

# Execution environment
prompt += f"\n\n## Execution Environment\n- OS: {os_name}\n- Shell: {shell}\n- ..."
```

---

## Conversation History

Multi-turn context is managed by `ChatSession` and injected as part of the message array:

```python
session = ChatSession()
session.add_message("user", "scan 10.0.0.1")
session.add_message("assistant", json_response)
```

### Context Window Management

1. **Oldest-first truncation** when exceeding token limits
2. **Tool output summarization**: `nmap output: 5 ports found`
3. **Knowledge graph summarization**: `3 hosts, 12 ports, 2 vulns`
4. **Compaction**: `CompactionEngine` compresses long histories via LLM summarization when `CONTEXT_OVERFLOW` is detected

---

## Output Format

The LLM is instructed to return valid JSON:

```json
{
  "needs_tools": true,
  "reasoning": "Step-by-step analysis of the request",
  "response": "Direct answer when needs_tools=false, or analysis post-execution",
  "steps": [
    {
      "tool": "",
      "command": "nmap -sV -p 1-1000 10.0.0.1",
      "description": "Port scan target with service detection"
    }
  ]
}
```

### Field Reference

| Field | Type | When Present | Description |
|-------|------|-------------|-------------|
| `needs_tools` | `bool` | Always | Whether tool execution is required |
| `reasoning` | `string` | Always | Step-by-step analysis and methodology |
| `response` | `string` | Always | Direct answer or post-execution synthesis |
| `steps` | `array` | `needs_tools=true` | List of shell commands to execute |

Each step contains:

| Sub-field | Type | Description |
|-----------|------|-------------|
| `tool` | `string` | Tool name (can be empty for raw commands) |
| `command` | `string` | Exact shell command |
| `description` | `string` | Purpose and what to look for in output |

---

## Message Construction

The `build_messages()` function in `openai_compat.py` assembles the messages array for API calls:

```python
def build_messages(system_prompt, user_prompt, history, *, compat=None):
    messages = []
    if system_prompt:
        role = "developer" if compat and compat.supports_developer_role else "system"
        messages.append({"role": role, "content": system_prompt})
    if history:
        for msg in history:
            if msg.get("role") == "system":
                continue  # Skip system messages from history
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_prompt})
    return messages
```

Key behaviors:
- Uses `developer` role instead of `system` when the provider supports it (compat flag)
- Strips duplicate system messages from conversation history
- Appends user input as the final message

---

## System Prompt Refresh

To balance context efficiency with instruction persistence, the system prompt is refreshed periodically:

```python
def _should_use_compact(self) -> bool:
    return self._llm_calls > 0 and bool(self._llm_calls % self.SYSTEM_REFRESH_INTERVAL)
```

- **First call**: Full persona + system prompt
- **Subsequent calls**: Compact variants to save tokens
- **Every N calls** (configurable): Full system prompt is re-sent to prevent instruction drift

---

## Prompt Bar Rendering

`chat/prompts.py` also provides professional-grade prompt bar rendering for the terminal UI:

```python
from siyarix.chat.prompts import make_prompt_bar

# Renders:
# ▌ siyarix  [integrated]  openai  persona:redteam  msgs:42  up:01:23:45  sid:a1b2c3  ▐
# ╰─ ➜ (Tab: autocomplete, ?: help)
```

The prompt bar includes:

- **Mode indicator** with colour coding (integrated=cyan, autonomous=magenta, offline=yellow, stealth=red)
- **Provider name** in blue
- **Active persona** in green (when set)
- **Message count** and **uptime**
- **Session ID** (truncated)
- **Mode-specific hint** text

---

## Related Modules

| Module | Path | Purpose |
|--------|------|---------|
| `SIYARIX_SYSTEM_PROMPT` | `src/siyarix/chat/prompts.py:171` | Full system prompt |
| `NEUTRAL_SYSTEM_PROMPT` | `src/siyarix/chat/prompts.py:233` | Minimal neutral prompt |
| `COMPACT_PROMPT` | `src/siyarix/chat/prompts.py:263` | Compact variant for follow-up calls |
| `COMPACT_NEUTRAL` | `src/siyarix/chat/prompts.py:268` | Compact neutral variant |
| `_platform_context()` | `src/siyarix/chat/prompts.py:139` | Dynamic platform context injection |
| `_build_system_prompt()` | `src/siyarix/chat/engine.py:550` | Full system prompt builder with persona integration |
| `build_persona_prompt()` | `src/siyarix/personas.py:218` | Persona preamble generation |
| `build_messages()` | `src/siyarix/chat/openai_compat.py` | Messages array construction |
| `make_prompt_bar()` | `src/siyarix/chat/prompts.py:121` | Terminal prompt bar rendering |
| `mode_prompt_hint()` | `src/siyarix/chat/prompts.py:101` | Mode-specific one-line hints |
| `CompactionEngine` | `src/siyarix/compaction.py` | Long context compression |
