# Tool Execution

AI-planned tools are executed through a structured pipeline that handles discovery, invocation, parsing, and error recovery.

## Tool lifecycle

```
Discovery → Selection → Invocation → Parsing → Finding Storage
```

## Tool discovery (`tool_registry.py`)

At startup, the `ToolRegistry` scans PATH for 100+ known security tools.

### Discovery process

```python
registry = ToolRegistry()
registry.scan_path()  # Scans PATH, checks versions
```

For each tool:

1. Check if binary exists on PATH
2. Run `--version` to verify and extract version
3. Record tool info: name, tags, platform, binary path

### Tag categories

| Category | Tools |
|----------|-------|
| Port scanning | nmap, masscan, unicornscan, rustscan, naabu, zmap, zgrab |
| Web scanning | nikto, nuclei, wpscan, zaproxy, whatweb, aquatone, gowitness |
| Exploitation | metasploit, impacket, sqlmap, searchsploit |
| Enumeration | gobuster, ffuf, subfinder, amass, assetfinder, findomain, httpx, katana, hakrawler, gospider, waybackurls, gau, wfuzz, dirb, dirsearch, feroxbuster, kiterunner, arjun, paramspider |
| Vulnerability | nuclei, trivy, grype, semgrep, nikto, wpscan, scoutsuite, prowler, lynis |
| Secrets | gitleaks, trufflehog, jwt_tool |
| Password | hydra, john, hashcat, hash_identifier |
| Network | bettercap, ettercap, aircrack-ng, responder, crackmapexec, bloodhound, certipy, kerbrute, enum4linux, smbclient, smbmap, evil-winrm, ldapsearch, impacket |
| DNS | dnsrecon, dnsenum, massdns, shuffledns, dnsx, subfinder, dig |
| TLS | sslscan, sslyze, testssl, ssh_audit |
| Cloud | cloud scanner (built-in AWS/Azure/GCP/K8s/Docker) |
| IoT | IoT scanner (built-in — firmware, serial) |
| Mobile | mobile scanner (built-in — APK analysis) |
| OSINT | theHarvester, shodan, whois, recon-ng |
| Forensics | volatility, yara, exiftool |

## Tool selection

The planner selects tools by tag:

```python
def select_tools(intent: str, target: str) -> list[str]:
    tags = INTENT_TO_TAGS[intent]
    tools = registry.find_by_tags(tags)
    return filter_by_platform(tools)
```

Multiple tools for the same capability are ordered by specificity.

## Command construction

Commands are built from tool metadata:

```python
tool = registry.get("nmap")
command = f"{tool.binary} {tool.default_args} {target}"
```

Tool-specific arguments can be overridden via `command_profiles.py`.

## Execution (`executor.py`)

```python
result = await safe_run_sync(
    command=command,
    timeout=config.get("scan_timeout", 300),
    env=env_vars,
)
```

Execution features:

- **Timeout**: Tool is killed after `scan_timeout` seconds
- **Environment injection**: API keys, proxy settings injected as env vars
- **PTY support**: Interactive tools via `pty_support.py`
- **Output capture**: stdout + stderr with size limits

## Output parsing (`parsers/`)

Each tool has a dedicated parser:

```python
# Example: NmapParser
parser = NmapParser()
findings = parser.parse(nmap_xml_output)
# Returns: [Finding(port=22, service="ssh"), ...]
```

Supported parsers (114+, partial list):

| Parser | Tool | Input format |
|--------|------|-------------|
| `nmap_parser.py` | Nmap | XML (`-oX`) |
| `masscan_parser.py` | Masscan | JSON (`-oL`) |
| `nuclei_parser.py` | Nuclei | JSON |
| `metasploit_parser.py` | Metasploit | JSON |
| `hydra_parser.py` | Hydra | Text |
| `ffuf_parser.py` | FFUF | JSON |
| `gobuster_parser.py` | Gobuster | Text |
| `nikto_parser.py` | Nikto | Text/JSON |
| `burpsuite_parser.py` | Burp Suite | XML |
| `sqlmap_parser.py` | SQLMap | Text |
| `zaproxy_parser.py` | ZAP | JSON/XML |
| `wpscan_parser.py` | WPScan | JSON |
| `shodan_parser.py` | Shodan | JSON |
| `subfinder_parser.py` | Subfinder | Text/JSON |
| `amass_parser.py` | Amass | Text/JSON |
| `impacket_parser.py` | Impacket | Text |
| `bettercap_parser.py` | Bettercap | JSON |
| `trivy_parser.py` | Trivy | JSON |
| `grype_parser.py` | Grype | JSON |
| `semgrep_parser.py` | Semgrep | JSON |
| `gitleaks_parser.py` | Gitleaks | JSON |
| `trufflehog_parser.py` | TruffleHog | JSON |
| ... and 90+ more | Various | Various formats |

## Finding extraction

Parsers produce structured `Finding` objects:

```python
@dataclass
class Finding:
    tool: str
    target: str
    port: int | None
    service: str | None
    vulnerability: str | None
    severity: str  # critical, high, medium, low, info
    evidence: str
    timestamp: str
```

Findings are:

1. Added to the knowledge graph
2. Stored in the offline store
3. Logged to the audit trail
4. Displayed to the user

## Error handling

### Tool not found

```python
# DynamicResolver tries these locations:
- PATH
- Common install directories (/usr/bin, /usr/local/bin)
- WSL paths (for Windows WSL2)
- Tool installer can auto-install
```

### Tool execution failure

```python
# Retry logic
if is_transient_error(exit_code, stderr):
    await asyncio.sleep(backoff_delay)
    result = await retry_execution()
else:
    log_error("Non-transient tool failure")
    mark_plan_step_failed()
```

### Parser failure

If a parser fails to match expected output format:

1. Raw output is logged for debugging
2. Finding extraction is skipped for that tool
3. The engine continues with remaining steps

## Tool auto-install

If a tool is not found but required:

```python
installer = ToolInstaller()
result = await installer.install("nmap")
# Tries: winget, choco, brew, apt, pip
```
