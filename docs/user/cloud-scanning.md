# Cloud Security Scanning

Siyarix includes multi-cloud security scanning for AWS, Azure, GCP, Kubernetes, and Docker configurations. Each provider SDK is queried only when the respective cloud credentials are available.

---

## Supported Providers

| Provider | Checks | Requirements |
|----------|--------|-------------|
| AWS | 5 | `boto3`, AWS credentials configured |
| Azure | 3 | `azure-identity`, Azure credentials |
| GCP | 3 | `google-cloud-resource-manager`, GCP credentials |
| Kubernetes | 3 | `kubernetes` Python package, kubeconfig |
| Docker | 3 | `docker` Python package, Docker daemon |

---

## Scanning

```bash
# Scan all configured cloud providers
siyarix scan --cloud all

# Scan a specific provider
siyarix scan --cloud aws
siyarix scan --cloud azure
siyarix scan --cloud gcp
siyarix scan --cloud kubernetes
siyarix scan --cloud docker

# Natural language
siyarix run "check AWS for security misconfigurations"
```

---

## AWS Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| S3_PUBLIC_ACCESS | S3 bucket allows public read access | HIGH |
| IAM_OVERLY_PERMISSIVE | IAM policy grants `*:*` to all principals | CRITICAL |
| SECURITY_GROUP_OPEN | Security group allows SSH from 0.0.0.0/0 | HIGH |
| UNENCRYPTED_EBS | EBS volume does not have encryption enabled | MEDIUM |
| CLOUDTRAIL_DISABLED | AWS CloudTrail is not enabled | HIGH |

## Azure Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| NSG_OPEN | Network Security Group allows RDP/SSH from any source | HIGH |
| BLOB_PUBLIC_ACCESS | Blob storage container allows anonymous access | HIGH |
| RBAC_OVERPRIVILEGED | RBAC role assignment is overly permissive | MEDIUM |

## GCP Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| BUCKET_PUBLIC_ACCESS | GCS bucket allows public access | HIGH |
| FIREWALL_OPEN | GCP firewall rule allows 0.0.0.0/0 on management ports | HIGH |
| IAM_PRIMITIVE_ROLE | IAM primitive role (owner/editor/viewer) assigned | MEDIUM |

## Kubernetes Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| POD_ROOT_USER | Container runs as root | HIGH |
| PRIVILEGE_ESCALATION | Privilege escalation allowed | HIGH |
| HOST_NETWORK | Pod uses host network namespace | MEDIUM |

## Docker Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| ROOT_USER | Container runs as root | HIGH |
| SENSITIVE_ENV | Environment variable exposes sensitive data | MEDIUM |
| NO_HEALTHCHECK | Container missing health check | LOW |

---

## Credential Configuration

Credentials are resolved from the following sources (in order):

1. **Environment variables**: `AWS_ACCESS_KEY_ID`, `AZURE_CLIENT_ID`, `GOOGLE_APPLICATION_CREDENTIALS`, etc.
2. **Default credential chains**: Each SDK's standard resolution (instance profiles, `~/.aws/credentials`, etc.)
3. **Credential store**: `siyarix auth set-key <provider>`

---

## Output

Results include check ID, title, severity, description, and remediation guidance. Use the `--output` flag for structured formats:

```bash
siyarix scan --cloud aws --output json
```

---

## Planned Enhancements

The current cloud scanner performs provider-specific API checks. A comprehensive `CloudScanner` with deep multi-account support, cross-provider correlation, and automated remediation is planned for a future release.
