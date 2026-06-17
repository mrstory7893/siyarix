# Contribution Guide

Thank you for contributing to Siyarix. Please read and follow these guidelines.

## Prerequisites

- Python 3.11+
- Git
- Familiarity with `asyncio`, type hints, and `pytest`
- GitHub account

## Development setup

```bash
git clone https://github.com/YOUR-USERNAME/siyarix.git
cd siyarix
python -m venv .venv
# source .venv/bin/activate   (Linux/macOS)
# .\.venv\Scripts\Activate.ps1  (Windows)
pip install -e ".[all,cli,siem,dev]"
```

## Workflow

1. Find or create an issue — discuss significant changes before starting
2. Create a branch: `git checkout -b feat/my-feature`
3. Make changes following code conventions
4. Run quality checks:
   ```bash
   pytest                          # Run tests (asyncio_mode=auto)
   ruff check src/ tests/          # Lint
   mypy src/siyarix/               # Type check (strict mode)
   ```
5. Commit with conventional commit message (DCO signed)
6. Push and open a pull request targeting `main`

## Code conventions

### Style

- PEP 8 as enforced by Ruff (line length: 100)
- Type hints on all public functions and methods
- `from __future__ import annotations` at top of every module
- Dataclasses for structured data
- `asyncio` for I/O-bound operations

### Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Classes | PascalCase | `ExecutionEngine` |
| Functions | snake_case | `get_health()` |
| Variables | snake_case | `scan_target` |
| Constants | UPPER_CASE | `DEFAULTS` |
| Private | Leading underscore | `_get_engine()` |

### Imports

Group in order separated by blank lines:
1. Standard library (`os`, `sys`, `asyncio`)
2. Third-party (`typer`, `rich`, `pydantic`)
3. Internal (`siyarix.config`, `.audit_log`)

### Error handling

- Raise `SiyarixException` subclasses for domain errors
- Use specific exception types; avoid bare `except:`
- Map exceptions to exit codes via `exit_code_for()`

## Commit conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `test` | Adding/updating tests |
| `refactor` | Code change (neither fix nor add) |
| `perf` | Performance improvement |
| `style` | Formatting, linting (no logic change) |
| `ci` | CI/CD configuration |
| `chore` | Build, dependencies, tooling |
| `security` | Security fix or hardening |

### DCO sign-off

Every commit must include a `Signed-off-by` trailer certifying the [Developer Certificate of Origin](https://developercertificate.org/):

```bash
git commit -s -m "type(scope): description"
```

## Pull request process

### Before opening

- All tests pass: `pytest -q`
- Lint clean: `ruff check src/ tests/`
- Type checks pass: `mypy src/siyarix/`
- New functionality includes tests
- Changed behavior includes documentation updates

### PR description

Include what changed, why (link to issue), how it was tested, and screenshots/logs for UI changes.

### Review

- At least one maintainer review required
- CI must pass (tests, lint, type check, security scan)
- Address review feedback promptly

## Adding a new AI provider

1. Create a provider profile in `src/siyarix/providers/profiles/`
2. Register in `ProviderManager`
3. Add API key environment variable to setup docs
4. Add tests in `tests/test_providers.py`
5. Update provider lists in documentation

## Adding a new tool parser

1. Create parser in `src/siyarix/parsers/` implementing `BaseParser` protocol
2. Register in `ParserRegistry`
3. Add test fixtures with sample tool output
4. Add tests in `tests/test_parsers/`

## Security contributions

- Follow [SECURITY.md](../../SECURITY.md) for vulnerability disclosure
- Standard PRs welcome for non-critical hardening
- Contributors credited in release notes (with permission)

## AI-generated code disclosure

- You are responsible for all submitted code regardless of authorship method
- Disclose AI assistance in PR description if majority was AI-generated
- AI-generated code must follow all project standards and include tests
- Maintainers may request modifications to AI-generated contributions

## Licensing

By contributing, you agree that your contributions are licensed under [AGPL-3.0-or-later](../../LICENSE). Every commit must be DCO-signed.

### Corporate contributors

- Confirm your employer's open-source contribution policy
- By signing off, you represent you have authorization to contribute under AGPL-3.0-or-later
- Do not submit proprietary code without explicit written permission
- Use your personal GitHub account

### Plugin exception

Third-party plugins in `~/.siyarix/plugins/` are not required to be AGPL-licensed. See [Plugin Exception](../legal/plugin-exception.md).

### SPDX header

Every source file must include:

```python
# SPDX-License-Identifier: AGPL-3.0-or-later
```
