# Siyarix Plugin Exception to AGPL-3.0-or-later

## Purpose

To foster a rich ecosystem of third-party plugins, Siyarix grants a special exception to the AGPL-3.0 terms for plugins, modules, and extensions that are not derivative works of Siyarix itself.

## Exception text

As a special exception to the GNU Affero General Public License version 3 or later (the "AGPL"), the copyright holders of Siyarix give you permission to convey a work that contains **unmodified Siyarix code** combined with **plugins** (as defined below) under terms of your choice, provided that:

### 1. Plugin definition

A "Plugin" is any file or module that:

- Is loaded dynamically at runtime via Siyarix's plugin loader (`~/.siyarix/plugins/`)
- Does **not** contain or constitute a modified version of any Siyarix source file
- Communicates with Siyarix only through documented public APIs

### 2. Conditions

When conveying a combined work under this exception:

- **Siyarix itself** (including any modifications you make to it) must remain under AGPL-3.0-or-later — you must provide its complete corresponding source code under the AGPL when required
- **Plugins** may be licensed under any terms of your choice, including proprietary licenses
- You must not misrepresent the origin of Siyarix or imply that Siyarix endorses your plugins
- You must include a copy of this exception notice with the combined work

### 3. What this means

| Scenario | Permitted? |
|----------|-----------|
| Write a proprietary plugin for internal use | Yes |
| Sell a commercial plugin under a paid license | Yes |
| Distribute an open-source plugin under MIT/Apache/GPL | Yes |
| Modify Siyarix core and distribute without source | No (core remains AGPL) |
| Bundle a modified Siyarix with a proprietary plugin | Yes, if core changes are shared under AGPL |

### 4. No additional restrictions

This exception does not authorize you to impose any further restrictions on recipients' exercise of rights granted under the AGPL for the Siyarix code itself.

---

*SPDX-License-Identifier: AGPL-3.0-or-later WITH Siyarix-plugin-exception*
