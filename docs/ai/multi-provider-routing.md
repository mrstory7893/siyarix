# Multi-Provider Routing

Siyarix supports **25 AI providers** (24 cloud/local + 1 offline registry), all accessed through a unified OpenAI-compatible adapter in `openai_compat.py`. The `ProviderManager` singleton manages provider registration, credential pooling, failover, exponential-backoff cooldown, and multi-model ensemble decisions.

---

## Supported Providers

| Provider | Type | Env Variable | Default Model | Base URL |
|----------|------|-------------|---------------|----------|
| OpenAI | Cloud | `OPENAI_API_KEY` | gpt-5.5 | (default) |
| Anthropic | Cloud | `ANTHROPIC_API_KEY` | claude-sonnet-4-6 | (via openai compat) |
| Google Gemini | Cloud | `GEMINI_API_KEY` | gemini-3.1-pro-preview | `generativelanguage.googleapis.com/v1beta/openai/` |
| DeepSeek | Cloud | `DEEPSEEK_API_KEY` | deepseek-v4-flash | `api.deepseek.com` |
| xAI (Grok) | Cloud | `XAI_API_KEY` | grok-4.1 | `api.x.ai` |
| Perplexity | Cloud | `PERPLEXITY_API_KEY` | sonar-pro | `api.perplexity.ai` |
| Groq | Cloud | `GROQ_API_KEY` | llama-4-scout | `api.groq.com/openai/v1` |
| Together AI | Cloud | `TOGETHER_API_KEY` | Llama-4-Scout | `api.together.xyz/v1` |
| OpenRouter | Cloud | `OPENROUTER_API_KEY` | openai/gpt-5.5 | `openrouter.ai/api/v1` |
| Cerebras | Cloud | `CEREBRAS_API_KEY` | gpt-oss-120b | `api.cerebras.ai/v1` |
| Fireworks AI | Cloud | `FIREWORKS_API_KEY` | kimi-k2.6 | `api.fireworks.ai/inference/v1` |
| Mistral AI | Cloud | `MISTRAL_API_KEY` | (from profile) | `api.mistral.ai` |
| Z.AI | Cloud | `ZAI_API_KEY` | glm-5.1 | `api.z.ai/api/paas/v4` |
| MiniMax | Cloud | `MINIMAX_API_KEY` | MiniMax-M3 | `api.minimax.io/v1` |
| Moonshot | Cloud | `MOONSHOT_API_KEY` | kimi-k2.6 | `api.moonshot.ai/v1` |
| NVIDIA NIM | Cloud | `NVIDIA_API_KEY` | Nemotron-3-Super | `integrate.api.nvidia.com/v1` |
| HuggingFace | Cloud | `HUGGINGFACE_API_KEY` | (varies) | `api-inference.huggingface.co/v1` |
| Azure OpenAI | Cloud | `AZURE_OPENAI_API_KEY` | gpt-5.5 | (user-configured) |
| OpenCodeZen | Cloud | `OPENCODE_API_KEY` | deepseek-v4-flash | `opencode.ai/zen/v1` |
| Ollama | Local | — | llama3.1 | `localhost:11434/v1` |
| LM Studio | Local | — | (varies) | `localhost:1234/v1` |
| llama.cpp | Local | — | (varies) | `localhost:18080/v1` |
| vLLM | Local | — | (varies) | `localhost:8000/v1` |
| LocalAI | Local | — | (varies) | `localhost:8080/v1` |
| Registry | Heuristic | — | — | — |

---

## Architecture

```
User Input → _execute_instruction()
                │
                ▼
         ProviderManager.select_provider(preferred)
                │
                ▼
         ┌──────────────┐
         │  Provider A  │ ← preferred (user config or auto-detect)
         │  (primary)   │
         └──────┬───────┘
                │
        ┌─── Success ────→ Return result
        │
        └─── Failure ────→ ProviderManager.classify_error()
                           ├── AUTH → mark credential "dead"
                           ├── RATE_LIMIT → exponential backoff
                           ├── TIMEOUT → retry with backoff
                           ├── CONTEXT_OVERFLOW → compact and retry
                           ├── MODEL_NOT_FOUND → fallback model
                           └── SERVER_ERROR → record_failure with cooldown
                                    │
                                    ▼
                           ProviderStateManager.record_failure()
                           (persistent cooldown across restarts via JSON)
```

---

## Provider Manager (Singleton)

`ProviderManager` is a thread-safe singleton that centralises all provider logic:

```python
from siyarix.providers import ProviderManager

pm = ProviderManager.get_instance()
```

### Registration

All 25 providers register via individual profile files in `src/siyarix/providers/profiles/`:

```python
pm.register(ProviderProfile(
    name="openai",
    display_name="OpenAI",
    default_model="gpt-5.5",
    api_key_env="OPENAI_API_KEY",
    base_url="",
    supports_streaming=True,
    supports_tools=True,
    supports_vision=True,
    cost_tier=CostTier.HIGH,
    provider_type=ProviderType.CLOUD,
    priority=10,
    docs_url="https://platform.openai.com/docs/models",
))
```

Each profile defines models via `ModelInfo` dataclasses:

```python
ModelInfo(
    name="gpt-5.5",
    supports_vision=True,
    supports_structured_output=True,
    supports_function_calling=True,
    context_window=1050000,
    cost_tier=CostTier.HIGH,
)
```

### Auto-Detect

When `model_provider = "auto"`, `ProviderManager.auto_detect_provider()` scans profiles in priority order:

```python
def auto_detect_provider(self) -> str | None:
    for profile in self.list_profiles():
        if resolve_api_key(profile.name, profile.api_key_env):
            return profile.name
        if profile.provider_type == ProviderType.LOCAL and profile.base_url:
            return profile.name
    return None
```

### Preference Ordering

`list_profiles()` respects `provider_priority` from `settings.toml`:

```toml
provider_priority = "openai, gemini, anthropic, groq"
```

Providers are sorted by (index in priority list, -priority).

---

## Provider Data Models

All provider data models live in `src/siyarix/providers/types.py`:

### ProviderProfile

```python
@dataclass
class ProviderProfile:
    name: str                          # Internal identifier (e.g. "openai")
    display_name: str                  # Human-readable name
    models: list[ModelInfo]            # Supported models with capability metadata
    default_model: str                 # Fallback model for this provider
    api_key_env: str                   # Environment variable for API key
    base_url: str                      # API base URL
    supports_streaming: bool           # Streaming support
    supports_tools: bool               # Function/tool calling
    supports_vision: bool              # Image input support
    supports_structured_output: bool   # JSON structured output mode
    sdk_dependency: str                # Optional SDK package requirement
    max_tokens: int                    # Max output tokens
    max_context_tokens: int            # Max context window size
    priority: int                      # Preference ordering
    cost_tier: CostTier                # FREE / LOW / MEDIUM / HIGH
    provider_type: ProviderType        # CLOUD or LOCAL
    fallback_models: list[str]         # Alternative models to try on failure
    docs_url: str                      # Link to provider documentation
```

### ProviderCredential

```python
@dataclass
class ProviderCredential:
    provider: str
    api_key: str = ""
    base_url: str = ""
    status: str = "active"             # "active", "dead", or "cooldown"
    cooldown_until: float = 0.0
    failure_count: int = 0
    last_used: float = 0.0

    @property
    def is_available(self) -> bool:
        # True unless dead, in cooldown, or missing both key and URL
```

### ModelInfo

```python
@dataclass
class ModelInfo:
    name: str
    supports_vision: bool = False
    supports_tools: bool = True
    supports_structured_output: bool = False
    supports_function_calling: bool = True
    context_window: int = 8192
    cost_tier: CostTier = CostTier.MEDIUM
```

### Enums

- **FailoverReason**: AUTH, RATE_LIMIT, BILLING, TIMEOUT, SERVER_ERROR, CONTEXT_OVERFLOW, MODEL_NOT_FOUND, UNKNOWN
- **CostTier**: FREE, LOW, MEDIUM, HIGH
- **ProviderType**: CLOUD, LOCAL

### ClassifiedError

```python
@dataclass
class ClassifiedError:
    reason: FailoverReason
    retryable: bool = True
    should_rotate_credential: bool = False
    should_fallback: bool = False
    should_compress: bool = False
    message: str = ""
```

---

## Error Classification & Failover

### Classification Strategy

`ProviderManager.classify_error()` uses a multi-pass strategy:

1. **HTTP status code** — maps to `FailoverReason`
2. **Error message text** — scans for keywords ("rate limit", "timeout", "401", etc.)
3. **Credential rotation** hints returned for auth/billing failures

### Failover Reasons

| Reason | HTTP Status | Retryable | Action |
|--------|------------|-----------|--------|
| `AUTH` | 401, 403 | No | Mark credential dead, rotate |
| `RATE_LIMIT` | 429 | Yes | Exponential backoff (10s→20s→40s→...→3600s) |
| `BILLING` | 402 | No | Mark credential dead |
| `TIMEOUT` | 408 | Yes | Backoff (5s→10s→...→300s) |
| `SERVER_ERROR` | 500, 502, 503, 504, 529 | Yes | Backoff (5s→10s→...→300s) |
| `CONTEXT_OVERFLOW` | — | Yes | Compact history, retry |
| `MODEL_NOT_FOUND` | 404 | No | Fall back to alternative model |
| `UNKNOWN` | — | No | Propagate error |

### Failure Recording

`ProviderManager.record_failure()` handles circuit-breaking logic:

- **AUTH/BILLING**: Credential marked as "dead" — no further attempts
- **RATE_LIMIT**: Exponential backoff, `min(3600, 10 * (2^failure_count))` seconds
- **TIMEOUT/SERVER_ERROR**: Shorter backoff, `min(300, 5 * (2^failure_count))` seconds
- Delegates to `ProviderStateManager` for persistent across-restart tracking

```python
pm.record_failure(provider, classified.reason)
```

### Per-Session Skip-Known-Bad Cache

`ProviderStateManager` maintains a per-session cache that remembers failing `(provider, model)` pairs for 5 minutes:

```python
state_manager.mark_skip_candidate(session_id, "openai", "gpt-5.5")
state_manager.is_candidate_skipped(session_id, "openai", "gpt-5.5")  # True for 5 min
```

### Availability Checks

```python
pm.get_available_providers(preferred=["openai", "gemini"])
# Returns only non-cooldown providers, preferred ones first
```

---

## Provider State Manager

`ProviderStateManager` persists cooldown/failure state across restarts to a **JSON file** (`provider_state.json`):

```python
COOLDOWN_STEPS = [30.0, 60.0, 300.0]
MAX_COOLDOWN = 300.0
```

State is loaded on init and saved on every failure/success event. The persistent state tracks:

- **`disabled`**: Per-provider cooldown expiration timestamps
- **`failure_counts`**: Consecutive failure counts per provider
- **`last_fail_time`**: Timestamp of the most recent failure

```python
state_manager.record_failure(provider, reason)  # Saves to JSON
state_manager.record_success(provider)           # Clears cooldown
state_manager.is_disabled(provider)              # Check cooldown
state_manager.cooldown_remaining(provider)       # Seconds until available
```

---

## Credential Resolution

`resolve_api_key()` is the canonical key-resolution function, with three-tier fallback:

1. **Credential Store** — `CredentialStore.retrieve(provider, "api_key")`
2. **Environment Variable** — `PROVIDER_API_KEY` or profile-specific env var
3. **Empty string** — local providers (Ollama, LM Studio) may not need a key

```python
def resolve_api_key(provider: str, env_var: str | None = None) -> str | None:
    # 1. Try credential store
    # 2. Try environment variable
    # 3. Return None
```

`get_provider_env_var()` resolves the canonical env var name for any provider.

---

## Model ID Normalization

`model_aliases.py` provides provider-specific model name resolution:

```python
from siyarix.model_aliases import normalize_model_id, resolve_alias, list_aliases, register_alias

model = normalize_model_id("anthropic", "claude-opus-4.8")  # → "claude-opus-4-8"
model = normalize_model_id("gemini", "gemini-3-pro")        # → "gemini-3.1-pro-preview"
model = normalize_model_id("deepseek", "deepseek-v4")       # → "deepseek-v4-flash"
```

`ProviderManager.resolve_model_id()` wraps this for centralised access.

---

## Ollama Utilities

`ollama_utils.py` provides Ollama-specific helpers:

```python
from siyarix.providers.ollama_utils import ensure_ollama_running

# Launches Ollama in background if configured and not already running
ensure_ollama_running()
```

Auto-launch is triggered when `model_provider` is set to `"ollama"` or when `_start_ollama_on_launch` is enabled in settings.

---

## Provider Selection

```python
# Auto-detect the first available provider
provider, model = pm.select_provider(preferred=None)

# Use a specific provider
provider, model = pm.select_provider(preferred="openai")
```

### Capability-Based Filtering

```python
# Get all cloud providers supporting function calling
providers = pm.get_providers_by_capability(function_calling=True, local=False, free=False)

# Get only free-tier local providers
free_local = pm.get_providers_by_capability(free=True, local=True)

# Get vision-capable providers
vision_providers = pm.get_providers_by_capability(vision=True)
```

---

## Usage Tracking

`UsageTracker` (in `usage.py`) tracks token consumption and estimated cost per provider:

```python
from siyarix.providers import UsageTracker

tracker = UsageTracker()
tracker.record_call("openai", "gpt-5.5", input_tokens=500, output_tokens=150, cost_tier=CostTier.HIGH)
print(tracker.summary())
# LLM calls: 1 | Tokens: 500↑ 150↓ | Est. cost: $0.0086
```

Usage is persisted to JSON and can be loaded across sessions.

---

## Health Check

```bash
siyarix health
```

Checks all configured providers, reporting status (available/unavailable), latency, and error counts.

---

## Provider Statistics

```python
stats = pm.stats()
# {
#     "total_providers": 25,
#     "credentials": {"openai": 1, "anthropic": 0, ...},
#     "error_counts": {"openai": 3},
# }
```

---

## Related Modules

| Module | Path | Purpose |
|--------|------|---------|
| `ProviderManager` | `src/siyarix/providers/manager.py` | Singleton provider registry, failover, ensemble, stats |
| `ProviderStateManager` | `src/siyarix/providers/state.py` | Persistent cooldown state (JSON-based), skip-known-bad cache |
| `UsageTracker` | `src/siyarix/providers/usage.py` | Token usage and cost estimation |
| `ProviderProfile` / `ModelInfo` | `src/siyarix/providers/types.py` | Data models for provider metadata |
| `openai_compat.py` | `src/siyarix/chat/openai_compat.py` | Universal OpenAI-compatible adapter |
| `normalize_model_id` | `src/siyarix/model_aliases.py` | Model ID normalization and alias resolution |
| `ensure_ollama_running` | `src/siyarix/providers/ollama_utils.py` | Ollama background launcher |
| `profiles/` | `src/siyarix/providers/profiles/` | 25 individual provider profiles |
