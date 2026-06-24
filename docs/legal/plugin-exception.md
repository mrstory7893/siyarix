# 🔌 The Siyarix Plugin Exception

Siyarix is proudly licensed under the strict **AGPL-3.0-or-later** license to ensure the core project remains open and free forever. However, we also want to foster a massive, vibrant ecosystem of third-party plugins. 

To make this possible, we grant a special **Plugin Exception** to the AGPL-3.0 terms.

> [!NOTE]
> **TL;DR:** Siyarix core must remain open-source (AGPL), but you can write plugins for Siyarix using *any* license you want—including closed-source, commercial, and proprietary licenses!

## 📜 The Official Exception Text

As a special exception to the GNU Affero General Public License version 3 or later (the "AGPL"), the copyright holders of Siyarix give you permission to convey a work that contains **unmodified Siyarix code** combined with **plugins** (as defined below) under terms of your choice, provided that you meet the following conditions:

### 1. What Defines a "Plugin"?

A "Plugin" is strictly defined as any file, script, or module that:
- Is loaded dynamically at runtime via the official Siyarix plugin loader (typically from `~/.siyarix/plugins/`).
- Does **not** contain, modify, or overwrite any original Siyarix source code.
- Communicates with Siyarix exclusively through documented, public APIs.

### 2. The Conditions

If you distribute a combined work (Siyarix + Your Plugin), you must adhere to these rules:
- **The Core Stays Open:** Siyarix itself (and any direct modifications you make to its core files) must remain under AGPL-3.0-or-later. If someone asks for the source code of the core engine, you must provide it.
- **Your Plugin is Yours:** Your plugins may be licensed under *any* terms of your choice.
- **No False Endorsement:** You must not misrepresent the origin of Siyarix, nor imply that the Siyarix project officially endorses your commercial plugin.
- **Include This Notice:** You must include a copy of this exact exception notice with your distribution.

### 3. Practical Scenarios: What is Allowed?

| Scenario | Is it Permitted? |
|----------|-----------|
| 🏢 Write a closed-source plugin for your internal red team. | **✅ Yes** |
| 💰 Sell a commercial, proprietary plugin under a paid license. | **✅ Yes** |
| 🌍 Distribute a free open-source plugin under MIT, Apache, or GPL. | **✅ Yes** |
| ❌ Modify the core `AgentEngine` in `src/siyarix/` and keep the code secret. | **❌ No** *(Core changes must be AGPL)* |
| 📦 Bundle a modified open-source Siyarix core with a closed-source proprietary plugin. | **✅ Yes** *(As long as you publish the core modifications)* |

### 4. No Additional Restrictions

This exception is designed to give you freedom with your plugins. It does **not** authorize you to impose any further restrictions on what users can do with the Siyarix core code itself under the AGPL.
