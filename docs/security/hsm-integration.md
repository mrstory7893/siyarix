# 🔐 Hardware Security Module (HSM) Integration

Siyarix is built for enterprise environments, which means we understand the need for physical, hardware-backed security. While our HSM integration is currently **under active development**, this document outlines our roadmap and current workarounds for secure key storage and cryptographic operations.

> [!NOTE]
> **Developer Status:** Basic HSM detection currently exists as a stub in `chat/stubs.py` (look for `HSMService`), but the full integration is not yet complete.

## 📊 Current Integration Status

We are working to support the most common hardware security standards:

| Hardware Type | Target Library | Current Status |
|---------------|----------------|----------------|
| **YubiKey** | `ykman` | 🚧 Under development |
| **PKCS#11 Devices** | `python-pkcs11` | 🚧 Under development |
| **TPM Modules** | TBD | 🚧 Under development |
| **Software Fallback** | Built-in | ✅ Fully Implemented (`CredentialStore`) |

## 🚀 Planned Capabilities

Once fully released, Siyarix's HSM integration will allow you to:
- **Secure Key Storage:** Lock your `CredentialStore` master encryption keys inside physical hardware.
- **Hardware Cryptography:** Offload sensitive signing and decryption operations to the HSM.
- **FIPS Compliance:** Meet strict enterprise and government FIPS/HSM compliance requirements.
- **Code Signing:** Cryptographically sign your Siyarix tool updates and generated assessment reports.

## 🛠️ Current Workaround: AWS KMS

If you are running Siyarix in a production environment that requires hardware-backed security *today*, you don't have to wait. The `CredentialStore` natively supports **AWS KMS envelope encryption**.

This allows you to leverage AWS CloudHSM as your root of trust:

```bash
# Enable the KMS provider
export SIYARIX_KMS_PROVIDER=aws

# Point it to your specific key
export AWS_KMS_KEY_ID=your-aws-kms-key-id
```

> [!TIP]
> This approach keeps your local credentials encrypted with a data key, which is itself encrypted by the hardware-backed AWS KMS master key!

## 📂 Cross-Platform PKCS#11 Paths (Reference)

For developers looking to contribute to the PKCS#11 integration, here are the default driver paths across platforms:

| OS Platform | Default Driver Path |
|-------------|---------------------|
| **Windows** | `C:\Windows\System32\opensc-pkcs11.dll` |
| **macOS** | `/usr/local/lib/opensc-pkcs11.so` |
| **Linux** | `/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so` |

## 🎯 Enterprise Use Cases

Why are we building this?
1. **Compliance:** Many organizations cannot deploy security tools unless keys are stored in FIPS-validated hardware.
2. **Key Protection:** Ensures that even if the host machine running Siyarix is compromised, the API keys (like your expensive OpenAI or Anthropic tokens) cannot be extracted.
3. **Irrefutable Reports:** By signing security reports with a hardware key, clients can cryptographically verify that a Siyarix report hasn't been altered post-generation.
