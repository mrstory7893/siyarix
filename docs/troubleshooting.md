# Troubleshooting

- If a subcommand fails with permission errors, ensure external tools (nmap, ffuf) are installed and in PATH.
- For AI integrations, verify API keys in `~/.siyarix/config.yaml` and ensure network access.
- For tests failing locally, run `pytest -k <testname> -vv` and inspect captured logs.
