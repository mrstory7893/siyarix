# Troubleshooting

## Installation issues

### pip install fails

```bash
python --version                      # Ensure Python 3.11+
pip install --upgrade pip
pip install siyarix -v                # Verbose output
```

### Import errors

```bash
pip install "siyarix[all]"           # Ensure all deps installed
```

### siyarix: command not found

```bash
python -m siyarix --version           # Run via module
# which siyarix  (Linux/macOS)
# where siyarix  (Windows)
```

## Runtime issues

### "No AI provider available"

**Cause**: No API keys set and no local provider running.

**Fix**:
```bash
export OPENAI_API_KEY="sk-..."       # Set a cloud key
ollama pull llama3.1 && ollama serve # Or start a local provider
```

### Connection errors

**Cause**: Provider endpoint unreachable.

**Fix**:
```bash
siyarix config get proxy
siyarix config set proxy ""
```

### Permission denied

**Cause**: Insufficient permissions for network interfaces or raw sockets.

**Fix**: Run with elevated privileges (`sudo` on Linux/macOS, Administrator on Windows).

### Tool discovery fails

**Cause**: Security tools not found on PATH.

**Fix**:
```bash
sudo apt install nmap                # Debian/Ubuntu
brew install nmap                     # macOS
winget install nmap                   # Windows
siyarix scan --list-tools             # Verify tool registry
```

## Debug mode

```bash
export SIYARIX_DEBUG=1
siyarix ...
```

Or set persistent log level:

```bash
siyarix config set log_level debug
```

## Reset

```bash
siyarix config reset                  # Reset settings to defaults
rm -rf ~/.siyarix                     # Full reset (settings, history, cache)
```

## Known limitations

- Python 3.11+ required; older versions not supported
- Windows raw sockets require Administrator privileges
- Docker environments may lack certain native tools
- WSL2 network performance may differ from native Linux

## Reporting issues

1. Enable debug logging: `export SIYARIX_DEBUG=1`
2. Collect diagnostics: `siyarix health`
3. Open an issue at https://github.com/mufthakherul/siyarix/issues

Include Python version, OS, and full error output.
