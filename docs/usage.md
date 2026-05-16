# Usage — Quick Reference

Common workflows:

- Scan a subnet quickly (default scan set):

```bash
siyarix scan 192.168.1.0/24
```

- Run an AI-assisted threat hunt over a target:

```bash
siyarix threat hunt --target example.com --ai
```

- Create and execute a hybrid plan (AI selects tools and order):

```bash
siyarix plan create --target my-app.com --ai-assist
siyarix plan run <PLAN_ID>
```

- Manage incidents:

```bash
siyarix incident list
siyarix incident show INC-001
siyarix incident resolve INC-001 --comment "False positive"
```

Output formats:
- `--format json` for CI pipelines
- `--format yaml` for human-readable machine-parseable reports

Examples and advanced usage are available in `docs/cli-reference.md`.
