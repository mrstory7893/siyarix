# Compliance Frameworks

Siyarix can assess targets against six industry compliance frameworks through automated probe execution and evidence collection. The compliance assessment framework is being actively developed — all check results currently return a `NOT_EVALUATED` status as the evaluation logic is being built out.

---

## Supported Frameworks

| Framework | Full Name | Controls |
|-----------|-----------|----------|
| PCI-DSS | Payment Card Industry Data Security Standard | 3 |
| ISO 27001 | Information Security Management Standard | 3 |
| NIST 800-53 | Security and Privacy Controls | 3 |
| SOC 2 | Service Organization Control 2 | 3 |
| GDPR | General Data Protection Regulation | 2 |
| HIPAA | Health Insurance Portability and Accountability Act | 2 |

---

## Running Compliance Checks

```bash
# Check a specific framework against a target
siyarix compliance run SOC2 10.0.0.1
siyarix compliance run PCI-DSS webapp.example.com
siyarix compliance run GDPR customer-db.internal
```

The `compliance run` command takes two positional arguments: the framework name and the target.

### Current Status

The compliance engine is under active development. Each `ComplianceCheck.run()` currently returns `NOT_EVALUATED` — the assessment probes and evidence collection logic are being implemented. Evidence data and target information are captured and stored for future evaluation.

---

## Control Examples by Framework

### PCI-DSS

| Control ID | Title |
|-----------|-------|
| Req-1.1 | Firewall configuration standards |
| Req-6.1 | Security patching process |
| Req-10.1 | Audit trail implementation |

### SOC 2

| Control ID | Title |
|-----------|-------|
| cc1.1 | Control environment |
| cc6.1 | Logical and physical access |
| cc6.2 | Access provisioning and deprovisioning |

### GDPR

| Control ID | Title |
|-----------|-------|
| Art. 32 | Security of processing |
| Art. 33 | Breach notification |

---

## Automated Evidence Collection

Each compliance control is assessed via automated probes. The evidence collection system stores assessment data in structured format for audit readiness:

- **Tool detection**: Required security tools present on systems
- **Process verification**: Logging, monitoring, and response processes
- **Configuration checks**: Encryption, access controls, audit settings
- **Documentation scan**: Policy and procedure documents present

---

## Output

Each control result includes:

| Field | Description |
|-------|-------------|
| `check_id` | Framework-specific identifier |
| `status` | Assessment result (currently `NOT_EVALUATED`) |
| `evidence_data` | Supporting information |
| `message` | Status description |

### Example Output

```json
{
  "framework": "SOC2",
  "target": "10.0.0.1",
  "results": [
    {
      "check_id": "cc1.1",
      "status": "NOT_EVALUATED",
      "message": "Stub check — not yet evaluated against live controls."
    }
  ]
}
```

---

## Report Generation

```bash
# Generate a compliance-focused report
siyarix report generate --format html --output compliance-report.html

# Export as JSON for pipeline integration
siyarix report generate --format json
```
