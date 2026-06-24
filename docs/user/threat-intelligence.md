# Threat Intelligence

Siyarix integrates with real-world threat intelligence feeds for IP reputation lookups and CVE enrichment. The threat intelligence module provides direct access to AlienVault OTX and the National Vulnerability Database (NVD), with MITRE ATT&CK database integration coming soon.

---

## Active Integrations

### AlienVault OTX

IP address reputation lookups via the AlienVault Open Threat Exchange API:

```python
from siyarix.threat_intel import AlienVaultOTX

otx = AlienVaultOTX()
result = await otx.lookup_ip("8.8.8.8")
# Returns: pulse_count, reputation, source
```

Requires the `ALIENVAULT_API_KEY` environment variable.

### National Vulnerability Database (NVD)

CVE lookup and details from the NVD API 2.0:

```python
from siyarix.threat_intel import NVDDatabase

nvd = NVDDatabase()
result = await nvd.lookup_cve("CVE-2024-0001")
# Returns: description, base_score (CVSS v3.1), source
```

### ThreatIntelManager

A unified facade for querying both providers:

```python
from siyarix.threat_intel import ThreatIntelManager

manager = ThreatIntelManager()
result = await manager.analyze_target("8.8.8.8")   # Routes to OTX
result = await manager.analyze_target("CVE-2024-0001")  # Routes to NVD
```

---

## MITRE ATT&CK Integration (Coming Soon)

A `MITREAttackDB` class is stubbed and ready — the full database layer with tactic/technique mappings, CVE correlation, and finding enrichment is under construction:

```bash
# View MITRE ATT&CK coverage (available now)
siyarix security mitre-coverage

# Detailed MITRE technique analysis and CVE mapping — coming in a future release
```

The planned MITRE ATT&CK integration will provide:

- Complete tactic and technique database
- CVE-to-technique mapping
- Automatic finding enrichment with ATT&CK context
- Coverage analysis and gap identification

---

## Planned Enhancements

The following capabilities are on the Siyarix roadmap:

- **MISP feed ingestion**: Import MISP JSON events as structured threat intelligence
- **STIX 2.x support**: Import STIX indicators and observed data
- **OpenIOC import**: Import Mandiant OpenIOC format
- **Knowledge Graph integration**: Link threat indicators to findings as graph nodes
- **Built-in CVE mappings**: Automated CVE-to-MITRE technique correlation
- **ThreatIntel data model**: Standardized dataclass for unified threat representation

---

## Use Cases (Current)

- **IP reputation checking**: Quick lookups against AlienVault OTX during reconnaissance
- **CVE enrichment**: Fetch CVSS scores and descriptions during vulnerability assessment
- **Threat hunting context**: Combine OTX reputation data with scan findings

## Use Cases (Planned)

- **Threat hunting**: Match scan findings against known attacker TTPs
- **Risk scoring**: Elevate severity when findings match active threat campaigns
- **Reporting**: Include MITRE ATT&CK mapping in assessment reports
- **Coverage analysis**: Identify gaps in detection coverage
