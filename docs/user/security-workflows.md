# Security Workflows

Siyarix provides end-to-end automation for common security operations workflows — reconnaissance, vulnerability assessment, incident response, threat hunting, and compliance validation.

---

## Network Reconnaissance

```bash
# Quick scan for live hosts and open ports (top 100 ports)
siyarix scan-quick 10.0.0.0/24

# Comprehensive scan with service detection (all ports)
siyarix scan-full target.example.com

# Deep multi-pass scan (discovery → fingerprint → vuln → enumeration)
siyarix scan-deep target.example.com

# Asset and service discovery
siyarix discover example.com

# Deep discovery with OS, service, and vulnerability enumeration
siyarix discover example.com --deep

# Natural language equivalent
siyarix run "enumerate all subdomains and live hosts for example.com"

# With offline/registry mode (no AI provider required)
siyarix scan 10.0.0.0/24 --mode offline
```

---

## Vulnerability Assessment

```bash
# Natural language vulnerability scan
siyarix run "scan target.example.com for common vulnerabilities"

# Multi-tool web application scan
siyarix scan-web https://target.com

# Agent-driven assessment
siyarix agent "find all vulnerabilities on the web server and categorize by severity"

# Deep vulnerability scan
siyarix scan-deep 10.0.0.1 --save
```

---

## Web Application Testing

```bash
# OWASP Top 10 automated scan
siyarix run "scan web application at https://target.com for OWASP Top 10"

# Specialized web scan preset
siyarix scan-web https://target.com
```

Siyarix chains tools (Nikto, Nuclei, WPScan, WhatWeb) based on target fingerprinting.

---

## Incident Response

```bash
# Security dashboard overview
siyarix security dashboard

# List active incidents
siyarix security incidents

# Show incident details
siyarix security incident INC-001

# Create a new incident
siyarix security incident-create --title "SQLi on login" --description "Blind SQL injection detected" --category intrusion --severity high

# List incident response playbooks
siyarix security playbooks

# Execute a YAML playbook
siyarix playbook run response-playbook.yml
```

---

## Exploitation and Red Team Campaigns

For authorized engagements, Siyarix supports campaign management:

```bash
# Plan a multi-phase campaign
siyarix run "plan campaign: recon -> scan -> enumerate -> exploit"

# Track campaign progress via /campaign in REPL
```

---

## Threat Hunting and Intelligence

```bash
# Execute a predefined threat hunt query
siyarix security hunt q_ps_exec

# List available hunt queries
siyarix security queries

# List hunt queries filtered by MITRE tactic
siyarix security queries --mitre-tactic execution

# View MITRE ATT&CK coverage
siyarix security mitre-coverage
```

---

## Compliance and Governance

```bash
# Run SOC 2 compliance checks against a target
siyarix compliance run SOC2 10.0.0.1

# Generate a compliance-focused report
siyarix report generate --format html --output compliance-report.html
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
# View audit logs
siyarix audit logs

# Verify audit chain integrity
siyarix audit verify

# Generate compliance audit report
siyarix audit report soc2 -o audit-report.md
```
