# Finding Import Pipeline (Coming Soon)

The ability to import scan results from external security tools into a unified finding format is a planned feature for Siyarix. An initial `SecurityImporter` stub has been created, and the full import pipeline is under active development.

---

## Current Status

A `SecurityImporter` class exists as a stub in the codebase. It accepts a path and returns an empty result set. The actual parsing, format detection, and finding conversion logic has not yet been implemented.

```python
from siyarix.chat.stubs import SecurityImporter

importer = SecurityImporter()
result = importer.auto_import("scan.nessus")
# result.total_imported == 0  (stub - returns empty)
```

---

## Planned Capabilities

The following import formats are on the Siyarix roadmap:

| Format | File Extension | Source |
|--------|---------------|--------|
| Nessus | `.nessus` | Tenable Nessus XML |
| Burp Suite | `.xml` | Burp Suite project XML |
| Metasploit | `.json` | Metasploit DB export |
| STIX 2.x | `.json` | Threat intelligence feeds |
| OpenIOC | `.ioc` | Mandiant OpenIOC |
| Nikto | `.json` / `.xml` | Nikto web scanner |
| Nuclei | `.json` | ProjectDiscovery Nuclei |
| Trivy | `.json` | Aqua Security Trivy |

### Planned Pipeline

The full import pipeline will include:

- **Auto-detection** of format by file extension and content analysis
- **Unified finding format** with standardized severity, CVE, CWE, and CVSS fields
- **Deduplication** of findings from overlapping scans
- **Cross-source correlation** for enriched reporting

---

## Use Cases

- **Migration**: Import results from legacy tools into Siyarix
- **Consolidation**: Combine findings from multiple scanners into one report
- **Correlation**: Cross-reference external findings with native scans
- **Reporting**: Generate unified reports from mixed tool sources

---

## Stay Tuned

The finding import pipeline is actively being developed. Follow the project for updates on release timelines and new format support. The `SecurityImporter` will be fully documented here once the implementation is complete.
