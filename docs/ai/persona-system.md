# Persona System

Siyarix uses a persona system to shape the LLM's response style, focus area, and depth of expertise. Personas are dynamic prompt preambles prepended to the system prompt before each AI interaction. The system supports **10 security-domain personas** plus **3 special modes** for auto-selection, universal coverage, and neutral operation.

---

## Quick Reference

| Command | Effect |
|---------|--------|
| `/persona` | Show current persona |
| `/persona list` | List all available personas |
| `/persona <name>` | Switch to a named persona |
| `/persona auto` | Analyse request and auto-select best-fit persona |
| `/persona universal` | Full-spectrum cybersecurity professional |
| `/persona none` | No persona — neutral assistant |

The current persona is shown in the bottom status line:

```
Time: 12.3s | Mode: integrated | Persona: redteam | LLM: connected
```

---

## Available Personas

### Named Personas

| Name | Label | Focus Area | Prompt Theme |
|------|-------|------------|-------------|
| `redteam` | Red Team / Offensive Security | Adversary emulation, penetration testing, exploitation, C2 operations, evasion | PTES, OSTMM, TIBER-EU, EDR/ASLR bypass, Cobalt Strike, BloodHound, Chisel |
| `blueteam` | Blue Team / Defensive Security | Detection engineering, SOC operations, threat hunting, defence architecture, IR | Sigma/YARA/KQL/SPL, PICERL, NIST CSF, Velociraptor, osquery, Suricata, Zeek |
| `purpleteam` | Purple Team / Collaborative Security | Attack validation, detection coverage assessment, adversary emulation exercises | Atomic Red Team, Caldera, Stratus Red Team, ATT&CK mapping |
| `dfir` | DFIR / Digital Forensics & Incident Response | Forensic analysis, incident command, malware triage, timeline reconstruction | SAMS methodology, Volatility, Plaso, Autopsy, chain of custody |
| `threatintel` | Threat Intelligence / CTI | Threat research, TTP mapping, IoC extraction, threat actor profiling | Intelligence lifecycle, Diamond Model, MITRE ATT&CK, STIX, MISP/OpenCTI |
| `cloudsec` | Cloud Security / CloudSec | AWS/Azure/GCP security, IAM hardening, container security, Kubernetes | Prowler, ScoutSuite, kube-bench, trivy, zero trust, shared responsibility model |
| `appsec` | Application Security / AppSec | SAST/DAST, secure code review, threat modelling, SSDLC, supply chain security | STRIDE/PASTA, OWASP Top 10, Semgrep, CodeQL, SLSA, SBOM |
| `networksec` | Network Security / NetSec | Network architecture, firewall policy, segmentation, protocol analysis, zero trust | Zeek, Suricata, iptables, nftables, Wireshark, microsegmentation |
| `governance` | Governance / GRC | Compliance, policy, risk management, audit, regulatory frameworks | ISO 27001, SOC 2, PCI DSS v4.0, NIST CSF 2.0, FAIR, FedRAMP |
| `securityexplorer` | Security Explorer / Research | Vulnerability research, reverse engineering, tool discovery, CTF | Ghidra/IDA, AFL++, CVE research, adversarial ML, fuzzing |

### Special Modes

| Name | Behavior |
|------|----------|
| `auto` | Analyses the user's request and selects the best-fit persona automatically using LLM reasoning. Injects all persona descriptions into the prompt for context-aware selection. |
| `universal` | Full-spectrum cybersecurity professional — covers all domains in a single preamble with balanced red + blue + purple + DFIR + threat intel + cloud + appsec + network sec + governance + research expertise. |
| `none` | No persona preamble — uses `NEUTRAL_SYSTEM_PROMPT`, LLM decides its own voice. Minimal framing with platform context only. |

---

## How It Works

### Prompt Construction

When the LLM is called, the system prompt is built dynamically by `_build_system_prompt()` in `chat/engine.py`:

```python
def _build_system_prompt(self, compact: bool = False) -> str:
    persona_name = self._settings.get("persona") or "auto"

    if compact:
        if persona_name == "none":
            prompt = COMPACT_NEUTRAL
        else:
            p = get_persona(persona_name)
            label = p["label"] if p else "default"
            prompt = f"## Active Persona: {label}\n{COMPACT_PROMPT}"
    elif persona_name == "none":
        prompt = NEUTRAL_SYSTEM_PROMPT
    else:
        preamble = build_persona_prompt(persona_name)
        if preamble:
            prompt = preamble + "\n\n" + SIYARIX_SYSTEM_PROMPT
        else:
            prompt = SIYARIX_SYSTEM_PROMPT
    return prompt
```

**Logic Summary:**

| Persona Setting | First Call | Subsequent Calls (Compact) |
|----------------|-----------|---------------------------|
| `none` | `NEUTRAL_SYSTEM_PROMPT` only | `COMPACT_NEUTRAL` |
| Named persona (e.g. `redteam`) | Persona preamble + `SIYARIX_SYSTEM_PROMPT` | Persona label + `COMPACT_PROMPT` |
| `universal` | Universal preamble + `SIYARIX_SYSTEM_PROMPT` | Persona label + `COMPACT_PROMPT` |
| `auto` | Auto preamble (lists all personas) + `SIYARIX_SYSTEM_PROMPT` | Persona label + `COMPACT_PROMPT` |

### Persona Preamble Function

`build_persona_prompt()` in `personas.py` generates the preamble text:

```python
def build_persona_prompt(persona_name: str) -> str:
    p = get_persona(persona_name)
    if not p or persona_name == "none":
        return ""

    if persona_name == "auto":
        lines = ["## Active Persona: Auto (Smart Select)"]
        lines.append(
            "Analyse the user's request below and automatically adopt the persona "
            "that best fits the task. Available personas:"
        )
        for name, pp in PERSONAS.items():
            if name not in ("auto", "none"):
                lines.append(f"  - **{pp['label']}**: {pp['description']}")
        return "\n".join(lines)

    return f"## Active Persona: {p['label']}\n{p['prompt']}"
```

### System Prompts

Two core prompts are defined in `src/siyarix/chat/prompts.py`:

| Constant | Purpose | Size |
|----------|---------|------|
| `SIYARIX_SYSTEM_PROMPT` | Full-spectrum cybersecurity professional — includes platform context, operational framework (Intent/Scope/Depth/Risk), decision logic, output format (JSON), tool execution steps, shell quoting rules, output analysis instructions, and communication standards. | ~60 lines |
| `NEUTRAL_SYSTEM_PROMPT` | Minimal assistant — no persona framing. Includes approach determination, output format, tool execution steps, and communication standards. | ~30 lines |

### Compact Variants

| Variant | Purpose |
|---------|---------|
| `COMPACT_PROMPT` | Continue as active persona with abbreviated instructions. Used for subsequent LLM calls within the same interaction. |
| `COMPACT_NEUTRAL` | Continue as neutral Siyarix with minimal JSON output instruction. |

### Platform Context Injection

Both prompts dynamically inject platform context via `_platform_context()`:

```
## Platform Context
- OS: Windows 10 (AMD64)
- Shell: cmd /c
- WARNING: Windows system detected — commands must use Windows-compatible flags:
  * nmap: use -sT (TCP connect) instead of -sS (SYN scan); omit -O
  * Use forward slashes or escaped backslashes in paths
  * For DNS: use nslookup if dig is unavailable
  * Find binaries with `where` instead of `which`
```

### Custom Instructions & Workspace Context

The prompt builder also injects:

- **Custom Instructions** from `additional_system_message` setting
- **Workspace context files** (`AGENTS.md`, `SOUL.md`) when present in the current working directory
- **Execution environment** info (OS, shell type)

---

## Persona Data Model

Personas are defined in `src/siyarix/personas.py` as a dictionary with 13 entries (10 named + 3 special):

```python
PERSONAS: dict[str, dict[str, Any]] = {
    "red team": {
        "name": "red team",
        "label": "Red Team / Offensive Security",
        "description": "Adversary emulation, penetration testing, exploitation, C2 operations, evasion",
        "prompt": "You are an elite red-team operator...",
    },
    "blue team": { ... },
    "purple team": { ... },
    "dfir": { ... },
    "threat intelligence": { ... },
    "cloud security": { ... },
    "appsec": { ... },
    "network security": { ... },
    "governance": { ... },
    "security explorer": { ... },
    "universal": { ... },    # Special: all-in-one
    "auto": { ... },         # Special: smart select
    "none": { ... },         # Special: no persona
}
```

### Lookup Functions

```python
get_persona(name: str) -> dict | None             # Case-insensitive lookup with normalization
list_personas() -> list[dict]                      # All named personas (excludes auto, none, universal)
build_persona_prompt(name: str) -> str             # Generate the preamble text
```

Persona name matching supports fuzzy lookup via `_normalize_persona_key()` which strips spaces, hyphens, and underscores before comparison.

---

## Example Persona: Red Team

```python
"red team": {
    "name": "red team",
    "label": "Red Team / Offensive Security",
    "description": "Adversary emulation, penetration testing, exploitation, C2 operations, evasion",
    "prompt": (
        "You are an elite red-team operator who conducts realistic adversary emulation. You follow "
        "established methodologies — PTES, OSTMM, TIBER-EU — and operate across the full attack "
        "lifecycle: reconnaissance, weaponisation, delivery, exploitation, installation, C2, and "
        "exfiltration. You chain low-severity weaknesses into high-impact compromise paths, "
        "bypass modern defences (EDR, ASLR, CFG, AMSI), and maintain covert C2 with operational "
        "security. Your toolkit includes Cobalt Strike, Mythic, Sliver, BloodHound, Mimikatz, "
        "Rubeus, Certipy, Impacket, Chisel, and custom tooling. You think in assumptions of "
        "breach and test every control as if a nation-state adversary is the benchmark."
    ),
}
```

---

## Configuration

Set persona via `/persona` command during a session, or persist it in `settings.toml`:

```toml
persona = "redteam"
```

The setting is read at the start of each LLM interaction, so changes take effect immediately without restart.

---

## Integration with Interaction Modes

Personas are active in all LLM-dependent modes (`integrated`, `autonomous`) and in `hybrid` mode within `AgentCore`. In `registry` and `offline` modes, persona has no effect since no LLM is called — the heuristic planner operates independently of persona context.

---

## Related Modules

| Module | Path | Purpose |
|--------|------|---------|
| `PERSONAS` | `src/siyarix/personas.py` | Persona definitions (10 security personas + 3 special modes) |
| `build_persona_prompt` | `src/siyarix/personas.py:218` | Generates persona preamble text |
| `SIYARIX_SYSTEM_PROMPT` | `src/siyarix/chat/prompts.py:171` | Full-spectrum system prompt |
| `NEUTRAL_SYSTEM_PROMPT` | `src/siyarix/chat/prompts.py:233` | Minimal neutral system prompt |
| `COMPACT_PROMPT` | `src/siyarix/chat/prompts.py:263` | Compact variant for follow-up calls |
| `COMPACT_NEUTRAL` | `src/siyarix/chat/prompts.py:268` | Compact neutral variant |
| `_build_system_prompt` | `src/siyarix/chat/engine.py:550` | System prompt builder with persona integration |
