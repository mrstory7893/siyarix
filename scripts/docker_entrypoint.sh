#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# =============================================================================
# Siyarix Docker Entrypoint
# =============================================================================
# - Initializes config if missing
# - Fixes permissions on SIYARIX_HOME
# - Executes the given command or drops into the siyarix CLI
# =============================================================================
set -e

SIYARIX_HOME="${SIYARIX_HOME:-$HOME/.siyarix}"

# ----  Initialise config if it does not exist yet  ---------------------------
if [ ! -f "$SIYARIX_HOME/config.yaml" ] && [ ! -f "$SIYARIX_HOME/config.yml" ]; then
    echo "[entrypoint] No siyarix config found – running init ..."
    mkdir -p "$SIYARIX_HOME"
    siyarix init --non-interactive 2>/dev/null || true
fi

# ----  Ensure correct ownership  --------------------------------------------
mkdir -p "$SIYARIX_HOME"
chown -R "$(id -u):$(id -g)" "$SIYARIX_HOME" 2>/dev/null || true

# ----  Execute command (default: siyarix CLI)  ------------------------------
if [ $# -eq 0 ]; then
    echo "[entrypoint] Starting siyarix CLI ..."
    exec siyarix
fi

exec "$@"
