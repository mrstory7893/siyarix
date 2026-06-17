# Experience Intelligence & Continuous Learning

Siyarix v3.0.0 includes a continuous learning system that uses semantic memory via vector embeddings to record experiences, find similar past operations, and improve decision-making over time.

The subsystem comprises three components: **MemoryManager** (semantic embedding storage), **ContinuousLearning** (experience recording and recall), and **ResponseGenerator** (structured AI output formatting).

---

## Architecture

```
User Action / Tool Result
          │
          ▼
┌─────────────────────┐     ┌──────────────────────┐
│  MemoryManager      │     │  ContinuousLearning   │
│  • embedding gen    │◄────│  • record experience  │
│  • vector storage   │     │  • find similar       │
│  • cosine search    │     │  • update patterns    │
│  • importance decay │     │  • consolidate        │
└─────────┬───────────┘     └──────────┬───────────┘
          │                            │
          └────────────┬───────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Planner /     │
              │  AgentCore     │
              │  • informed    │
              │    decisions   │
              └────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │ ResponseGenerator │
              │ • structured AI   │
              │   responses       │
              └────────────────┘
```

---

## 1. MemoryManager

The `MemoryManager` (`memory.py`) provides embedding-based semantic memory. It generates vector embeddings for text content and stores them for similarity-based retrieval.

### Embedding Generation

```python
from siyarix.memory import MemoryManager

memory = MemoryManager()
embedding = await memory.generate_embedding(
    "Host 10.0.0.1 has Apache 2.4.41 vulnerable to CVE-2024-1234"
)
```

Embeddings are generated via the configured AI provider (OpenAI, Ollama, or simulated fallback using character-level similarity).

### Similarity Search

```python
similar = await memory.find_similar(
    query="Apache vulnerabilities",
    top_k=5
)
# Returns list of (content, similarity_score, metadata) tuples
```

Cosine similarity is used for vector comparison. Results include original content, metadata (source, timestamp, severity), and similarity score.

### Importance Decay

Memory entries have an importance score that decays over time. Entries accessed infrequently or older than the retention threshold are pruned during consolidation cycles.

---

## 2. ContinuousLearning

The `ContinuousLearning` class (`core/learning.py`) manages long-term semantic memory by recording experiences and querying similar past experiences.

### Experience Recording

```python
@dataclass
class Experience:
    content: str
    embedding: list[float]
    metadata: dict
    timestamp: datetime

learning = ContinuousLearning()
await learning.record_experience(
    content="Scanned 10.0.0.0/24 with nmap, found 5 open hosts",
    metadata={"target": "10.0.0.0/24", "tool": "nmap", "findings": 5}
)
```

### Finding Similar Experiences

```python
similar = await learning.query_similar(
    query="Scan 10.0.0.0/24 for open ports",
    top_k=3
)
# Returns past experiences with similar context
```

This enables the planner and agent core to make informed decisions based on historical patterns. For example, if a previous scan of a similar subnet led to specific follow-up actions, those patterns influence current planning.

### Consolidation

Repeated similar observations are consolidated into abstract knowledge:

```
Raw observations:
  - "Host A runs Apache 2.4.41"
  - "Host B runs Apache 2.4.41"
  - "Host C runs Apache 2.4.49"

Consolidated:
  "Apache 2.4.x is the predominant web server (3 hosts identified).
   Multiple versions present; 2.4.41 has known high-severity CVEs."
```

### Persistence

Experiences are persisted to `~/.siyarix/memory/` as JSON files, enabling cross-session memory. The system loads existing memory on startup and saves new experiences automatically.

---

## 3. ResponseGenerator

The `ResponseGenerator` (`response.py`) produces structured, context-aware AI responses. It converts raw findings and execution results into formatted output suitable for display in the REPL, API responses, or report sections.

```python
from siyarix.response import ResponseGenerator

generator = ResponseGenerator()
response = await generator.generate(
    intent="explain_finding",
    data={
        "finding": finding,
        "context": context_summary,
        "user_question": "What does this mean?"
    }
)
```

The generator adapts its output based on:
- **User context**: Current phase, recent commands, target inventory
- **Finding severity**: Critical findings get detailed explanations
- **Output format**: Structured for the requested output format (table, JSON, etc.)

---

## Integration Points

| Component | Integration | Purpose |
|-----------|-------------|---------|
| **AgentCore** | `execute_goal()` → `query_similar()` | Past experiences influence planning |
| **Planner** | Plan generation → similar experience context | Better tool selection based on history |
| **REPL** | User input → context from memory | Proactive suggestions from learned patterns |
| **ReportEngine** | Finding enrichment → experience correlation | Context-aware report generation |

---

## Planned Enhancements

The following advanced XI features are planned for future releases:

- **ContextTracker**: Session phase tracking across 8 operation phases (IDLE, RECON, SCANNING, ENUMERATION, EXPLOITATION, POST_EXPLOIT, REPORTING, CLEANUP) with real-time phase transitions
- **SkillProfiler**: Evaluate user expertise (BEGINNER → EXPERT) based on tool diversity, command volume, error rate, and advanced feature usage — adapting UI complexity and confirmation levels accordingly
- **Predictor**: Next-action prediction using four strategies (phase-based, tool follow-up, findings-based, learned patterns) with confidence scoring and feedback-driven weight adjustment
- **Streaming Event System**: Dedicated event stream (`xi.*` events) for real-time phase changes, skill updates, prediction readiness, and pattern learning notifications
