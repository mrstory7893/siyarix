# 📜 AGPL-3.0-or-later License Guide

Siyarix is proudly distributed under the **GNU Affero General Public License v3.0 or later** (SPDX: `AGPL-3.0-or-later`). This guide translates the legalese into plain language to help you understand your rights and responsibilities.

## ⚖️ What Does AGPL-3.0 Mean?

The AGPL-3.0 is a robust, free software license published by the Free Software Foundation. It takes the strong protections of the standard GNU GPL v3 and adds a crucial network use provision.

### 🎉 Your Key Rights

Under this license, you are completely free to:
- **Use:** Run Siyarix for absolutely any purpose.
- **Study:** Dive into the source code and see exactly how it works.
- **Modify:** Tweak, change, and adapt the code to suit your specific needs.
- **Share:** Redistribute copies to anyone.
- **Improve:** Release your epic improvements back to the public!

### 🤝 Your Key Conditions

If you choose to distribute Siyarix (or a modified version of it) to others, you must play by these rules:
1. **Provide Source Code:** You must make the complete source code available.
2. **License under AGPL-3.0:** Your distribution must also be licensed under AGPL-3.0 or later.
3. **State Your Changes:** Clearly document any modifications you made to the original code.
4. **Include Notices:** Keep the original copyright and license notices intact.
5. **No Extra Restrictions:** Do not impose any additional legal restrictions on the recipients.

### 🌐 The "Network Use" Clause (Section 13)

> [!IMPORTANT]
> **The Golden Rule of AGPL:** If you run a modified version of Siyarix over a network and users interact with it remotely, you *must* make your modified source code available to those users.

This ensures that if a company deploys Siyarix as a backend "Security-as-a-Service," they cannot keep their improvements hidden from the community.

## 🤔 "AGPL-3.0-only" vs "AGPL-3.0-or-later"

| Variant | What it means |
|---------|---------|
| **AGPL-3.0-only** | You are bound strictly to version 3.0. If the FSF releases v4 tomorrow, you are stuck on v3. |
| **AGPL-3.0-or-later** | You are licensed under v3.0, but if the FSF releases a newer version, you can automatically adopt it! |

Siyarix uses the **"or later"** variant to future-proof the project.

## 🧑‍💻 What This Means For You

### Individual Users
You can use Siyarix for security testing, research, and learning without any restrictions. There are no license fees, no paywalls, and no registration forms. Go hack!

### Organizations
- **Internal Use:** You can modify and run Siyarix internally without ever releasing your source code.
- **Service Deployment:** If you offer Siyarix as a network service to outside clients, you must provide them access to your source code.
- **Distribution:** If you bundle Siyarix into a commercial product, your entire product must be AGPL-3.0 compatible.

### Developers
- **Contributing:** By opening a PR, your contributions are licensed under AGPL-3.0-or-later.
- **Modifications:** If you distribute your changes, you must share the source.
- **Bundling:** You can freely combine Siyarix with other AGPL-compatible software.

## 🔌 The Plugin Exception

We love developers building on top of Siyarix! Therefore, third-party plugins loaded dynamically via `~/.siyarix/plugins/` are **exempt** from AGPL requirements. They can use any license you want—even a proprietary, closed-source one. 

> [!NOTE]
> Check out the [Plugin Exception](plugin-exception.md) document for the exact legal details.

## 🧩 Compatibility Cheatsheet

**Compatible Licenses (Can be mixed with AGPL):**
- ✅ **GPL-3.0:** Perfect match.
- ✅ **Apache-2.0:** You can include Apache-2.0 code in AGPL projects.
- ✅ **MIT, BSD, ISC:** Permissive licenses play nicely with AGPL.
- ✅ **CC0:** Public domain is always free.

**Incompatible Licenses (Cannot be mixed):**
- ❌ **GPL-2.0:** AGPL-3.0 and GPL-2.0 do not mix.
- ❌ **Proprietary Licenses:** You cannot lock AGPL code inside a closed-source proprietary app.

## 📚 Further Reading
- The full, unabridged legal text is available in the `LICENSE` file.
- Read our [NOTICE File Explained](notice-file-explained.md) for attribution details.
- Review our [Disclaimer](disclaimer.md) regarding warranties.
