# Project instructions

This repository is the design for a 9.6 kW (240 V / 40 A) Level 2 J1772 EV charger bench unit, built around the Pionix ChargeBridge evaluation board (CB-EVAL v1.2 with a CB-CCS-EVSE-LU module) and EVerest on an x86 PC. It's a private bench test device, not a listed product.

## Layout

- `cb-l2-evse.html`: the deliverable. Schematic sheets 1–2, priced BOM, build notes, step-by-step assembly with to-scale drawings.
- `cb-eval-board/`: git submodule, Pionix's KiCad project. Its v1.2 schematic is authoritative over the v1.1 PDF datasheet (the PDF's J11 pin table is wrong).
- `datasheets/`: manufacturer PDFs (Git LFS), indexed in `datasheets/README.md`.
- `scripts/`: generators and tools; see `scripts/README.md`.
- `session/`: exported OpenCode session with the full design history.

## Working rules

- The BOM table, the Simulations section and the Assembly section are generated. Edit `scripts/build_bom.py`, `scripts/sim/run.py` or `scripts/build_assembly.py` and re-run them; don't hand-edit those parts of the HTML. `python3 scripts/sim/run.py --check` must pass before committing. Schematic sheets 1–2 and the build notes are hand-maintained SVG/HTML.
- Keep the schematic, BOM and assembly drawings consistent with each other. A wiring change usually touches all three.
- For CB-EVAL connectivity, use `scripts/board_nets.py` (KiCad's own netlist via kicad-cli). Don't rely on `scripts/netlist.py`; it swaps the pins of some rotated or mirrored two-pin parts.
- Never invent prices or dimensions. Record only values read from a vendor page or datasheet, with the date for prices, and mark anything unverified.
- Use `scripts/cfx search` / `scripts/cfx fetch` for web lookups (run `scripts/setup.sh` first). Polycase, Mouser and Home Depot block automated browsers; ask the user to save pages by hand.
- After editing the HTML, render it (for example `chromium --headless --screenshot`) and look at the result before reporting done.

## Design decisions to preserve

- Input: owned NEMA 14-50 cord on an existing 50 A GFCI circuit. N lands on isolated terminal TB1-5 and is never bonded to PE.
- CB-EVAL J11 has no ground pin. CP returns through the single 0 V–PE bond (PS1 −V to PE3).
- EMG IN (J4.11) has a 100 kΩ pull-up to 24 V. Any NC safety contact needs R1 (2.2 kΩ) with two parallel 2.2 kΩ pull-downs, R2a and R2b, so either pull-down alone still trips. The Pionix board must not be modified (R9 stays fitted). The E-stop S1 is fitted in the right wall: S1-a in K1's coil circuit, S1-b in the J4.11 loop.
- Relay 1 (J5.10 / J5.9) drives K1 through a TPS27S100, limited to about 5.2 A. Keep the coil under 2 A continuous and relay PWM off. K1 aux NC 21-22 goes from +24 V to J5.12, with R3 3.3 kΩ to 0 V for wetting current.
- The meter's N reference comes from F1/F2 terminal 4. L2 doesn't pass through the meter.

## Session history

`session/cb-l2-evse.opencode-session.json` is the exported design session. In it, `/home/brian/gl` is this repository's root and `~/.local/bin/cfx` is now `scripts/cfx`.
