# SPDX-License-Identifier: AGPL-3.0-or-later

"""Slash command registry and profiles for Siyarix chat.

Provides a comprehensive CommandRegistry with categories, aliases,
argument metadata, and help system — powers autocomplete, help, and dispatch.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, asdict, field
from datetime import datetime, UTC
from enum import Enum
from pathlib import Path

from siyarix.config import get_config_dir

logger = logging.getLogger(__name__)


# ── Command Categories ────────────────────────────────────────────────────

class CommandCategory(str, Enum):
    NAVIGATION = "Navigation"
    SESSION = "Session"
    CONFIGURATION = "Configuration"
    TOOLS = "Tools"
    ANALYSIS = "Analysis"
    REPORT = "Report"
    SYSTEM = "System"
    MODE = "Mode"
    EXPORT = "Export"
    LEARNING = "Learning"
    TEAM = "Team"
    ADVANCED = "Advanced"
    HELP = "Help"

    def __str__(self) -> str:
        return self.value


# ── Command Info Dataclass ────────────────────────────────────────────────

@dataclass
class ArgInfo:
    name: str
    description: str = ""
    optional: bool = False
    choices: list[str] | None = None  # fixed set of valid values


@dataclass
class CommandInfo:
    """Metadata for a single slash command."""

    name: str                          # primary name e.g. "/help"
    category: CommandCategory
    description: str                   # one-line help text
    usage: str = ""                    # e.g. "/history [n] [filter]"
    aliases: list[str] = field(default_factory=list)
    args: list[ArgInfo] = field(default_factory=list)
    hidden: bool = False
    handler: str = ""                  # method name on CommandHandlersMixin
    mode_filter: list[str] | None = None  # e.g. ["autonomous", "integrated"] means available only in these modes

    @property
    def all_names(self) -> list[str]:
        return [self.name] + self.aliases


# ── Command Registry ──────────────────────────────────────────────────────

class CommandRegistry:
    """Central registry of all slash commands with lookup and filtering."""

    _commands: dict[str, CommandInfo] = {}
    _by_category: dict[CommandCategory, list[CommandInfo]] = {}
    _initialized = False

    @classmethod
    def initialize(cls) -> None:
        if cls._initialized:
            return
        cls._initialized = True
        cls._commands.clear()
        cls._by_category.clear()
        for cat in CommandCategory:
            cls._by_category[cat] = []

        for info in _BUILTIN_COMMANDS:
            for name in info.all_names:
                cls._commands[name] = info
            cls._by_category.setdefault(info.category, []).append(info)

    @classmethod
    def get(cls, name: str) -> CommandInfo | None:
        cls.initialize()
        return cls._commands.get(name)

    @classmethod
    def all_commands(cls) -> list[CommandInfo]:
        cls.initialize()
        seen = set()
        result = []
        for info in _BUILTIN_COMMANDS:
            if info.name not in seen:
                seen.add(info.name)
                result.append(info)
        return result

    @classmethod
    def visible_commands(cls) -> list[CommandInfo]:
        return [c for c in cls.all_commands() if not c.hidden]

    @classmethod
    def visible_commands_for_mode(cls, mode: str) -> list[CommandInfo]:
        """Return commands visible for the given mode, with mode-relevant
        commands promoted to the top.

        Commands with a mode_filter that includes the current mode are
        boosted to the top of the list; all other visible commands follow.
        Commands with mode_filter that do NOT include the current mode
        are moved to the bottom (but not hidden — the user can still
        switch modes)."""
        seen = set()
        promoted = []
        normal = []
        demoted = []
        for c in cls.visible_commands():
            if c.name in seen:
                continue
            seen.add(c.name)
            if c.mode_filter is None:
                normal.append(c)
            elif mode in c.mode_filter:
                promoted.append(c)
            else:
                demoted.append(c)
        return promoted + normal + demoted

    @classmethod
    def categorized_for_mode(cls, mode: str) -> dict[CommandCategory, list[CommandInfo]]:
        """Return commands grouped by category, filtered/ordered by mode."""
        grouped: dict[CommandCategory, list[CommandInfo]] = {}
        for cmd in cls.visible_commands_for_mode(mode):
            grouped.setdefault(cmd.category, []).append(cmd)
        return grouped

    @classmethod
    def by_category(cls, cat: CommandCategory) -> list[CommandInfo]:
        cls.initialize()
        return cls._by_category.get(cat, [])

    @classmethod
    def search(cls, query: str) -> list[CommandInfo]:
        """Fuzzy search commands by name, alias, or description."""
        q = query.lower()
        results = []
        for info in cls.all_commands():
            if q in info.name.lower():
                results.append(info)
                continue
            if any(q in a.lower() for a in info.aliases):
                results.append(info)
                continue
            if q in info.description.lower():
                results.append(info)
                continue
            for arg in info.args:
                if q in arg.name.lower():
                    results.append(info)
                    break
        return results

    @classmethod
    def suggestions_for(cls, command_name: str) -> list[CommandInfo]:
        """Find commands similar to the given partial name."""
        cls.initialize()
        q = command_name.lstrip("/").lower()
        matches = []
        for info in cls.visible_commands():
            if q in info.name.lstrip("/").lower():
                matches.append(info)
        matches.sort(key=lambda c: (
            0 if c.name.lstrip("/").lower().startswith(q) else 1,
            c.name,
        ))
        return matches[:8]

    @classmethod
    def top_commands(cls, limit: int = 10) -> list[CommandInfo]:
        """Return the most commonly useful commands for the welcome screen."""
        return [c for c in cls.visible_commands() if not c.hidden][:limit]


# ── Built-in command definitions ──────────────────────────────────────────

_BUILTIN_COMMANDS: list[CommandInfo] = [
    # ── Help ──
    CommandInfo(
        name="/help",
        category=CommandCategory.HELP,
        description="Show contextual help system with categories",
        usage="/help [category|command]",
        aliases=["/?", "/h"],
        args=[
            ArgInfo("category", "Filter help by category name", optional=True),
        ],
        handler="_cmd_help",
    ),
    # ── Navigation ──
    CommandInfo(
        name="/exit",
        category=CommandCategory.NAVIGATION,
        description="Exit chat mode",
        aliases=["/quit", "/bye"],
        handler="_cmd_exit",
    ),
    CommandInfo(
        name="/clear",
        category=CommandCategory.NAVIGATION,
        description="Clear screen and conversation",
        usage="/clear",
        aliases=["/clean", "/cls"],
        handler="_cmd_clear",
    ),
    CommandInfo(
        name="/new",
        category=CommandCategory.NAVIGATION,
        description="Start a fresh conversation",
        aliases=["/fresh"],
        handler="_cmd_new",
    ),
    CommandInfo(
        name="/cancel",
        category=CommandCategory.NAVIGATION,
        description="Cancel current task without exiting",
        aliases=["/esc"],
        handler="_cmd_esc",
    ),
    CommandInfo(
        name="/history",
        category=CommandCategory.NAVIGATION,
        description="Browse conversation history with optional search",
        usage="/history [n] [filter]",
        args=[
            ArgInfo("n", "Number of messages to show (max 200)", optional=True),
            ArgInfo("filter", "Keyword to search for", optional=True),
        ],
        handler="_cmd_history",
    ),
    CommandInfo(
        name="/search",
        category=CommandCategory.NAVIGATION,
        description="Search chat history for a keyword",
        usage="/search <text>",
        args=[ArgInfo("text", "Keyword to search for")],
        handler="_cmd_search",
    ),
    # ── Session ──
    CommandInfo(
        name="/session",
        category=CommandCategory.SESSION,
        description="Show detailed session metadata",
        aliases=["/info"],
        handler="_cmd_session",
    ),
    CommandInfo(
        name="/save",
        category=CommandCategory.SESSION,
        description="Save current session to disk",
        usage="/save [session_id]",
        args=[ArgInfo("session_id", "Optional custom session ID", optional=True)],
        handler="_cmd_save",
    ),
    CommandInfo(
        name="/load",
        category=CommandCategory.SESSION,
        description="Load a saved session by ID",
        usage="/load <session_id>",
        args=[ArgInfo("session_id", "Session ID to load")],
        handler="_cmd_load",
    ),
    CommandInfo(
        name="/fork",
        category=CommandCategory.SESSION,
        description="Fork current session into a new branch",
        usage="/fork [message_index] [summary]",
        args=[
            ArgInfo("message_index", "Message index to fork at", optional=True),
            ArgInfo("summary", "Summary of the fork", optional=True),
        ],
        handler="_cmd_fork",
    ),
    CommandInfo(
        name="/diff",
        category=CommandCategory.SESSION,
        description="Diff between two sessions",
        usage="/diff <session_a> <session_b>",
        args=[
            ArgInfo("session_a", "First session ID"),
            ArgInfo("session_b", "Second session ID"),
        ],
        handler="_cmd_diff",
    ),
    CommandInfo(
        name="/log",
        category=CommandCategory.SESSION,
        description="Manage session logs",
        usage="/log list|show|export <session_id>",
        args=[
            ArgInfo("action", "list, show, or export"),
            ArgInfo("session_id", "Session ID (for show/export)", optional=True),
        ],
        handler="_cmd_log",
    ),
    CommandInfo(
        name="/reset",
        category=CommandCategory.SESSION,
        description="Reset mode and target to defaults",
        handler="_cmd_reset",
    ),
    CommandInfo(
        name="/stats",
        category=CommandCategory.SESSION,
        description="Show usage statistics for current session",
        usage="/stats [detail]",
        args=[ArgInfo("detail", "Show detailed breakdown", optional=True)],
        handler="_cmd_stats",
    ),
    # ── Configuration ──
    CommandInfo(
        name="/config",
        category=CommandCategory.CONFIGURATION,
        description="View/edit configuration settings",
        usage="/config [show|set|get|list|tools]",
        args=[
            ArgInfo("action", "show, set <key> <value>, get <key>, list, tools"),
        ],
        handler="_cmd_config",
    ),
    CommandInfo(
        name="/key",
        category=CommandCategory.CONFIGURATION,
        description="Manage API keys for AI providers",
        usage="/key [set|remove|list|rotate] <provider> <key>",
        args=[
            ArgInfo("action", "set, remove, list, or rotate"),
            ArgInfo("provider", "Provider name (e.g. gemini, openai)", optional=True),
            ArgInfo("key", "API key value", optional=True),
        ],
        handler="_cmd_key",
    ),
    CommandInfo(
        name="/theme",
        category=CommandCategory.CONFIGURATION,
        description="Switch color themes",
        usage="/theme [list|preview|set] <theme> [syntax_theme]",
        args=[
            ArgInfo("action", "list, preview, set, or theme name", optional=True),
            ArgInfo("theme", "Theme name", optional=True),
        ],
        handler="_cmd_theme",
    ),
    CommandInfo(
        name="/alias",
        category=CommandCategory.CONFIGURATION,
        description="Create and manage command aliases",
        usage="/alias [list|set|remove] <name> <command>",
        args=[
            ArgInfo("action", "list, set, or remove"),
            ArgInfo("name", "Alias name", optional=True),
            ArgInfo("command", "Command to alias", optional=True),
        ],
        handler="_cmd_alias",
    ),
    CommandInfo(
        name="/language",
        category=CommandCategory.CONFIGURATION,
        description="Switch output language",
        usage="/language [list|<lang>]",
        args=[
            ArgInfo("lang", "Language code (en, fr, de, es, etc.)", optional=True),
        ],
        handler="_cmd_language",
    ),
    CommandInfo(
        name="/savecmd",
        category=CommandCategory.CONFIGURATION,
        description="Save a command profile for reuse",
        usage="/savecmd <name> <command>",
        args=[
            ArgInfo("name", "Profile name"),
            ArgInfo("command", "Command to save"),
        ],
        handler="_cmd_savecmd",
    ),
    CommandInfo(
        name="/cmds",
        category=CommandCategory.CONFIGURATION,
        description="List saved command profiles",
        handler="_cmd_cmds",
    ),
    CommandInfo(
        name="/cmd",
        category=CommandCategory.CONFIGURATION,
        description="Run a saved command profile",
        usage="/cmd <profile_name>",
        args=[ArgInfo("profile_name", "Name of saved profile")],
        handler="_cmd_cmd",
    ),
    # ── Mode ──
    CommandInfo(
        name="/mode",
        category=CommandCategory.MODE,
        description="Switch execution mode",
        usage="/mode <mode>",
        args=[
            ArgInfo("mode", "Mode name", choices=[
                "autonomous", "integrated", "offline", "stealth",
                "verbose", "quiet", "expert", "beginner",
                "interactive", "batch", "redteam", "blueteam",
                "compliance", "audit",
            ]),
        ],
        aliases=["/m"],
        handler="_cmd_mode",
    ),
    CommandInfo(
        name="/model",
        category=CommandCategory.CONFIGURATION,
        description="Switch AI model/provider on the fly",
        usage="/model <provider> [model_name]",
        args=[
            ArgInfo("provider", "Provider name (gemini, openai, anthropic, etc.)"),
            ArgInfo("model_name", "Specific model name (optional)", optional=True),
        ],
        handler="_cmd_model",
    ),
    CommandInfo(
        name="/provider",
        category=CommandCategory.CONFIGURATION,
        description="Show detailed provider info and models",
        usage="/provider [name]",
        aliases=["/providers"],
        args=[ArgInfo("name", "Provider name to inspect", optional=True)],
        handler="_cmd_provider",
    ),
    CommandInfo(
        name="/persona",
        category=CommandCategory.CONFIGURATION,
        description="Switch mindset/persona",
        usage="/persona [list|<name>]",
        args=[ArgInfo("name", "Persona name", optional=True)],
        handler="_cmd_persona",
    ),
    CommandInfo(
        name="/redteam",
        category=CommandCategory.TEAM,
        description="Switch to red team mode (offensive focus)",
        aliases=["/offensive"],
        handler="_cmd_redteam",
        mode_filter=["blueteam", "integrated", "autonomous", "stealth",
                      "verbose", "quiet", "expert", "beginner",
                      "interactive", "batch", "compliance", "audit"],
    ),
    CommandInfo(
        name="/blueteam",
        category=CommandCategory.TEAM,
        description="Switch to blue team mode (defensive focus)",
        aliases=["/defensive"],
        handler="_cmd_blueteam",
        mode_filter=["redteam", "integrated", "autonomous", "stealth",
                      "verbose", "quiet", "expert", "beginner",
                      "interactive", "batch", "compliance", "audit"],
    ),
    # ── Tools ──
    CommandInfo(
        name="/tools",
        category=CommandCategory.TOOLS,
        description="List discovered security tools with search/filter",
        usage="/tools [category]",
        args=[ArgInfo("category", "Tool category filter", optional=True)],
        handler="_cmd_tools",
    ),
    CommandInfo(
        name="/run",
        category=CommandCategory.TOOLS,
        description="Run a tool or shell command",
        usage="/run <command>",
        args=[ArgInfo("command", "Command or tool to run")],
        handler="_cmd_run",
    ),
    CommandInfo(
        name="/scan",
        category=CommandCategory.TOOLS,
        description="Quick scan configuration on target",
        usage="/scan <target>",
        args=[ArgInfo("target", "Target IP/hostname/URL")],
        handler="_cmd_scan",
    ),
    CommandInfo(
        name="/target",
        category=CommandCategory.CONFIGURATION,
        description="Set or show the current target",
        usage="/target [host]",
        args=[ArgInfo("host", "Target host/IP/URL", optional=True)],
        handler="_cmd_target",
    ),
    CommandInfo(
        name="/intents",
        category=CommandCategory.TOOLS,
        description="List cross-platform command intents",
        usage="/intents [filter]",
        args=[ArgInfo("filter", "Keyword to filter intents", optional=True)],
        handler="_cmd_intents",
    ),
    CommandInfo(
        name="/translate",
        category=CommandCategory.TOOLS,
        description="Translate a command intent to all shells",
        usage="/translate <intent>",
        args=[ArgInfo("intent", "Command intent to translate")],
        handler="_cmd_translate",
    ),
    CommandInfo(
        name="/security-cmds",
        category=CommandCategory.TOOLS,
        description="Show security commands for current platform",
        handler="_cmd_security_cmds",
    ),
    CommandInfo(
        name="/plugins",
        category=CommandCategory.TOOLS,
        description="List and manage Siyarix plugins",
        usage="/plugins [list|status]",
        args=[ArgInfo("action", "list or status", optional=True)],
        handler="_cmd_plugins",
    ),
    CommandInfo(
        name="/playbook",
        category=CommandCategory.TOOLS,
        description="Load and run playbooks",
        usage="/playbook [list|run|show] <path>",
        args=[
            ArgInfo("action", "list, run, or show"),
            ArgInfo("path", "Playbook file path", optional=True),
        ],
        handler="_cmd_playbook",
    ),
    # ── Analysis ──
    CommandInfo(
        name="/context",
        category=CommandCategory.ANALYSIS,
        description="Show current session context",
        handler="_cmd_context",
    ),
    CommandInfo(
        name="/examples",
        category=CommandCategory.ANALYSIS,
        description="Show practical prompt examples",
        handler="_cmd_examples",
    ),
    CommandInfo(
        name="/review",
        category=CommandCategory.ANALYSIS,
        description="Toggle command review prompt before execution",
        usage="/review [on|off]",
        args=[ArgInfo("state", "on or off", optional=True)],
        handler="_cmd_review",
    ),
    CommandInfo(
        name="/intel",
        category=CommandCategory.ANALYSIS,
        description="Threat intelligence lookup",
        usage="/intel lookup|status [indicator]",
        args=[
            ArgInfo("action", "lookup or status"),
            ArgInfo("indicator", "CVE, IP, domain to look up", optional=True),
        ],
        handler="_cmd_intel",
    ),
    CommandInfo(
        name="/kb",
        category=CommandCategory.ANALYSIS,
        description="Knowledge base operations",
        usage="/kb search|list <query>",
        args=[
            ArgInfo("action", "search or list"),
            ArgInfo("query", "Search query", optional=True),
        ],
        handler="_cmd_kb",
    ),
    # ── Report ──
    CommandInfo(
        name="/report",
        category=CommandCategory.REPORT,
        description="Generate executive report from current session",
        usage="/report [format]",
        args=[
            ArgInfo("format", "Output format (markdown, html, json)", optional=True),
        ],
        handler="_cmd_report",
    ),
    CommandInfo(
        name="/export",
        category=CommandCategory.EXPORT,
        description="Export conversation in various formats",
        usage="/export <format> [path]",
        args=[
            ArgInfo("format", "Export format", choices=["json", "md", "markdown", "html", "pdf", "txt"]),
            ArgInfo("path", "Output file path", optional=True),
        ],
        handler="_cmd_export",
    ),
    # ── System ──
    CommandInfo(
        name="/status",
        category=CommandCategory.SYSTEM,
        description="Show session and runtime status dashboard",
        handler="_cmd_status",
    ),
    CommandInfo(
        name="/env",
        category=CommandCategory.SYSTEM,
        description="Show terminal environment summary",
        handler="_cmd_env",
    ),
    CommandInfo(
        name="/platform",
        category=CommandCategory.SYSTEM,
        description="Show platform and shell information",
        handler="_cmd_platform",
    ),
    CommandInfo(
        name="/version",
        category=CommandCategory.SYSTEM,
        description="Show Siyarix version",
        handler="_cmd_version",
    ),
    CommandInfo(
        name="/uptime",
        category=CommandCategory.SYSTEM,
        description="Show chat session uptime",
        handler="_cmd_uptime",
    ),
    CommandInfo(
        name="/shells",
        category=CommandCategory.SYSTEM,
        description="List supported shells",
        handler="_cmd_shells",
    ),
    CommandInfo(
        name="/upgrade",
        category=CommandCategory.SYSTEM,
        description="Check for Siyarix updates",
        handler="_cmd_upgrade",
    ),
    CommandInfo(
        name="/docs",
        category=CommandCategory.SYSTEM,
        description="Open Siyarix documentation",
        usage="/docs [section]",
        args=[ArgInfo("section", "Documentation section", optional=True)],
        handler="_cmd_docs",
    ),
    CommandInfo(
        name="/bug",
        category=CommandCategory.SYSTEM,
        description="Report a bug (opens GitHub issues)",
        handler="_cmd_bug",
    ),
    CommandInfo(
        name="/suggest",
        category=CommandCategory.SYSTEM,
        description="Suggest a feature (opens GitHub discussions)",
        handler="_cmd_suggest",
    ),
    CommandInfo(
        name="/tutorial",
        category=CommandCategory.SYSTEM,
        description="Launch interactive tutorial",
        usage="/tutorial [topic]",
        args=[ArgInfo("topic", "Tutorial topic", optional=True)],
        handler="_cmd_tutorial",
    ),
    CommandInfo(
        name="/benchmark",
        category=CommandCategory.SYSTEM,
        description="Run performance benchmark",
        usage="/benchmark [provider] [model]",
        args=[
            ArgInfo("provider", "Provider to benchmark", optional=True),
            ArgInfo("model", "Model to benchmark", optional=True),
        ],
        handler="_cmd_benchmark",
    ),
    # ── Learning ──
    CommandInfo(
        name="/learn",
        category=CommandCategory.LEARNING,
        description="Toggle Continuous Learning System",
        usage="/learn [on|off|status]",
        args=[ArgInfo("state", "on, off, or status", optional=True)],
        handler="_cmd_learn",
    ),
    CommandInfo(
        name="/skills",
        category=CommandCategory.LEARNING,
        description="Manage learned skills",
        usage="/skills [stats|list|add|export]",
        handler="_cmd_skills",
    ),
    CommandInfo(
        name="/feedback",
        category=CommandCategory.LEARNING,
        description="Provide feedback on the last response",
        usage="/feedback <rating> [comment]",
        args=[
            ArgInfo("rating", "Rating: 1-5 or good/bad"),
            ArgInfo("comment", "Optional comment", optional=True),
        ],
        handler="_cmd_feedback",
    ),
    # ── Advanced Operations ──
    CommandInfo(
        name="/split",
        category=CommandCategory.ADVANCED,
        description="Toggle split pane view",
        usage="/split [timeline|metrics|cheatsheet|attack_map]",
        handler="_cmd_split",
    ),
    CommandInfo(
        name="/batch",
        category=CommandCategory.ADVANCED,
        description="Execute batch command file",
        usage="/batch run <file>",
        args=[ArgInfo("file", "Batch script file path")],
        handler="_cmd_batch",
    ),
    CommandInfo(
        name="/opsec",
        category=CommandCategory.ADVANCED,
        description="Operational security controls",
        usage="/opsec isolate|burn|status|disable",
        handler="_cmd_opsec",
    ),
    CommandInfo(
        name="/stealth",
        category=CommandCategory.ADVANCED,
        description="Evasion configuration",
        usage="/stealth status|on|off|level <level>",
        handler="_cmd_stealth",
    ),
    CommandInfo(
        name="/audit",
        category=CommandCategory.ADVANCED,
        description="Compliance and legal export",
        usage="/audit export|status|verify",
        handler="_cmd_audit",
    ),
    CommandInfo(
        name="/queue",
        category=CommandCategory.ADVANCED,
        description="Offline command queue management",
        usage="/queue status|list|retry|clear|flush",
        handler="_cmd_queue",
    ),
    CommandInfo(
        name="/cache",
        category=CommandCategory.ADVANCED,
        description="Cache management",
        usage="/cache status|clear|invalidate [domain]",
        handler="_cmd_cache",
    ),
    CommandInfo(
        name="/performance",
        category=CommandCategory.ADVANCED,
        description="Resource optimization",
        usage="/performance status|tune|configure",
        handler="_cmd_performance",
    ),
    CommandInfo(
        name="/campaign",
        category=CommandCategory.ADVANCED,
        description="Multi-target campaign management",
        usage="/campaign list|create|status",
        handler="_cmd_campaign",
    ),
    CommandInfo(
        name="/ticket",
        category=CommandCategory.ADVANCED,
        description="External ticket creation",
        usage="/ticket create|list",
        handler="_cmd_ticket",
    ),
    CommandInfo(
        name="/retest",
        category=CommandCategory.ADVANCED,
        description="Verification scan scheduling",
        usage="/retest schedule|status",
        handler="_cmd_retest",
    ),
    CommandInfo(
        name="/agent",
        category=CommandCategory.ADVANCED,
        description="Sub-agent lifecycle management",
        usage="/agent run <goal>|status",
        handler="_cmd_agent",
    ),
    CommandInfo(
        name="/siem",
        category=CommandCategory.ADVANCED,
        description="SIEM/SOAR integration (legacy)",
        usage="/siem connect|status",
        handler="_cmd_siem",
    ),
]

# Initialize the registry
CommandRegistry.initialize()

# ── Backward compatibility: HELP_CATEGORIES and SLASH_HELP ────────────────

HELP_CATEGORIES: list[tuple[str, dict[str, str]]] = []
_cat_map: dict[CommandCategory, str] = {
    CommandCategory.NAVIGATION: "Navigation & Session",
    CommandCategory.SESSION: "Session Management",
    CommandCategory.CONFIGURATION: "Configuration",
    CommandCategory.MODE: "Mode Switching",
    CommandCategory.TOOLS: "Tools & Execution",
    CommandCategory.ANALYSIS: "Analysis & Intelligence",
    CommandCategory.REPORT: "Reporting",
    CommandCategory.EXPORT: "Export & Sharing",
    CommandCategory.SYSTEM: "System Information",
    CommandCategory.LEARNING: "Learning & Feedback",
    CommandCategory.TEAM: "Team Operations",
    CommandCategory.HELP: "Help & Support",
    CommandCategory.ADVANCED: "Advanced Operations",
}

for cat in CommandCategory:
    cmds_in_cat = CommandRegistry.by_category(cat)
    if cmds_in_cat:
        entries: dict[str, str] = {}
        for ci in cmds_in_cat:
            if not ci.hidden:
                key = ci.usage if ci.usage else ci.name
                desc = ci.description
                if ci.aliases:
                    desc += f" (aliases: {', '.join(ci.aliases)})"
                entries[key] = desc
        if entries:
            label = _cat_map.get(cat, cat.value)
            HELP_CATEGORIES.append((label, entries))

SLASH_HELP: dict[str, str] = {}
for _label, _entries in HELP_CATEGORIES:
    for k, v in _entries.items():
        primary = k.split()[0]
        SLASH_HELP[primary] = v


# ── Command Profile (unchanged) ───────────────────────────────────────────

@dataclass
class CommandProfile:
    name: str
    command: str
    description: str | None = None
    created_at: str = ""


class CommandProfileStore:
    """Persistent storage for reusable command profiles."""

    def __init__(self) -> None:
        self._profiles_dir = get_config_dir() / "command_profiles"
        self._profiles_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        safe = name.replace("/", "_").replace("\\", "_")
        return self._profiles_dir / f"{safe}.json"

    def save(self, profile: CommandProfile) -> None:
        if not profile.created_at:
            profile.created_at = datetime.now(tz=UTC).isoformat()
        self._path(profile.name).write_text(
            json.dumps(asdict(profile), indent=2), encoding="utf-8"
        )

    def get(self, name: str) -> CommandProfile | None:
        path = self._path(name)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return CommandProfile(**data)

    def list_profiles(self) -> list[CommandProfile]:
        profiles: list[CommandProfile] = []
        for p in sorted(self._profiles_dir.glob("*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                profiles.append(CommandProfile(**data))
            except Exception:
                continue
        return profiles

    list_credentials = list_profiles

    def delete(self, name: str) -> bool:
        path = self._path(name)
        if path.exists():
            path.unlink()
            return True
        return False

    def render(self, command: str, params: dict[str, str]) -> str:
        rendered = command
        for k, v in params.items():
            rendered = rendered.replace(f"{{{k}}}", v).replace(f"${{{k}}}", v)
        return rendered


# ── Command History (for autocomplete ranking) ────────────────────────────

class CommandHistory:
    """Tracks recently used commands for smarter autocomplete ranking."""

    def __init__(self, maxlen: int = 100) -> None:
        self._history: list[str] = []
        self._maxlen = maxlen

    def record(self, command: str) -> None:
        cmd = command.split()[0].lower()
        # Move to front
        if cmd in self._history:
            self._history.remove(cmd)
        self._history.insert(0, cmd)
        if len(self._history) > self._maxlen:
            self._history.pop()

    def recent(self, limit: int = 10) -> list[str]:
        return self._history[:limit]

    def frequency_score(self, command: str) -> float:
        """Score a command by recency. 1.0 = most recent, 0.0 = not used."""
        cmd = command.split()[0].lower()
        try:
            idx = self._history.index(cmd)
            return max(0.0, 1.0 - (idx / max(len(self._history), 1)))
        except ValueError:
            return 0.0


# Global instances
command_history = CommandHistory()

__all__ = [
    "CommandCategory",
    "CommandInfo",
    "ArgInfo",
    "CommandRegistry",
    "CommandProfile",
    "CommandProfileStore",
    "CommandHistory",
    "command_history",
    "HELP_CATEGORIES",
    "SLASH_HELP",
    "_BUILTIN_COMMANDS",
]
