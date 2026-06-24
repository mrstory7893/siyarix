# Operational Security

Siyarix provides operational security (OPSEC) controls for conducting assessments with reduced detectability. The `OPSECManager` and `StealthEngine` work together to provide layered evasion capabilities.

## OPSEC Controls

### TOR Routing

Route outbound connections through TOR:

```bash
siyarix config set proxy socks5://127.0.0.1:9050
```

All HTTP/HTTPS traffic from tools and AI provider calls routes through TOR.

### DNS over HTTPS

Prevent DNS leakage:

```bash
siyarix config set proxy dns+https://dns.cloudflare.com/dns-query
```

### Traffic Jitter

Random delays between requests to avoid pattern detection:

```toml
[jitter]
enabled = true
min_delay = 1.0
max_delay = 5.0
```

### User-Agent Rotation

```toml
client_profile = "desktop_chrome"
# Options: desktop_chrome, desktop_firefox, android_mobile, ios_safari
```

### Proxy Rotation

```toml
proxy_pool = "http://proxy1:8080,http://proxy2:8080,http://proxy3:8080"
```

Each connection picks a random proxy from the pool.

### Request Pacing

Controls the rate of outbound requests to avoid rate limiting and detection patterns:

```toml
[pacing]
requests_per_second = 2.0
burst_size = 5
```

### DNS Staggering

DNS queries are staggered across multiple resolvers to prevent DNS-based correlation:

```toml
[dns]
stagger = true
resolvers = ["1.1.1.1", "8.8.8.8", "9.9.9.9"]
```

## Stealth Engine (`stealth.py`)

The `StealthEngine` manages evasion levels and provides comprehensive operational security controls:

```python
class StealthConfig:
    level: str  # none, light, medium, heavy
    use_tor: bool
    use_proxy_chain: bool
    jitter_enabled: bool
    user_agent_rotation: bool
    dns_over_https: bool
```

### Evasion Levels

| Level | TOR | Jitter | Proxy rotation | UA rotation | DoH | Pacing | Stagger |
|-------|-----|--------|----------------|-------------|-----|--------|---------|
| none | No | No | No | No | No | No | No |
| light | No | Yes | No | Yes | Yes | Yes | No |
| medium | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| heavy | Yes | Yes | Yes | Yes | Yes | Yes | Yes (+ random delays 5-15s) |

### Decoy Traffic

The stealth engine can generate decoy traffic to mask actual assessment activities:

```toml
[decoy]
enabled = true
targets = ["https://example.com", "https://google.com"]
interval_seconds = 30
```

### Honeypot Detection

The engine can detect and avoid known honeypot networks and sandbox environments.

## Session Burning

After completing an assessment:

```bash
siyarix session-log --clear
```

Clears command history, knowledge graph, tool outputs, and session logs.

## Audit Logging

All actions are logged regardless of OPSEC settings. The audit log is tamper-evident (SHA-256 hash chain):

```bash
siyarix audit-log   # View audit trail
siyarix audit-log verify  # Verify chain integrity
```

## Operational Security Manager (`opsec.py`)

The `OPSECManager` provides:

- **Session isolation**: Each session operates in a sandboxed environment
- **Secure cleanup**: Temporary files and artifacts are wiped on session end
- **Memory scrubbing**: Sensitive data is cleared from memory
- **Cooldown tracking**: Tracks timing between operations to avoid pattern detection
- **Cover operations**: Can generate benign-looking traffic to mask assessment activities

## Red Team Simulation Safety

1. Define rules of engagement in a workflow file
2. Use persona `redteam` for offensive operations with appropriate constraints
3. Enable safe mode for initial reconnaissance
4. Press Ctrl+C for emergency stop (once cancels task, twice exits entirely)
5. Log all actions to the audit trail
6. Generate comprehensive report after completion
7. Burn session artifacts when done

## Recommended Assessment Configuration

```toml
stealth_mode = true
proxy_pool = "socks5://127.0.0.1:9050,socks5://127.0.0.1:9051"
client_profile = "desktop_chrome"
tls_verify = true
default_output_format = "json"
scan_timeout = 600
```
