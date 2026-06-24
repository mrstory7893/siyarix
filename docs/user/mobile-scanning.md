# Mobile Application Scanning (Under Active Development)

Siyarix's mobile application security scanning capability is currently under active development. A `MobileScanner` stub has been created, and the full implementation — including APK analysis, iOS IPA support, and dynamic analysis — is on the roadmap.

---

## Current Status

A `MobileScanner` class exists as a stub. It accepts a path and returns an empty result set. No actual APK analysis, permission scanning, or vulnerability detection has been implemented yet.

```python
from siyarix.chat.stubs import MobileScanner

scanner = MobileScanner()
result = scanner.scan_apk("app.apk")
# result == {}  (stub - returns empty)
```

---

## Planned Capabilities

The mobile scanner roadmap includes:

### Android APK Analysis

- **Dangerous permissions**: Detect over-privileged permission requests (location, camera, SMS, etc.)
- **Insecure flags**: `allowBackup`, `debuggable`, `usesCleartextTraffic`
- **Hardcoded secrets**: API keys, tokens, passwords in decompiled code
- **Manifest analysis**: Exported components, intent filters, and attack surface

### iOS IPA Analysis

- **Plist inspection**: Sensitive data in Info.plist
- **Binary analysis**: PIE, ARC, stack canary checks
- **Entitlement review**: Capability over-provisioning

### Dynamic Analysis (Roadmap)

- **Network traffic interception**: Detect cleartext and weak TLS
- **Runtime injection testing**: Attempt common manipulation techniques
- **Data storage analysis**: Insecure local storage detection

---

## Stay Tuned

The mobile scanner is being actively developed. Updates on platform support, check coverage, and release timelines will be shared as the implementation progresses.
