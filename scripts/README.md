# Scripts

All of these write into `../cb-l2-evse.html` and only need Python 3.10+ (standard library), except `cfx`.

- `build_bom.py`: regenerates the priced BOM table. Each part is one `r(...)` row; edit rows to change parts or prices, then run `python3 scripts/build_bom.py`.
- `build_assembly.py`: regenerates the Assembly section and its to-scale drawings. Part positions, terminals and wire routes are defined near the top. Run `python3 scripts/build_assembly.py`.
- `netlist.py`: geometry-based netlister for KiCad 9 schematics, used to review the CB-EVAL board, e.g. `python3 scripts/netlist.py cb-eval-board/cb-eval-board/relais.kicad_sch`.
- `cfx`: Camoufox headless-browser helper for web search and page/PDF text. Run `scripts/setup.sh` once, then `scripts/cfx search "query"` or `scripts/cfx fetch URL`.
- `setup.sh`: creates `.venv` and downloads the Camoufox browser (about 600 MB).
- `export-session.sh`: re-exports the OpenCode design session into `session/`.

`data/` holds the research behind the numbers:
- `prices/`: vendor price lookups from 26 Oct 2026
- `dims/summary.md`: part dimensions with source URLs (the PDFs are in `../datasheets/`)
- `board_geom.json`: CB-EVAL connector positions, from the KiCad PCB
- `polycase_ZH-161407_page.txt`: text of the Polycase product page (saved by hand; the site blocks automated access)
- `cb-l2-evse.revB.html`: the page as of Rev B, before this repository existed
