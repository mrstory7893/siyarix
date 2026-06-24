# 🥷 Operational Security (OPSEC)

When conducting a red team assessment, flying under the radar is often just as important as finding the vulnerability. Siyarix features a robust `OPSECManager` and a `StealthEngine` that work together to provide layered evasion capabilities, keeping your operations quiet and untraceable.

> [!IMPORTANT]
> OPSEC features are designed for authorized red team engagements where stealth is explicitly requested by the client to test their SOC (Security Operations Center) response.

## 🛡️ Core OPSEC Controls

### 🧅 TOR Routing
Want to hide your origin IP? You can easily route all outbound Siyarix connections (including HTTP/HTTPS tool traffic and AI API calls) through the TOR network:

```bash
siyarix config set proxy socks5://127.0.0.1:9050
```

### 🔒 DNS over HTTPS (DoH)
Stop your ISP or local network administrators from snooping on your DNS queries:

```bash
siyarix config set proxy dns+https://dns.cloudflare.com/dns-query
```

### ⏱️ Traffic Jitter
If you send requests exactly every 1.0 seconds, blue teams will spot you immediately. Add random "jitter" to blend in with normal human web traffic:

```toml
[jitter]
enabled = true
min_delay = 1.0
max_delay = 5.0
```

### 🎭 User-Agent Rotation
Don't let a static user-agent string give you away. Siyarix can cycle through realistic browser profiles:

```toml
client_profile = "desktop_chrome"
# Other options: desktop_firefox, android_mobile, ios_safari
```

### 🔄 Proxy Rotation
Spread your traffic across a pool of IP addresses to defeat rate-limiting and IP-based blocking:

```toml
proxy_pool = "http://proxy1:8080,http://proxy2:8080,http://proxy3:8080"
```

### 🐌 Request Pacing
Control your speed. Slow and steady avoids triggering automated intrusion detection systems:

```toml
[pacing]
requests_per_second = 2.0
burst_size = 5
```

### 🔀 DNS Staggering
Prevent SOC analysts from correlating your activities by scattering your DNS lookups across multiple public resolvers:

```toml
[dns]
stagger = true
resolvers = ["1.1.1.1", "8.8.8.8", "9.9.9.9"]
```

## 👻 The Stealth Engine (`stealth.py`)

Configuring all those settings manually can be tedious. The Siyarix `StealthEngine` bundles them into easy-to-use "Evasion Levels".

| Level | TOR | Jitter | Proxy Rotation | UA Rotation | DoH | Pacing | Staggering |
|-------|-----|--------|----------------|-------------|-----|--------|------------|
| **None** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Light** | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Medium**| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Heavy** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ *(+ 5-15s random delays)* |

### 🎯 Decoy Traffic
The most advanced feature of the Stealth Engine is its ability to generate "noise." Siyarix can automatically browse benign websites in the background, burying your actual attack traffic inside a mountain of normal logs.

```toml
[decoy]
enabled = true
targets = ["https://example.com", "https://google.com"]
interval_seconds = 30
```

### 🍯 Honeypot Detection
The Stealth Engine actively monitors network responses to detect known honeypot signatures and sandbox environments, automatically aborting the scan if it realizes it's being tricked by the blue team.

## 🔥 Session Burning

When the engagement is over, leave no trace on your own machine. "Burning" the session permanently wipes your command history, the knowledge graph, tool outputs, and session logs.

```bash
siyarix session-log --clear
```

## 📜 Audit Logging Note

> [!WARNING]
> While Siyarix hides your traffic from the target, **it does not hide your actions from yourself**.
> To maintain accountability, all actions are still logged to the local tamper-evident audit log, regardless of your OPSEC settings.

```bash
siyarix audit-log         # View your local audit trail
siyarix audit-log verify  # Verify the cryptographic integrity of the log
```

## 🛠️ Recommended Configuration for Red Teams

If you are setting up for an authorized red team engagement, we recommend starting with this `siyarix.toml` configuration:

```toml
stealth_mode = true
proxy_pool = "socks5://127.0.0.1:9050,socks5://127.0.0.1:9051"
client_profile = "desktop_chrome"
tls_verify = true
default_output_format = "json"
scan_timeout = 600
```
