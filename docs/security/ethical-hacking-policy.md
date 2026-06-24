# Ethical Hacking Policy

Siyarix is a cybersecurity operations platform. This document defines the boundaries for ethical and legal use. Please read it carefully before using the platform.

## Authorized Use

Siyarix may only be used against systems you own or have explicit written authorization to test:

- **Your own infrastructure**: Systems, networks, and applications you own
- **Authorized penetration tests**: Systems covered by a signed Statement of Work (SoW)
- **Bug bounty programs**: Programs with explicit rules of engagement
- **CTF competitions**: Authorized capture-the-flag environments
- **Educational labs**: Isolated training environments (HackTheBox, TryHackMe, etc.)
- **Research**: Systems with IRB or organizational approval
- **Enterprise security operations**: Security assessments of systems you are responsible for
- **Supply chain security**: Software composition analysis of systems you own or operate
- **Compliance validation**: Automated compliance checks against regulatory frameworks on authorized systems

## Prohibited Use

The following are strictly prohibited:

- Testing systems without authorization
- Denial-of-service attacks against any system
- Social engineering against non-consenting individuals
- Data exfiltration beyond authorized scope
- Modification or destruction of data without explicit permission
- Any illegal activity
- Violation of the Computer Fraud and Abuse Act (CFAA) or equivalent laws
- Nation-state offensive cyber operations without lawful international mandate
- Development of cyber weapons targeting civilian infrastructure
- Integration with weapons systems or platforms

## Rules of Engagement

1. **Define scope**: Document what is in and out of scope before starting
2. **Set boundaries**: Use safe mode (`SIYARIX_SAFE_MODE=1`) for initial reconnaissance
3. **Stop on detection**: If you trigger IDS/IPS alerts, stop and coordinate with the client
4. **Protect data**: Use DLP masking and encrypted storage for any data collected
5. **Report responsibly**: Share findings only with authorized stakeholders
6. **Least privilege**: Use the minimum access level and techniques necessary
7. **Documentation**: Maintain clear records of authorization, scope, methodology, and findings

## Legal Compliance

Users must comply with all applicable laws:

- **United States**: CFAA, GDPR (if processing EU data)
- **United Kingdom**: Computer Misuse Act 1990
- **EU**: GDPR, national cybercrime laws
- **Other jurisdictions**: Local computer misuse and data protection laws

## Safe Mode

Restricts Siyarix to reconnaissance-only operations:

```bash
export SIYARIX_SAFE_MODE=1
siyarix scan quick target
```

In safe mode:
- No exploitation tools are available
- No destructive commands can be executed
- Only scanning and enumeration tools are permitted
- Permission gate enforces maximum strictness

## Responsible Disclosure

- Do not exploit vulnerabilities beyond what is necessary to confirm existence
- Do not disclose publicly without giving the vendor reasonable time to patch
- Do not sell or trade vulnerability information without authorization
- Do not use vulnerabilities for personal gain

## Reporting Misuse

If you discover misuse of Siyarix:

- Open a security advisory at https://github.com/mufthakherul/siyarix/security/advisories
- Email the maintainers (details in SECURITY.md)
- Include details of the misuse

## Full Policy

See the Ethical Use Policy and Responsible AI Use Policy for the complete ethical use framework, including detailed sections on prohibited activities, authorized use requirements, compliance, and enforcement.
