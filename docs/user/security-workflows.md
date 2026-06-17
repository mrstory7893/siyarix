# Security Workflows

Siyarix provides end-to-end automation for common security operations workflows — reconnaissance, vulnerability assessment, incident response, threat hunting, and compliance validation.

---

## Network Reconnaissance

```bash
# Quick scan for live hosts and open ports
siyarix scan quick 10.0.0.0/24

# Comprehensive scan with service detection
siyarix scan full target.example.com

# Asset and service discovery
siyarix discover example.com

# Natural language equivalent
siyarix run "enumerate all subdomains and live hosts for example.com"
```

---

## Vulnerability Assessment

```bash
# Natural language vulnerability scan
siyarix run "scan target.example.com for common vulnerabilities"

# Multi-tool comprehensive scan
siyarix scan --all 10.0.0.1

# Structured workflow pipeline
siyarix workflow run assessment.yml

# Agent-driven assessment
siyarix agent "find all vulnerabilities on the web server and categorize by severity"
```

---

## Web Application Testing

```bash
# OWASP Top 10 automated scan
siyarix run "scan web application at https://target.com for OWASP Top 10"

# Specialized web scan
siyarix scan web https://target.com
```

Siyarix chains tools (Nikto, Nuclei, WPScan, ZAP) based on target fingerprinting.

---

## Cloud Infrastructure Security

```bash
# Scan cloud providers
siyarix scan --cloud aws
siyarix scan --cloud all

# Natural language
siyarix run "check AWS for misconfigured S3 buckets and security groups"
```

Checks include: open S3 buckets, permissive security groups, unencrypted storage, disabled logging, and IAM over-privilege.

---

## Infrastructure as Code

```bash
# Scan IaC templates for misconfigurations
siyarix run "scan IaC templates for security issues"

# CI/CD pipeline gate
siyarix ci-gate
```

Supports Terraform, CloudFormation, Helm, and Dockerfile analysis via pattern matching. Enhanced scanning with full AST parsing is planned for a future release.

---

## Incident Response

```bash
# Security dashboard overview
siyarix security dashboard

# List active incidents
siyarix security incidents

# Execute containment playbook
siyarix security playbooks run incident-response

# Investigate with AI assistance
siyarix security hunt "find indicators of compromise in the network"
```

---

## Exploitation and Red Team Campaigns

For authorized engagements, Siyarix supports campaign management and exploitation chains:

```bash
# Plan a multi-phase campaign
siyarix run "plan campaign: recon -> scan -> enumerate -> exploit"

# Track campaign progress
# (via /campaign in REPL)
```

---

## Threat Hunting and Intelligence

```bash
# AI-assisted threat hunting
siyarix security hunt "find indicators of compromise in the network"

# MITRE ATT&CK mapping
siyarix security mitre --technique T1078

# Import threat intelligence feeds
siyarix run "import threat intel from stix_feed.json"
```

---

## Compliance and Governance

```bash
# Run SOC 2 compliance checks
siyarix run "check SOC 2 compliance on the infrastructure"

# Via command group
siyarix compliance run --framework soc-2

# Generate compliance report
siyarix report generate --format html --include compliance
```

Supported frameworks: SOC 2, ISO 27001, NIST 800-53, GDPR, HIPAA, PCI-DSS.

---

## Autonomous Agent Workflows

```bash
# Full autonomous multi-step objective
siyarix agent "enumerate all services, find vulnerabilities, generate a report"

# With explicit mode
siyarix agent "scan network" --mode autonomous
```

The agent decomposes objectives, assigns sub-tasks, executes them, and aggregates results.

---

## Audit Trail Verification

Every command is logged with SHA-256 hash chaining for tamper-evident proof:

```bash
# View session audit log
siyarix session-log

# Verify audit chain integrity
siyarix audit verify
```
