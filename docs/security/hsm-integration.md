# HSM Integration

Siyarix supports Hardware Security Modules (HSMs) for secure key storage and cryptographic operations. **Note**: This feature is currently under development. Basic HSM detection exists as a stub in `chat/stubs.py` (`HSMService`), but full integration is not yet complete.

## Status

| Type | Library | Status |
|------|---------|--------|
| YubiKey | `ykman` | Under development |
| PKCS#11 | `python-pkcs11` | Under development |
| TPM | (placeholder) | Under development |
| Software fallback | Built-in | Implemented (CredentialStore) |

## Planned Capabilities

When complete, HSM integration will support:

- Secure key storage for credential store encryption
- Hardware-backed cryptographic operations
- FIPS/HSM compliance for enterprise deployments
- Code signing for tool updates and reports
- YubiKey, PKCS#11, and TPM interfaces

## Current Workaround

For production deployments requiring hardware-backed security, the `CredentialStore` supports AWS KMS envelope encryption:

```bash
export SIYARIX_KMS_PROVIDER=aws
export AWS_KMS_KEY_ID=your-key-id
```

This provides hardware-backed key management through AWS CloudHSM without requiring local HSM hardware.

## Cross-Platform PKCS#11 Paths (Reference)

| Platform | Default path |
|----------|-------------|
| Windows | `C:\Windows\System32\opensc-pkcs11.dll` |
| macOS | `/usr/local/lib/opensc-pkcs11.so` |
| Linux | `/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so` |

## Use Cases (Planned)

- Enterprise deployments: Meet FIPS/HSM compliance requirements
- Key protection: Store API keys and signing keys in hardware
- Credential store backup: HSM as root of trust for credential encryption
- Code signing: Sign tool updates and reports with HSM-backed keys
