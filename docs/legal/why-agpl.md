# 🤔 Why the AGPL License?

Siyarix is a cybersecurity tool. Every single line of code in this repository can be used for defense, for academic research, or—in the wrong hands—for harm. 

We chose the **AGPL-3.0-or-later** license deliberately. We didn't pick it as a legal formality; we picked it as a structural safeguard. Here is why.

## 🛡️ Security Demands Openness

Security tools occupy a unique space in the open-source world. A bug in a text editor is annoying. A bug in a vulnerability scanner, an exploit module, or an AI-powered attack planner can cause catastrophic, real-world damage.

The AGPL ensures that:
- **Every fix stays open:** If a massive corporation finds and patches a critical bug in their customized fork of Siyarix, they are legally obligated to share that fix. The entire community benefits.
- **No hidden flaws:** Proprietary, closed-source forks hide their internals, making independent community audits impossible. AGPL guarantees that the source code is always exposed to the light.
- **Research continuity:** Academic and security research built on top of Siyarix can never be permanently locked behind a corporate paywall.

## ⚖️ Ethical Accountability

AGPL enforces our ethical stance by making evasion impossible.
- **Accountability:** Every modification is mathematically traceable. If a modified version of Siyarix is utilized in a cyber incident, the code must be available for forensic review. There is no "black box" defense.
- **License as Policy:** The AGPL's famous "network clause" means that anyone running Siyarix as a backend service (e.g., a "Red-Team-as-a-Service" SaaS platform) *must* make their core modifications available to their users. This outright prevents opaque, unaccountable security services from profiting off community work while hiding their methods.

> [!NOTE]
> The one exception to this is our [Plugin Exception](plugin-exception.md). Third-party plugins can use any license they want, allowing developers to monetize their specific workflows while the Siyarix core engine remains completely open.

## 🚫 A Deterrent to Weaponization

No piece of paper can physically stop a malicious actor. But the AGPL makes large-scale, corporate weaponization of Siyarix incredibly difficult:
- **You cannot hide modifications:** A commercial entity building enhanced, secret exploit capabilities into a Siyarix fork cannot keep those enhancements proprietary if they deploy them over a network. 
- **Ecosystem pressure:** Organizations using Siyarix for legitimate compliance work can inspect the entire codebase, verifying there are no hidden backdoors or unethical data-harvesting features.
- **No proprietary arms races:** AGPL prevents multiple vendors from competing over "who has the most dangerous closed-source Siyarix fork." 

## 🤝 Unbreakable Community Trust

Open-source security requires absolute trust. You need to trust that the code does exactly what it claims, that contributors are acting in good faith, and that the project won't suddenly be sold out to a single corporation.

**The AGPL makes Siyarix acquisition-proof.** 

A massive corporation cannot buy Siyarix, close the source code, and relicense it under a proprietary, expensive enterprise model. The community's work remains the community's work—forever. 

As an operator, you deserve to know:
- The code you audit today is exactly the code that runs tomorrow.
- There is no secret, proprietary "Enterprise Edition" hoarding all the good features.
- The Siyarix project answers solely to the community, not to a board of shareholders.

## 💡 The Bottom Line

We did not choose the AGPL by accident. We chose it because a cybersecurity tool without strong copyleft protection is a tool waiting to be taken, closed, and turned against the very community that built it. 

**Keep Siyarix open. Keep Siyarix safe.**
