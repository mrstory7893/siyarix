#!/usr/bin/env bash
# =============================================================================
# Siyarix Installer for Android/Termux
#   Run: curl -fsSL https://siyarix.dev/install_android.sh | bash
#   Or:  bash install_android.sh
# =============================================================================
set -euo pipefail

SIYARIX_VERSION="${SIYARIX_VERSION:-3.0.0}"
DRY_RUN="${SIYARIX_DRY_RUN:-0}"
TERMUX_HOME="${HOME:-/data/data/com.termux/files/home}"
TERMUX_PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"

banner() {
  echo ""
  echo "   ███████╗██╗██╗   ██╗ █████╗ ██████╗ ██╗██╗  ██╗"
  echo "   ██╔════╝██╚██╗ ██╔╝██╔══██╗██╔══██╗██║╚██╗██╔╝"
  echo "   ███████╗██║╚████╔╝ ███████║██████╔╝██║ ╚███╔╝"
  echo "   ╚════██║██║ ╚██╔╝  ██╔══██║██╔══██╗██║ ██╔██╗"
  echo "   ███████║██║  ██║   ██║  ██║██║  ██║██║██╔╝ ██╗"
  echo "   ╚══════╝╚═╝  ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
  echo "   AI Cybersecurity Orchestration Agent v${SIYARIX_VERSION}"
  echo "   Android/Termux Installer"
  echo ""
}

info()  { echo -e "\033[34m==>\033[0m $*"; }
ok()    { echo -e "\033[32m  ✓\033[0m $*"; }
warn()  { echo -e "\033[33m  !\033[0m $*"; }
err()   { echo -e "\033[31m  ✗\033[0m $*" >&2; }

run() {
  if [ "$DRY_RUN" = "1" ]; then
    info "[DRY-RUN] Would run: $*"
    return 0
  fi
  "$@"
}

detect_termux() {
  if [ -n "${TERMUX_VERSION:-}" ]; then
    return 0
  fi
  if [ -d "/data/data/com.termux" ]; then
    return 0
  fi
  return 1
}

check_python() {
  for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
      local ver
      ver=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
      local maj="${ver%.*}"
      local min="${ver#*.}"
      if [ "$maj" -ge 3 ] && [ "$min" -ge 11 ]; then
        PYTHON="$cmd"
        return 0
      fi
    fi
  done
  return 1
}

install_termux_deps() {
  info "Installing Termux build dependencies..."
  run pkg update -y
  run pkg install -y python clang make libffi openssl binutils termux-elf-cleaner
}

setup_termux_storage() {
  if [ ! -d "${HOME}/storage" ]; then
    info "Requesting Termux storage permissions..."
    warn "Please grant storage permission when prompted by Android"
    run termux-setup-storage 2>/dev/null || true
  fi
}

setup_siyarix_alias() {
  local bashrc="${HOME}/.bashrc"
  if [ ! -f "$bashrc" ]; then
    touch "$bashrc"
  fi
  if ! grep -q "siyarix" "$bashrc" 2>/dev/null; then
    echo "" >> "$bashrc"
    echo "# Siyarix alias" >> "$bashrc"
    echo "alias siyarix='python3 -m siyarix'" >> "$bashrc"
    ok "Added siyarix alias to ~/.bashrc"
  fi
}

install_via_pip() {
  info "Installing Siyarix via pip..."
  run pip install --upgrade pip
  run pip install siyarix 2>/dev/null ||
    run pip install --break-system-packages siyarix 2>/dev/null ||
    run python3 -m pip install siyarix
}

main() {
  banner

  # Parse args
  while [ $# -gt 0 ]; do
    case "$1" in
      --help|-h)
        echo "Usage: bash install_android.sh [options]"
        echo ""
        echo "Options:"
        echo "  --dry-run       Simulate installation"
        echo "  --help, -h      Show this help"
        exit 0
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      *)
        err "Unknown option: $1"
        exit 1
        ;;
    esac
  done

  # Detect Termux
  if ! detect_termux; then
    err "This script is for Android/Termux only."
    err "Detected environment is not Termux."
    err "Install Termux from F-Droid or Google Play first."
    exit 1
  fi
  ok "Termux environment detected"

  # Check Python
  if ! check_python; then
    info "Python 3.11+ not found. Installing via pkg..."
    run pkg update -y
    run pkg install -y python
    if ! check_python; then
      err "Failed to install Python."
      exit 1
    fi
  fi
  ok "Python found: $($PYTHON --version 2>&1)"

  # Install build deps
  install_termux_deps

  # Storage permissions
  setup_termux_storage

  # Install siyarix
  install_via_pip

  # Setup alias
  setup_siyarix_alias

  # Verify
  if python3 -c "import siyarix; print(siyarix.__version__)" &>/dev/null; then
    local ver
    ver=$(python3 -c "import siyarix; print(siyarix.__version__)")
    ok "Siyarix v${ver} installed successfully!"
    info "Config directory: ${TERMUX_HOME}/.siyarix"
    info "Run: siyarix --help"
    info "Or:  python3 -m siyarix --help"
  else
    err "Installation verification failed."
    exit 1
  fi
}

main "$@"
