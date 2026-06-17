# 🛠️ The Onboarding Wizard

Siyarix is a high-performance, AI-native platform. To give you the best experience, we've built a comprehensive, 12-step interactive setup wizard. It’s designed to handle all the "boring stuff"—configuration, tool discovery, and security hardening—so you can start hacking (authorized, of course!) in minutes.

---

## 🚀 Quick Start

Ready to begin? Just type the command:

```bash
siyarix
```

If Siyarix detects that it hasn't been initialized yet, the wizard will launch automatically. You can also re-run it at any time to reconfigure your workspace:

```bash
siyarix init
siyarix init --force   # Re-run even if already configured
```

---

## 📝 The 12 Steps to Success

The wizard is divided into logical sections to ensure your environment is perfectly tuned.

| Step | What Happens? | Why It Matters |
|------|---------------|----------------|
| **0** | **Welcome & Ethics** | You'll see our ASCII logo and sign the ethical use pledge. We take safety seriously! |
| **1-2** | **System & Requirements** | Siyarix detects your OS, RAM, and Python version to ensure compatibility. |
| **3** | **Dependencies** | Automatically installs any missing core Python packages. |
| **4** | **Tool Discovery** | We scan your system for essential tools like `nmap`, `openssl`, and `dig`. |
| **5** | **Credential Vault** | Initializes your encrypted storage (AES-256-GCM) for API keys. |
| **6** | **AI Brain Selection** | Choose your AI provider (Cloud or Local). See below for details! |
| **7** | **Mode Configuration** | Choose between Autonomous, Integrated, or Registry-only execution. |
| **8** | **Persona Selection** | Pick a security "mindset" (Red Team, Blue Team, DFIR, etc.) for the AI. |
| **9** | **User Preferences** | Customize your theme, output format, and log levels. |
| **10** | **Network Diagnostics** | We test your internet and API connectivity to make sure everything is reachable. |
| **11** | **Finalize** | Siyarix creates your directory structure, sets up PATH, and you're ready to go! |

---

## 🧠 Step 6: Choosing Your AI Brain

This is the most important step. Siyarix gives you total flexibility:

### 🌟 Recommended (Smart Auto-Detect)
Siyarix analyzes your available RAM and suggests the perfect local model.
- **Light (<= 4GB RAM)**: Fast, lightweight models like `drana-infinity-3b`.
- **Balanced (4-8GB RAM)**: Solid all-rounders like `drana-infinity-7b`.
- **Capable (8-16GB RAM)**: High-performance reasoning with `mythos-sec:8b`.
- **High-End (16GB+ RAM)**: Maximum intelligence with `mythos-sec:24b`.

### ☁️ Cloud Providers
Connect to over 11 world-class cloud providers including **OpenAI**, **Anthropic**, **Google Gemini**, **Groq**, and **DeepSeek**.

### 🏠 Local Offline Engines
Run everything 100% locally using **Ollama**, **LM Studio**, **llama.cpp**, or **vLLM**.

---

## 📂 What Happens to My Files?

After the wizard finishes, Siyarix creates a dedicated workspace in your home directory (`~/.siyarix/`). This keeps your logs, cache, and configurations organized and private.

```text
~/.siyarix/
├── personas/           # Your AI personality definitions
├── memory/             # The in-memory knowledge graph
├── logs/audit/         # Your tamper-evident audit trail
├── cache/tool_outputs/ # Lightning-fast results from previous scans
├── templates/reports/  # Custom HTML/PDF report templates
└── settings.toml       # Your central configuration file
```

---

## 🤖 Unattended / CI Setup

If you're running Siyarix in a non-interactive environment (like a CI pipeline), the wizard won't start. Instead, you can configure everything via environment variables:

```bash
export MODEL_PROVIDER=openai
export OPENAI_API_KEY=sk-...
siyarix config set model_provider openai
siyarix auth set-key openai
```

---

## What's Next?

Now that your workspace is primed and ready, it's time to run your first command!

- 👉 **[First Run](first-run.md)** — Launch your first scan.
- 👉 **[CLI Commands Reference](../user/cli-commands.md)** — The complete command manual.
