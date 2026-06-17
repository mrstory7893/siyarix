# Compliance Frameworks

Siyarix can assess targets against six industry compliance frameworks through automated probe execution and evidence collection.

---

## Supported Frameworks

| Framework | Full Name | Controls |
|-----------|-----------|----------|
| PCI-DSS | Payment Card Industry Data Security Standard | 4 |
| ISO 27001 | Information Security Management Standard | 4 |
| NIST 800-53 | Security and Privacy Controls | 4 |
| SOC 2 | Service Organization Control 2 | 4 |
| GDPR | General Data Protection Regulation | 4 |
| HIPAA | Health Insurance Portability and Accountability Act | 2 |

---

## Running Compliance Checks

```bash
# Check all frameworks
siyarix run "check compliance on the infrastructure"

# Check a specific framework
siyarix run "run SOC 2 compliance scan"

# Via command group
siyarix compliance run --framework soc-2
siyarix compliance run --framework all
```

---

## Control Examples by Framework

### PCI-DSS

| Control ID | Title | What is Checked |
|-----------|-------|-----------------|
| PCI-6.5 | Address common coding vulnerabilities | Security tools present for SAST/DAST |
| PCI-7.1 | Restrict access to need-to-know | IAM/logging processes verified |
| PCI-8.1 | Unique user IDs | Auth mechanisms in place |
| PCI-10.1 | Audit trails | Audit logging confirmed active |

### SOC 2

| Control ID | Title | What is Checked |
|-----------|-------|-----------------|
| SOC-CC1 | Control Environment | Governance processes detected |
| SOC-CC3 | Risk Assessment | Risk assessment tools found |
| SOC-CC6 | Logical and Physical Access | Access controls verified |
| SOC-CC7 | System Operations | Monitoring and response tools |

### GDPR

| Control ID | Title | What is Checked |
|-----------|-------|-----------------|
| GDPR-5 | Lawful Processing | Consent mechanisms verified |
| GDPR-17 | Right to Erasure | Data deletion processes exist |
| GDPR-32 | Security of Processing | Encryption and security tools in place |
| GDPR-33 | Breach Notification | Incident response plan confirmed |

---

## Automated Evidence Collection

Each compliance control is assessed via automated probes:

- **Tool detection**: Required security tools present on systems
- **Process verification**: Logging, monitoring, and response processes
- **Configuration checks**: Encryption, access controls, audit settings
- **Documentation scan**: Policy and procedure documents present

---

## Output

Each control result includes:

| Field | Description |
|-------|-------------|
| `control_id` | Framework-specific identifier |
| `title` | Human-readable name |
| `description` | What the control requires |
| `compliant` | PASS / FAIL |
| `evidence` | Supporting information |
| `remediation` | Steps to achieve compliance |
| `applicable` | Whether the control applies to the target |

### Example Output

```json
{
  "framework": "soc-2",
  "controls": [
    {
      "control_id": "SOC-CC6",
      "title": "Logical and Physical Access",
      "compliant": true,
      "evidence": "Access control mechanisms detected",
      "severity": "high"
    }
  ]
}
```

---

## Report Generation

```bash
# Generate a compliance-focused report
siyarix report generate --format html --include compliance

# Export as JSON for pipeline integration
siyarix report generate --format json
```
