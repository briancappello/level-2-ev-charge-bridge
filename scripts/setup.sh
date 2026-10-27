#!/usr/bin/env bash
# One-time setup: Python venv for the Camoufox web tools. The build scripts
# (build_bom.py, build_assembly.py, netlist.py) only need the standard library.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 -m venv "$root/.venv"
"$root/.venv/bin/pip" install -q -U pip
"$root/.venv/bin/pip" install -q -r "$root/scripts/requirements.txt"
"$root/.venv/bin/python" -m camoufox fetch
echo "Done. Try: scripts/cfx search \"TPS27S100 datasheet\""
