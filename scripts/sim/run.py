#!/usr/bin/env python3
"""Circuit simulations for the cb-l2-evse design (ngspice).

    python3 scripts/sim/run.py           run everything, write netlists, update cb-l2-evse.html
    python3 scripts/sim/run.py --check   run everything and exit non-zero if any check fails

Component values come from the CB-EVAL v1.2 KiCad netlist (kicad-cli) and from
the design's BOM. Thresholds for the board's 74LVC1G17 Schmitt inputs come from
TI's datasheet (datasheets/TI_SN74LVC1G17_schmitt_buffer.pdf), interpolated to 3.3 V.
"""
import argparse, html, itertools, math, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NETDIR = Path(__file__).resolve().parent / "netlists"
NGSPICE = shutil.which("ngspice")

VT_HI = 2.08   # 74LVC1G17 VT+ max at 3.3 V: input is guaranteed to read high above this
VT_LO = 1.01   # 74LVC1G17 VT- min at 3.3 V: input is guaranteed to read low below this
SUPPLY = (21.6, 24.0, 29.0)  # HDR-60-24 adjustment range and nominal
CLOSED, OPEN = 0.05, 1e12    # contact resistance models (ohms)

ZENER = ".model DZ D(IS=1e-14 N=1 RS=20 BV=5.1 IBV=1m)"            # MM3Z5V1 (only its clamp matters)
D1N4148 = ".model D1N4148 D(IS=2.52n RS=0.568 N=1.752 BV=100 IBV=100u CJO=4p TT=20n)"

CHECKS = []  # (group, description, value_text, passed)

def check(group, desc, value, ok):
    CHECKS.append((group, desc, value, bool(ok)))

def ngspice(name, deck):
    NETDIR.mkdir(exist_ok=True)
    (NETDIR / f"{name}.cir").write_text(deck)
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "deck.cir"
        path.write_text(deck.replace("@WRDIR@", td))
        r = subprocess.run([NGSPICE, "-b", str(path)], capture_output=True, text=True, timeout=300)
        out = r.stdout + r.stderr
        data = {}
        for f in Path(td).glob("*.dat"):
            data[f.stem] = [tuple(float(x) for x in ln.split()) for ln in f.read_text().split("\n") if ln.strip()]
    if r.returncode != 0 or "error" in out.lower() and "no error" not in out.lower():
        bad = [ln for ln in out.splitlines() if "rror" in ln]
        if bad:
            raise RuntimeError(f"ngspice failed on {name}:\n" + "\n".join(bad[:10]))
    vals = {}
    for m in re.finditer(r"^\s*([\w().:+-]+)\s*=\s*([-+0-9.eE]+)\s*$", out, re.M):
        vals[m.group(1).lower()] = float(m.group(2))
    return vals, data, out

def tol_corners(nominals, tol):
    keys = list(nominals)
    for signs in itertools.product((-1, 1), repeat=len(keys)):
        yield {k: nominals[k] * (1 + s * tol) for k, s in zip(keys, signs)}

# ----------------------------------------------------------------------------------------
# 1. Emergency input loop (J4.11): board R9/R43/R76/D22, our R1/R2 and NC contact chain
# ----------------------------------------------------------------------------------------
def emg_deck(vs, r, chain, sw2, failed=()):
    rv = lambda k: OPEN if k in failed else r[k]
    return f"""* EMG IN loop, J4.11 (CB-EVAL LevelShiftInput2 + R1, R2a || R2b)
V24 vp 0 {vs}
Rchain vp a {chain}
R1 a emg {rv('R1')}
R2a emg 0 {rv('R2a')}
R2b emg 0 {rv('R2b')}
R9 vp emg {r['R9']}
R43 emg x {r['R43']}
R76 x 0 {r['R76']}
D22 0 x DZ
Rsw2 emg 0 {sw2}
{ZENER}
.control
op
print v(emg) v(x) v(a)
.endc
.end
"""

def sim_emg():
    nom = {"R1": 2200, "R2a": 2200, "R2b": 2200, "R9": 100e3, "R43": 20e3, "R76": 1e6}
    rows = []
    worst = {"run": (1e9, None), "trip": (-1e9, None)}
    single = {"R2a": -1e9, "R2b": -1e9}
    for vs in SUPPLY:
        for r in tol_corners(nom, 0.01):
            for f in single:
                v, *_ = ngspice("emg_loop_one_pulldown_failed", emg_deck(vs, r, OPEN, OPEN, failed=(f,)))
                single[f] = max(single[f], v["v(x)"])
            for state, chain in (("run", CLOSED), ("trip", OPEN)):
                v, *_ = ngspice("emg_loop_corner", emg_deck(vs, r, chain, OPEN))
                x = v["v(x)"]
                if state == "run" and x < worst["run"][0]: worst["run"] = (x, (vs, v["v(emg)"]))
                if state == "trip" and x > worst["trip"][0]: worst["trip"] = (x, (vs, v["v(emg)"]))
    v, *_ = ngspice("emg_loop_closed", emg_deck(24, nom, CLOSED, OPEN))
    rows.append(("NC chain closed (normal)", v["v(emg)"], v["v(x)"], "high"))
    v, *_ = ngspice("emg_loop_open", emg_deck(24, nom, OPEN, OPEN))
    rows.append(("NC chain open or wire broken", v["v(emg)"], v["v(x)"], "low"))
    v, *_ = ngspice("emg_loop_sw2", emg_deck(24, nom, CLOSED, CLOSED))
    i_sw2 = (24 - v["v(emg)"]) / nom["R1"] + (24 - v["v(emg)"]) / nom["R9"]
    rows.append(("On-board SW2 pressed, chain closed", v["v(emg)"], v["v(x)"], "low"))
    v, *_ = ngspice("emg_loop_r2a_failed", emg_deck(24, nom, OPEN, OPEN, failed=("R2a",)))
    rows.append(("Chain open, R2a failed open", v["v(emg)"], v["v(x)"], "low"))
    v, *_ = ngspice("emg_loop_r2a_failed_closed", emg_deck(24, nom, CLOSED, OPEN, failed=("R2a",)))
    rows.append(("Chain closed, R2a failed open", v["v(emg)"], v["v(x)"], "high"))
    v, *_ = ngspice("emg_loop_both_failed", emg_deck(24, nom, OPEN, OPEN, failed=("R2a", "R2b")))
    rows.append(("Chain open, both pull-downs failed open", v["v(emg)"], v["v(x)"], "high (no trip)"))
    v, *_ = ngspice("emg_loop_r1_failed", emg_deck(24, nom, CLOSED, OPEN, failed=("R1",)))
    rows.append(("Chain closed, R1 failed open", v["v(emg)"], v["v(x)"], "low (trips)"))
    r1_fail = v["v(x)"]
    nc = {"R9": 100e3, "R43": 20e3, "R76": 1e6, "R1": OPEN, "R2a": OPEN, "R2b": OPEN}
    v, *_ = ngspice("emg_loop_no_estop", emg_deck(24, nc, OPEN, OPEN))
    rows.append(("No E-stop fitted (J4.11 open)", v["v(emg)"], v["v(x)"], "high"))
    run_x, (run_vs, run_emg) = worst["run"]
    trip_x, (trip_vs, trip_emg) = worst["trip"]
    check("E-stop loop", "Closed loop reads high at every supply and ±1% corner",
          f"worst {run_x:.2f} V at the Schmitt input ({run_vs} V supply), needs ≥ {VT_HI} V", run_x >= VT_HI)
    check("E-stop loop", "Open loop reads low at every supply and ±1% corner",
          f"worst {trip_x:.2f} V ({trip_vs} V supply), needs ≤ {VT_LO} V", trip_x <= VT_LO)
    w1 = max(single.values())
    check("E-stop loop", "Either pull-down alone still trips (R2a or R2b failed open), every supply and corner",
          f"worst {w1:.2f} V, needs ≤ {VT_LO} V", w1 <= VT_LO)
    check("E-stop loop", "R1 failed open trips (fails safe)", f"{r1_fail:.2f} V", r1_fail <= VT_LO)
    vmax = max(SUPPLY) * 1100 * 1.01 / (2200 * 0.99 + 1100 * 1.01)
    vmax1 = max(SUPPLY) * 2200 * 1.01 / (2200 * 0.99 + 2200 * 1.01)
    check("E-stop loop", "J4.11 stays within the board's 30 V input rating, even with one pull-down failed",
          f"{vmax:.1f} V normally, {vmax1:.1f} V with one failed", vmax1 <= 30)
    check("E-stop loop", "On-board SW2 short stays within R1's 0.5 W rating",
          f"{i_sw2 * 1e3:.1f} mA, {(24 / 2200) ** 2 * 2200:.2f} W in R1 at 24 V; {(29 / 2178) ** 2 * 2178:.2f} W at 29 V",
          (29 / 2178) ** 2 * 2178 <= 0.5)
    check("E-stop loop", "No-E-stop configuration reads normal (high)", f"{rows[-1][2]:.2f} V", rows[-1][2] >= VT_HI)
    return rows

# ----------------------------------------------------------------------------------------
# 2. Relay 1 feedback (J5.12): board R68/R97/D32, our R3 and K1 aux NC 21-22
# ----------------------------------------------------------------------------------------
def fb_deck(src_v, src_r, aux, r3, r68=20e3, r97=1e6):
    return f"""* Relay 1 feedback, J5.12 (CB-EVAL LevelShiftInput7 + R3 + K1 aux 21-22)
Vs vp 0 {src_v}
Rsrc vp s {src_r}
Vam s s2 0
Raux s2 fb {aux}
R3 fb 0 {r3}
R68 fb x {r68}
R97 x 0 {r97}
D32 0 x DZ
{ZENER}
.control
op
print v(fb) v(x) v(s) i(vam)
.endc
.end
"""

def sim_fb():
    rows = []
    lo_i, hi_p = 1e9, 0
    for vs in SUPPLY:
        for r3 in (3300 * 0.99, 3300 * 1.01):
            v, *_ = ngspice("relay1_feedback_corner", fb_deck(vs, 0.001, CLOSED, r3))
            i = v["i(vam)"]
            lo_i = min(lo_i, i); hi_p = max(hi_p, v["v(fb)"] ** 2 / r3)
    configs = [
        ("+24 V through aux, with R3 (this design)", 24, 0.001, 3300),
        ("+24 V through aux, no R3", 24, 0.001, OPEN),
        ("Board FB OUT (3.3 V via 330 Ω), with R3", 3.3, 330, 3300),
        ("Board FB OUT (3.3 V via 330 Ω), no R3", 3.3, 330, OPEN),
    ]
    for label, sv, sr, r3 in configs:
        v, *_ = ngspice("relay1_feedback_aux_closed", fb_deck(sv, sr, CLOSED, r3))
        i_aux = v["i(vam)"]
        v2, *_ = ngspice("relay1_feedback_aux_open", fb_deck(sv, sr, OPEN, r3))
        rows.append((label, i_aux * 1e3, v["v(x)"], v2["v(x)"]))
    check("Relay feedback", "Aux contact current ≥ 5 mA (EH04-11N minimum) at every supply and R3 corner",
          f"{lo_i * 1e3:.1f} mA minimum (21.6 V, R3 +1%)", lo_i >= 5e-3)
    check("Relay feedback", "K1 open (aux closed) reads high", f"{rows[0][2]:.2f} V", rows[0][2] >= VT_HI)
    check("Relay feedback", "K1 closed (aux open) reads low", f"{rows[0][3]:.3f} V", rows[0][3] <= VT_LO)
    check("Relay feedback", "R3 dissipation within its 0.5 W rating", f"{hi_p:.3f} W at 29 V", hi_p <= 0.5 * 0.6)
    return rows

# ----------------------------------------------------------------------------------------
# 3. Control pilot: ±12 V 1 kHz through 1 kΩ, cable capacitance, EV states A-D
# ----------------------------------------------------------------------------------------
STATES = {"A": [], "B": [2740], "C": [2740, 1300], "D": [2740, 270]}
NOMINAL = {"A": 12.0, "B": 9.0, "C": 6.0, "D": 3.0}
DUTY = 40 / 0.6 / 100   # 40 A -> 66.7 %
EDGE = 1e-6             # assumed source edge time (the module's real slew rate isn't published)

def cp_deck(state, c_total):
    ton = 1e-3 * DUTY - EDGE
    ev = ""
    if STATES[state]:
        ev = "Dev cp ev D1N4148\n" + "".join(f"Rev{i} ev 0 {r}\n" for i, r in enumerate(STATES[state]))
    return f"""* Control pilot, state {state}, {c_total*1e12:.0f} pF total on CP
Vosc osc 0 PULSE(-12 12 0 {EDGE} {EDGE} {ton} 1m)
Rs osc cp 1k
Cmod cp 0 300p
Ccab cp 0 {max(c_total - 300e-12, 1e-15)}
{ev}{D1N4148}
.control
tran 50n 3m
wrdata @WRDIR@/cp.dat v(cp)
.endc
.end
"""

def analyse_cp(data):
    t = [p[0] for p in data]; v = [p[1] for p in data]
    T0 = 2e-3  # last full period
    hi = [vv for tt, vv in zip(t, v) if T0 + 0.1e-3 <= tt <= T0 + 1e-3 * DUTY - 0.02e-3]
    lo = [vv for tt, vv in zip(t, v) if T0 + 1e-3 * DUTY + 0.1e-3 <= tt <= T0 + 0.98e-3]
    vhi, vlo = sum(hi) / len(hi), sum(lo) / len(lo)
    a, b = vlo + 0.1 * (vhi - vlo), vlo + 0.9 * (vhi - vlo)
    ta = tb = None
    for tt, vv in zip(t, v):
        if tt < T0 - 0.01e-3: continue
        if ta is None and vv >= a: ta = tt
        if ta is not None and vv >= b: tb = tt; break
    cross = [tt for (tt, vv), (t2, v2) in zip(zip(t, v), zip(t[1:], v[1:])) if tt >= T0 - 0.01e-3 and vv > 0 >= v2]
    duty = (cross[0] - T0) / 1e-3 if cross else float("nan")
    return vhi, vlo, (tb - ta), duty

def sim_cp():
    results, waves = {}, {}
    for c in (300e-12, 1600e-12):
        for st in STATES:
            _, d, _ = ngspice(f"cp_state{st}_{int(c*1e12)}pF", cp_deck(st, c))
            results[(st, c)] = analyse_cp(d["cp"])
            waves[(st, c)] = d["cp"]
    for st in STATES:
        vhi, vlo, tr, duty = results[(st, 1600e-12)]
        check("Control pilot", f"State {st} high level within ±0.5 V of {NOMINAL[st]:.0f} V at 1600 pF",
              f"{vhi:.2f} V", abs(vhi - NOMINAL[st]) <= 0.5)
        check("Control pilot", f"State {st} low level is −12 V (EV diode blocks)", f"{vlo:.2f} V", abs(vlo + 12) <= 0.3)
    st_w, tr = max(((st, results[(st, 1600e-12)][2]) for st in STATES), key=lambda kv: kv[1])
    check("Control pilot", "10–90% rise time at 1600 pF under 10 µs (assumed limit; confirm in SAE J1772 / IEC 61851-1)",
          f"{tr*1e6:.1f} µs worst (state {st_w})", tr < 10e-6)
    d = results[("C", 1600e-12)][3]
    check("Control pilot", "Duty cycle error at 1600 pF under 0.5 %", f"{d*100:.2f} % vs {DUTY*100:.2f} %", abs(d - DUTY) < 0.005)
    return results, waves

# ----------------------------------------------------------------------------------------
# 4. PT1000 front end (ADCs sheet): bridge R91/R70/R89/R90, INA333 gain R92, 2.048 V reference
# ----------------------------------------------------------------------------------------
def pt(t): return 1000 * (1 + 3.9083e-3 * t - 5.775e-7 * t * t)

def pt_deck(r, temps, vref=2.048):
    rs = " ".join(f"{pt(t):.3f}" for t in temps)
    gain = 1 + 100e3 / r["R92"]
    return f"""* PT1000_1 front end (R91, R70, R89, R90, U11 INA333 with Rg = R92)
.param rpt=1000
Vref ref 0 {vref}
R91 ref p {r['R91']}
Rpt p m {{rpt}}
R70 m 0 {r['R70']}
R89 ref n {r['R89']}
R90 n m {r['R90']}
* INA333 as an ideal difference amplifier, output limited to the 0-3.3 V rails
Bina out 0 V = max(0, min(3.3, {gain} * (v(p) - v(n))))
Rload out 0 100k
.control
foreach val {rs}
  alterparam rpt = $val
  reset
  op
  print v(out)
end
.endc
.end
"""

def sim_pt1000():
    temps = list(range(-40, 181, 5))
    nom = {"R91": 4990, "R70": 4990, "R89": 4990, "R90": 825, "R92": 3440}
    vout = lambda txt: [float(x) for x in re.findall(r"v\(out\)\s*=\s*([-+0-9.eE]+)", txt)]
    curve = list(zip(temps, vout(ngspice("pt1000_front_end", pt_deck(nom, temps))[2])))
    # temperature where the ADC clips at 2.048 V (linear interpolation)
    clip = next((round(t1 + (2.048 - v1) * (t2 - t1) / (v2 - v1)) for (t1, v1), (t2, v2) in zip(curve, curve[1:]) if v1 < 2.048 <= v2), None)
    # worst-case temperature error from 0.1 % resistors, using nominal scaling coefficients
    probe = [25, 80, 100]
    def v2t(vo):  # invert the nominal curve by linear interpolation
        for (t1, v1), (t2, v2) in zip(curve, curve[1:]):
            if v1 <= vo <= v2: return t1 + (vo - v1) * (t2 - t1) / (v2 - v1)
        return float("nan")
    worst = 0.0
    for r in tol_corners(nom, 0.001):
        o = vout(ngspice("pt1000_corner", pt_deck(r, probe))[2])
        for t, vo in zip(probe, o):
            worst = max(worst, abs(v2t(vo) - t))
    check("PT1000", "ADC full scale (2.048 V) is above a 90 °C terminal alarm", f"clips at about {clip} °C", clip is not None and clip > 100)
    check("PT1000", "Worst-case error from 0.1 % resistors, uncalibrated, at 25/80/100 °C", f"±{worst:.1f} °C", worst < 3)
    return curve, clip, worst

# ----------------------------------------------------------------------------------------
# SVG plotting and HTML
# ----------------------------------------------------------------------------------------
def plot(series, xr, yr, xlab, ylab, w=640, h=300, hlines=(), xfmt="{:g}", yfmt="{:g}", xticks=None, yticks=None, title=""):
    L, R, T, B = 54, 16, 14, 40
    pw, ph = w - L - R, h - T - B
    X = lambda x: L + (x - xr[0]) / (xr[1] - xr[0]) * pw
    Y = lambda y: T + (1 - (y - yr[0]) / (yr[1] - yr[0])) * ph
    s = [f'<svg class="sim-svg" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}">']
    for yt in yticks or []:
        s.append(f'<path class="sim-grid" d="M{L} {Y(yt):.1f} H{L+pw}"/><text class="sim-tk" x="{L-6}" y="{Y(yt)+3.5:.1f}" text-anchor="end">{yfmt.format(yt)}</text>')
    for xt in xticks or []:
        s.append(f'<path class="sim-grid" d="M{X(xt):.1f} {T} V{T+ph}"/><text class="sim-tk" x="{X(xt):.1f}" y="{T+ph+14}" text-anchor="middle">{xfmt.format(xt)}</text>')
    s.append(f'<rect class="sim-frame" x="{L}" y="{T}" width="{pw}" height="{ph}"/>')
    for yv, lab in hlines:
        s.append(f'<path class="sim-ref" d="M{L} {Y(yv):.1f} H{L+pw}"/><text class="sim-tk" x="{L+pw-4}" y="{Y(yv)-4:.1f}" text-anchor="end">{html.escape(lab)}</text>')
    for pts, color, lab, dash in series:
        pts = [(x, y) for x, y in pts if xr[0] <= x <= xr[1]]
        d = "M" + " L".join(f"{X(x):.1f} {Y(max(yr[0], min(yr[1], y))):.1f}" for x, y in pts)
        da = ' stroke-dasharray="5 3"' if dash else ""
        s.append(f'<path class="sim-line" d="{d}" stroke="{color}"{da}/>')
    s.append(f'<text class="sim-ax" x="{L+pw/2}" y="{h-6}" text-anchor="middle">{html.escape(xlab)}</text>')
    s.append(f'<text class="sim-ax" transform="translate(14 {T+ph/2}) rotate(-90)" text-anchor="middle">{html.escape(ylab)}</text>')
    s.append("</svg>")
    leg = "".join(f'<span><i style="border-color:{c};{"border-top-style:dashed" if dsh else ""}"></i>{html.escape(l)}</span>' for _, c, l, dsh in series if l)
    return "".join(s), (f'<div class="legend">{leg}</div>' if leg else "")

def decimate(pts, n=1500):
    step = max(1, len(pts) // n)
    return pts[::step]

def build_section(emg_rows, fb_rows, cp, pt1000):
    cp_res, waves = cp
    curve, clip, worst = pt1000
    out = ['<h2 id="simulations">Circuit simulations</h2>',
           '<p class="hint">Generated by <code>scripts/sim/run.py</code> with ngspice. Board component values come from the CB-EVAL v1.2 KiCad netlist. '
           f'The board\'s 74LVC1G17 inputs are guaranteed high above {VT_HI} V and low below {VT_LO} V (TI datasheet, 3.3 V). '
           'Re-run the script after changing any of these circuits.</p>']
    passed = sum(1 for c in CHECKS if c[3])
    out.append(f'<p><strong>{passed} of {len(CHECKS)} checks pass.</strong></p>')
    out.append('<div class="tablewrap"><table class="sim-checks"><thead><tr><th>Circuit</th><th>Check</th><th>Result</th><th></th></tr></thead><tbody>')
    for g, desc, val, ok in CHECKS:
        out.append(f'<tr><td>{html.escape(g)}</td><td>{html.escape(desc)}</td><td>{html.escape(val)}</td><td class="{"sim-pass" if ok else "sim-fail"}">{"Pass" if ok else "Fail"}</td></tr>')
    out.append('</tbody></table></div>')

    out.append('<h3>E-stop loop (J4.11)</h3><p>R1 2.2 kΩ in series, R2a and R2b 2.2 kΩ each in parallel to 0 V. Nominal values at 24 V; the checks above sweep 21.6–29 V and every ±1 % resistor corner.</p>')
    out.append('<div class="tablewrap"><table class="sim-t"><thead><tr><th>Condition</th><th>J4.11</th><th>Schmitt input</th><th>Reads</th></tr></thead><tbody>')
    for lab, ve, vx, reads in emg_rows:
        out.append(f'<tr><td>{html.escape(lab)}</td><td>{ve:.2f} V</td><td>{vx:.2f} V</td><td>{html.escape(reads)}</td></tr>')
    out.append('</tbody></table></div>')
    out.append('<p>R2a and R2b are in parallel so that either one alone still trips the input. With a single pull-down, its failing open would leave the board\'s 100 kΩ pull-up in control: an open loop would read normal, and nothing would show it while the loop is closed. Now it takes both failing. The step 9 trip test checks both are working.</p>')

    out.append('<h3>Relay 1 feedback (J5.12)</h3><div class="tablewrap"><table class="sim-t"><thead><tr><th>Wiring</th><th>Aux contact current</th><th>Input, K1 open</th><th>Input, K1 closed</th></tr></thead><tbody>')
    for lab, ima, vhi, vlo in fb_rows:
        out.append(f'<tr><td>{html.escape(lab)}</td><td>{(f"{ima:.2f} mA" if ima >= 0.1 else f"{ima*1e3:.1f} µA")}</td><td>{vhi:.2f} V</td><td>{vlo:.3f} V</td></tr>')
    out.append('</tbody></table></div><p>Only the +24 V source with R3 puts the 5 mA minimum through the EH04-11N contact. Without R3, K1 closed would leave J5.12 floating, held low only by the board\'s 1 MΩ.</p>')

    colors = {"A": "var(--muted)", "B": "var(--dc)", "C": "var(--pe)", "D": "var(--l2)"}
    ser = [(decimate([(t * 1e3 - 2.0, v) for t, v in waves[(st, 1600e-12)] if 1.95e-3 <= t <= 3e-3]), colors[st], f"State {st}", False) for st in STATES]
    svg, leg = plot(ser, (-0.05, 1.0), (-13.5, 13.5), "Time (ms)", "CP voltage (V)", xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                    yticks=[-12, -6, 0, 3, 6, 9, 12], title="Control pilot waveform for states A to D at 1600 pF")
    out.append('<h3>Control pilot</h3><p>One period at a 66.7 % duty cycle (40 A), with 1600 pF on CP: the module\'s 300 pF plus 1300 pF of cable. '
               f'The source edge is assumed to be {EDGE*1e6:.0f} µs, since Pionix doesn\'t publish the module\'s slew rate.</p>')
    out.append(f'<div class="sheet"><div class="scroll">{svg}</div></div>{leg}')
    ser2 = []
    for c, dash in ((300e-12, True), (1600e-12, False)):
        ser2.append((decimate([((t - 2e-3) * 1e6, v) for t, v in waves[("C", c)] if 1.999e-3 <= t <= 2.02e-3], 800), "var(--pe)", f"State C, {c*1e12:.0f} pF", dash))
    svg2, leg2 = plot(ser2, (-1, 20), (-13.5, 8), "Time from rising edge (µs)", "CP voltage (V)", xticks=[0, 5, 10, 15, 20],
                      yticks=[-12, -6, 0, 6], title="Control pilot rising edge at 300 and 1600 pF")
    tr3, tr16 = cp_res[("C", 300e-12)][2], cp_res[("C", 1600e-12)][2]
    out.append(f'<p>Rising edge: 10–90 % takes {tr3*1e6:.1f} µs at 300 pF and {tr16*1e6:.1f} µs at 1600 pF.</p>')
    out.append(f'<div class="sheet"><div class="scroll">{svg2}</div></div>{leg2}')

    svg3, _ = plot([([(t, v) for t, v in curve], "var(--sig)", "", False)], (-40, 180), (0, 3.4), "PT1000 temperature (°C)", "INA333 output (V)",
                   xticks=list(range(-40, 181, 20)), yticks=[0, 0.5, 1, 1.5, 2.048, 2.5, 3, 3.3],
                   hlines=[(2.048, "ADC full scale 2.048 V")], yfmt="{:g}", title="PT1000 front-end transfer curve")
    out.append(f'<h3>PT1000 front end</h3><p>The bridge and INA333 (gain 30.1) reach the ADC\'s 2.048 V full scale at about {clip} °C, so set terminal alarms well below that. '
               f'0.1 % resistor tolerance alone gives up to ±{worst:.1f} °C error without calibration. INA333 offset and gain error aren\'t modelled.</p>')
    out.append(f'<div class="sheet"><div class="scroll">{svg3}</div></div>')
    out.append('<p class="hint">Not simulated: the K1 coil drive. TI publishes a PSpice model of the TPS27S100 (SLVMC96A), '
               'but the ESB63\'s electronic AC/DC coil isn\'t a plain inductor, so measure its inrush on the bench instead.</p>')
    return "\n".join(out)

CSS = """
.sim-svg{display:block;min-width:600px;width:100%;height:auto}
.sim-svg text{font-family:Barlow,"Segoe UI",Arial,sans-serif}
.sim-frame{fill:none;stroke:var(--ink);stroke-width:1}
.sim-grid{stroke:var(--grid);stroke-width:1}
.sim-ref{stroke:var(--warn);stroke-width:1;stroke-dasharray:4 3}
.sim-line{fill:none;stroke-width:1.8;stroke-linejoin:round}
.sim-tk{font-size:11px;fill:var(--muted)}
.sim-ax{font-size:12px;fill:var(--ink)}
table.sim-checks td:nth-child(2),table.sim-t td:nth-child(2){text-align:left}
table.sim-checks td:first-child,table.sim-t td:first-child{white-space:normal;font-weight:600}
.sim-pass{color:var(--pe);font-weight:600}
.sim-fail{color:var(--warn);font-weight:600}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="only run checks; don't write the HTML")
    args = ap.parse_args()
    if not NGSPICE:
        sys.exit("ngspice not found. Install it (Fedora: sudo dnf install ngspice; Debian/Ubuntu: sudo apt install ngspice).")
    emg = sim_emg(); fb = sim_fb(); cp = sim_cp(); ptr = sim_pt1000()
    w = max(len(c[1]) for c in CHECKS)
    for g, desc, val, ok in CHECKS:
        print(f"{'PASS' if ok else 'FAIL'}  {g:15} {desc:{w}}  {val}")
    failed = [c for c in CHECKS if not c[3]]
    print(f"\n{len(CHECKS) - len(failed)}/{len(CHECKS)} checks pass")
    if not args.check:
        p = ROOT / "cb-l2-evse.html"
        s = p.read_text()
        sec = build_section(emg, fb, cp, ptr)
        if '<h2 id="simulations">' in s:
            a = s.index('<h2 id="simulations">'); b = s.index('<h2 id="assembly">')
            s = s[:a] + sec + "\n\n" + s[b:]
        else:
            b = s.index('<h2 id="assembly">'); s = s[:b] + sec + "\n\n" + s[b:]
        if ".sim-svg{" not in s:
            s = s.replace("</style>", CSS + "</style>", 1)
        p.write_text(s)
        print(f"updated {p.relative_to(ROOT)}")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
