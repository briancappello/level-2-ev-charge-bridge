#!/usr/bin/env bash
# Re-export the design OpenCode session into session/ (run after further work in it).
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
id="${1:-ses_f10f0b8a6ffepIrL6hYZ5qj2S1}"
opencode session export "$id" > "$root/session/cb-l2-evse.opencode-session.json"
echo "Exported $id to session/cb-l2-evse.opencode-session.json"
