#!/usr/bin/env sh
# =============================================================================
# Siyarix Installer for iOS/iSH
#   Run: curl -fsSL https://siyarix.dev/install_ios.sh | sh
#   Or:  sh install_ios.sh
# =============================================================================
set -e

SIYARIX_VERSION="${SIYARIX_VERSION:-1.0.0}"
DRY_RUN="${SIYARIX_DRY_RUN:-0}"
ISH_HOME="${HOME:-/root}"

banner() {
  echo ""
  echo "   ███████╗██╗██╗   ██╗ █████╗ ██████╗ ██╗██╗  ██╗"
  echo "   ██╔════╝██╚██╗ ██╔╝██╔══██╗██╔══██╗██║╚██╗██╔╝"
  echo "   ███████╗██║╚████╔╝ ███████║██████╔╝██║ ╚███╔╝"
  echo "   ╚════██║██║ ╚██╔╝  ██╔══██║██╔══██╗██║ ██╔██╗"
  echo "   ███████║██║  ██║   ██║  ██║██║  ██║██║██╔╝ ██╗"
  echo "   ╚══════╝╚═╝  ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
  echo "   AI Cybersecurity Orchestration Agent v${SIYARIX_VERSION}"
  echo "   iOS/iSH Installer"
  echo ""
}

info()  { echo "==> $*"; }
ok()    { echo "  ✓ $*"; }
warn()  { echo "  ! $*"; }
err()   { echo "  ✗ $*" >&2; }

run() {
  if [ "$DRY_RUN" = "1" ]; then
    info "[DRY-RUN] Would run: $*"
    return 0
  fi
  "$@"
}

detect_ish() {
  if [ -n "${TERM_PROGRAM:-}" ] && echo "$TERM_PROGRAM" | grep -qi "ish"; then
    return 0
  fi
  if uname -r 2>/dev/null | grep -qi "ish"; then
    return 0
  fi
  if [ -f "/proc/version" ] && grep -qi "ish" /proc/version 2>/dev/null; then
    return 0
  fi
  return 1
}

check_python() {
  for cmd in python3 python; do
    if command -v "$cmd" >/dev/null 2>&1; then
      local ver
      ver=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
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

install_via_apk() {
  info "Installing via apk (iSH Alpine)..."
  run apk update
  run apk add python3 py3-pip
}

install_siyarix() {
  info "Installing Siyarix..."
  run pip3 install --upgrade pip 2>/dev/null || true
  run pip3 install siyarix 2>/dev/null ||
    run python3 -m pip install siyarix 2>/dev/null ||
    run pip install siyarix
}

post_install_hints() {
  echo ""
  warn "On iOS/iSH, some security tools may not be available:"
  warn "  - nmap, masscan, wireshark are not available on iOS"
  warn "  - Use Siyarix's built-in Python-based scanners instead"
  warn "  - Siyarix will operate in registry/offline mode"
  echo ""
  info "Config stored at: ${ISH_HOME}/.siyarix"
  info "To persist config across iSH restarts, ensure your"
  info "iSH filesystem backup is enabled in iOS settings."
}

main() {
  banner

  while [ $# -gt 0 ]; do
    case "$1" in
      --help|-h)
        echo "Usage: sh install_ios.sh [options]"
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

  if ! detect_ish; then
    err "This script is for iOS/iSH only."
    err "Install iSH from the iOS App Store first."
    exit 1
  fi
  ok "iSH environment detected"

  if ! check_python; then
    info "Python not found. Installing via apk..."
    install_via_apk
    if ! check_python; then
      err "Failed to install Python."
      exit 1
    fi
  fi
  ok "Python found: $($PYTHON --version 2>&1)"

  install_siyarix

  # Verify
  if $PYTHON -c "import siyarix; print(siyarix.__version__)" >/dev/null 2>&1; then
    ver=$($PYTHON -c "import siyarix; print(siyarix.__version__)")
    ok "Siyarix v${ver} installed successfully!"
    post_install_hints
  else
    err "Installation verification failed."
    exit 1
  fi
}

main "$@"
