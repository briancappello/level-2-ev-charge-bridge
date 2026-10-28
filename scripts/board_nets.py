#!/usr/bin/env python3
"""Look up CB-EVAL nets from KiCad's own netlist (needs kicad-cli, KiCad 9+).

    python3 scripts/board_nets.py J5.12          net on one pin, with every connected pin
    python3 scripts/board_nets.py J11            every pin of a connector
    python3 scripts/board_nets.py --ref D22      every pin of a component, with pin functions
    python3 scripts/board_nets.py --sheet "LevelShiftInput2"   all parts on a (hierarchical) sheet

This replaces the geometry-based netlist.py, which swaps the pins of some
rotated or mirrored two-pin parts (it reported the input zeners backwards).
"""
import argparse, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCH = ROOT / "cb-eval-board" / "cb-eval-board" / "cb-eval-board.kicad_sch"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from netlist import parse, kids, kid  # S-expression parser only

def load():
    if not shutil.which("kicad-cli"):
        sys.exit("kicad-cli not found; install KiCad 9 or newer")
    if not SCH.exists():
        sys.exit(f"{SCH} missing; run: git submodule update --init")
    with tempfile.TemporaryDirectory() as td:
        # kicad-cli rewrites the project's .kicad_prl, so export from a copy to keep the submodule clean
        proj = Path(td) / "proj"
        shutil.copytree(SCH.parent, proj, ignore=shutil.ignore_patterns("production"))
        out = Path(td) / "board.net"
        subprocess.run(["kicad-cli", "sch", "export", "netlist", "--format", "kicadsexpr", "-o", str(out), str(proj / SCH.name)],
                       check=True, capture_output=True)
        t = parse(out.read_text())
    nets = {kid(n, "name")[1]: [(kid(x, "ref")[1], kid(x, "pin")[1], (kid(x, "pinfunction") or [None, ""])[1])
                                for x in kids(n, "node")] for n in kids(kid(t, "nets"), "net")}
    comps = {}
    for c in kids(kid(t, "components"), "comp"):
        sp = kid(c, "sheetpath")
        comps[kid(c, "ref")[1]] = (kid(c, "value")[1], kid(sp, "names")[1] if sp else "")
    pin2net = {(r, p): (n, f) for n, nodes in nets.items() for r, p, f in nodes}
    return nets, comps, pin2net

def show_pin(nets, pin2net, ref, pin):
    n, f = pin2net.get((ref, pin), ("(unconnected)", ""))
    others = " ".join(f"{r}.{p}" for r, p, _ in nets.get(n, []) if (r, p) != (ref, pin))
    if n in ("GND", "+3.3V", "+24V"): others = f"({len(nets[n])} pins)"
    print(f"{ref}.{pin:<4}{('(' + f + ')') if f else '':<14} {n:<44} {others}")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="REF.PIN or connector REF")
    ap.add_argument("--ref"); ap.add_argument("--sheet")
    a = ap.parse_args()
    nets, comps, pin2net = load()
    if a.sheet:
        for r, (v, sp) in sorted(comps.items()):
            if a.sheet in sp:
                print(f"{r:6} {v:20} {sp}")
                for (rr, p) in sorted(k for k in pin2net if k[0] == r): show_pin(nets, pin2net, rr, p)
        return
    ref = a.ref or (a.target or "").split(".")[0]
    if not ref: ap.error("give a target, --ref or --sheet")
    if a.target and "." in a.target and not a.ref:
        show_pin(nets, pin2net, ref, a.target.split(".", 1)[1]); return
    pins = sorted((p for (r, p) in pin2net if r == ref), key=lambda p: (len(p), p))
    if not pins: sys.exit(f"no component {ref}")
    print(f"{ref}: {comps[ref][0]}  [{comps[ref][1]}]")
    for p in pins: show_pin(nets, pin2net, ref, p)

if __name__ == "__main__":
    main()
