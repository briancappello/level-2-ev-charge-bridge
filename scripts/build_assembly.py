"""Generate the step-by-step assembly section for cb-l2-evse.html.

All geometry is in millimetres (1 SVG unit = 1 mm). The view is the inside of the
Polycase ZH-161407 base, looking at the back wall with the cover open.
Body outlines come from manufacturer datasheets (see data/dims/summary.md);
screw positions are approximate where the datasheet does not dimension them.
"""
import html
from pathlib import Path

W, H = 397.0, 346.0                    # enclosure interior
RAIL = {"U": 95.0, "L": 245.0}         # rail centre lines
RAIL_X0, RAIL_LEN = (W - 375) / 2, 375  # DR-62 rail, 375 mm

C = {}   # component id -> dict(x, y, w, h, label, sub, kind)
T = {}   # terminal name -> (x, y)

def comp(cid, x, rail, w, h, label, sub="", kind="dev"):
    y = RAIL[rail] - h / 2
    C[cid] = dict(x=x, y=y, w=w, h=h, label=label, sub=sub, kind=kind)
    return x + w

def term(name, x, y):
    T[name] = (x, y)

# ---- lower rail (power) -------------------------------------------------
x = 20.0
x = comp("clampL1", x, "L", 9.5, 50.5, "", kind="clamp")
for i, (nm, sub) in enumerate([("PE1", "cord G"), ("PE2", "J1772 PE"), ("PE3", "0 V bond")]):
    x0 = x; x = comp(nm, x, "L", 12.2, 55.5, nm, sub, kind="pe")
    term(f"{nm}.t", x0 + 6.1, RAIL["L"] - 20.75); term(f"{nm}.b", x0 + 6.1, RAIL["L"] + 20.75)
for i, (nm, sub) in enumerate([("TB1-1", "L1"), ("TB1-2", "L1 tap"), ("TB1-3", "L2"), ("TB1-4", "L2 tap"), ("TB1-5", "N")]):
    x0 = x; x = comp(nm, x, "L", 12.2, 55.5, nm.replace("TB1-", ""), sub, kind="ut")
    term(f"{nm}.t", x0 + 6.1, RAIL["L"] - 20.75); term(f"{nm}.b", x0 + 6.1, RAIL["L"] + 20.75)
x = comp("endcov", x, "L", 2.2, 55.5, "", kind="cover")
x = 140.0
comp("M1", x, "L", 36, 100, "M1", "SDM230", kind="dev")
m = C["M1"]
term("M1.1", x + 9, m["y"] + 7); term("M1.2", x + 27, m["y"] + 7)
term("M1.3", x + 9, m["y"] + 93); term("M1.4", x + 27, m["y"] + 93)
for n, dx in zip(range(5, 11), (3, 9, 15, 21, 27, 33)):
    term(f"M1.{n}", x + dx, m["y"] + 79)
x = 190.0
x = comp("AUX", x, "L", 9, 85, "", "", kind="dev")
a = C["AUX"]
term("AUX.21", a["x"] + 4.5, a["y"] + 7); term("AUX.33", a["x"] + 4.5, a["y"] + 15)
term("AUX.34", a["x"] + 4.5, a["y"] + 70); term("AUX.22", a["x"] + 4.5, a["y"] + 78)
x0 = x; x = comp("K1", x, "L", 54, 85, "K1", "ESB63-20N", kind="dev")
k = C["K1"]
for nm, dx in (("A1", 9), ("1", 27), ("3", 45)): term(f"K1.{nm}", x0 + dx, k["y"] + 7)
for nm, dx in (("A2", 9), ("2", 27), ("4", 45)): term(f"K1.{nm}", x0 + dx, k["y"] + 78)
x = comp("clampL2", x, "L", 9.5, 50.5, "", kind="clamp")

# ---- upper rail (control) ----------------------------------------------
x = 20.0
x = comp("clampU1", x, "U", 9.5, 50.5, "", kind="clamp")
x0 = x; x = comp("F12", x, "U", 35, 80, "F1/F2", "FAZ-C2/2", kind="dev")
f = C["F12"]
term("F.1", x0 + 8.75, f["y"] + 7); term("F.3", x0 + 26.25, f["y"] + 7)
term("F.2", x0 + 8.75, f["y"] + 73); term("F.4", x0 + 26.25, f["y"] + 73)
x = 70.0
comp("PS1", x, "U", 52.5, 90, "PS1", "HDR-60-24", kind="dev")
p = C["PS1"]
for nm, dx in (("-V1", 7), ("-V2", 16), ("+V1", 25), ("+V2", 34)): term(f"PS1.{nm}", x + dx, p["y"] + 7)
term("PS1.L", x + 7, p["y"] + 83); term("PS1.N", x + 16, p["y"] + 83)
x = 132.0
comp("UMPRO", x, "U", 123.8, 127.8, "", "", kind="housing")
u = C["UMPRO"]
BX, BY = x + (123.8 - 120) / 2, u["y"] + (127.8 - 108) / 2   # board origin
C["A1"] = dict(x=BX, y=BY, w=120, h=108, label="A1", sub="CB-EVAL v1.2", kind="board")
comp("clampU2", x + 123.8, "U", 9.5, 50.5, "", kind="clamp")

def jpin(conn, n):
    """Board terminal pin -> absolute (x, y) at the wire entry edge."""
    if conn == "J4": return (BX + 45.5 - (n - 1) * 3.5, BY + 4.6)
    if conn == "J5": return (BX + 90.5 - (n - 1) * 3.5, BY + 4.6)
    if conn == "J7": return (BX + 7 + (n - 1) * 3.5, BY + 103.4)
    if conn == "J11": return (BX + 52 + (n - 1) * 3.5, BY + 103.4)
for n in range(1, 13):
    for j in ("J4", "J5", "J7", "J11"): T[f"{j}.{n}"] = jpin(j, n)
T["RJ45"] = (BX + 120, BY + 46)

# ---- wall features --------------------------------------------------------
GL = {"G1": (85.0, "M40", 40.0, "14-50 cord"), "G2": (226.0, "M40", 40.0, "J1772 cable"),
      "G3": (350.0, "M20", 20.0, "Ethernet")}
S2_POS = (W, RAIL["U"])

# ---- wires ------------------------------------------------------------------
# (step, colour-class, width, label, points)
WIRES = []
def wire(step, cls, wdt, pts, label="", lp=None):
    WIRES.append(dict(step=step, cls=cls, w=wdt, pts=pts, label=label, lp=lp))
def P(name): return T[name]
AWG8, AWG18 = 3.0, 1.3

# step 4: power path (8 AWG)
g1, g2 = GL["G1"][0], GL["G2"][0]
wire(4, "pe", AWG8, [(g1 - 4, H), (g1 - 4, 326), (P("PE1.b")[0], 326), P("PE1.b")], "G")
wire(4, "l1", AWG8, [(g1 - 1, H), (g1 - 1, 320), (P("TB1-1.b")[0], 320), P("TB1-1.b")], "L1")
wire(4, "l2", AWG8, [(g1 + 2, H), (g1 + 2, 313), (P("TB1-3.b")[0], 313), P("TB1-3.b")], "L2")
wire(4, "n", AWG8, [(g1 + 5, H), (g1 + 5, 306), (P("TB1-5.b")[0], 306), P("TB1-5.b")], "N")
wire(4, "pe", AWG8, [P("PE1.t"), (P("PE1.t")[0], 214), (P("PE2.t")[0], 214), P("PE2.t")], "")
wire(4, "l1", AWG8, [P("TB1-1.t"), (P("TB1-1.t")[0], 180), (P("M1.1")[0], 180), P("M1.1")], "")
wire(4, "l1", AWG8, [P("M1.2"), (P("M1.2")[0], 186), (P("K1.1")[0], 186), P("K1.1")], "")
wire(4, "l2", AWG8, [P("TB1-3.t"), (P("TB1-3.t")[0], 192), (P("K1.3")[0], 192), P("K1.3")], "")
wire(4, "l1", AWG8, [(g2, H), P("K1.2")], "L1")
wire(4, "l2", AWG8, [(g2 + 5, H), (g2 + 5, 318), (P("K1.4")[0], 318), P("K1.4")], "L2")
wire(4, "pe", AWG8, [(g2 - 5, H), (g2 - 5, 300), (P("PE2.b")[0], 300), P("PE2.b")], "PE")

# step 5: control supply (18 AWG)
wire(5, "l1", AWG18, [P("TB1-2.t"), (P("TB1-2.t")[0], 170), (14, 170), (14, 42), (P("F.1")[0], 42), P("F.1")])
wire(5, "l2", AWG18, [P("TB1-4.t"), (P("TB1-4.t")[0], 174), (9, 174), (9, 36), (P("F.3")[0], 36), P("F.3")])
wire(5, "l1", AWG18, [P("F.2"), (P("F.2")[0], 146), (P("PS1.L")[0], 146), P("PS1.L")])
wire(5, "l2", AWG18, [P("F.4"), (P("F.4")[0], 150), (P("PS1.N")[0], 150), P("PS1.N")])
wire(5, "l2", AWG18, [P("F.4"), (P("F.4")[0] + 2, 154), (133.5, 154), (133.5, 302), (P("M1.3")[0], 302), P("M1.3")], "M1 N ref")
wire(5, "dc", AWG18, [P("PS1.+V1"), (P("PS1.+V1")[0], 44), (127, 44), (127, 166), (P("J7.11")[0], 166), P("J7.11")], "+24 V")
wire(5, "z", AWG18, [P("PS1.-V1"), (P("PS1.-V1")[0], 40), (129.5, 40), (129.5, 162), (P("J7.12")[0], 162), P("J7.12")], "0 V")
wire(5, "pe", AWG18, [P("PS1.-V2"), (P("PS1.-V2")[0], 48), (67, 48), (67, 210), (P("PE3.t")[0], 210), P("PE3.t")], "0 V–PE bond")

# step 6: control signals
wire(6, "dc", AWG18, [P("J5.10"), (P("J5.10")[0], 28), (270, 28), (270, 197), (P("K1.A1")[0], 197), P("K1.A1")])
wire(6, "z", AWG18, [P("K1.A2"), (P("K1.A2")[0], 296), (274, 296), (274, 24), (P("J5.9")[0], 24), P("J5.9")])
wire(6, "dc", AWG18, [P("PS1.+V2"), (P("PS1.+V2")[0], 32), (278, 32), (278, 201), (P("AUX.21")[0], 201), P("AUX.21")])
wire(6, "sig", AWG18, [P("AUX.22"), (P("AUX.22")[0], 300), (282, 300), (282, 20), (P("J5.12")[0], 20), P("J5.12")])
wire(6, "com", 1.8, [((P("M1.5")[0] + P("M1.6")[0]) / 2, P("M1.5")[1]), ((P("M1.5")[0] + P("M1.6")[0]) / 2, 322), (290, 322), (290, 16),
                     ((P("J4.8")[0] + P("J4.7")[0]) / 2, 16), ((P("J4.8")[0] + P("J4.7")[0]) / 2, P("J4.7")[1])], "RS-485 pair", (165, 320))
wire(6, "sig", AWG18, [(g2 + 2, H), (g2 + 2, 338), (258, 338), (258, 160), (P("J11.6")[0], 160), P("J11.6")], "CP", (238, 159))
wire(6, "sig", AWG18, [(C["K1"]["x"] + 36, 262), (262, 262), (262, 156), ((P("J11.2")[0] + P("J11.3")[0]) / 2, 156),
                       ((P("J11.2")[0] + P("J11.3")[0]) / 2, P("J11.2")[1])])
wire(6, "sig", AWG18, [(g2 - 6, H - 14), (g2 - 6, 332), (266, 332), (266, 152), ((P("J11.4")[0] + P("J11.5")[0]) / 2, 152),
                       ((P("J11.4")[0] + P("J11.5")[0]) / 2, P("J11.4")[1])])
wire(6, "sig", AWG18, [S2_POS, (300, S2_POS[1]), (300, 12), ((P("J4.10")[0] + P("J4.9")[0]) / 2, 12),
                       ((P("J4.10")[0] + P("J4.9")[0]) / 2, P("J4.10")[1])], "S2 pair", (330, 93))
wire(7, "com", 2.4, [T["RJ45"], (GL["G3"][0], T["RJ45"][1]), (GL["G3"][0], H)], "Ethernet")

# ---- rendering ------------------------------------------------------------------
STROKE = {"l1": "var(--l1)", "l2": "var(--l2)", "n": "var(--muted)", "pe": "var(--pe)", "dc": "var(--dc)",
          "z": "var(--dc)", "sig": "var(--sig)", "com": "var(--com)"}

def r(v): return f"{v:.1f}".rstrip("0").rstrip(".")

def draw_comp(cid, state):
    c = C[cid]; x, y, w, h = c["x"], c["y"], c["w"], c["h"]
    cls = {"new": "as-new", "old": "as-old"}[state]
    k = c["kind"]
    out = []
    if k == "clamp":
        out.append(f'<rect class="{cls} as-clamp" x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}" rx="1"/>')
    elif k == "cover":
        out.append(f'<rect class="{cls}" x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}"/>')
    elif k == "housing":
        out.append(f'<rect class="{cls} as-housing" x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}" rx="3"/>')
    elif k == "board":
        out.append(f'<rect class="{cls} as-board" x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}" rx="2"/>')
        for j, (bx, by) in (("J4", (5, 4.55)), ("J5", (50, 4.55)), ("J7", (3.5, 91)), ("J11", (48.5, 91))):
            out.append(f'<rect class="as-tb" x="{r(x+bx)}" y="{r(y+by)}" width="44" height="12.5"/>')
            out.append(f'<text class="as-t" x="{r(x+bx+22)}" y="{r(y+by+8.3)}" text-anchor="middle">{j}</text>')
        out.append(f'<rect class="as-tb" x="{r(x+98.4)}" y="{r(y+37.3)}" width="16.2" height="18"/>'
                   f'<text class="as-t" x="{r(x+106.5)}" y="{r(y+48)}" text-anchor="middle">RJ45</text>')
        out.append(f'<rect class="as-tb" x="{r(x+3.6)}" y="{r(y+67)}" width="11.5" height="10"/>'
                   f'<text class="as-t" x="{r(x+18)}" y="{r(y+74)}">J10 24 V jack</text>')
        out.append(f'<rect class="as-tb" x="{r(x+78.2)}" y="{r(y+42.8)}" width="8.9" height="22.4"/>'
                   f'<text class="as-t" x="{r(x+70)}" y="{r(y+72)}" text-anchor="middle">module</text>')
        for sx in (9, 16.5, 24, 31.5):
            out.append(f'<rect class="as-tb" x="{r(x+sx-3.25)}" y="{r(y+40.75)}" width="6.5" height="8.5"/>')
        out.append(f'<text class="as-t" x="{r(x+6)}" y="{r(y+38)}">SW2 E-stop · SW1 stop</text>'.replace(" · ", ", "))
        out.append(f'<text class="as-lbl" x="{r(x+60)}" y="{r(y+60)}" text-anchor="middle">A1</text>')
        out.append(f'<text class="as-t" x="{r(x+60)}" y="{r(y+86)}" text-anchor="middle">CB-EVAL 120 × 108</text>')
        return "".join(out)
    else:
        extra = " as-pe" if k == "pe" else ""
        out.append(f'<rect class="{cls}{extra}" x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}" rx="1.5"/>')
    if k in ("ut", "pe"):
        for yy in (RAIL["L"] - 20.75, RAIL["L"] + 20.75):
            out.append(f'<circle class="as-screw" cx="{r(x+w/2)}" cy="{r(yy)}" r="3.2"/>')
        out.append(f'<text class="as-t" x="{r(x+w/2)}" y="{r(RAIL["L"]-9)}" text-anchor="middle">{html.escape(c["label"])}</text>')
        if c["sub"]:
            out.append(f'<text class="as-t as-sub" transform="translate({r(x+w/2+1.5)} {r(RAIL["L"]+15)}) rotate(-90)">{html.escape(c["sub"])}</text>')
    elif k == "dev":
        if c["label"]:
            out.append(f'<text class="as-lbl" x="{r(x+w/2)}" y="{r(y+h/2-1)}" text-anchor="middle">{html.escape(c["label"])}</text>')
            out.append(f'<text class="as-t" x="{r(x+w/2)}" y="{r(y+h/2+7)}" text-anchor="middle">{html.escape(c["sub"])}</text>')
    return "".join(out)

def draw_terms(ids):
    pref = {"M1": "M1.", "K1": "K1.", "AUX": "AUX.", "F12": "F.", "PS1": "PS1."}
    out = []
    for cid in ids:
        if cid not in pref: continue
        for name, (tx, ty) in T.items():
            if name.startswith(pref[cid]):
                lab = name.split(".", 1)[1].replace("-V1", "−V").replace("-V2", "−V").replace("+V1", "+V").replace("+V2", "+V")
                rad = 1.6 if (cid == "M1" and lab in "5678910" and len(lab) <= 2 and lab not in ("1", "2", "3", "4")) else 2.8
                out.append(f'<circle class="as-screw" cx="{r(tx)}" cy="{r(ty)}" r="{rad}"/>')
                dy = -4.5 if ty < C[cid]["y"] + C[cid]["h"] / 2 else 8
                if cid == "M1" and rad < 2: dy = -3
                if cid == "AUX":
                    out.append(f'<text class="as-t" x="{r(tx-5)}" y="{r(ty+1.8)}" text-anchor="end">{html.escape(lab)}</text>')
                    continue
                out.append(f'<text class="as-t" x="{r(tx)}" y="{r(ty+dy)}" text-anchor="middle">{html.escape(lab)}</text>')
    return "".join(out)

def draw_wire(wd, state):
    d = "M" + " L".join(f"{r(a)} {r(b)}" for a, b in wd["pts"])
    dash = ' stroke-dasharray="4 2.5"' if wd["cls"] == "z" else ""
    if state == "old":
        return f'<path class="as-wire-old" d="{d}" stroke-width="{r(min(wd["w"], 1.6))}"/>'
    out = f'<path class="as-wire" d="{d}" stroke="{STROKE[wd["cls"]]}" stroke-width="{r(wd["w"])}"{dash}/>'
    for a, b in (wd["pts"][0], wd["pts"][-1]):
        out += f'<circle cx="{r(a)}" cy="{r(b)}" r="{r(wd["w"]*0.55+0.6)}" fill="{STROKE[wd["cls"]]}"/>'
    return out

def frame(extra_h=0):
    s = [f'<rect class="as-encl" x="0" y="0" width="{W}" height="{H}" rx="6"/>']
    for k, v in RAIL.items():
        s.append(f'<rect class="as-rail" x="{r(RAIL_X0)}" y="{r(v-17.5)}" width="{RAIL_LEN}" height="35"/>')
    # glands on bottom wall
    for gid, (gx, size, dia, lab) in GL.items():
        s.append(f'<rect class="as-gland" x="{r(gx-dia/2-3)}" y="{H}" width="{r(dia+6)}" height="12" rx="2"/>')
        s.append(f'<text class="as-t" x="{r(gx)}" y="{H+20}" text-anchor="middle">{size}: {lab}</text>')
    s.append(f'<rect class="as-gland" x="{W}" y="{r(S2_POS[1]-11.25)}" width="9" height="22.5" rx="2"/>'
             f'<text class="as-t" x="{W+12}" y="{r(S2_POS[1]+2)}">S2</text>')
    # scale bar
    s.append(f'<path class="as-scale" d="M10 {H+42} h100 M10 {H+38} v8 M60 {H+40} v4 M110 {H+38} v8"/>'
             f'<text class="as-t" x="115" y="{H+45}">100 mm</text>')
    return "".join(s)

ORDER = ["clampL1", "PE1", "PE2", "PE3", "TB1-1", "TB1-2", "TB1-3", "TB1-4", "TB1-5", "endcov", "M1", "AUX", "K1", "clampL2"]
UPPER = ["clampU1", "F12", "PS1", "UMPRO", "A1", "clampU2"]

def svg(step, comps_new, comps_old, title, extra=""):
    body = [frame()]
    for cid in comps_old: body.append(draw_comp(cid, "old"))
    for cid in comps_new: body.append(draw_comp(cid, "new"))
    body.append(draw_terms(comps_old + comps_new))
    if step >= 4:
        for wd in WIRES:
            if wd["step"] < step: body.append(draw_wire(wd, "old"))
        for wd in WIRES:
            if wd["step"] == step:
                body.append(draw_wire(wd, "new"))
                if wd["label"]:
                    lx, ly = wd["lp"] or (wd["pts"][-2] if len(wd["pts"]) > 2 else wd["pts"][0])
                    body.append(f'<text class="as-wl" x="{r(lx+2)}" y="{r(ly-1.5)}" fill="{STROKE[wd["cls"]]}">{html.escape(wd["label"])}</text>')
    if step >= 4:
        body.append('<path class="as-bridge" d="M{a} {y} H{b} M{c} {y} H{d}"/>'.format(
            a=r(P("TB1-1.t")[0]), b=r(P("TB1-2.t")[0]), c=r(P("TB1-3.t")[0]), d=r(P("TB1-4.t")[0]), y=r(RAIL["L"] - 8)))
    body.append(extra)
    return (f'<svg class="as-svg" viewBox="-12 -14 {W+48} {H+66}" role="img" aria-label="{html.escape(title)}">'
            + "".join(body) + "</svg>")

STEPS = []
def step(n, title, text_html, svg_html=None):
    STEPS.append((n, title, text_html, svg_html))

# Step 1
s1_extra = ""
for k, v in RAIL.items():
    s1_extra += f'<text class="as-t" x="{r(RAIL_X0+3)}" y="{r(v+2)}">DR-62 rail, {RAIL_LEN} mm</text>'
s1_extra += (f'<path class="as-dim" d="M{W+24} {RAIL["U"]} V{RAIL["L"]} M{W+20} {RAIL["U"]} h8 M{W+20} {RAIL["L"]} h8"/>'
             f'<text class="as-t" transform="translate({W+31} {r((RAIL["U"]+RAIL["L"])/2)}) rotate(90)" text-anchor="middle">150 mm</text>'
             f'<path class="as-dim" d="M0 -4 H{W} M0 -7 v6 M{W} -7 v6"/><text class="as-t" x="{W/2}" y="-7" text-anchor="middle">397 mm inside</text>')
for gid, (gx, size, dia, lab) in GL.items():
    s1_extra += f'<text class="as-t" x="{r(gx)}" y="{H+28}" text-anchor="middle">{r(gx)} mm from left</text>'
step(1, "Prepare the enclosure",
     """<ol>
<li>Hold a DR-62 rail across the base on the mounting bosses. Rail centre lines are drawn 150 mm apart, at 95 mm and 245 mm from the top inside wall. <span class="verify">Check that the ZH-161407 base has bosses for both rails before drilling anything. If it only has centred bosses, use the ZX-1614K internal panel and screw both rails to it.</span></li>
<li>Drill the bottom wall for the glands: two M40 holes (about 40.5 mm) and one M20 hole (about 20.5 mm). Put the centres 40 mm out from the base and at 85 mm, 226 mm and 350 mm from the left inside wall. The M40 lock nuts are 50 mm across, so keep the centres at least 55 mm apart.</li>
<li>Drill a 22.5 mm hole in the right wall for S2, level with the upper rail and 100 mm out from the base. The button needs 43 mm of depth behind the wall.</li>
<li>Fit the glands and S2, then fit both rails. The drill sizes are the usual thread size plus 0.5 mm; Bimed doesn't publish a clearance hole size.</li>
</ol>""",
     svg(1, [], [], "Enclosure interior with rails, gland holes and S2 hole", s1_extra))

# Step 2
step(2, "Fit the lower (power) rail",
     """<ol>
<li>Snap parts onto the lower rail from left to right: an end clamp, three UT 16-PE terminals (PE1–PE3), five UT 16 terminals (TB1-1 to TB1-5), then an end cover on the open side of TB1-5.</li>
<li>Plug one FBS 2-12 bridge into TB1-1/TB1-2 and another into TB1-3/TB1-4. TB1-5 (N) stays unbridged and isolated.</li>
<li>Leave a gap of about 11 mm, then snap on M1, the SDM230 meter.</li>
<li>Clip the EH04-11N aux contact onto the left side of K1, then snap K1 on with the aux on the left. Finish the rail with an end clamp. The lower rail uses about 243 of its 375 mm.</li>
</ol>""",
     svg(2, ORDER, [], "Lower rail populated: PE terminals, TB1, meter, contactor with aux"))

# Step 3
step(3, "Fit the upper (control) rail",
     """<ol>
<li>Screw the CB-EVAL board into the UM-PRO housing base with the board's J4/J5 edge toward the top. <span class="verify">Check which way Phoenix's drawing puts the 120 mm board side relative to the rail; it's drawn here with 120 mm along the rail.</span> Cut the right side element for the RJ45 jack, and the left one for the J10 24 V jack, which you'll need in step 9.</li>
<li>Snap parts onto the upper rail from left to right: an end clamp, F1/F2 (the 2-pole FAZ), PS1, the board housing, then an end clamp.</li>
<li>Switch F1/F2 off and leave it off until step 10.</li>
</ol>""",
     svg(3, UPPER, ORDER, "Upper rail populated: breaker, 24 V supply, board in housing"))

# Step 4
step(4, "Wire the power path (8 AWG)",
     """<ol>
<li>Pass the 14-50 cord through the left M40 gland. Land G on PE1, L1 on TB1-1, L2 on TB1-3 and N on TB1-5, all on the bottom screws. N stops at TB1-5 and is never connected to PE.</li>
<li>Run an 8 AWG green jumper from the top of PE1 to the top of PE2.</li>
<li>Run 8 AWG black from TB1-1 (top) to M1 terminal 1, and from M1 terminal 2 to K1 terminal 1. Run 8 AWG red from TB1-3 (top) to K1 terminal 3. L2 doesn't pass through the meter.</li>
<li>Pass the J1772 cable through the right M40 gland. Land L1 on K1 terminal 2, L2 on K1 terminal 4, and PE on PE2 (bottom).</li>
<li>Crimp ferrules on every stranded end and tighten each screw to the torque on its datasheet. Tighten the glands last, once the conductors are dressed.</li>
</ol>""",
     svg(4, [], ORDER + UPPER, "Power wiring: cord to TB1, through meter and contactor, out to J1772 cable"))

# Step 5
step(5, "Wire the 24 V supply (18 AWG)",
     """<ol>
<li>Run 18 AWG black from TB1-2 (top) to F1/F2 terminal 1, and 18 AWG red from TB1-4 (top) to terminal 3. The bridges make these taps of L1 and L2.</li>
<li>Run black from F1/F2 terminal 2 to PS1 L, and red from terminal 4 to PS1 N. PS1 has no earth terminal.</li>
<li>Run a second red from F1/F2 terminal 4 to M1 terminal 3, the meter's voltage reference. This keeps the meter's sense lead behind the 2 A breaker.</li>
<li>Run 18 AWG blue from PS1 +V to J7.11 and blue/white from PS1 −V to J7.12.</li>
<li>Run 18 AWG green from PS1's second −V terminal to PE3 (top). This is the single 0 V–PE bond the control pilot needs.</li>
</ol>""",
     svg(5, [], ORDER + UPPER, "Control supply wiring: taps through F1/F2 to PS1, meter reference, 24 V to the board, 0 V bond"))

# Step 6
r3 = P("J5.12"), P("J5.9")
s6_extra = (f'<rect class="as-res" x="{r(r3[0][0])}" y="{r(r3[0][1]-11)}" width="{r(r3[1][0]-r3[0][0])}" height="4" rx="1"/>'
            f'<text class="as-t" x="{r((r3[0][0]+r3[1][0])/2)}" y="{r(r3[0][1]-13)}" text-anchor="middle">R3</text>')
tt = C["K1"]
s6_extra += (f'<rect x="{r(tt["x"]+33)}" y="258" width="7" height="8" fill="var(--sheet)" stroke="var(--sig)" stroke-width="1"/>'
             f'<text class="as-t" x="{r(tt["x"]+44)}" y="265">TT1</text>'
             f'<rect x="{r(GL["G2"][0]-13)}" y="{H-18}" width="7" height="8" fill="var(--sheet)" stroke="var(--sig)" stroke-width="1"/>'
             f'<text class="as-t" x="{r(GL["G2"][0]-33)}" y="{H-12}">TT2</text>')
step(6, "Wire the control signals",
     """<ol>
<li><strong>Contactor coil:</strong> run J5.10 to K1 A1, and K1 A2 to J5.9.</li>
<li><strong>Weld detection:</strong> run PS1's second +V terminal to aux 21, and aux 22 to J5.12. Put R3 (3.3 kΩ) across J5.12 and J5.9, sharing each screw with the wire in a twin ferrule.</li>
<li><strong>Meter:</strong> run the Belden 9841 pair from M1 terminals 5 (A) and 6 (B) to J4.8 (A) and J4.7 (B). Tie the shield to M1 terminal 7 at the meter end only.</li>
<li><strong>Pilot:</strong> run the J1772 cable's CP conductor to J11.6. If the cable has a latch-sense conductor, land it on J11.7. Keep these runs away from the 8 AWG conductors.</li>
<li><strong>Temperature:</strong> stick TT1 on K1's body beside terminals 2/4 and wire it to J11.2/J11.3. Stick TT2 on the J1772 cable jacket just inside the gland and wire it to J11.4/J11.5. Neither lead goes to ground.</li>
<li><strong>Stop button:</strong> wire S2's NO contact to J4.10 and J4.9.</li>
<li><strong>Not used:</strong> leave J4.11 (EMG IN), J11.8 (ZC) and the HV inputs J1/J6 unconnected. To fit the optional E-stop, follow Sheet 2.</li>
</ol>""",
     svg(6, [], ORDER + UPPER, "Control signal wiring: coil, feedback, RS-485, pilot, temperature sensors, stop button", s6_extra))

# Step 7
step(7, "Connect the PC and configure EVerest",
     """<ol>
<li>Pass the Ethernet cable through the M20 gland, then crimp the RJ45 plug and plug it into the board.</li>
<li>On the PC, give the cable's interface a static address and run a DHCP server on it, for example <code>dnsmasq --interface=eth1 --bind-interfaces --dhcp-range=192.168.50.100,192.168.50.150,12h</code>. Find the module with <code>avahi-browse _chargebridge._udp -tr</code>.</li>
<li>In the EVerest config, set the maximum current to 40 A. Leave the relay 1 feedback polarity at its default (high = open). Set up the SDM230 on <code>/dev/cbserial0</code> at Modbus address 1, 9600 8N1, and set PT1000 limits for both channels.</li>
</ol>""",
     svg(7, [], ORDER + UPPER, "Ethernet cable routed from the RJ45 jack to the M20 gland"))

# Step 8
step(8, "Check it with the power off",
     """<ol>
<li>With the 14-50 plug out, check continuity from the plug's G pin to PE1, PE2, PE3, the J1772 PE pin and J7.12 (0 V, through the bond).</li>
<li>Check that N isn't connected to PE, and that TB1-5 shows no continuity to L1, L2 or PE.</li>
<li>Tug-test every conductor, and check that no copper shows outside a terminal or ferrule.</li>
<li>With F1/F2 off and K1 open, megger L1 and L2 to PE at 500 V DC. Expect well over 1 MΩ. The meter is still connected, so keep the test short.</li>
</ol>""")

# Step 9
step(9, "Bring it up on 24 V only",
     """<ol>
<li>Keep the 14-50 unplugged and F1/F2 off. Plug the 24 V supply that came with the Pionix kit into J10.</li>
<li>Check that the PC finds the module and that EVerest starts.</li>
<li>Plug the J1772 handle into an EV simulator. In state B (2.74 kΩ + diode), the pilot should read +9 V and then show a 66.7% duty cycle. In state C (with 1.3 kΩ added), K1 should pull in with an audible click, feedback 1 should read closed, and TT1/TT2 should read room temperature.</li>
<li>Press S2: K1 should drop out. Pull the handle out: the session should end.</li>
<li>Unplug the J10 supply.</li>
</ol>""")

# Step 10
step(10, "First run on 240 V",
     """<ol>
<li>Close the cover. Plug into the 14-50 and press the receptacle breaker's GFCI test button. It must trip; reset it.</li>
<li>Switch F1/F2 on. PS1 should come up, then the board and EVerest.</li>
<li>Repeat the simulator test. In state C, measure about 240 V between L1 and L2 at the simulator, and 0 V when it leaves state C.</li>
<li>Charge a car. Watch K1 and TT1 temperatures and the meter's current for the first hour at 40 A.</li>
</ol>""")

parts = ['<h2 id="assembly">Assembly</h2>',
         '<p class="hint">Drawings are to scale at 1 mm per unit, looking into the enclosure base with the cover open. '
         'Part outlines come from manufacturer datasheets. Screw positions on K1, the aux contact and the meter are approximate, '
         'so check them against the labels on your parts. Parts and wires added in each step are drawn in colour; earlier ones are grey.</p>']
for n, title, text_html, svg_html in STEPS:
    parts.append(f'<section class="as-step"><h3>Step {n}: {html.escape(title)}</h3><div class="as-body">{text_html}</div>')
    if svg_html:
        parts.append(f'<div class="sheet"><div class="scroll">{svg_html}</div></div>')
    parts.append('</section>')
SECTION = "\n".join(parts)

CSS = """
.as-step{margin-top:8px}
.as-step h3{margin-top:36px}
.as-body ol{max-width:76ch;padding-left:1.3em}
.as-body li{margin:.3em 0}
.as-svg{display:block;min-width:820px;width:100%;height:auto}
.as-svg text{font-family:Barlow,"Segoe UI",Arial,sans-serif;fill:var(--ink)}
.as-t{font-size:5px;fill:var(--muted)}
.as-sub{font-size:4.2px}
.as-lbl{font-size:8px;font-weight:700}
.as-wl{font-size:5.5px;font-weight:600}
.as-encl{fill:var(--grid);stroke:var(--ink);stroke-width:1.6}
.as-rail{fill:none;stroke:var(--muted);stroke-width:.8;stroke-dasharray:3 2}
.as-new{fill:var(--sheet);stroke:var(--dc);stroke-width:1.2}
.as-old{fill:var(--sheet);stroke:var(--rule);stroke-width:.9}
.as-pe.as-new{stroke:var(--pe)}
.as-clamp{fill:var(--rule)}
.as-housing{fill:none;stroke-dasharray:4 2}
.as-board{fill:var(--grid)}
.as-tb{fill:var(--sheet);stroke:var(--muted);stroke-width:.6}
.as-screw{fill:var(--sheet);stroke:var(--ink);stroke-width:.6}
.as-gland{fill:var(--sheet);stroke:var(--ink);stroke-width:1}
.as-scale,.as-dim{fill:none;stroke:var(--ink);stroke-width:.7}
.as-wire{fill:none;stroke-linecap:round;stroke-linejoin:round}
.as-wire-old{fill:none;stroke:var(--rule);stroke-linecap:round;stroke-linejoin:round}
.as-bridge{stroke:var(--l2);stroke-width:2.2;stroke-linecap:round;opacity:.7}
.as-res{fill:var(--sheet);stroke:var(--sig);stroke-width:.8}
"""

p = str(Path(__file__).resolve().parent.parent / "cb-l2-evse.html")
s = open(p).read()
if '<h2 id="assembly">' in s:
    a = s.index('<h2 id="assembly">'); b = s.index('<div class="callout">')
    s = s[:a] + SECTION + "\n\n" + s[b:]
else:
    b = s.index('<div class="callout">')
    s = s[:b] + SECTION + "\n\n" + s[b:]
if ".as-step{" not in s:
    s = s.replace("</style>", CSS + "</style>", 1)
open(p, "w").write(s)
print("steps:", len(STEPS), "lower rail end:", round(C["clampL2"]["x"] + 9.5, 1), "upper rail end:", round(C["clampU2"]["x"] + 9.5, 1))
