# Security Workflows

Siyarix isn't just a wrapper around your CLI—it's a comprehensive operations center. This guide walks you through common, real-world security workflows, demonstrating how to use Siyarix to automate reconnaissance, assess vulnerabilities, hunt for threats, and more.

---

## 🔍 Network Reconnaissance

Don't waste time remembering nmap flags. Let Siyarix handle the syntax while you focus on the results.

```bash
# Get a quick lay of the land
siyarix scan quick 10.0.0.0/24

# Go deep with comprehensive service detection
siyarix scan full target.example.com

# Map out entire subdomains and related assets
siyarix discover example.com
```

---

## 🛡️ Vulnerability Assessment

Whether you prefer natural language or strict tool definitions, Siyarix adapts to your workflow.

```bash
# Just tell it what you want (Natural Language)
siyarix run "scan target.example.com for common vulnerabilities"

# Throw everything at the wall (Multi-tool scan)
siyarix scan --all 10.0.0.1

# Execute a highly structured, repeatable workflow pipeline
siyarix workflow run assessment.yml
```

---

## ⛓️ Exploitation Chains

For authorized red team engagements, Siyarix can map out entire operational chains.

```bash
# Plan a multi-phase campaign
siyarix exploit chain "recon -> scan -> enumerate -> exploit -> exfil"
```
*Note: The exploitation system dynamically resolves dependencies between phases and conditionally executes steps based on what it finds in previous stages.*

---

## 🚨 Incident Response

When the sirens go off, you need answers fast. 

```bash
# Fire up the interactive security dashboard
siyarix security dashboard

# Get a quick overview of active incidents
siyarix security incidents

# Instantly trigger an automated containment playbook
siyarix security playbooks run containment-playbook
```

---

## 🏹 Threat Hunting & Intelligence

Go on the offensive and look for indicators of compromise (IOCs) proactively.

```bash
# Let AI assist your hunt
siyarix security hunt "find indicators of compromise in the network"

# Map directly to MITRE ATT&CK
siyarix security mitre --technique T1078
# Siyarix will identify and execute the tools needed to investigate "Valid Accounts"
```

---

## 📋 Compliance & Governance

Stop dreading audits. Siyarix automates evidence collection and mapping against major frameworks.

```bash
# Run automated SOC 2 checks
siyarix run "check SOC 2 compliance on the infrastructure"
```
*The compliance engine supports SOC 2, ISO 27001, NIST, GDPR, HIPAA, and PCI-DSS, offering control-by-control validation and pass/fail reporting.*

---

## ☁️ Cloud & Infrastructure Security

Keep your cloud footprint tight and secure.

```bash
# Scan major cloud providers
siyarix scan --cloud aws
siyarix scan --cloud azure
siyarix scan --cloud gcp
```
*Siyarix checks for open S3 buckets, overly permissive security groups, unencrypted storage, and more.*

**Infrastructure as Code (IaC):**
```bash
# Catch misconfigurations before they are deployed
siyarix run "scan IaC templates for security issues"
```

---

## 🌐 Web Application Testing

Automate the OWASP Top 10 and beyond.

```bash
# Kick off a comprehensive web scan
siyarix run "scan web application at https://target.com for OWASP Top 10"
```
*Behind the scenes, Siyarix intelligentally chains tools like Nikto, Nuclei, WPScan, and ZAProxy based on the target fingerprint.*

---

## 🤖 Goal-Driven Autonomous Agents

For complex tasks, give Siyarix an objective and let it do the heavy lifting using an Observe-Reason-Act loop.

```bash
# Define the objective, step back, and let the agent work
siyarix agent "enumerate all services, find vulnerabilities, and generate a report"
```
*The agent will decompose the goal, assign tasks to sub-agents, execute them safely, and aggregate everything into a clean report.*

---

## 🔐 Unbreakable Audit Trails

Every single command Siyarix runs is logged using SHA-256 chaining, ensuring tamper-evident proof of your actions.

```bash
# Review the tamper-evident log for the current session
siyarix session-log
```
*These logs include the exact command executed, arguments, timestamps, and the AI rationale behind the action.*
