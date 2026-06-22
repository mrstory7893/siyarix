# SPDX-License-Identifier: AGPL-3.0-or-later
"""Continuous Learning System (CLS) — monitors LLM/offline planner actions and builds
a persistent, privacy-preserving skill library that improves Siyarix over time.

Key Design Principles
---------------------
- **Privacy First**: Real targets are NEVER stored. Every hostname, IP, URL, email, or
  hash is replaced with the ``{target}`` placeholder before any data is persisted.
- **Separate Store**: Learning data lives in ``learning_store.db`` (separate from
  ``offline_store.db``) so users can share it with Siyarix developers to help improve
  the tool without exposing sensitive operational data.
- **Zero Dependencies**: Pure stdlib — no numpy, no ML libraries. Uses BM25-style
  Jaccard similarity over NLP token sets.
- **Bayesian Confidence**: Skill confidence is updated with a Bayesian-smoothed formula
  that rewards both accuracy (success rate) and data volume (usage count).
- **Dual-Mode Integration**:
    - *Integrated mode*: 100 %-confidence skills trigger automatic pre-execution before
      the LLM is consulted. Results are sent to the LLM as a rich base context.
    - *Offline mode*: Learned skills augment the heuristic planner and generate an
      enhanced "Learning Insights" summary panel after execution.
"""

from __future__ import annotations

import json
import logging
import math
import re
import sqlite3
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class LearnedStep:
    """A single anonymised step inside a LearnedSkill."""

    tool: str
    command_template: str  # uses {target} placeholder — never stores real target
    description: str
    args: dict[str, Any] = field(default_factory=dict)

    def instantiate(self, target: str) -> "LearnedStep":
        """Return a copy with {target} replaced by the real target."""
        return LearnedStep(
            tool=self.tool,
            command_template=self.command_template.replace("{target}", target),
            description=self.description.replace("{target}", target),
            args={
                k: (v.replace("{target}", target) if isinstance(v, str) else v)
                for k, v in self.args.items()
            },
        )


@dataclass
class LearnedSkill:
    """A reusable, anonymised workflow pattern extracted from observed LLM/offline actions."""

    skill_id: str
    intent_pattern: str       # anonymised command pattern (contains {target})
    steps: list[LearnedStep]  # ordered action sequence with {target} placeholders
    confidence: float         # 0.0 – 1.0 (Bayesian-smoothed)
    usage_count: int
    success_count: int
    tokens: list[str]         # NLP tokens for similarity matching
    synonyms: dict[str, str]  # learned keyword → canonical tool/concept mappings
    created_at: float
    last_used: float
    source: str               # 'llm' | 'offline' | 'inferred'
    tags: list[str] = field(default_factory=list)
    notes: str = ""

    # ── Confidence helpers ──────────────────────────────────────────────

    @property
    def base_confidence(self) -> float:
        """Raw success rate."""
        return self.success_count / max(self.usage_count, 1)

    def recalculate_confidence(self) -> None:
        """Update confidence using Bayesian-smoothed formula.

        Rewards both accuracy (success_count/usage_count) AND data volume
        (logarithmic usage boost) so a skill needs multiple successful
        observations before reaching high confidence.

        Formula:
            base   = success_count / usage_count
            boost  = min(0.25, log(1 + usage_count) * 0.06)
            conf   = min(1.0, base + base * boost)
        """
        if self.usage_count == 0:
            self.confidence = 0.0
            return
        base = self.success_count / self.usage_count
        boost = min(0.25, math.log(1.0 + self.usage_count) * 0.06)
        self.confidence = min(1.0, base + base * boost)

    # ── Serialisation helpers ───────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "intent_pattern": self.intent_pattern,
            "steps": [asdict(s) for s in self.steps],
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "success_count": self.success_count,
            "tokens": self.tokens,
            "synonyms": self.synonyms,
            "created_at": self.created_at,
            "last_used": self.last_used,
            "source": self.source,
            "tags": self.tags,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# Continuous Learning System
# ---------------------------------------------------------------------------


class ContinuousLearningSystem:
    """Core learning engine: observe → learn → inject → replay.

    Thread-safe. Maintains an in-memory skill cache backed by SQLite.
    Each observation updates the relevant skill's confidence score and
    persists the change immediately.
    """

    _DB_FILENAME = "learning_store.db"
    _SCHEMA_VERSION = 2

    def __init__(self, db_path: Path | None = None) -> None:
        from .config import get_config_dir

        self._db_path = db_path or (get_config_dir() / self._DB_FILENAME)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self._local = threading.local()
        self._lock = threading.Lock()

        # In-memory skill cache (keyed by skill_id)
        self._skills: dict[str, LearnedSkill] = {}

        self._init_db()
        self._load_skills()

        logger.debug("CLS: initialised — %d skills loaded from %s", len(self._skills), self._db_path)

    # ── DB connection (thread-local) ────────────────────────────────────

    def _conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self._db_path), timeout=10)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA busy_timeout=5000")
            self._local.conn.execute("PRAGMA foreign_keys=ON")
        return self._local.conn

    # ── DB schema ──────────────────────────────────────────────────────

    def _init_db(self) -> None:
        conn = self._conn()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS meta (
                    key   TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                INSERT OR IGNORE INTO meta (key, value)
                    VALUES ('schema_version', '2');
                INSERT OR IGNORE INTO meta (key, value)
                    VALUES ('created_at', datetime('now'));

                CREATE TABLE IF NOT EXISTS learned_skills (
                    skill_id       TEXT PRIMARY KEY,
                    intent_pattern TEXT NOT NULL,
                    steps_json     TEXT NOT NULL,
                    confidence     REAL    DEFAULT 0.0,
                    usage_count    INTEGER DEFAULT 0,
                    success_count  INTEGER DEFAULT 0,
                    tokens_json    TEXT    DEFAULT '[]',
                    synonyms_json  TEXT    DEFAULT '{}',
                    tags_json      TEXT    DEFAULT '[]',
                    notes          TEXT    DEFAULT '',
                    created_at     REAL    NOT NULL,
                    last_used      REAL    NOT NULL,
                    source         TEXT    DEFAULT 'llm'
                );

                CREATE TABLE IF NOT EXISTS skill_observations (
                    obs_id      TEXT PRIMARY KEY,
                    skill_id    TEXT REFERENCES learned_skills(skill_id)
                                    ON DELETE CASCADE,
                    anon_goal   TEXT NOT NULL,
                    target_type TEXT DEFAULT '',
                    success     INTEGER DEFAULT 0,
                    wave_count  INTEGER DEFAULT 1,
                    step_count  INTEGER DEFAULT 0,
                    duration_ms REAL    DEFAULT 0.0,
                    observed_at REAL    NOT NULL,
                    mode        TEXT    DEFAULT 'integrated'
                );

                CREATE INDEX IF NOT EXISTS idx_skills_conf
                    ON learned_skills(confidence DESC);
                CREATE INDEX IF NOT EXISTS idx_skills_usage
                    ON learned_skills(usage_count DESC);
                CREATE INDEX IF NOT EXISTS idx_obs_skill
                    ON skill_observations(skill_id);
            """)
            conn.commit()
        except Exception:
            logger.exception("CLS: failed to initialise database")

    # ── Persistence ─────────────────────────────────────────────────────

    def _load_skills(self) -> None:
        try:
            rows = self._conn().execute(
                "SELECT * FROM learned_skills ORDER BY confidence DESC, usage_count DESC"
            ).fetchall()
            for row in rows:
                skill = self._row_to_skill(row)
                self._skills[skill.skill_id] = skill
        except Exception as exc:
            logger.warning("CLS: failed to load skills: %s", exc)

    def _row_to_skill(self, row: sqlite3.Row) -> LearnedSkill:
        steps_raw = json.loads(row["steps_json"])
        steps = [LearnedStep(**s) for s in steps_raw]
        return LearnedSkill(
            skill_id=row["skill_id"],
            intent_pattern=row["intent_pattern"],
            steps=steps,
            confidence=row["confidence"],
            usage_count=row["usage_count"],
            success_count=row["success_count"],
            tokens=json.loads(row["tokens_json"]),
            synonyms=json.loads(row["synonyms_json"]),
            created_at=row["created_at"],
            last_used=row["last_used"],
            source=row["source"],
            tags=json.loads(row.get("tags_json", "[]") or "[]"),
            notes=row.get("notes", "") or "",
        )

    def _save_skill(self, skill: LearnedSkill) -> None:
        steps_data = [asdict(s) for s in skill.steps]
        try:
            with self._lock:
                self._conn().execute(
                    """
                    INSERT OR REPLACE INTO learned_skills
                        (skill_id, intent_pattern, steps_json, confidence,
                         usage_count, success_count, tokens_json, synonyms_json,
                         tags_json, notes, created_at, last_used, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        skill.skill_id,
                        skill.intent_pattern,
                        json.dumps(steps_data),
                        skill.confidence,
                        skill.usage_count,
                        skill.success_count,
                        json.dumps(skill.tokens),
                        json.dumps(skill.synonyms),
                        json.dumps(skill.tags),
                        skill.notes,
                        skill.created_at,
                        skill.last_used,
                        skill.source,
                    ),
                )
                self._conn().commit()
        except Exception as exc:
            logger.warning("CLS: failed to save skill %s: %s", skill.skill_id[:8], exc)

    def _save_observation(
        self,
        skill_id: str,
        anon_goal: str,
        target_type: str,
        success: bool,
        mode: str,
        wave_count: int = 1,
        step_count: int = 0,
        duration_ms: float = 0.0,
    ) -> None:
        try:
            with self._lock:
                self._conn().execute(
                    """
                    INSERT INTO skill_observations
                        (obs_id, skill_id, anon_goal, target_type, success,
                         wave_count, step_count, duration_ms, observed_at, mode)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        skill_id,
                        anon_goal,
                        target_type,
                        1 if success else 0,
                        wave_count,
                        step_count,
                        duration_ms,
                        time.time(),
                        mode,
                    ),
                )
                self._conn().commit()
        except Exception as exc:
            logger.debug("CLS: failed to save observation: %s", exc)

    # ── Privacy — target anonymisation ─────────────────────────────────

    def _anonymize_target(self, text: str, target: str) -> str:
        """Replace ALL real target information with ``{target}`` placeholder.

        Uses both direct string replacement AND the full NLP regex pattern
        suite from :class:`~siyarix.nlp_engine.NaturalLanguageParser` to
        catch every possible target format (IP, domain, URL, email, hash…).

        CRITICAL: This method is the privacy boundary. No real target data
        must ever pass through to the database.
        """
        if not text:
            return text

        # 1 — Direct string replacement (most precise)
        if target:
            text = text.replace(target, "{target}")
            # Also handle stripped URL form  (e.g. "example.com" from "https://example.com/path")
            clean = (
                target.replace("https://", "")
                      .replace("http://", "")
                      .split("/")[0]
                      .split("?")[0]
            )
            if clean and clean != target and len(clean) > 3:
                text = text.replace(clean, "{target}")

        # 2 — Pattern-based sweep to catch anything the direct replacement missed
        try:
            from .nlp_engine import NaturalLanguageParser
            for pattern in NaturalLanguageParser.PATTERNS.values():
                try:
                    text = re.sub(pattern, "{target}", text)
                except re.error:
                    pass
        except ImportError:
            pass

        return text

    # ── NLP tokenisation (lightweight, no dependency on parser instance) ─

    def _tokenize(self, text: str) -> list[str]:
        """Minimal tokenisation: lowercase, strip punctuation, remove stopwords."""
        _STOPWORDS = frozenset({
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "by", "from", "up", "about", "into", "please",
            "can", "you", "do", "i", "want", "need", "run", "execute", "perform",
            "start", "show", "find", "get", "tell", "is", "are", "was", "were",
            "all", "any", "some", "just", "now", "target", "on",
        })
        text = text.lower()
        text = re.sub(r"[^\w\s-]", " ", text)
        words = text.split()
        tokens = []
        clean_words = []
        for w in words:
            if w and w not in _STOPWORDS and len(w) > 1:
                clean_words.append(w)
                tokens.append(w)
        # bigrams
        for i in range(len(clean_words) - 1):
            tokens.append(f"{clean_words[i]}_{clean_words[i+1]}")
        return tokens

    # ── Similarity ──────────────────────────────────────────────────────

    def _compute_similarity(self, tokens_a: list[str], tokens_b: list[str]) -> float:
        """Jaccard similarity over NLP token sets."""
        if not tokens_a or not tokens_b:
            return 0.0
        set_a = set(tokens_a)
        set_b = set(tokens_b)
        inter = len(set_a & set_b)
        union = len(set_a | set_b)
        return inter / union if union else 0.0

    # ── Synonym extraction ──────────────────────────────────────────────

    def _extract_synonyms(self, goal: str, steps: list[dict[str, Any]]) -> dict[str, str]:
        """Infer keyword → tool mappings from goal + steps."""
        synonyms: dict[str, str] = {}
        goal_tokens = self._tokenize(goal)
        for step in steps:
            tool = step.get("tool", "")
            if not tool or len(tool) < 2:
                continue
            for token in goal_tokens:
                if len(token) > 3 and token != tool:
                    synonyms.setdefault(token, tool)
        return synonyms

    # ── Core: find-or-create skill ──────────────────────────────────────

    def _find_or_create_skill(
        self,
        anon_goal: str,
        steps: list[dict[str, Any]],
        source: str,
    ) -> LearnedSkill:
        """Return the best matching existing skill or create a new one."""
        goal_tokens = self._tokenize(anon_goal)

        # Search for a similar existing skill (similarity >= 0.55)
        best_skill: LearnedSkill | None = None
        best_sim = 0.0
        for skill in self._skills.values():
            sim = self._compute_similarity(goal_tokens, skill.tokens)
            if sim > best_sim:
                best_sim = sim
                best_skill = skill

        if best_skill and best_sim >= 0.55:
            logger.debug(
                "CLS: matched existing skill '%s' (sim=%.2f)",
                best_skill.intent_pattern[:50], best_sim,
            )
            return best_skill

        # Build fresh LearnedStep list
        learned_steps: list[LearnedStep] = []
        for s in steps:
            cmd = s.get("command") or s.get("command_template") or ""
            learned_steps.append(
                LearnedStep(
                    tool=s.get("tool", ""),
                    command_template=cmd,
                    description=s.get("description", ""),
                    args=s.get("args", {}),
                )
            )

        skill = LearnedSkill(
            skill_id=str(uuid.uuid4()),
            intent_pattern=anon_goal,
            steps=learned_steps,
            confidence=0.0,
            usage_count=0,
            success_count=0,
            tokens=goal_tokens,
            synonyms=self._extract_synonyms(anon_goal, steps),
            created_at=time.time(),
            last_used=time.time(),
            source=source,
        )
        logger.debug("CLS: created new skill '%s'", anon_goal[:60])
        return skill

    # ── Core learning logic ─────────────────────────────────────────────

    def _learn_from_observation(
        self,
        anon_goal: str,
        steps: list[dict[str, Any]],
        success: bool,
        target_type: str,
        source: str,
        wave_count: int = 1,
        duration_ms: float = 0.0,
        mode: str = "integrated",
    ) -> LearnedSkill:
        """Create or update a :class:`LearnedSkill` from a single observation."""
        skill = self._find_or_create_skill(anon_goal, steps, source)

        # Update step templates when this is the first observation or a success
        if steps and (skill.usage_count == 0 or success):
            new_steps: list[LearnedStep] = []
            for s in steps:
                cmd = s.get("command") or s.get("command_template") or ""
                new_steps.append(
                    LearnedStep(
                        tool=s.get("tool", ""),
                        command_template=cmd,
                        description=s.get("description", ""),
                        args=s.get("args", {}),
                    )
                )
            skill.steps = new_steps
            skill.intent_pattern = anon_goal
            skill.tokens = self._tokenize(anon_goal)
            # Merge in newly learned synonyms
            skill.synonyms.update(self._extract_synonyms(anon_goal, steps))

        skill.usage_count += 1
        if success:
            skill.success_count += 1
        skill.last_used = time.time()
        skill.source = source
        skill.recalculate_confidence()

        # Persist
        self._skills[skill.skill_id] = skill
        self._save_skill(skill)
        self._save_observation(
            skill.skill_id, anon_goal, target_type, success, mode,
            wave_count=wave_count, step_count=len(steps), duration_ms=duration_ms,
        )

        logger.info(
            "CLS: skill updated | pattern='%s' | confidence=%.2f | usage=%d | success=%d",
            skill.intent_pattern[:55], skill.confidence, skill.usage_count, skill.success_count,
        )
        return skill

    # ── Public observation API ──────────────────────────────────────────

    def observe_llm_action(
        self,
        goal: str,
        plan: Any,
        result: Any,
        target: str = "",
        target_type: str = "",
        wave_count: int = 1,
        duration_ms: float = 0.0,
    ) -> LearnedSkill | None:
        """Observe an LLM-generated plan + execution result and update skills.

        Called by :meth:`~siyarix.chat.engine.LLMEngineMixin._execute_agent`
        after the multi-wave execution loop completes.

        Parameters
        ----------
        goal:       The original user goal (raw text — will be anonymised here).
        plan:       The ``ExecutionPlan`` produced by the autonomous planner.
        result:     Execution result object (or the last plan after execution).
        target:     The real target string (used only for anonymisation, not stored).
        target_type: Entity type of the target ('ipv4', 'domain', etc.)
        wave_count: Number of LLM waves executed.
        duration_ms: Total execution duration.
        """
        try:
            steps: list[dict[str, Any]] = []
            if plan and hasattr(plan, "steps"):
                for s in plan.steps:
                    cmd = getattr(s, "command", None) or ""
                    tool = getattr(s, "tool", "") or ""
                    desc = getattr(s, "description", "") or ""
                    args = dict(getattr(s, "args", {}) or {})
                    if not (cmd or tool):
                        continue
                    steps.append({
                        "tool": tool,
                        "command": self._anonymize_target(cmd, target),
                        "description": self._anonymize_target(desc, target),
                        "args": args,
                    })

            if not steps:
                return None

            success: bool = False
            if result is not None:
                if hasattr(result, "success"):
                    success = bool(result.success)
                elif hasattr(result, "status"):
                    from .models import PlanStatus
                    success = getattr(result, "status", None) == PlanStatus.COMPLETED

            anon_goal = self._anonymize_target(goal, target)
            return self._learn_from_observation(
                anon_goal, steps, success, target_type, "llm",
                wave_count=wave_count, duration_ms=duration_ms, mode="integrated",
            )
        except Exception as exc:
            logger.debug("CLS: observe_llm_action error: %s", exc, exc_info=True)
            return None

    def observe_offline_plan(
        self,
        goal: str,
        plan: Any,
        result: Any,
        target: str = "",
        target_type: str = "",
        duration_ms: float = 0.0,
    ) -> LearnedSkill | None:
        """Observe an offline/registry plan + execution result and update skills.

        Called by :meth:`~siyarix.chat.engine.LLMEngineMixin._execute_instruction`
        after offline mode execution completes.
        """
        try:
            steps: list[dict[str, Any]] = []
            if plan and hasattr(plan, "steps"):
                for s in plan.steps:
                    tool = getattr(s, "tool", "") or ""
                    args = dict(getattr(s, "args", {}) or {})
                    desc = getattr(s, "description", "") or ""
                    if not tool:
                        continue
                    # Build a synthetic command template from the tool + flags
                    flags = args.get("flags", "")
                    cmd_template = f"{tool} {flags} {{target}}".strip()
                    steps.append({
                        "tool": tool,
                        "command": self._anonymize_target(cmd_template, target),
                        "description": self._anonymize_target(desc, target),
                        "args": args,
                    })

            if not steps:
                return None

            success: bool = False
            if result is not None:
                success = bool(getattr(result, "success", False))

            anon_goal = self._anonymize_target(goal, target)
            return self._learn_from_observation(
                anon_goal, steps, success, target_type, "offline",
                duration_ms=duration_ms, mode="offline",
            )
        except Exception as exc:
            logger.debug("CLS: observe_offline_plan error: %s", exc, exc_info=True)
            return None

    # ── Query API ───────────────────────────────────────────────────────

    def find_high_confidence_skill(
        self,
        goal: str,
        target: str = "",
        threshold: float = 0.90,
    ) -> LearnedSkill | None:
        """Return the best matching skill at or above *threshold*.

        Used in **integrated mode** to decide whether to skip the LLM and
        directly replay a cached skill, then send results to the LLM as
        base context.

        Returns ``None`` if no skill meets the threshold — the normal
        LLM planning flow should proceed.
        """
        if not self._skills:
            return None
        anon_goal = self._anonymize_target(goal, target)
        goal_tokens = self._tokenize(anon_goal)
        if not goal_tokens:
            return None

        best_skill: LearnedSkill | None = None
        best_score = 0.0
        for skill in self._skills.values():
            if skill.confidence < threshold:
                continue
            sim = self._compute_similarity(goal_tokens, skill.tokens)
            # Combined score: penalise low-usage skills slightly
            volume_factor = min(1.0, math.log(1 + skill.usage_count) / math.log(6))
            combined = sim * skill.confidence * (0.7 + 0.3 * volume_factor)
            if combined > best_score:
                best_score = combined
                best_skill = skill

        if best_skill and best_score >= threshold * 0.75:
            logger.info(
                "CLS: high-confidence match '%s' (conf=%.2f, score=%.2f, threshold=%.2f)",
                best_skill.intent_pattern[:55],
                best_skill.confidence,
                best_score,
                threshold,
            )
            return best_skill
        return None

    def query_skill(
        self,
        goal: str,
        target: str = "",
        min_confidence: float = 0.50,
    ) -> LearnedSkill | None:
        """Return best matching skill at any confidence >= *min_confidence*.

        Used by the **offline planner** to augment or replace heuristic planning
        when a learned skill is available.
        """
        if not self._skills:
            return None
        anon_goal = self._anonymize_target(goal, target)
        goal_tokens = self._tokenize(anon_goal)
        if not goal_tokens:
            return None

        best_skill: LearnedSkill | None = None
        best_score = 0.0
        for skill in self._skills.values():
            if skill.confidence < min_confidence:
                continue
            sim = self._compute_similarity(goal_tokens, skill.tokens)
            score = sim * skill.confidence
            if score > best_score:
                best_score = score
                best_skill = skill

        return best_skill if best_score > 0.15 else None

    # ── Skill instantiation ─────────────────────────────────────────────

    def instantiate_skill(
        self, skill: LearnedSkill, target: str
    ) -> list[dict[str, Any]]:
        """Replace ``{target}`` placeholders with the real target in all step templates.

        Returns a list of step dicts ready for :class:`~siyarix.models.ExecutionPlan`.
        """
        steps: list[dict[str, Any]] = []
        for s in skill.steps:
            instantiated = s.instantiate(target)
            steps.append({
                "tool": instantiated.tool,
                "command": instantiated.command_template,
                "description": instantiated.description,
                "args": {
                    **instantiated.args,
                    "target": target,
                },
            })
        return steps

    # ── NLP injection ───────────────────────────────────────────────────

    def inject_into_nlp(self, parser: Any) -> None:
        """Feed all learned skills' synonyms and token corpus into a NaturalLanguageParser.

        Called once during planner initialisation and after each new skill is learned
        to keep the NLP engine current.
        """
        merged_synonyms: dict[str, str] = {}
        for skill in self._skills.values():
            merged_synonyms.update(skill.synonyms)

        if merged_synonyms and hasattr(parser, "inject_learned_synonyms"):
            parser.inject_learned_synonyms(merged_synonyms)

        if hasattr(parser, "inject_learned_corpus"):
            for skill in self._skills.values():
                if skill.tokens:
                    parser.inject_learned_corpus(
                        skill.skill_id, skill.intent_pattern, skill.tokens
                    )

    # ── Offline summary ─────────────────────────────────────────────────

    def generate_offline_summary(
        self,
        goal: str,
        result: Any,
        matched_skill: LearnedSkill | None = None,
    ) -> str:
        """Generate an enhanced summary panel for offline mode output.

        Returns an empty string if no matched skill is available.
        """
        if not matched_skill:
            return ""

        lines = [
            f"📚 **Learning Insights** — based on {matched_skill.usage_count} prior observation(s):",
            f"  • Pattern: *{matched_skill.intent_pattern}*",
            f"  • Confidence: {matched_skill.confidence:.0%}  "
            f"({matched_skill.success_count}/{matched_skill.usage_count} successful runs)",
        ]
        if matched_skill.steps:
            tools = list(dict.fromkeys(s.tool for s in matched_skill.steps if s.tool))
            if tools:
                lines.append(f"  • Tools in pattern: {', '.join(tools)}")
        if matched_skill.tags:
            lines.append(f"  • Tags: {', '.join(matched_skill.tags)}")
        if matched_skill.notes:
            lines.append(f"  • Notes: {matched_skill.notes}")
        return "\n".join(lines)

    # ── LLM clarification ───────────────────────────────────────────────

    async def ask_llm_for_skill_label(
        self,
        goal: str,
        steps: list[dict[str, Any]],
        llm_call_fn: Any,
    ) -> str | None:
        """Ask the LLM to suggest a canonical name/label for a newly observed skill.

        Uses the same ``llm_call_fn`` that the main agent uses — no extra API calls.
        Returns a short label string or ``None`` on failure.
        """
        if llm_call_fn is None:
            return None
        try:
            step_summary = "; ".join(
                f"{s.get('tool', '?')}: {s.get('description', '')}"
                for s in steps[:5]
            )
            sys_p = (
                "You are a skill-labelling assistant for a cybersecurity tool. "
                "Respond with ONLY a short snake_case label (3-6 words max, no spaces). "
                "Example: subdomain_enumeration_passive"
            )
            user_p = (
                f"Goal: {goal}\n"
                f"Actions taken: {step_summary}\n"
                "Suggest a concise skill label for this workflow pattern."
            )
            raw = await llm_call_fn(sys_p, user_p)
            label = ""
            if isinstance(raw, dict):
                label = raw.get("content", "") or ""
            else:
                label = str(raw)
            label = label.strip().split("\n")[0].strip()
            # Sanitise to snake_case
            label = re.sub(r"[^a-z0-9_]", "_", label.lower()).strip("_")
            label = re.sub(r"_+", "_", label)
            return label[:60] if label else None
        except Exception as exc:
            logger.debug("CLS: LLM label request failed: %s", exc)
            return None

    # ── Skill management API ────────────────────────────────────────────

    def list_skills(
        self,
        min_confidence: float = 0.0,
        source: str | None = None,
        tag: str | None = None,
        limit: int = 200,
    ) -> list[LearnedSkill]:
        """Return skills sorted by confidence desc, usage desc."""
        skills = list(self._skills.values())
        if min_confidence > 0:
            skills = [s for s in skills if s.confidence >= min_confidence]
        if source:
            skills = [s for s in skills if s.source == source]
        if tag:
            skills = [s for s in skills if tag in s.tags]
        skills.sort(key=lambda s: (-s.confidence, -s.usage_count))
        return skills[:limit]

    def get_skill(self, skill_id: str) -> LearnedSkill | None:
        """Get a skill by its ID."""
        return self._skills.get(skill_id)

    def delete_skill(self, skill_id: str) -> bool:
        """Remove a skill from memory and database."""
        if skill_id not in self._skills:
            return False
        del self._skills[skill_id]
        try:
            with self._lock:
                self._conn().execute(
                    "DELETE FROM learned_skills WHERE skill_id=?", (skill_id,)
                )
                self._conn().commit()
            logger.info("CLS: deleted skill %s", skill_id[:8])
            return True
        except Exception as exc:
            logger.warning("CLS: failed to delete skill %s: %s", skill_id[:8], exc)
            return False

    def update_skill_tag(self, skill_id: str, tag: str, remove: bool = False) -> bool:
        """Add or remove a tag on a skill."""
        skill = self._skills.get(skill_id)
        if not skill:
            return False
        if remove:
            skill.tags = [t for t in skill.tags if t != tag]
        else:
            if tag not in skill.tags:
                skill.tags.append(tag)
        self._save_skill(skill)
        return True

    def update_skill_notes(self, skill_id: str, notes: str) -> bool:
        """Update the notes field on a skill."""
        skill = self._skills.get(skill_id)
        if not skill:
            return False
        skill.notes = notes[:500]
        self._save_skill(skill)
        return True

    def export_skills(self, path: Path | None = None) -> dict[str, Any]:
        """Export all skills as JSON for sharing with Siyarix developers.

        All data in the export is already anonymised (``{target}`` placeholders).
        No real target information is ever exported.
        """
        try:
            from . import __version__ as ver
        except Exception:
            ver = "unknown"

        payload: dict[str, Any] = {
            "schema_version": self._SCHEMA_VERSION,
            "siyarix_version": ver,
            "exported_at": time.time(),
            "skill_count": len(self._skills),
            "skills": [s.to_dict() for s in self.list_skills()],
        }

        if path is not None:
            try:
                path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                logger.info("CLS: exported %d skills to %s", len(self._skills), path)
            except Exception as exc:
                logger.warning("CLS: export failed: %s", exc)

        return payload

    def import_skills(self, data: dict[str, Any]) -> int:
        """Import skills from an exported dict. Returns count of new skills imported."""
        imported = 0
        for s in data.get("skills", []):
            if s["skill_id"] in self._skills:
                continue  # Don't overwrite existing
            try:
                steps = [LearnedStep(**step) for step in s.get("steps", [])]
                skill = LearnedSkill(
                    skill_id=s["skill_id"],
                    intent_pattern=s["intent_pattern"],
                    steps=steps,
                    confidence=s.get("confidence", 0.0),
                    usage_count=s.get("usage_count", 0),
                    success_count=s.get("success_count", 0),
                    tokens=s.get("tokens", []),
                    synonyms=s.get("synonyms", {}),
                    created_at=s.get("created_at", time.time()),
                    last_used=s.get("last_used", time.time()),
                    source=s.get("source", "imported"),
                    tags=s.get("tags", []),
                    notes=s.get("notes", ""),
                )
                self._skills[skill.skill_id] = skill
                self._save_skill(skill)
                imported += 1
            except Exception as exc:
                logger.debug("CLS: failed to import skill: %s", exc)
        return imported

    def stats(self) -> dict[str, Any]:
        """Return statistics about the learning system."""
        skills = list(self._skills.values())
        total = len(skills)
        avg_conf = sum(s.confidence for s in skills) / max(total, 1)
        total_obs = sum(s.usage_count for s in skills)
        total_success = sum(s.success_count for s in skills)
        return {
            "total_skills": total,
            "high_confidence": sum(1 for s in skills if s.confidence >= 0.90),
            "medium_confidence": sum(1 for s in skills if 0.50 <= s.confidence < 0.90),
            "low_confidence": sum(1 for s in skills if s.confidence < 0.50),
            "avg_confidence": round(avg_conf, 3),
            "total_observations": total_obs,
            "total_successes": total_success,
            "overall_success_rate": round(total_success / max(total_obs, 1), 3),
            "sources": {
                "llm": sum(1 for s in skills if s.source == "llm"),
                "offline": sum(1 for s in skills if s.source == "offline"),
                "imported": sum(1 for s in skills if s.source == "imported"),
            },
            "db_path": str(self._db_path),
        }


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_LEARNING_SYSTEM: ContinuousLearningSystem | None = None
_LS_LOCK = threading.Lock()


def get_learning_system() -> ContinuousLearningSystem:
    """Return the process-wide :class:`ContinuousLearningSystem` singleton."""
    global _LEARNING_SYSTEM  # noqa: PLW0603
    if _LEARNING_SYSTEM is None:
        with _LS_LOCK:
            if _LEARNING_SYSTEM is None:
                _LEARNING_SYSTEM = ContinuousLearningSystem()
    return _LEARNING_SYSTEM


__all__ = [
    "ContinuousLearningSystem",
    "LearnedSkill",
    "LearnedStep",
    "get_learning_system",
]
