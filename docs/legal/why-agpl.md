# Why AGPL?

Siyarix is a cybersecurity tool. Every line of code can be used for defense, research, or harm. The **AGPL-3.0-or-later** license was chosen deliberately — not as a formality, but as a structural safeguard.

## Security

Security tools occupy a unique position in open source. A bug in a text editor is an inconvenience. A bug in a vulnerability scanner, exploit module, or AI-powered attack planner can cause real damage.

AGPL ensures that:

- **Every fix stays open** — If a vendor patches a critical bug in a modified Siyarix fork, they must share that fix. The community benefits from all improvements, not just upstream ones.
- **No hidden flaws** — Proprietary forks of security tools hide their internals, making it impossible for the community to audit them. AGPL guarantees source access.
- **Research continuity** — Security research built on Siyarix (e.g., a new exploitation technique or detection method) cannot be closed behind a paywall.

## Ethical issue

Security testing without guardrails is dangerous. AGPL reinforces the project's ethical stance in two ways:

**Accountability** — Every modification to Siyarix is traceable. If a modified version is used in an incident, the code is available for forensic review. There is no "black box" defense.

**License as policy** — The AGPL's network clause means that anyone running Siyarix as a service (a scanning platform, a bug bounty pipeline, a red-team-as-a-service offering) must make their modifications available to users. This prevents the creation of opaque, unaccountable security services built on community work.

The [Plugin Exception](plugin-exception.md) is the one carve-out: third-party plugins can use any license, because plugin authors should retain control over their own IP. The core remains protected.

## Deterrent to weaponization

No license can stop someone from using a tool for harm, but AGPL makes large-scale weaponized deployment harder in practice:

- **Cannot hide modifications** — A commercial entity building enhanced exploit capabilities into a Siyarix fork cannot keep those enhancements secret. If they deploy it as a service, users must get the source.
- **Ecosystem pressure** — Organizations that want to use Siyarix for legitimate security work can inspect the codebase and verify it has no hidden backdoors, data exfiltration, or unethical features.
- **No proprietary arms race** — AGPL prevents a scenario where multiple vendors compete on "who has the most dangerous closed-source Siyarix fork," driving an unchecked escalation of offensive capabilities outside community oversight.

## Community trust

Open source security requires trust — that the code does what it claims, that contributors act in good faith, and that the project cannot be captured by a single entity.

AGPL protects that trust by making the project **acquisition-proof**. A company cannot buy Siyarix and relicense it under a proprietary license. The project cannot be closed. The community's work remains the community's work, forever.

This matters especially for a cybersecurity tool where users need to know:

- The code they audit today is the code that runs
- No proprietary "enterprise edition" exists with hidden capabilities
- The project answers to the community, not to shareholders

## Bottom line

AGPL was not chosen by accident. It was chosen because a cybersecurity tool without strong copyleft protection is a tool that can be taken, closed, and turned against the community that built it.

---

*SPDX-License-Identifier: AGPL-3.0-or-later*
