# Deception Technology & Canary Tokens (Under Active Development)

Siyarix's deception technology capabilities are currently under active development. A `CanaryTokenManager` stub and related components have been created, and the full implementation — including honeypot detection, canary token deployment, and trapdoor credentials — is on the roadmap.

---

## Current Status

A `CanaryTokenManager` class exists as a stub in the codebase. It supports minimal operations (deploy, list, status, summary) but returns empty or placeholder results. The full deception technology suite has not yet been implemented.

```python
from siyarix.chat.stubs import CanaryTokenManager, CanaryTokenType

manager = CanaryTokenManager()
manager.deploy_to_target("webapp.example.com", [CanaryTokenType.WEB])
# Returns None (stub)

tokens = manager.list_tokens()
# Returns [] (stub)
```

---

## Planned Capabilities

### Canary Tokens

| Token Type | Description | Deployment Target |
|------------|-------------|-------------------|
| WEB | URL that alerts on request | Web access logs |
| DNS (planned) | DNS name that alerts on resolution | DNS zone files |
| AWS Key (planned) | Fake AWS credential that alerts on use | Config files |
| Credential (planned) | Fake username/password pair | Credential stores |
| File (planned) | File that alerts on open | Filesystem |
| DB Record (planned) | Database record that alerts on query | Database tables |
| API Key (planned) | Fake API key that alerts on use | Config/code |

### Honeypot Detection (Planned)

- Signature-based identification of known honeypots (Cowrie, Dionaea, Honeyd, Glastopf, T-Pot)
- SSH banner analysis
- HTTP response fingerprinting
- Service behavior pattern matching

### Fake Banners (Planned)

- Realistic decoy banners for SSH, HTTP, FTP, and other services
- Customizable service fingerprints
- Automated deployment to decoy systems

### Trapdoor Credentials (Planned)

- Fake credentials that trigger alerts on use
- Integration with credential store
- Alert routing and notification

---

## Stay Tuned

The deception technology suite is being actively developed. Updates on feature availability and release timelines will be shared as the implementation progresses.
