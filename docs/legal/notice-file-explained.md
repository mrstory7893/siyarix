# 📌 The NOTICE File Explained

If you look at the root of the Siyarix project, you'll see a file called `NOTICE`. This file isn't just metadata—it serves highly specific legal functions required by our AGPL-3.0 license. 

Here is a human-readable breakdown of what it is and why it matters.

## 🎯 What is the Purpose of the NOTICE?

The `NOTICE` file serves six critical functions:
1. **Project Identity:** Clearly states the project name, description, and homepage.
2. **Copyright Notice:** Identifies who legally holds the copyright.
3. **License Reference:** Links to the AGPL-3.0 license.
4. **Third-Party Attributions:** Gives credit to the amazing open-source libraries we rely on.
5. **AI Architecture:** Documents how our multi-provider AI system works.
6. **Disclaimer of Affiliation:** Clarifies that we are independent and not officially affiliated with companies like OpenAI or Google.

## 📄 NOTICE vs. LICENSE

It's easy to confuse these two files. Here is the difference:

| File | Purpose |
|------|---------|
| `LICENSE` | The unedited, exact legal text of the AGPL-3.0 directly from `gnu.org`. You cannot modify this file. |
| `NOTICE` | Project-specific legal notices required by AGPL-3.0 Section 5(a). |

> [!IMPORTANT]
> **AGPL-3.0 Section 5(a) requires that the `NOTICE` file be preserved in all downstream distributions.** If you fork Siyarix, do not delete the `NOTICE` file!

## 🔍 Breaking Down the NOTICE Sections

Here is what you will find inside the file:

### (a) Project Identity
Basic metadata, including the project name, a short description, the homepage URL, and the SPDX identifier (`AGPL-3.0-or-later`).

### (b) Copyright Notice
The legal declaration that the copyright is held by MD MUFTHAKHERUL ISLAM MIRAZ and the Siyarix contributors.

### (c) License Reference
A pointer to the full license text and an explanation of the "or-later" provision.

### (d) Third-Party Dependencies
A comprehensive table giving credit to our direct runtime dependencies (like `typer`, `rich`, `httpx`, and `pydantic`). We list the package name, version, license type, and SPDX identifier. Open source is built on the shoulders of giants!

### (e) AI Model Provider Architecture
A technical clarification of our provider-agnostic abstraction layer. It explains that Siyarix dynamically selects providers, handles failovers, and can run entirely offline—proving that we aren't hard-coupled to any single corporate API.

### (f) Disclaimer of Affiliation
We explicitly state that Siyarix is an independent project. We are **not** affiliated with, endorsed by, or sponsored by Google, OpenAI, Anthropic, Meta, or any other AI provider we interact with.

### (g) Project Homepage
Helpful links to our source code, issue tracker, and distribution channels.

## 🏷️ The SPDX Header

The file concludes with a machine-readable tag:
```text
SPDX-License-Identifier: AGPL-3.0-or-later
```

## ⚖️ Why Does This Matter?

Maintaining an accurate `NOTICE` file ensures:
1. **Legal Compliance:** We strictly follow AGPL-3.0 attribution rules.
2. **Respect:** We properly credit the developers whose libraries we use.
3. **Transparency:** We are clear about how our AI routing architecture works.
4. **Protection:** We prevent trademark confusion by disclaiming affiliations with tech giants.
