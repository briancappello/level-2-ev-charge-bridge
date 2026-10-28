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
x0 = x; x = comp("K1", x, "L", 53.5, 95.8, "K1", "Finder 22.64", kind="dev")   # 4-pole, poles 1-2 and 3-4 used
k = C["K1"]
for nm, dx in (("A1", 5), ("1", 15), ("3", 26), ("5", 37), ("7", 48)): term(f"K1.{nm}", x0 + dx, k["y"] + 7)
for nm, dx in (("A2", 5), ("2", 15), ("4", 26), ("6", 37), ("8", 48)): term(f"K1.{nm}", x0 + dx, k["y"] + k["h"] - 7)
x = comp("AUX", x, "L", 8.8, 90, "", "", kind="dev")                       # Finder 022.65: NC 21-22, NO 33-34
a = C["AUX"]
term("AUX.21", a["x"] + 4.4, a["y"] + 7); term("AUX.33", a["x"] + 4.4, a["y"] + 14)
term("AUX.34", a["x"] + 4.4, a["y"] + 76); term("AUX.22", a["x"] + 4.4, a["y"] + 83)
x = comp("clampL2", x, "L", 9.5, 50.5, "", kind="clamp")
# RCM1 support parts on the right end of the lower rail (clear of the wire lanes at x 258-290)
x = 294.0
x = comp("clampL3", x, "L", 9.5, 50.5, "", kind="clamp")
x0 = x; x = comp("PS2", x, "L", 17.5, 90, "PS2", "12 V", kind="dev")          # Mean Well DDR-15G-12, 17.5 x 90 mm
p2 = C["PS2"]
term("PS2.+Vo", x0 + 5, p2["y"] + 7); term("PS2.-Vo", x0 + 12.5, p2["y"] + 7)       # pins 1, 2 on top
term("PS2.-Vin", x0 + 5, p2["y"] + 83); term("PS2.+Vin", x0 + 12.5, p2["y"] + 83)   # pins 3, 4 on the bottom
x0 = x; x = comp("K2", x, "L", 6.2, 87.8, "", "", kind="dev")                 # Finder 38.51, 6.2 x 87.8 mm
k2 = C["K2"]
term("K2.A1", x0 + 3.1, k2["y"] + 6); term("K2.A2", x0 + 3.1, k2["y"] + 13)
term("K2.11", x0 + 3.1, k2["y"] + k2["h"] - 20); term("K2.12", x0 + 3.1, k2["y"] + k2["h"] - 13); term("K2.14", x0 + 3.1, k2["y"] + k2["h"] - 6)
x = comp("clampL4", x, "L", 9.5, 50.5, "", kind="clamp")
# RCM14-04: 46.7 x 32.5 mm seen from the front with its 14 mm aperture vertical, J1772 L1/L2 pass through it
C["RCM1"] = dict(x=210 - 46.7 / 2, y=299.5, w=46.7, h=32.5, label="RCM1", sub="RCM14-04", kind="rcm")
for n, dx in ((4, 34.4), (3, 36.9), (2, 39.4), (1, 41.9)):   # JST XH, 2.5 mm pitch, pin 4 nearest the aperture
    T[f"RCM.{n}"] = (C["RCM1"]["x"] + dx, C["RCM1"]["y"])

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
GL = {"G1": (85.0, "M40", 40.0, "14-50 cord"), "G2": (210.0, "M40", 40.0, "J1772 cable"),
      "G3": (350.0, "M20", 20.0, "Ethernet")}
S2_POS = (W, RAIL["U"])
S1_POS = (W, 175.0)        # E-stop, 80 mm below S2 on the right wall
S2_BODY = (43, 30)          # depth behind wall, width (Schneider XB5AA31: 43 mm behind panel, 30 mm body)
S1_BODY = (45, 30)          # AutomationDirect GCX3131 with two contact blocks side by side: 45 mm behind panel
H1_POS = (W, 40.0)         # pilot light, above S2
S3_POS = (W, 245.0)        # RCM1 test button, below S1
H1_BODY = (40, 30)         # AutomationDirect ECX2052-24L (depth approximate)
S3_BODY = (45, 30)         # AutomationDirect GCX1100, one contact layer
S1T = {"a.1": (W - 41, S1_POS[1] - 11), "a.2": (W - 41, S1_POS[1] - 4), "b.1": (W - 41, S1_POS[1] + 4), "b.2": (W - 41, S1_POS[1] + 11)}

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
wire(4, "l1", AWG8, [(207, H), (207, 297), (P("K1.2")[0], 297), P("K1.2")], "L1", (196, 343))
wire(4, "l2", AWG8, [(213, H), (213, 297), (P("K1.4")[0], 297), P("K1.4")], "L2", (215, 343))
wire(4, "pe", AWG8, [(198, H), (198, 340), (181, 340), (181, 303), (P("PE2.b")[0], 303), P("PE2.b")], "PE", (160, 302))

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
wire(7, "dc", AWG18, [P("J5.10"), (P("J5.10")[0], 28), (340, 28), (340, S1T["a.1"][1]), S1T["a.1"]], "coil+ via S1-a", (300, 27))
wire(7, "dc", AWG18, [S1T["a.2"], (330, S1T["a.2"][1]), (330, 178), (P("K1.A1")[0], 178), P("K1.A1")])
wire(7, "dc", AWG18, [P("PS1.+V2"), (P("PS1.+V2")[0], 50), (107, 50), (107, 4), (346, 4), (346, S1T["b.1"][1]), S1T["b.1"]])
wire(7, "sig", AWG18, [S1T["b.2"], (338, S1T["b.2"][1]), (338, P("K2.11")[1]), P("K2.11")], "S1-b to K2", (339, 228))
wire(7, "sig", AWG18, [P("K2.14"), (344, P("K2.14")[1]), (344, 8), (P("J4.11")[0], 8), (P("J4.11")[0], 20)], "K2 to R1", (300, 7))
wire(7, "z", AWG18, [P("K1.A2"), (P("K1.A2")[0], 296), (274, 296), (274, 24), (P("J5.9")[0], 24), P("J5.9")])
wire(7, "dc", AWG18, [P("PS1.+V1"), (P("PS1.+V1")[0], 44), (127, 44), (127, 166), (296, 166), (296, 297), (P("PS2.+Vin")[0], 297), P("PS2.+Vin")], "PS2 +24 V in", (230, 165))
wire(7, "z", AWG18, [P("PS1.-V1"), (P("PS1.-V1")[0], 40), (129.5, 40), (129.5, 162), (300, 162), (300, 293), (P("PS2.-Vin")[0], 293), P("PS2.-Vin")])
wire(7, "dc", 2.0, [T["RCM.4"], (T["RCM.4"][0] + 3, 295), (292, 295), (292, 198), (318, 198), (318, 203)], "RCM1 harness", (247, 294))
wire(7, "sig", 1.8, [(W - S3_BODY[0], S3_POS[1]), (342, S3_POS[1]), (342, 196), (P("K2.A1")[0], 196), (P("K2.A1")[0], 200)], "S3 pair", (343, 243))
wire(7, "sig", AWG18, [P("AUX.34"), (256, P("AUX.34")[1]), (256, 170), (350, 170), (350, H1_POS[1] + 4), (W - H1_BODY[0], H1_POS[1] + 4)], "H1 via aux 33-34", (300, 169))
wire(7, "z", AWG18, [(W - H1_BODY[0], H1_POS[1] - 4), (348, H1_POS[1] - 4), (348, 2), (P("J5.5")[0], 2), P("J5.5")])
wire(6, "dc", AWG18, [P("PS1.+V2"), (P("PS1.+V2")[0], 32), (278, 32), (278, 201), (P("AUX.21")[0], 201), P("AUX.21")])
wire(6, "sig", AWG18, [P("AUX.22"), (P("AUX.22")[0], 300), (282, 300), (282, 20), (P("J5.12")[0], 20), P("J5.12")])
wire(6, "com", 1.8, [((P("M1.5")[0] + P("M1.6")[0]) / 2, P("M1.5")[1]), ((P("M1.5")[0] + P("M1.6")[0]) / 2, 322), (290, 322), (290, 16),
                     ((P("J4.8")[0] + P("J4.7")[0]) / 2, 16), ((P("J4.8")[0] + P("J4.7")[0]) / 2, P("J4.7")[1])], "RS-485 pair", (165, 320))
wire(6, "sig", AWG18, [(224, H), (224, 338), (258, 338), (258, 160), (P("J11.6")[0], 160), P("J11.6")], "CP", (238, 159))
wire(6, "sig", AWG18, [(C["K1"]["x"] + 36, 262), (262, 262), (262, 156), ((P("J11.2")[0] + P("J11.3")[0]) / 2, 156),
                       ((P("J11.2")[0] + P("J11.3")[0]) / 2, P("J11.2")[1])])
wire(6, "sig", AWG18, [(100, 280.5), (136.5, 280.5), (136.5, 152), ((P("J11.4")[0] + P("J11.5")[0]) / 2, 152),
                       ((P("J11.4")[0] + P("J11.5")[0]) / 2, P("J11.4")[1])])
wire(6, "sig", AWG18, [(W - S2_BODY[0], S2_POS[1]), (300, S2_POS[1]), (300, 12), ((P("J4.10")[0] + P("J4.9")[0]) / 2, 12),
                       ((P("J4.10")[0] + P("J4.9")[0]) / 2, P("J4.10")[1])], "S2 pair", (330, 93))
wire(8, "com", 2.4, [T["RJ45"], (GL["G3"][0], T["RJ45"][1]), (GL["G3"][0], H)], "Ethernet")

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
    elif k == "rcm":
        out.append(f'<rect class="{cls}" x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}" rx="2"/>')
        out.append(f'<rect class="as-ap" x="{r(x+w/2-7)}" y="{r(y)}" width="14" height="{r(h)}"/>')
        out.append(f'<rect class="as-tb" x="{r(x+33)}" y="{r(y)}" width="10.5" height="4"/>')
        out.append(f'<text class="as-wl" x="{r(x+2)}" y="{r(y+14)}">RCM1</text><text class="as-t" x="{r(x+w/2+9)}" y="{r(y+22)}">14 mm</text>')
        return "".join(out)
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
    pref = {"M1": "M1.", "K1": "K1.", "AUX": "AUX.", "F12": "F.", "PS1": "PS1.", "PS2": "PS2.", "K2": "K2."}
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
                if cid in ("PS2", "K2"):
                    lab = {"+Vo": "+12", "-Vo": "0", "-Vin": "−in", "+Vin": "+in"}.get(lab, lab)
                    rad = 1.7
                    out[-1] = f'<circle class="as-screw" cx="{r(tx)}" cy="{r(ty)}" r="{rad}"/>'
                    if cid == "K2":
                        out.append(f'<text class="as-t" x="{r(tx+5)}" y="{r(ty+1.8)}">{html.escape(lab)}</text>')
                        continue
                if cid == "AUX":
                    out.append(f'<text class="as-t" x="{r(tx+5)}" y="{r(ty+1.8)}">{html.escape(lab)}</text>')
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
    for lab, (px, py), (dep, wid), head in (("H1", H1_POS, H1_BODY, 22.5), ("S2", S2_POS, S2_BODY, 22.5), ("S1", S1_POS, S1_BODY, 40), ("S3", S3_POS, S3_BODY, 22.5)):
        s.append(f'<rect class="as-old" x="{r(px-dep)}" y="{r(py-wid/2)}" width="{dep}" height="{wid}" rx="1.5"/>'
                 f'<rect class="as-gland" x="{W}" y="{r(py-head/2)}" width="9" height="{head}" rx="3"/>'
                 f'<text class="as-t" x="{W+12}" y="{r(py+2)}">{lab}</text>')
    s.append(f'<path class="as-scale" d="M{r(W-41)} {r(S1_POS[1])} H{W}"/>'
             f'<text class="as-t" x="{r(W-24)}" y="{r(S1_POS[1]-6.5)}" text-anchor="middle">a</text>'
             f'<text class="as-t" x="{r(W-24)}" y="{r(S1_POS[1]+10)}" text-anchor="middle">b</text>')
    # scale bar
    s.append(f'<path class="as-scale" d="M10 {H+42} h100 M10 {H+38} v8 M60 {H+40} v4 M110 {H+38} v8"/>'
             f'<text class="as-t" x="115" y="{H+45}">100 mm</text>')
    return "".join(s)

ORDER = ["clampL1", "PE1", "PE2", "PE3", "TB1-1", "TB1-2", "TB1-3", "TB1-4", "TB1-5", "endcov", "M1", "K1", "AUX", "clampL2", "clampL3", "PS2", "K2", "clampL4"]
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
<li>Drill the bottom wall for the glands: two M40 holes (about 40.5 mm) and one M20 hole (about 20.5 mm). Put the centres 40 mm out from the base and at 85 mm, 210 mm and 350 mm from the left inside wall. The M40 lock nuts are 50 mm across, so keep the centres at least 55 mm apart.</li>
<li>Drill four 22.5 mm holes in the right wall, all 100 mm out from the base. Measured from the top inside wall: H1 (pilot light) at 40 mm, S2 (stop) at 95 mm, S1 (E-stop) at 175 mm, and S3 (RCM1 test) at 245 mm. Each needs 40–45 mm behind the wall; S1 needs 45 mm with its two contact blocks side by side. Mirror them onto the left wall if that's the side that will face you.</li>
<li>Fit the glands, H1, S2, S1 and S3, then fit both rails. Clip S1's second NC block (ECX1030) beside the first, not behind it. The drill sizes are the usual thread size plus 0.5 mm; Bimed doesn't publish a clearance hole size.</li>
</ol>""",
     svg(1, [], [], "Enclosure interior with rails, gland holes and four panel-device holes", s1_extra))

# Step 2
step(2, "Fit the lower (power) rail",
     """<ol>
<li>Snap parts onto the lower rail from left to right: an end clamp, three UT 16-PE terminals (PE1–PE3), five UT 16 terminals (TB1-1 to TB1-5), then an end cover on the open side of TB1-5.</li>
<li>Plug one FBS 2-12 bridge into TB1-1/TB1-2 and another into TB1-3/TB1-4. TB1-5 (N) stays unbridged and isolated.</li>
<li>Leave a gap of about 11 mm, then snap on M1, the SDM230 meter.</li>
<li>Clip the 022.65 aux module onto the right side of K1 (Finder 22.64), then snap K1 on with the aux to its right, followed by an end clamp. Only K1's first two poles (1-2 and 3-4) are used.</li>
<li>Leave the next 30 mm of rail clear for wiring. Then fit an end clamp, PS2 (the DDR-15G-12, input terminals at the bottom), K2 (the Finder 38.51 relay) and a final end clamp. The rail is used up to about 337 of its 375 mm.</li>
</ol>""",
     svg(2, ORDER, [], "Lower rail populated: PE terminals, TB1, meter, contactor with aux, 12 V supply and relay K2"))

# Step 3
step(3, "Fit the upper (control) rail",
     """<ol>
<li>Screw the CB-EVAL board into the UM-PRO housing base with the board's J4/J5 edge toward the top. <span class="verify">Check which way Phoenix's drawing puts the 120 mm board side relative to the rail; it's drawn here with 120 mm along the rail.</span> Cut the right side element for the RJ45 jack, and the left one for the J10 24 V jack, which you'll need in step 10.</li>
<li>Snap parts onto the upper rail from left to right: an end clamp, F1/F2 (the 2-pole FAZ), PS1, the board housing, then an end clamp.</li>
<li>Switch F1/F2 off and leave it off until step 11. Leave PS1 at its factory 24 V setting; don't turn it above 26.4 V, the top of K1's coil range.</li>
</ol>""",
     svg(3, UPPER, ORDER, "Upper rail populated: breaker, 24 V supply, board in housing"))

# Step 4
step(4, "Wire the power path (8 AWG)",
     """<ol>
<li>Pass the 14-50 cord through the left M40 gland. Land G on PE1, L1 on TB1-1, L2 on TB1-3 and N on TB1-5, all on the bottom screws. N stops at TB1-5 and is never connected to PE.</li>
<li>Run an 8 AWG green jumper from the top of PE1 to the top of PE2.</li>
<li>Run 8 AWG black from TB1-1 (top) to M1 terminal 1, and from M1 terminal 2 to K1 terminal 1. Run 8 AWG red from TB1-3 (top) to K1 terminal 3. L2 doesn't pass through the meter.</li>
<li>Pass the J1772 cable through the right M40 gland. Thread only its L1 and L2 through RCM1's 14 mm hole, then land L1 on K1 terminal 2 and L2 on K1 terminal 4. Route PE around RCM1, never through it, to PE2 (bottom). The pilot and sensor conductors also go around it.</li>
<li>Fix RCM1 to the base just above the gland with two adhesive cable-tie mounts and ties through its flange holes, with its connector toward the right.</li>
<li>Crimp ferrules on every stranded end and tighten each screw to the torque on its datasheet. Tighten the glands last, once the conductors are dressed.</li>
</ol>""",
     svg(4, ["RCM1"], ORDER + UPPER, "Power wiring: cord to TB1, through meter and contactor, J1772 L1/L2 through RCM1 to K1"))

# Step 5
step(5, "Wire the 24 V supply (18 AWG)",
     """<ol>
<li>Run 18 AWG black from TB1-2 (top) to F1/F2 terminal 1, and 18 AWG red from TB1-4 (top) to terminal 3. The bridges make these taps of L1 and L2.</li>
<li>Run black from F1/F2 terminal 2 to PS1 L, and red from terminal 4 to PS1 N. PS1 has no earth terminal.</li>
<li>Run a second red from F1/F2 terminal 4 to M1 terminal 3, the meter's voltage reference. This keeps the meter's sense lead behind the 2 A breaker.</li>
<li>Run 18 AWG blue from PS1 +V to J7.11 and blue/white from PS1 −V to J7.12.</li>
<li>Run 18 AWG green from PS1's second −V terminal to PE3 (top). This is the single 0 V–PE bond the control pilot needs.</li>
</ol>""",
     svg(5, [], ORDER + UPPER + ["RCM1"], "Control supply wiring: taps through F1/F2 to PS1, meter reference, 24 V to the board, 0 V bond"))

# Step 6
r3 = P("J5.12"), P("J5.9")
s6_extra = (f'<rect class="as-res" x="{r(r3[0][0])}" y="{r(r3[0][1]-11)}" width="{r(r3[1][0]-r3[0][0])}" height="2.6" rx=".8"/>'
            f'<rect class="as-res" x="{r(r3[0][0])}" y="{r(r3[0][1]-7)}" width="{r(r3[1][0]-r3[0][0])}" height="2.6" rx=".8"/>'
            f'<text class="as-t" x="{r((r3[0][0]+r3[1][0])/2)}" y="{r(r3[0][1]-13)}" text-anchor="middle">R3a, R3b</text>')
tt = C["K1"]
s6_extra += (f'<rect x="{r(tt["x"]+33)}" y="258" width="7" height="8" fill="var(--sheet)" stroke="var(--sig)" stroke-width="1"/>'
             f'<text class="as-t" x="{r(tt["x"]+44)}" y="265">TT1</text>'
             f'<rect x="93" y="276.5" width="7" height="8" fill="var(--sheet)" stroke="var(--sig)" stroke-width="1"/>'
             f'<text class="as-t" x="82" y="292">TT2</text>')
step(6, "Wire the control signals",
     """<ol>
<li><strong>Weld detection:</strong> run PS1's second +V terminal to aux 21, and aux 22 to J5.12. Fit R3a and R3b (3.9 kΩ each) side by side across J5.12 and J5.9, crimping both resistor leads and the wire at J5.12 into one ferrule. Together they draw over 10 mA, the 022.65 contact's minimum load.</li>
<li><strong>Meter:</strong> run the Belden 9841 pair from M1 terminals 5 (A) and 6 (B) to J4.8 (A) and J4.7 (B). Tie the shield to M1 terminal 7 at the meter end only.</li>
<li><strong>Pilot:</strong> run the J1772 cable's CP conductor to J11.6. If the cable has a latch-sense conductor, land it on J11.7. Keep these runs away from the 8 AWG conductors.</li>
<li><strong>Temperature:</strong> stick TT1 on K1's body beside terminals 2/4 and wire it to J11.2/J11.3. Stick TT2 on TB1-3's housing, the incoming L2 terminal, and wire it to J11.4/J11.5. Neither lead goes to ground.</li>
<li><strong>Stop button:</strong> wire S2's NO contact to J4.10 and J4.9.</li>
<li><strong>Not used:</strong> leave J11.8 (ZC) and the HV inputs J1/J6 unconnected.</li>
</ol>""",
     svg(6, [], ORDER + UPPER + ["RCM1"], "Control signal wiring: feedback, RS-485, pilot, temperature sensors, stop button", s6_extra))

# Step 7
j411, j49 = P("J4.11"), P("J4.9")
s7_extra = (f'<rect class="as-res" x="{r(j411[0]-2)}" y="20" width="4" height="14" rx="1"/>'
            f'<path class="as-wire" stroke="var(--sig)" stroke-width="1.3" d="M{r(j411[0])} 34 V{r(j411[1])}"/>'
            f'<text class="as-t" x="{r(j411[0]-3)}" y="28" text-anchor="end">R1</text>'
            f'<rect class="as-res" x="{r(j411[0])}" y="{r(j411[1]-6)}" width="{r(j49[0]-j411[0])}" height="2.2" rx=".6"/>'
            f'<rect class="as-res" x="{r(j411[0])}" y="{r(j411[1]-10)}" width="{r(j49[0]-j411[0])}" height="2.2" rx=".6"/>'
            f'<text class="as-t" x="{r(j49[0]+2)}" y="{r(j411[1]-6)}">R2a, R2b</text>'
            f'<path class="as-wire" stroke="var(--dc)" stroke-width="1.3" d="M{r(P("AUX.21")[0]+1.5)} {r(P("AUX.21")[1])} V{r(P("AUX.33")[1])}"/>'
            f'<text class="as-t" x="{r(C["K2"]["x"]+3.1)}" y="{r(C["K2"]["y"]-3)}" text-anchor="middle">K2</text>')
step(7, "Wire the safety and status circuits",
     """<ol>
<li><strong>Contactor coil through the E-stop:</strong> run J5.10 to S1-a (S1's upper contact block), S1-a on to K1 A1, and K1 A2 back to J5.9. Pressing S1 cuts the coil directly.</li>
<li><strong>E-stop loop:</strong> run a wire from PS1's second +V terminal (in a twin ferrule with the aux 21 feed) to S1-b, S1's lower contact block. Run S1-b's other side to K2 terminal 11, and K2 terminal 14 to R1 at J4.11. Fit R2a and R2b separately, each from J4.11 to J4.9. Put each terminal's leads and wire into one ferrule (at most 1.5 mm²). Keep R2a and R2b as two separate resistors; don't solder them together into one part, or a single bad joint could take out both.</li>
<li><strong>12 V supply:</strong> run 18 AWG from PS1 +V (in a twin ferrule with the J7.11 wire) to PS2 +Vin, and from PS1 −V (in a twin ferrule with the J7.12 wire) to PS2 −Vin. Jumper PS2 −Vo to PS2 −Vin, so the 12 V side shares 0 V.</li>
<li><strong>RCM1 harness</strong> (JST XHP-4 housing with pre-crimped leads): pin 1 to PS2 −Vo (0 V), pin 2 to PS2 +Vo (+12 V), pin 3 to one side of S3, pin 4 to K2 A2. Run PS2 +Vo to K2 A1 too, observing the A1+ / A2− marking. In normal running RCM1 holds pin 4 low and K2 energised. A fault, a lost 12 V supply or a failed relay coil drops K2 and opens the E-stop loop.</li>
<li><strong>Test button:</strong> run S3's other side to PS2 +Vo. Pressing S3 puts 12 V on RCM1's test input, which simulates a fault.</li>
<li><strong>Pilot light:</strong> jumper aux 21 to aux 33, run aux 34 to H1 +, and H1 − to J5.5 (0 V). H1 lights whenever K1's main contacts are closed.</li>
</ol>""",
     svg(7, [], ORDER + UPPER + ["RCM1"], "Safety and status wiring: E-stop, RCM1 with K2, PS2 and S3, pilot light", s7_extra))

# Step 8
step(8, "Connect the PC and configure EVerest",
     """<ol>
<li>Pass the Ethernet cable through the M20 gland, then crimp the RJ45 plug and plug it into the board.</li>
<li>On the PC, give the cable's interface a static address and run a DHCP server on it, for example <code>dnsmasq --interface=eth1 --bind-interfaces --dhcp-range=192.168.50.100,192.168.50.150,12h</code>. Find the module with <code>avahi-browse _chargebridge._udp -tr</code>.</li>
<li>Start from EVerest's <code>applications/pionix_chargebridge/config/config-CB-EVAL-SIM.yaml</code>. Set the maximum current to 40 A, and under <code>safety.relay_1</code> set <code>feedback_enabled: true</code>. Leave <code>inverted_emergency_input: 0</code> (J4.11 low means emergency).</li>
<li>Set up the SDM230 on <code>/dev/cbserial0</code> at Modbus address 1, 9600 8N1, and set PT1000 limits for both channels, well below the front end's 126 °C full scale.</li>
</ol>
<p class="hint"><span class="verify">The example config ships with <code>feedback_inverted: true</code>. Confirm the polarity in step 10: feedback must report open while K1 is open. Flip the setting if it doesn't.</span></p>""",
     svg(8, [], ORDER + UPPER + ["RCM1"], "Ethernet cable routed from the RJ45 jack to the M20 gland"))

# Step 9
step(9, "Check it with the power off",
     """<ol>
<li>With the 14-50 plug out, check continuity from the plug's G pin to PE1, PE2, PE3, the J1772 PE pin and J7.12 (0 V, through the bond).</li>
<li>Check that N isn't connected to PE, and that TB1-5 shows no continuity to L1, L2 or PE.</li>
<li>Check that only L1 and L2 pass through RCM1's hole.</li>
<li>Tug-test every conductor, and check that no copper shows outside a terminal or ferrule.</li>
<li>With F1/F2 off and K1 open, megger L1 and L2 to PE at 500 V DC. Expect well over 1 MΩ. The meter is still connected, so keep the test short.</li>
</ol>""")

# Step 10
step(10, "Bring it up on 24 V only",
     """<ol>
<li>Keep the 14-50 unplugged and F1/F2 off. Plug the 24 V supply that came with the Pionix kit into J10. It back-feeds PS1's output terminals, so PS2, RCM1 and K2 come up too: K2 should click on.</li>
<li>Check that the PC finds the module and that EVerest starts.</li>
<li>Plug the J1772 handle into an EV simulator. In state B (2.74 kΩ + diode), the pilot should read +9 V and then show a 66.7% duty cycle. In state C (with 1.3 kΩ added), K1 should pull in with an audible click, H1 should light, feedback 1 should read closed, and TT1/TT2 should read room temperature.</li>
<li>Press S2: K1 should drop out and H1 go dark. Pull the handle out: the session should end.</li>
<li>Start a session, then press S1. K1 should drop out, and EVerest should report an emergency stop that stays latched until you unplug. Twist S1 to reset it, then unplug and replug the handle and confirm charging resumes.</li>
<li>Start a session, then press S3. K2 should click off, K1 drop out, and EVerest latch an emergency. Release S3, then unplug and replug the handle.</li>
<li>The S1 and S3 tests prove the E-stop loop, both pull-downs, K2 and RCM1's output all work. Repeat them after moving the unit and every few months, and before charging from an outlet that has no GFCI.</li>
<li>Unplug the J10 supply.</li>
</ol>""")

# Step 11
step(11, "First run on 240 V",
     """<ol>
<li>Close the cover. Plug into the 14-50 and press the receptacle breaker's GFCI test button. It must trip; reset it.</li>
<li>Switch F1/F2 on. PS1 should come up, then the board and EVerest, and K2 should click on.</li>
<li>Repeat the simulator test. In state C, measure about 240 V between L1 and L2 at the simulator, and 0 V when it leaves state C.</li>
<li>Charge a car. Watch K1 and TT1 temperatures and the meter's current for the first hour at 40 A.</li>
</ol>""")

parts = ['<h2 id="assembly">Assembly</h2>',
         '<p class="hint">Drawings are to scale at 1 mm per unit, looking into the enclosure base with the cover open. '
         'Part outlines come from manufacturer datasheets. Screw positions on K1, its aux module, the meter, PS2 and K2 are approximate, '
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
.as-ap{fill:var(--grid);stroke:var(--muted);stroke-width:.6;stroke-dasharray:2 1.5}
"""

p = str(Path(__file__).resolve().parent.parent / "cb-l2-evse.html")
s = open(p).read()
if '<h2 id="assembly">' in s:
    a = s.index('<h2 id="assembly">'); b = s.index('<div class="callout">')
    s = s[:a] + SECTION + "\n\n" + s[b:]
else:
    b = s.index('<div class="callout">')
    s = s[:b] + SECTION + "\n\n" + s[b:]
def put_css(s, name, css):
    """Insert or replace a marker-delimited CSS block so style changes always apply."""
    start, end = f"/* {name}-css */", f"/* /{name}-css */"
    block = f"{start}{css}{end}\n"
    if start in s:
        i = s.index(start); j = s.index(end, i) + len(end) + 1
        return s[:i] + block + s[j:]
    if name == "assembly" and "\n.as-step{" in s:   # unmarked block from earlier versions
        i = s.index("\n.as-step{") + 1; j = s.index(".as-res{", i); j = s.index("\n", j) + 1
        j2 = s.find(".as-ap{", i)
        if j2 != -1 and j2 < s.index("</style>", i): j = s.index("\n", j2) + 1
        return s[:i] + block + s[j:]
    return s.replace("</style>", block + "</style>", 1)
s = put_css(s, "assembly", CSS)
open(p, "w").write(s)
print("steps:", len(STEPS), "lower rail end:", round(C["clampL2"]["x"] + 9.5, 1), "upper rail end:", round(C["clampU2"]["x"] + 9.5, 1))
