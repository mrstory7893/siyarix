# Contributing to Siyarix

Thank you for considering contributing to Siyarix. Whether you are a security professional, Python developer, documentation writer, or student, your contributions help build the future of AI-native security orchestration.

Please take a moment to review this document before contributing.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Commit Conventions](#commit-conventions)
- [Reporting Issues](#reporting-issues)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Security Contributions](#security-contributions)
- [Plugins & Extensions](#plugins--extensions)
- [Documentation](#documentation)
- [AI-Generated Code Policy](#ai-generated-code-policy)
- [Licensing](#licensing)

---

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

---

## Getting Started

### Prerequisites

- **Python 3.11 or later**
- **Git** installed and configured
- **GitHub account** for forking and opening pull requests

### Development Setup

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/siyarix.git
cd siyarix

# Create a virtual environment
python -m venv .venv

# Activate the environment
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Install Siyarix in editable mode with all extras
pip install -e ".[all,cli,siem]"

# Install development tooling
pip install pytest ruff mypy pre-commit
```

### Verify Your Setup

```bash
pytest -q           # Run the test suite
ruff check .        # Lint checking
mypy src/siyarix/   # Static type checking
```

---

## Contribution Workflow

1. **Find an opportunity**: Browse [open issues](https://github.com/mufthakherul/siyarix/issues) or start a [discussion](https://github.com/mufthakherul/siyarix/discussions). For significant changes, discuss first before implementation.

2. **Create a branch**: Always work from a feature branch based on `main`.

   ```bash
   git checkout -b feat/my-feature
   ```

3. **Develop and test**: Write code, add tests, run the test suite, and lint your changes.

4. **Run quality checks**: Execute the full verification suite before committing.

   ```bash
   pytest
   ruff check .
   mypy src/siyarix/
   ```

5. **Commit your changes**: Use [Conventional Commits](#commit-conventions) and sign off with `git commit -s`.

6. **Open a pull request**: Push your branch and submit a PR against the `main` branch. Provide a clear description of the changes and their motivation.

---

## Coding Standards

- **Language**: Python 3.11+ with modern async/await patterns throughout
- **Formatting**: [Ruff](https://docs.astral.sh/ruff/) for formatting and linting. Run `ruff format .` before committing.
- **Type Safety**: Full type annotations required for all public APIs and encouraged for internal code
- **Documentation**: Google-style or NumPy-style docstrings for all public functions and classes
- **Testing**: Feature additions require tests. Bug fixes require regression tests. Target 75%+ coverage for new code.
- **Naming**: Use descriptive, professional naming. Avoid abbreviations and ambiguous terms.

---

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/) to maintain a readable and automated changelog.

**Format**: `<type>(<scope>): <description>`

| Type       | Usage                                    |
|------------|------------------------------------------|
| `feat`     | New feature                              |
| `fix`      | Bug fix                                  |
| `docs`     | Documentation only                        |
| `test`     | Adding or updating tests                 |
| `refactor` | Code improvement without behavior change |
| `security` | Security hardening or vulnerability fix  |
| `chore`    | Maintenance, dependencies, tooling       |
| `perf`     | Performance improvement                  |
| `ci`       | CI/CD configuration changes             |

All commits must be signed off (`git commit -s`) to certify agreement with the [Developer Certificate of Origin](https://developercertificate.org/).

---

## Reporting Issues

### Bug Reports

When filing a bug report, include:

- Clear, concise description of the issue
- Minimal, reproducible example or steps to reproduce
- Environment details: OS version, Python version, Siyarix version (`siyarix --version`)
- Relevant logs or error output (sanitize sensitive data)
- Expected vs actual behavior

### Feature Requests

Explain the problem you are trying to solve before describing the solution. Provide context on how the feature benefits security operators and how it fits within Siyarix's architecture.

### Security Vulnerabilities

**Do not** report security vulnerabilities via public GitHub issues. Follow the responsible disclosure process in [SECURITY.md](SECURITY.md).

---

## Pull Request Guidelines

Before submitting a pull request:

- [ ] All tests pass (`pytest -q`)
- [ ] Linting passes (`ruff check .`)
- [ ] Type checking passes (`mypy src/siyarix/`)
- [ ] New tests cover the changes
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages follow Conventional Commits format
- [ ] Commits are signed off
- [ ] PR description clearly states **what** changed and **why**

### Review Process

- Maintainers will review your PR within approximately 1 week
- Address review feedback through additional commits (no force-pushing)
- Once approved, a maintainer will merge your PR

---

## Security Contributions

Security researchers who discover vulnerabilities in Siyarix following the coordinated disclosure process in [SECURITY.md](SECURITY.md) are eligible for recognition in the project's security acknowledgments.

---

## Plugins & Extensions

Siyarix supports dynamic plugin discovery from `~/.siyarix/plugins/`. When contributing a plugin, parser, provider adapter, or tool handler:

1. Follow existing patterns in `src/siyarix/`
2. Register your module through the appropriate registry
3. Add external dependencies to `pyproject.toml` under the correct extras group
4. Include tests for your plugin

---

## Documentation

Documentation is maintained alongside code. When making changes:

- Update or add docstrings to public APIs
- Update relevant user-facing documentation
- Keep the MkDocs documentation site in sync with code changes

---

## AI-Generated Code Policy

We welcome the use of AI coding assistants (GitHub Copilot, ChatGPT, etc.) to accelerate development. By using AI-generated code in your contributions, you confirm that:

- You remain fully responsible for the code's correctness and quality
- You disclose significant AI assistance in your PR description
- AI-generated code meets the same quality, testing, and licensing standards as human-written code
- You have the right to contribute the code under AGPL-3.0-or-later

---

## Licensing

By contributing to Siyarix, you agree that your contributions will be licensed under the [GNU Affero General Public License v3.0 or later](LICENSE) (SPDX: `AGPL-3.0-or-later`). You retain copyright over your contributions and grant the project a perpetual, worldwide, non-exclusive, royalty-free license to use them under these terms.

---

*Thank you for being part of the Siyarix community.*
