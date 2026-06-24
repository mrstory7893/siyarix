# Offline / Registry Mode

When no AI provider is connected or `--mode offline` / `--mode registry` is specified, Siyarix operates using heuristic planning and a local tool registry — no LLM required.

## How It Works

1. The **RegistryPlanner** matches your instruction against approximately 450 keyword patterns and 14–15 auto-DAG workflow templates using NLP intent parsing
2. The **RegistryExecutor** executes each step through the `ToolRegistry` with full guardrails, DLP, and alternative tool fallback
3. Results are persisted to the **OfflineStore** (SQLite) for later review and diffing across scans

## Deep Scan

The `siyarix scan-deep` command runs 4 progressive passes:

1. **Discovery** — host discovery and full port sweep
2. **Fingerprint** — OS detection, service versioning, default scripts
3. **Vulnerability** — template-based vulnerability scanning (nuclei, nikto)
4. **Enumeration** — directory, subdomain, and DNS enumeration

Each pass runs tools in parallel with automatic alternative fallback.

## Programmatic Usage

```python
from siyarix.offline_registry import offline_instruction_hint, no_provider_message

hint = offline_instruction_hint("scan example.com")
msg = no_provider_message()
```

## Related Commands

- `siyarix scan <target> --mode offline`
- `siyarix scan-deep <target>`
- `siyarix discover <target> --deep`
- `siyarix run "<instruction>" --mode registry`
