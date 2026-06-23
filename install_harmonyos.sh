#!/usr/bin/env bash
# =============================================================================
# Siyarix Installer for HarmonyOS
#   Run: curl -fsSL https://siyarix.dev/install_harmonyos.sh | bash
#   Or:  bash install_harmonyos.sh
# =============================================================================
set -euo pipefail

SIYARIX_VERSION="${SIYARIX_VERSION:-3.0.0}"
DRY_RUN="${SIYARIX_DRY_RUN:-0}"

banner() {
  echo ""
  echo "   ███████╗██╗██╗   ██╗ █████╗ ██████╗ ██╗██╗  ██╗"
  echo "   ██╔════╝██╚██╗ ██╔╝██╔══██╗██╔══██╗██║╚██╗██╔╝"
  echo "   ███████╗██║╚████╔╝ ███████║██████╔╝██║ ╚███╔╝"
  echo "   ╚════██║██║ ╚██╔╝  ██╔══██║██╔══██╗██║ ██╔██╗"
  echo "   ███████║██║  ██║   ██║  ██║██║  ██║██║██╔╝ ██╗"
  echo "   ╚══════╝╚═╝  ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
  echo "   AI Cybersecurity Orchestration Agent v${SIYARIX_VERSION}"
  echo "   HarmonyOS Installer"
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

detect_harmonyos() {
  if [ -f "/system/etc/param/ohos.para" ]; then
    return 0
  fi
  if [ -n "${OHOS_ARCH:-}" ]; then
    return 0
  fi
  if uname -a 2>/dev/null | grep -qi "ohos"; then
    return 0
  fi
  if [ -d "/ohos" ] || [ -d "/system/app/HwResourceManager" ]; then
    return 0
  fi
  return 1
}

find_python() {
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

install_via_ohpm() {
  if command -v ohpm &>/dev/null; then
    info "Installing via ohpm..."
    run ohpm install @siyarix/cli 2>/dev/null && return 0
    warn "ohpm package not found, falling back to pip"
  fi
  if command -v hpm &>/dev/null; then
    info "Installing via hpm..."
    run hpm install @siyarix/cli 2>/dev/null && return 0
    warn "hpm package not found, falling back to pip"
  fi
  return 1
}

install_via_pip() {
  info "Installing via pip..."
  run pip install --upgrade pip 2>/dev/null || true
  run pip install siyarix 2>/dev/null ||
    run pip3 install siyarix 2>/dev/null ||
    run python3 -m pip install siyarix
}

main() {
  banner

  while [ $# -gt 0 ]; do
    case "$1" in
      --help|-h)
        echo "Usage: bash install_harmonyos.sh [options]"
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

  if ! detect_harmonyos; then
    err "This script is for HarmonyOS only."
    exit 1
  fi
  ok "HarmonyOS environment detected"

  if ! find_python; then
    err "Python 3.11+ is required on HarmonyOS."
    err "Install Python via OHPM or from the HarmonyOS app store."
    exit 1
  fi
  ok "Python found: $($PYTHON --version 2>&1)"

  install_via_ohpm || install_via_pip

  # Verify
  if $PYTHON -c "import siyarix; print(siyarix.__version__)" &>/dev/null; then
    ver=$($PYTHON -c "import siyarix; print(siyarix.__version__)")
    ok "Siyarix v${ver} installed successfully!"
    warn "Note: HarmonyOS support is experimental."
    warn "Some security tools may not be available on this platform."
    info "Run: siyarix --help"
  else
    err "Installation verification failed."
    exit 1
  fi
}

main "$@"
