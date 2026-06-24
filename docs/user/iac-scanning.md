# Infrastructure as Code Scanning (Under Active Development)

Siyarix's Infrastructure as Code (IaC) scanning capability is currently under active development. An `IaCScanner` stub has been created, and the full implementation — including Terraform, CloudFormation, Helm, and Dockerfile analysis — is on the roadmap.

---

## Current Status

An `IaCScanner` class exists as a stub. It accepts a path and returns an empty result set. No actual scanning, pattern matching, or AST parsing has been implemented yet.

```python
from siyarix.chat.stubs import IaCScanner

scanner = IaCScanner()
result = scanner.scan_path("infrastructure/terraform")
# result == {}  (stub - returns empty)
```

---

## Planned Capabilities

The IaC scanner roadmap includes:

| Format | Scope |
|--------|-------|
| Terraform | `.tf`, `.tfvars` — HCL analysis |
| CloudFormation | `.yaml`, `.json` — resource configuration checks |
| Helm | `values.yaml`, templates — Kubernetes security |
| Dockerfile | `Dockerfile` — container build best practices |
| Generic secrets | Pattern-based secret detection across all files |

### Planned Checks

The full scanner will detect:

- **Misconfigurations**: Public S3 buckets, open security groups, IAM over-privilege
- **Secrets exposure**: Hardcoded API keys, passwords, tokens, private keys
- **Compliance violations**: Encryption disabled, logging off, insecure defaults
- **Supply chain risks**: Unpinned container tags, unofficial base images

---

## CI/CD Integration (Planned)

```bash
# Future usage will include:
siyarix run "scan IaC templates for security issues"

# With dedicated CI gate
siyarix ci-gate
```

---

## Stay Tuned

The IaC scanner is being actively developed. Updates on supported formats, check coverage, and release timelines will be shared as the implementation progresses.
