# Siyarix Support

---

## Community Support Channels

| Channel | Purpose | Typical Response Time |
|---------|---------|-----------------------|
| **GitHub Issues** | Bug reports, feature requests, technical questions | 2-5 business days |
| **GitHub Discussions** | General questions, ideas, community help, show and tell | Community-driven |
| **Pull Requests** | Code and documentation contributions | Reviewed within 1 week |
| **Documentation** | Self-service help via project documentation | Available immediately |

---

## Before Requesting Support

To resolve issues quickly, please perform the following checks first:

1. **Read the documentation** -- Review the relevant documentation in the `docs/` directory and the [Documentation Map](docs/DOCS_MAP.md).

2. **Search existing issues** -- Your question or problem may have already been addressed. Search both open and closed issues on GitHub.

3. **Run diagnostics** -- Use the built-in diagnostic commands:

   ```bash
   siyarix health          # System health check
   siyarix shell doctor    # Shell environment diagnostics
   ```

4. **Review logs** -- Check the log directory for error details:

   ```bash
   # Default log location
   ~/.siyarix/logs/

   # Increase log verbosity
   export SIYARIX_LOG_LEVEL=DEBUG
   ```

5. **Verify configuration** -- Check your configuration file:

   ```bash
   cat ~/.siyarix/config.yaml
   siyarix config show
   ```

---

## Filing a Support Request

When opening a support issue on GitHub, please include the following information to help us diagnose the problem efficiently:

| Required Information | How to Obtain |
|---------------------|---------------|
| **Siyarix version** | `siyarix --version` or `pip show siyarix` |
| **Operating system** | `uname -a` (macOS/Linux) or `[System.Environment]::OSVersion` (Windows) |
| **Python version** | `python --version` |
| **Installation method** | pip, Homebrew, Docker, etc. |
| **AI providers configured** | List which providers you have configured |
| **What you were doing** | Describe your objective and the command(s) you used |
| **Actual behavior** | Include full error output (sanitize sensitive data) |
| **Expected behavior** | What you expected to happen |
| **Reproduction steps** | Minimal, complete steps to reproduce the issue |
| **Configuration (sanitized)** | Relevant portions of `~/.siyarix/config.yaml` (redact keys) |
| **Logs (sanitized)** | Relevant log entries from `~/.siyarix/logs/` |

---

## Security Issues

**Do not** file public GitHub issues for security vulnerabilities. Security reports must follow the coordinated disclosure process in [SECURITY.md](SECURITY.md).

---

## Commercial Support

For enterprise deployments requiring:

- Guaranteed response times (SLA)
- Custom integration and development
- Dedicated support engineer
- Priority bug fixes and feature requests
- On-premise deployment assistance
- Training and onboarding sessions

See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) or contact the project maintainers.

---

## Contributing

Found a bug you can fix? Have a feature idea you want to implement? See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow, coding standards, and pull request guidelines.

---

*Siyarix is maintained by a small team. We strive to respond to all support requests promptly and appreciate your patience and understanding.*

---

*SPDX-License-Identifier: AGPL-3.0-or-later*
