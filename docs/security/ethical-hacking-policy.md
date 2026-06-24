# ⚖️ Ethical Hacking Policy

Siyarix is a powerful cybersecurity orchestration platform. Because great power comes with great responsibility, this document clearly defines the boundaries for the ethical and legal use of our software. 

> [!CAUTION]
> **Please read this carefully.** By using Siyarix, you agree to adhere strictly to these guidelines.

## ✅ Authorized Use

Siyarix is designed for defense and authorized testing. You may **only** use Siyarix against systems that you either own or have explicit, written authorization to assess. 

**Acceptable use cases include:**
- **Your Own Infrastructure:** Systems, networks, and apps that belong to you.
- **Authorized Penetration Tests:** Client systems covered by a legally binding Statement of Work (SoW).
- **Bug Bounty Programs:** Programs where you are acting strictly within their published rules of engagement.
- **Educational Labs:** Isolated training platforms like HackTheBox or TryHackMe.
- **Security Operations:** Blue team assessments of enterprise systems you are responsible for securing.
- **Compliance Validation:** Automated checks against regulatory frameworks on authorized corporate networks.

## 🚫 Prohibited Use

Siyarix is **not** a tool for malicious actors. The following activities are strictly prohibited:

- ❌ Testing or scanning systems without explicit authorization.
- ❌ Launching Denial-of-Service (DoS) or Distributed Denial-of-Service (DDoS) attacks.
- ❌ Social engineering against non-consenting individuals.
- ❌ Exfiltrating data beyond the agreed-upon scope of an authorized test.
- ❌ Modifying or destroying data without express permission.
- ❌ Any activity that violates the Computer Fraud and Abuse Act (CFAA) or local equivalent laws.
- ❌ Nation-state offensive operations without a lawful international mandate.

> [!IMPORTANT]
> Siyarix must **never** be integrated with kinetic weapons systems or platforms.

## 📜 Rules of Engagement

When conducting an authorized assessment, follow these professional standards:

1. **Define the Scope:** Always document exactly what is "in scope" and "out of scope" before starting.
2. **Start Safe:** Use Safe Mode (`SIYARIX_SAFE_MODE=1`) for your initial reconnaissance.
3. **Stop on Detection:** If your actions trigger a client's IDS/IPS alerts, pause the operation and coordinate with the stakeholders.
4. **Protect Data:** Rely on our built-in DLP engine and encrypted storage to protect any sensitive data you collect.
5. **Least Privilege:** Always use the minimum access level and the quietest techniques necessary to prove the vulnerability.
6. **Document Everything:** Keep crystal-clear records of your authorization, methodology, and findings.

## 🌍 Legal Compliance

You are responsible for complying with the laws of your jurisdiction, as well as the jurisdiction of your targets:

- **United States:** Computer Fraud and Abuse Act (CFAA).
- **United Kingdom:** Computer Misuse Act 1990.
- **European Union:** General Data Protection Regulation (GDPR) and national cybercrime legislation.

## 🦺 Safe Mode

When in doubt, use Safe Mode. Safe Mode restricts Siyarix strictly to reconnaissance, ensuring you can't accidentally break anything.

```bash
export SIYARIX_SAFE_MODE=1
siyarix scan quick target.com
```

**In Safe Mode:**
- Exploitation tools are entirely disabled.
- Destructive commands are hard-blocked.
- The Permission Gate runs at maximum strictness.

## 🗣️ Responsible Disclosure

If you find a vulnerability using Siyarix:
- Do not exploit it further than necessary to prove it exists.
- Report it privately to the vendor and give them reasonable time to patch it.
- **Never** sell, trade, or publicly dump vulnerability data for personal gain or notoriety.

## 🚩 Reporting Misuse

If you discover someone using Siyarix for illegal or malicious purposes, please let us know immediately:
- Open a private security advisory on our [GitHub Security Page](https://github.com/mufthakherul/siyarix/security/advisories).
- Email the core maintainers (contact details are in `SECURITY.md`).

> [!NOTE]
> For the complete legal framework, please refer to our full Ethical Use Policy and Responsible AI Use Policy documents.
