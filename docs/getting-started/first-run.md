# Your First Run with Siyarix

Welcome! You've installed Siyarix, and you're ready to get started. Before you dive into complex scans or autonomous agents, there's one important first step: **The Onboarding Wizard.**

---

## 🤝 The Mandatory First Step: Onboarding

Siyarix is a sophisticated platform that works best when it's tailored to your environment and tools. To ensure everything is set up perfectly, Siyarix requires a one-time onboarding process.

### How to Start It
Simply launch Siyarix from your terminal:

```bash
siyarix
```

If it's your very first time, the **Interactive Onboarding Wizard** will spring to life automatically.

### What to Expect
The wizard is a friendly, 12-step guided experience that handles:
- **Ethics Pledge**: A quick alignment on authorized, ethical security testing.
- **System Check**: Detecting your OS, RAM, and available tools.
- **Tool Discovery**: Siyarix scans your system to see which of the 100+ supported tools you already have installed.
- **AI Brain Selection**: Choosing your preferred AI provider (OpenAI, Gemini, Anthropic, or even a local offline model like Ollama).
- **Persona Setup**: Picking the "mindset" Siyarix should adopt (Red Team, Blue Team, etc.).

For a deep dive into each step, check out the [Full Onboarding Guide](onboarding.md).

---

## 🚀 Exploring After Setup

Once you've completed the wizard, you're in the driver's seat! Here's how to start exploring:

### 🩺 Run a Quick Health Check
Make sure everything is running smoothly after the setup:

```bash
siyarix health
```

### ⚡ Execute a Basic Scan
Let's see Siyarix in action by running a quick port scan against a domain:

```bash
siyarix scan quick example.com
```

### 💬 Enter the Chat REPL
Why stick to static commands? Launch the interactive, context-aware chat mode:

```bash
siyarix chat
# Or just run `siyarix` with no arguments after setup
```

---

## 🆘 Getting Help Anytime

If you're ever unsure about a command or option, just append `--help`:

```bash
siyarix --help
# Or get help for a specific command:
siyarix scan --help
```

---

## What's Next?

Now that your workspace is initialized and you've run your first commands, check out these resources to become a Siyarix pro:

- 👉 **[Interactive Chat](../user/interactive-chat.md)** — Master the AI-powered REPL.
- 👉 **[Security Workflows](../user/security-workflows.md)** — See how Siyarix handles real-world scenarios.
- 👉 **[CLI Commands Reference](../user/cli-commands.md)** — The complete command manual.
