# 🧠 Responsible AI Usage Policy

Siyarix leverages cutting-edge Artificial Intelligence to plan tasks, reason through complex networks, and assist operators. Because AI is powerful but unpredictable, this policy governs how we handle AI responsibly within the platform.

## 🏗️ How We Use AI

Siyarix doesn't just use AI for chat. We deeply integrate it into the operational workflow:
1. **Task Planning:** Converting your natural language goals (e.g., "Find open databases on this subnet") into structured, tool-specific execution plans.
2. **Interactive Chat:** Providing a multi-turn, context-aware security assistant.
3. **Report Generation:** Summarizing raw vulnerabilities into polished, actionable executive reports.
4. **Tool Selection:** Dynamically recommending the best cybersecurity tool for a specific objective.

## 👁️ Human Oversight is Mandatory

AI is an assistant, not an autopilot. Siyarix is designed to keep the human in the loop:
- **The Permission Gate:** Every single command the AI attempts to run is strictly validated before execution.
- **User Confirmation:** If the AI suggests a destructive or highly sensitive command, execution halts, and the user must explicitly type `y` to approve it.
- **Full Audit Trail:** Every action, whether triggered by a human or an AI, is permanently logged.

> [!CAUTION]
> **The AI assists, but you are legally responsible for the commands you authorize.** Never blindly approve a command you do not fully understand.

## ⚠️ Known Limitations of AI

Current generation AI models are brilliant, but flawed. Be aware that the AI may:
- Generate incorrect, illogical, or incomplete execution plans.
- Suggest tools that are not actually installed on your system.
- Misinterpret your intent (especially if your prompt is vague).
- **Hallucinate** flags, arguments, or entirely fake IP addresses.

## 🕵️‍♂️ Provider Transparency

You should always know exactly *who* is processing your data. Siyarix logs the exact provider and model used for every operation:

```bash
siyarix audit-log
# Output will clearly show: Provider (e.g., Anthropic), Model (e.g., claude-3-5-sonnet), and Latency.
```

## 🛡️ Data Protection & Privacy

When you use cloud-based AI providers (like OpenAI or Gemini), data leaves your machine. We protect you with:
1. **Bidirectional Masking:** Our DLP engine intercepts and redacts IPs, hostnames, and credentials *before* they hit the internet.
2. **Session Scoping:** Masks are temporary and isolated to your current session.
3. **No Centralized Logging:** Siyarix itself does not harvest or centrally log your provider requests.
4. **The Ultimate Privacy:** If you are dealing with ultra-sensitive environments, Siyarix fully supports local, offline models (via Ollama or LM Studio) so your data never leaves your laptop.

## 🎛️ The Power of Choice

You are never locked into a single AI ecosystem. Siyarix allows you to:
- Dynamically switch AI providers mid-session.
- Configure an automatic failover chain (e.g., if OpenAI goes down, fallback to local Ollama).
- Disable AI entirely and rely purely on our deterministic, offline heuristic templates.

## 🚩 Reporting AI Misbehavior

If the AI suggests something harmful, hallucinates dangerously, or bypasses a safety rail:
- Please open an issue on our [GitHub Repository](https://github.com/mufthakherul/siyarix/issues).
- Provide the input prompt, the expected behavior, the actual output, and the provider used.
- **Do not include sensitive target data or actual credentials in your bug report!**

## ⚖️ Your Ethical Obligations

By using Siyarix's AI features, you agree to:
- **Never** use the AI to generate targeted phishing campaigns or social engineering lures.
- **Never** prompt the AI to write bespoke malware, ransomware, or destructive worms.
- **Never** use the AI to attack systems outside your authorized scope.
- Comply with the Terms of Service of the specific AI provider you are routing through.
