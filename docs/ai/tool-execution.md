# Tool Execution

AI-planned tools are executed through a structured pipeline that handles discovery, registration, availability evaluation, invocation, output parsing, error recovery, cross-platform installation, and version detection.

---

## Tool Lifecycle

```
Discovery (ToolRegistry) → Registration (ToolCapabilityGraph)
  → Availability Check (ToolAvailabilityContext)
  → Permission Gate (PermissionGate + ShellReview)
  → Invocation (ToolHandlers / internal_tools)
  → Output Capture (safe_run_async / safe_run_async_stream)
  → Danger Analysis (DangerAnalyzer)
  → DLP Redaction (DLPEngine)
  → Finding Storage (Knowledge Graph)
  → Version Detection (ToolVersion)
  → Installation (ToolInstaller)
```

---

## Tool Registry

`ToolRegistry` (in `registry.py`) is the central hub for tool management. It maintains a `ToolCapabilityGraph` for capability-based lookups, a handler map for tool-specific invocation, and a `ParserRegistry` for output parsing.

```python
from siyarix.registry import ToolRegistry

registry = ToolRegistry()
registry.discover_from_path()  # Discover curated + interpreter tools
registry.scan_path()           # Scan every executable on $PATH
```

### Registration

Tools are registered as `ToolCapability` objects with optional custom handlers:

```python
from siyarix.tool_models import ToolCapability, ToolCategory, RiskLevel

tool = ToolCapability(
    name="nmap",
    description="Network port scanner and service detector",
    category=ToolCategory.RECON,
    risk_level=RiskLevel.MEDIUM,
    tags=["port-scan", "network", "service-detection"],
    binary="nmap",
    installed=True,
    version="7.95",
)
registry.register(tool, handler_factory=make_nmap_handler)
```

### Supported Tools (Curated)

26 curated security tools with dedicated handler mappings:

| Tool | Category | Handler |
|------|----------|---------|
| nmap | RECON | `make_nmap_handler` |
| nikto | SCANNING | `make_web_handler` |
| nuclei | SCANNING | `make_web_handler` |
| gobuster | SCANNING | `make_web_handler` |
| ffuf | SCANNING | `make_web_handler` |
| hydra | EXPLOITATION | `make_brute_handler` |
| masscan | RECON | `make_portscan_handler` |
| amass | RECON | `make_recon_handler` |
| subfinder | RECON | `make_recon_handler` |
| wpscan | SCANNING | `make_web_handler` |
| sqlmap | SCANNING | `make_web_handler` |
| shodan | RECON | `make_recon_handler` |
| bettercap | NETWORK | `make_network_handler` |
| ettercap | NETWORK | `make_network_handler` |
| aircrack-ng | NETWORK | `make_network_handler` |
| hashcat | CRYPTO | `make_crypto_handler` |
| john | CRYPTO | `make_crypto_handler` |
| burpsuite | WEB | `make_web_handler` |
| zaproxy | WEB | `make_web_handler` |
| whatweb | WEB | `make_web_handler` |
| curl | UTILITY | `make_curl_handler` |
| wget | UTILITY | `make_curl_handler` |
| dig | RECON | `make_dns_handler` |
| whois | RECON | `make_whois_handler` |
| graph_analyzer | REPORTING | `make_graph_analyzer_handler` |
| threat_intel | REPORTING | `make_threat_intel_handler` |

Plus 20+ system/interpreter tools (ls, date, df, free, ps, uname, python3, node, go, etc.) and all executables discovered on `$PATH`.

---

## Tool Data Model

### ToolCapability

```python
@dataclass
class ToolCapability:
    name: str                           # Tool name
    description: str                    # Human-readable description
    category: ToolCategory              # RECON, SCANNING, EXPLOITATION, etc.
    risk_level: RiskLevel               # SAFE, LOW, MEDIUM, HIGH, CRITICAL
    aliases: list[str]                  # Alternative names
    tags: list[str]                     # Capability tags
    inputs: dict[str, str]              # Expected input parameters
    input_schema: dict[str, Any]        # JSON schema for inputs
    outputs: dict[str, str]             # Output structure
    dependencies: list[str]             # Required tools
    related_tools: list[str]            # Similar tools
    workflows: list[str]                # Associated workflows
    binary: str                         # Path to binary
    version: str                        # Detected version
    installed: bool                     # Available on PATH
    source: str                         # Source of tool metadata
    metadata: dict[str, Any]            # Additional metadata (personas, etc.)
    parser: str                         # Parser module name
    availability: dict | None           # Availability expression
    usage_count: int                    # Number of times used
    last_used: float                    # Timestamp of last usage
    avg_duration_ms: float              # Average execution time
```

### ToolCategory

| Category | Example Tools |
|----------|--------------|
| `RECON` | nmap, masscan, amass, subfinder, shodan, dig, whois |
| `SCANNING` | nikto, nuclei, wpscan, sqlmap, gobuster, ffuf |
| `EXPLOITATION` | hydra, metasploit |
| `POST_EXPLOIT` | mimikatz, bloodhound, impacket |
| `REPORTING` | graph_analyzer, threat_intel |
| `NETWORK` | bettercap, ettercap, aircrack-ng |
| `WEB` | burpsuite, zaproxy, whatweb |
| `CRYPTO` | hashcat, john |
| `FORENSICS` | volatility, yara, exiftool |
| `CONTAINER` | trivy, grype, kube-bench |
| `CLOUD` | prowler, scoutsuite, pacu |
| `DEVSECOPS` | semgrep, gitleaks, trufflehog |
| `UTILITY` | curl, dig, nslookup, whois, jq, python3 |

---

## Tool Capability Graph

`ToolCapabilityGraph` (in `tool_graph.py`) maintains a graph of tool relationships and supports:

### Pathfinding for Tool Chaining

```python
from siyarix.tool_graph import ToolCapabilityGraph

graph = ToolCapabilityGraph()
graph.add_tool(nmap_capability)
graph.add_tool(searchsploit_capability)
graph.add_edge(ToolEdge(source="nmap", target="searchsploit", weight=0.8))

# Find chain from nmap → searchsploit
chain = graph.get_chain("nmap", "searchsploit")  # ["nmap", "searchsploit"]
```

### Optimal Tool Scoring

```python
# Score tools by relevance to a goal
results = graph.find_optimal_tools("port scan", available=["nmap", "masscan", "curl"])
# Returns scored ToolCapability list, ordered by relevance
```

### Category and Availability Lookups

```python
graph.get_tools_by_category(ToolCategory.RECON)
graph.get_available_tools()
graph.get_tool("nmap")               # Also resolves aliases
```

---

## Tool Handlers

Tool-specific invocation handlers in `tool_handlers.py` manage arguments and execution for each tool:

| Handler | Tools | Features |
|---------|-------|----------|
| `make_nmap_handler` | nmap | Flags, target, timeout |
| `make_portscan_handler` | masscan, rustscan | Flags, target, timeout |
| `make_web_handler` | nikto, nuclei, gobuster, ffuf, wpscan, sqlmap, whatweb, burpsuite, zaproxy | Target flags, stealth decoys, extra args |
| `make_recon_handler` | amass, subfinder, shodan | Tool-specific subcommands |
| `make_brute_handler` | hydra | Service, username, wordlist |
| `make_network_handler` | bettercap, ettercap, aircrack-ng | Mode-specific arguments |
| `make_crypto_handler` | hashcat, john | Hash file, wordlist, mode |
| `make_curl_handler` | curl, wget | Flags, target |
| `make_dns_handler` | dig, nslookup | Flags, target |
| `make_whois_handler` | whois | Target |
| `make_generic_handler` | Any tool | Target validation, args, flags |

### Example Handler

```python
def make_nmap_handler(tool_name: str) -> ToolHandler:
    async def handler(**kwargs: Any) -> dict[str, Any]:
        target = kwargs.get("target", "")
        if not target:
            return {"status": "error", "error": "No target specified", "tool": tool_name}
        flags = kwargs.get("flags", "-sT -T4 --top-ports 100")
        cmd = [tool_name] + flags.split() + [target]
        result = await _run(tool_name, cmd, kwargs.get("timeout", 120))
        return {"status": "success" if not result.exit_code else "error", "output": result.stdout, ...}
    return handler
```

### Internal Tools

`internal_tools.py` provides built-in handlers that operate on Siyarix's own data:

| Handler | Tool | Actions |
|---------|------|---------|
| `make_graph_analyzer_handler` | graph_analyzer | shortest_path, blast_radius, find_crown_jewel_paths (via KnowledgeGraph) |
| `make_threat_intel_handler` | threat_intel | cve_lookup, mitre_lookup (via ThreatIntelFeed, MITREAttackDB) |

---

## Tool Availability Evaluation

`ToolAvailabilityContext` evaluates whether a tool can run in the current environment:

```python
from siyarix.tool_availability import (
    ToolAvailabilityContext,
    evaluate_availability,
    check_tool_available,
)
```

### Availability Signals

| Signal | Evaluates | Expression |
|--------|-----------|------------|
| `always` | Always available | `{"always": true}` |
| `auth` | Provider API key configured | `{"auth": {"provider": "openai"}}` |
| `config` | Config value set/matches | `{"config": {"key": "feature_x", "value": "enabled"}}` |
| `env` | Environment variable set/matches | `{"env": {"var": "API_KEY"}}` |
| `installed` | Binary exists on PATH | `{"installed": {"name": "nmap"}}` |

### Boolean Expressions

```python
# All must pass
result = evaluate_availability({
    "allOf": [
        {"installed": {"name": "nmap"}},
        {"env": {"var": "STEALTH_MODE"}}
    ]
}, ctx)

# Any must pass
result = evaluate_availability({
    "anyOf": [
        {"installed": {"name": "nmap"}},
        {"installed": {"name": "masscan"}}
    ]
}, ctx)
```

The signal system is extensible — custom signals can be registered via `register_signal()`.

---

## Tool Metadata

`tool_metadata.py` provides tool categorization and metadata lookup with a two-tier fallback:

1. **`data/cyber_tools.json`** — extensible JSON database of tool definitions
2. **Built-in static mappings** — fallback for tools not yet in the database

```python
from siyarix.tool_metadata import categorize_tool, risk_for_tool, describe_tool, tags_for_tool, personas_for_tool

cat = categorize_tool("nmap")          # ToolCategory.RECON
risk = risk_for_tool("metasploit")      # RiskLevel.HIGH
desc = describe_tool("nuclei")          # "Template-based vulnerability scanner"
tags = tags_for_tool("nmap")            # ["port-scan", "network", "service-detection"]
personas = personas_for_tool("nuclei")  # ["pentester", "redteam", "blueteam", "devsecops"]
```

### Tool Version

`tool_version.py` provides JSON database access for tool metadata:

```python
from siyarix.tool_version import get_tool_metadata

meta = get_tool_metadata("nuclei")
# Returns: {"description": "...", "category": "scanning", "risk_level": "medium", ...}
```

---

## Tool Selection

### Capability-Based Selection

```python
registry.get_by_tags(["port_scanning"])
# Returns: [nmap, masscan, rustscan, ...]
```

### Search

```python
registry.search("vulnerability scanner", top_k=5)
# Scored by name match → tag match → description match
```

### Alternatives

```python
registry.get_tool_alternatives("nmap")
# Returns: ["masscan", "rustscan", "naabu"]
```

---

## Execution

Commands are executed via `subprocess_utils.py` which provides three execution modes:

```python
from siyarix.subprocess_utils import (
    safe_run_async,        # Standard async execution
    safe_run_async_stream, # Streaming with line-by-line output
    safe_run_sync,         # Synchronous execution
    safe_run_sandboxed,    # Sandboxed execution with bwrap/Docker
)
```

### Execution Features

| Feature | Description |
|---------|-------------|
| **Timeout** | Process killed after `timeout` seconds |
| **Environment injection** | API keys, proxy settings injected as env vars |
| **PTY support** | Interactive tools via PTY allocation |
| **Output capture** | stdout + stderr with configurable size limits |
| **Streaming** | Line-by-line output for real-time display |
| **Injection guards** | Pre-execution arg validation and sanitization |
| **Orphan tracking** | Process cleanup on exit via `_ORPHAN_TRACKER` |
| **Sudo support** | Automatic password prompting via TTY or `SIYARIX_SUDO_PASSWORD` |
| **Destructive pattern detection** | Blocks rm -rf /, mkfs, dd, fork bombs |
| **Path traversal protection** | Blocks ../ and %2e%2e patterns |

### Sandboxed Execution

```python
result = safe_run_sandboxed(
    command=["nmap", "-sV", target],
    timeout=60,
    allow_network=False,
    use_seccomp=True,
)
# Uses bwrap on Linux, Docker fallback, restricted env on Windows/mobile
```

---

## Output Parsing

Parsers convert raw tool output into structured `Finding` objects. Located in `src/siyarix/parsers/`. The `ParserRegistry` in `ToolRegistry` maps tools to their parsers.

```python
# Automatic parsing when executing via ToolRegistry
result = await registry.execute("nmap", target="10.0.0.1")
# result["findings"] contains parsed Finding objects
```

### Finding Lifecycle

1. **Parsed** from raw tool output by dedicated parser
2. **Added** to the knowledge graph via `_ingest_finding_to_graph()`
3. **Stored** in the offline store
4. **Logged** to the audit trail
5. **Deduplicated** by MD5 hash across (target, port, CVE, severity)
6. **Displayed** to the user

---

## Tool Installation

`ToolInstaller` (in `tool_installer.py`) handles automated installation across platforms:

```python
from siyarix.tool_installer import ToolInstaller

installer = ToolInstaller()
result = installer.install("nmap")
# ToolInstallResult(tool="nmap", success=True, method="auto")
```

### Platform Support

| Platform | Package Managers Used |
|----------|---------------------|
| Windows | `winget` → `choco` (with predefined Winget ID mappings) |
| Linux | `apt-get` → `pacman` → `dnf` → `apk` |
| macOS | `brew` |

### Winget ID Mappings (Windows)

| Tool | Winget ID |
|------|-----------|
| nmap | `Insecure.Nmap` |
| openssl | `ShiningLight.OpenSSL` |
| git | `Git.Git` |
| curl | `cURL.cURL` |
| ffuf | `ffuf.ffuf` |
| nuclei | `ProjectDiscovery.Nuclei` |
| yara | `VirusTotal.YARA` |

### Batch Installation

```python
results = installer.auto_install_missing(["nmap", "ffuf", "nuclei"])
```

---

## Error Handling

### Tool Not Found

`safe_run_async` automatically generates installation hints:

```
Binary not found: 'nmap' is not installed or not found in PATH.
Install it with: winget install Insecure.Nmap
```

### Tool Execution Failure

```python
# Automatic retry with -Pn flag for filtered ports
recovery = await validator.plan_recovery(failed_step, "connection refused")
# RecoveryPlan(action=RETRY, modified_step={...flags: "... -Pn"})
```

### Registry-Level Execution Pipeline

When executing via `ToolRegistry.execute()`:

1. Availability check (against `tool.availability` expression)
2. Permission gate check (`PermissionGate`)
3. Interactive review (`ShellReview.review_and_confirm`)
4. Handler invocation with timing
5. Automatic parser dispatch for output analysis
6. Usage statistics tracking (usage_count, avg_duration_ms)

---

## Custom Tools

Tools can be loaded from a custom JSON file at `config_dir / custom_tools.json`:

```json
{
    "my-tool": {
        "description": "Custom security scanner",
        "category": "scanning",
        "risk_level": "medium",
        "aliases": ["mt"],
        "tags": ["custom", "scanner"],
        "binary": "my-tool",
        "version": "1.0"
    }
}
```

---

## Related Modules

| Module | Path | Purpose |
|--------|------|---------|
| `ToolRegistry` | `src/siyarix/registry.py` | Central tool registry with discovery, handlers, parsers |
| `ToolCapability` | `src/siyarix/tool_models.py` | Tool data model (name, category, risk, tags, etc.) |
| `ToolCapabilityGraph` | `src/siyarix/tool_graph.py` | Tool chaining, similarity graph, optimal scoring |
| `ToolHandlers` | `src/siyarix/tool_handlers.py` | Tool-specific invocation handlers (11 handlers) |
| `InternalTools` | `src/siyarix/internal_tools.py` | Built-in graph_analyzer and threat_intel handlers |
| `ToolAvailability` | `src/siyarix/tool_availability.py` | Pre-execution availability evaluation with extensible signals |
| `ToolInstaller` | `src/siyarix/tool_installer.py` | Cross-platform auto-installation (winget/choco/apt/brew) |
| `ToolMetadata` | `src/siyarix/tool_metadata.py` | Tool categorization, risk, description, tags, personas |
| `ToolVersion` | `src/siyarix/tool_version.py` | JSON database access for tool metadata |
| `ToolCallRepair` | `src/siyarix/tool_call_repair.py` | Plain-text tool call parsing and promotion |
| `subprocess_utils.py` | `src/siyarix/subprocess_utils.py` | Async subprocess execution (safe_run_async + streaming + sandboxed) |
| `security_hardening.py` | `src/siyarix/security_hardening.py` | Danger analysis, input validation, secret redaction |
| `parsers/` | `src/siyarix/parsers/` | Tool-specific output parsers (100+) |
