# Scripts

The build scripts write into `../cb-l2-evse.html`. Everything needs only Python 3.10+ and its standard library, plus ngspice for `sim/`, KiCad for `board_nets.py`, and the `.venv` for `cfx`.

- `build_bom.py`: regenerates the priced BOM table. Each part is one `r(...)` row; edit rows to change parts or prices, then run `python3 scripts/build_bom.py`.
- `build_assembly.py`: regenerates the Assembly section and its to-scale drawings. Part positions, terminals and wire routes are defined near the top. Run `python3 scripts/build_assembly.py`.
- `sim/run.py`: ngspice circuit simulations (E-stop loop, relay feedback, control pilot, PT1000) with pass/fail checks. Writes the Simulations section of the page and the decks in `sim/netlists/`. `--check` runs the checks only (this is what CI runs). Needs ngspice.
- `board_nets.py`: looks up CB-EVAL nets from KiCad's own netlist, e.g. `python3 scripts/board_nets.py J5.12` or `--ref D22`. Needs `kicad-cli` (KiCad 9+).
- `netlist.py`: the earlier geometry-based netlister. Kept for its S-expression parser; its connectivity is unreliable for rotated or mirrored two-pin parts, so use `board_nets.py` instead.
- `cfx`: Camoufox headless-browser helper for web search and page/PDF text. Run `scripts/setup.sh` once, then `scripts/cfx search "query"` or `scripts/cfx fetch URL`.
- `setup.sh`: creates `.venv` and downloads the Camoufox browser (about 600 MB).
- `export-session.sh`: re-exports the OpenCode design session into `session/`.

`data/` holds the research behind the numbers:
- `prices/`: vendor price lookups from 26 Oct 2026
- `dims/summary.md`: part dimensions with source URLs (the PDFs are in `../datasheets/`)
- `board_geom.json`: CB-EVAL connector positions, from the KiCad PCB
- `polycase_ZH-161407_page.txt`: text of the Polycase product page (saved by hand; the site blocks automated access)
- `cb-l2-evse.revB.html`: the page as of Rev B, before this repository existed
