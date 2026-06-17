# Execution Engine

The Execution Engine is the runtime that transforms `ExecutionPlan` objects into executed commands. It builds execution plans from goals, resolves dependencies, dispatches steps in parallel via the `WorkerPool`, routes output through parsers, and handles errors with exponential backoff.

---

## Architecture

```
ExecutionPlan (from Planner)
         │
         ▼
┌──────────────────────────────────────────────────┐
│                ExecutionEngine                    │
│                                                   │
│  1. Validate plan structure & integrity           │
│  2. Check PermissionGate per step (BLOCK/REVIEW/  │
│     ALLOW)                                        │
│  3. Resolve dependency ordering (topological)     │
│  4. Group steps into parallel layers              │
│  5. Dispatch via WorkerPool (bounded concurrency) │
│  6. Route output through tool-specific parsers    │
│  7. Extract findings → KnowledgeGraph             │
│  8. Handle errors (retry, backoff, fail)          │
│  9. Aggregate results → EngineResult              │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
                EngineResult
         (steps_completed, steps_failed,
          findings, duration, errors)
```

---

## Plan Structure

```python
@dataclass
class ExecutionPlan:
    target: str                          # Target host/network/URL
    steps: list[ExecutionStep]           # Ordered/parallel steps
    errors: list[str]                    # Planning errors (if any)
    mode: ExecutionMode                  # REGISTRY | AUTONOMOUS | HYBRID | INTERACTIVE
    metadata: dict                       # Planner metadata, confidence, etc.
```

### ExecutionStep

```python
@dataclass
class ExecutionStep:
    tool: str                            # Tool name from ToolRegistry
    command: str                         # Full command string to execute
    args: dict                           # Structured arguments
    dependencies: list[int]              # Step indices that must complete first
    output_parser: str                    # Parser class name for results
    timeout: int                         # Per-step timeout in seconds
    retry_count: int                     # Maximum retries on transient failure
    allow_review: bool                   # Whether step requires REVIEW gate
```

---

## Executor Types

Siyarix provides three executor implementations, selected by the `ExecutionMode`:

| Executor | Mode | Behavior |
|----------|------|----------|
| **BaseExecutor** | INTERACTIVE | Per-step user confirmation, incremental output, interactive review |
| **RegistryExecutor** | REGISTRY | Deterministic template execution, no AI dependency, offline-capable |
| **AutonomousExecutor** | AUTONOMOUS | Full autonomy, Observe-Reason-Act loop, continuous until objective met |

```python
if plan.mode == ExecutionMode.REGISTRY:
    executor = RegistryExecutor(plan, gate, worker_pool)
elif plan.mode == ExecutionMode.AUTONOMOUS:
    executor = AutonomousExecutor(plan, gate, worker_pool, provider_manager)
elif plan.mode == ExecutionMode.HYBRID:
    executor = HybridExecutor(plan, gate, worker_pool, provider_manager)
elif plan.mode == ExecutionMode.INTERACTIVE:
    executor = BaseExecutor(plan, gate, worker_pool, interactive=True)

result = await executor.execute()
```

---

## Dependency Resolution

Steps are organized into dependency layers using topological ordering:

```
Layer 0: [recon_scan, dns_enum]          # No dependencies
Layer 1: [nuclei_scan, nikto_scan]        # Depends on recon_scan
Layer 2: [metasploit_exploit]             # Depends on nuclei + nikto
Layer 3: [report_generation]              # Depends on exploit results
```

Steps within the same layer execute concurrently via `asyncio.gather()`.
Cross-layer dependencies enforce sequential execution.

---

## WorkerPool

Bounded async concurrency via `WorkerPool`:

```python
pool = WorkerPool(
    max_workers=config.get("default_parallel", 3),
    queue_size=config.get("queue_size", 50)
)
results = await pool.map(execute_step, parallel_steps)
```

- Configurable max concurrent workers
- Backpressure via bounded queue
- Graceful task cancellation on shutdown

---

## Tool Execution

Each tool step is executed via `safe_run_sync()`:

1. **Tool resolution**: Resolve tool name → binary path via `ToolRegistry` + `dynamic_resolver`
2. **Command formatting**: Substitute target and arguments into command template
3. **Subprocess execution**: Run as subprocess with configurable timeout
4. **I/O capture**: Simultaneous stdout/stderr capture
5. **Exit code evaluation**: Determine success/failure from return code

```python
async def safe_run_sync(step: ExecutionStep) -> StepResult:
    binary = await ToolRegistry.resolve_binary(step.tool)
    command = format_command(binary, step.args)
    
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        timeout=step.timeout
    )
    stdout, stderr = await proc.communicate()
    
    return StepResult(
        tool=step.tool,
        exit_code=proc.returncode,
        stdout=stdout.decode(),
        stderr=stderr.decode(),
        duration=proc.duration
    )
```

---

## Output Parsing

Tool output is routed through tool-specific parsers:

```python
parser = get_parser(step.output_parser)  # e.g., NmapParser, NucleiParser
findings = parser.parse(step_result.stdout)
```

Each parser extracts structured findings:
- **Port Scanners**: ports, protocols, service versions, banners
- **Vuln Scanners**: vulnerability IDs, severity, CVSS vectors, descriptions
- **Web Scanners**: URLs, technologies, directories, forms
- **Recon Tools**: subdomains, DNS records, WHOIS data

Findings are immediately inserted into the **KnowledgeGraph** for downstream reasoning.

---

## Error Recovery

The `recovery` module implements exponential backoff with jitter:

```python
async def execute_with_retry(step):
    for attempt in range(step.retry_count + 1):
        try:
            return await execute_step(step)
        except TransientError as e:
            if attempt == step.retry_count:
                raise
            delay = min(2 ** attempt + random.uniform(0, 1), MAX_BACKOFF)
            await asyncio.sleep(delay)
```

| Error Type | Behavior |
|-----------|----------|
| **Transient** (connection reset, timeout) | Retry with exponential backoff + jitter |
| **Permanent** (invalid target, bad tool) | Fail immediately, log error |
| **Permission** (gate BLOCK) | Fail immediately, log to AuditLogger |
| **Resource** (OOM, disk full) | Pause, retry after cooldown |

---

## CommandPipeline

The `CommandPipeline` enables chaining commands in a DAG:

```yaml
pipeline:
  - id: recon
    tool: nmap
    target: $target
    flags: -sV -sC
  - id: vuln_scan
    tool: nuclei
    depends_on: [recon]
    input: "{recon.output}"
  - id: report
    tool: report
    depends_on: [vuln_scan]
    format: sarif
```

Pipelines support:
- Step chaining via `depends_on` references
- Variable interpolation (`$target`, `{step.output}`)
- Conditional execution based on prior step status
- Pipeline-level timeout and error handling

---

## EngineResult

```python
@dataclass
class EngineResult:
    steps_completed: int                  # Successful steps
    steps_failed: int                     # Failed steps
    steps_skipped: int                    # Steps skipped (dependency failure)
    findings: list[Finding]              # Extracted findings from parsers
    duration: float                       # Total execution time (seconds)
    errors: list[StepError]              # Error details for failed steps
    artifacts: dict[str, str]            # Output artifacts (file paths)
    session_id: str                       # Associated session ID
```

---

## Integration Points

| Component | Integration |
|-----------|------------|
| **PermissionGate** | Pre-execution BLOCK/REVIEW/ALLOW per step |
| **DLP Engine** | Post-gate data leak inspection |
| **KnowledgeGraph** | Findings inserted in real-time |
| **AuditLogger** | Every execution logged with SHA-256 chain |
| **EventBus** | Events emitted per step lifecycle |
| **MetricsCollector** | Execution duration, success rate, error rate |
| **CacheManager** | Cached tool outputs (LRU + TTL) |
| **OfflineStore** | Results persisted for offline retrieval |
