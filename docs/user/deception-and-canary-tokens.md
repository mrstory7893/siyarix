# Deception and Canary Tokens

Siyarix provides deception capabilities for detecting unauthorized access and gathering threat intelligence through honeypot detection, fake banners, and trapdoor credentials. A full `CanaryTokenManager` for deploying and managing canary tokens across multiple channels is planned for a future release.

---

## Honeypot Detection

The `HoneypotDetector` identifies known honeypots by matching service banners against 9 signatures.

### Detected Honeypots

| Signature | Type | Detection Pattern |
|-----------|------|------------------|
| Cowrie SSH | SSH honeypot | SSH banner contains "cowrie" |
| Dionaea | Malware honeypot | SIP banner contains "Dionaea" |
| Honeyd | Virtual honeypot | Banner says "Honeyd Virtual" |
| Glastopf | Web honeypot | Response contains "Glastopf" |
| T-Pot | Honeypot platform | Banner contains "T-Pot" |
| MHN | Modern Honeypot Network | Server identifies as MHN |
| Nmap honeypot | Scan detection | Nmap output pattern match |
| Canary tokens | Token detection | Known canary token patterns |
| Custom | User-defined | Configurable signatures |

### Usage

```bash
# Detect honeypots during scan
siyarix run "check if target is running honeypot services"
```

The detector checks SSH banners, HTTP responses, and service fingerprints.

---

## Fake Banners

The `FakeBannerGenerator` creates realistic decoy banners for defense:

```python
from siyarix.deception import FakeBannerGenerator

generator = FakeBannerGenerator()
ssh_banner = generator.generate_banner("ssh")     # "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3"
http_banner = generator.generate_banner("http")   # "Apache/2.4.41 (Ubuntu)"
ftp_banner = generator.generate_banner("ftp")     # "220 vsFTPd 3.0.3"
```

---

## Trapdoor Credentials

Trapdoor credentials are fake entries in the credential store that trigger alerts when used:

```python
from siyarix.deception import TrapdoorCredentialManager

manager = TrapdoorCredentialManager()
manager.add_trapdoor("admin", "fake_password_hash")
# If someone attempts authentication with these credentials, an alert fires
```

---

## Canary Token Management (Planned)

A comprehensive `CanaryTokenManager` is planned to provide:

| Token Type | Description | Deployment Target |
|------------|-------------|------------------|
| Web | URL that alerts on request | Web access logs |
| DNS | DNS name that alerts on resolution | DNS zone files |
| AWS Key | Fake AWS credential that alerts on use | Config files |
| Credential | Fake username/password pair | Credential stores |
| File | File that alerts on open | Filesystem |
| DB Record | Database record that alerts on query | Database tables |
| API Key | Fake API key that alerts on use | Config/code |

---

## Current Capabilities Summary

| Feature | Status |
|---------|--------|
| Honeypot detection (9 signatures) | Implemented |
| Fake banner generation | Implemented |
| Trapdoor credential management | Implemented |
| Canary token deployment and alerting | Planned |
| Token lifecycle management | Planned |
