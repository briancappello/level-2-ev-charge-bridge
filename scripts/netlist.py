#!/usr/bin/env python3
"""Minimal KiCad 9 schematic netlister (geometry based), kept for its S-expression parser.

Don't trust its connectivity: it swaps the pins of some rotated or mirrored two-pin
parts (it reported the CB-EVAL input zeners backwards). Use board_nets.py, which
reads KiCad's own netlist via kicad-cli.
"""
import sys, os, re, math, collections

def tokenize(s):
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in ' \t\r\n':
            i += 1
        elif c == '(' or c == ')':
            yield c; i += 1
        elif c == '"':
            j = i + 1; buf = []
            while s[j] != '"':
                if s[j] == '\\': buf.append(s[j+1]); j += 2
                else: buf.append(s[j]); j += 1
            yield ('S', ''.join(buf)); i = j + 1
        else:
            j = i
            while j < n and s[j] not in ' \t\r\n()': j += 1
            yield s[i:j]; i = j

def parse(s):
    stack = [[]]
    for t in tokenize(s):
        if t == '(':
            stack.append([])
        elif t == ')':
            x = stack.pop(); stack[-1].append(x)
        else:
            stack[-1].append(t[1] if isinstance(t, tuple) else t)
    return stack[0][0]

def kids(node, name):
    return [c for c in node if isinstance(c, list) and c and c[0] == name]

def kid(node, name):
    k = kids(node, name)
    return k[0] if k else None

def prop(node, name):
    for p in kids(node, 'property'):
        if p[1] == name: return p[2]
    return None

R = lambda v: round(float(v) * 100)  # 0.01 mm grid

class Sheet:
    def __init__(self, path):
        self.path = path
        self.tree = parse(open(path).read())
        self.libpins = {}
        ls = kid(self.tree, 'lib_symbols')
        for sym in kids(ls, 'symbol') if ls else []:
            pins = []
            def walk(n, unit):
                for c in n:
                    if isinstance(c, list) and c:
                        if c[0] == 'symbol':
                            m = re.search(r'_(\d+)_(\d+)$', c[1])
                            walk(c, int(m.group(1)) if m else 0)
                        elif c[0] == 'pin':
                            at = kid(c, 'at')
                            num = kid(c, 'number')[1]
                            nm = kid(c, 'name')[1]
                            pins.append((unit, num, nm, float(at[1]), float(at[2]), c[1]))
            walk(sym, 0)
            self.libpins[sym[1]] = pins

    def items(self):
        T = self.tree
        comps, wires, labels, junctions, sheets, nc = [], [], [], [], [], []
        for s in kids(T, 'symbol'):
            lib = kid(s, 'lib_id')[1]
            at = kid(s, 'at'); x, y, a = float(at[1]), float(at[2]), float(at[3]) if len(at) > 3 else 0
            mir = kid(s, 'mirror'); mir = mir[1] if mir else None
            unit = int(kid(s, 'unit')[1]) if kid(s, 'unit') else 1
            ref = prop(s, 'Reference'); val = prop(s, 'Value')
            dnp = kid(s, 'dnp'); dnp = dnp and dnp[1] == 'yes'
            pins = []
            for (u, num, nm, px, py, ptype) in self.libpins.get(lib, []):
                if u not in (0, unit): continue
                qx, qy = px, -py
                if mir == 'x': qy = -qy
                if mir == 'y': qx = -qx
                ang = math.radians(-a)
                rx = qx * math.cos(ang) - qy * math.sin(ang)
                ry = qx * math.sin(ang) + qy * math.cos(ang)
                pins.append((num, nm, ptype, (R(x + rx), R(y + ry))))
            comps.append(dict(ref=ref, val=val, lib=lib, pins=pins, dnp=dnp,
                              mpn=prop(s, 'MPN'), power=lib.startswith('power:') or (ref or '').startswith('#')))
        for w in kids(T, 'wire') + kids(T, 'bus'):
            pts = [(R(p[1]), R(p[2])) for p in kids(kid(w, 'pts'), 'xy')]
            for i in range(len(pts) - 1): wires.append((pts[i], pts[i+1]))
        for kind in ('label', 'global_label', 'hierarchical_label'):
            for l in kids(T, kind):
                at = kid(l, 'at'); labels.append((kind, l[1], (R(at[1]), R(at[2]))))
        for j in kids(T, 'junction'):
            at = kid(j, 'at'); junctions.append((R(at[1]), R(at[2])))
        for j in kids(T, 'no_connect'):
            at = kid(j, 'at'); nc.append((R(at[1]), R(at[2])))
        for sh in kids(T, 'sheet'):
            name = prop(sh, 'Sheetname') or prop(sh, 'Sheet name')
            fn = prop(sh, 'Sheetfile') or prop(sh, 'Sheet file')
            spins = []
            for p in kids(sh, 'pin'):
                at = kid(p, 'at'); spins.append((p[1], (R(at[1]), R(at[2]))))
            sheets.append(dict(name=name, file=fn, pins=spins))
        return comps, wires, labels, junctions, sheets, nc

def onseg(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    if (x - x1) * (y2 - y1) != (y - y1) * (x2 - x1): return False
    return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)

def netlist(path):
    sh = Sheet(path)
    comps, wires, labels, junctions, sheets, nc = sh.items()
    parent = {}
    def f(p):
        parent.setdefault(p, p)
        while parent[p] != p:
            parent[p] = parent[parent[p]]; p = parent[p]
        return p
    def u(a, b): parent[f(a)] = f(b)
    pts = set()
    for a, b in wires:
        u(a, b); pts.add(a); pts.add(b)
    special = [p for c in comps for *_, p in c['pins']] + [p for *_, p in labels] + \
              [p for s in sheets for _, p in s['pins']] + junctions
    for p in list(pts) + special:
        for a, b in wires:
            if onseg(p, a, b): u(p, a)
        f(p)
    # same-name labels join (local labels per sheet, globals everywhere)
    byname = collections.defaultdict(list)
    for kind, name, p in labels: byname[name].append(p)
    for c in comps:
        if c['power'] and c['val'] != 'PWR_FLAG':
            for *_, p in c['pins']: byname[c['val']].append(p)
    for name, ps in byname.items():
        for p in ps[1:]: u(ps[0], p)
    nets = collections.defaultdict(lambda: dict(names=set(), nodes=[]))
    for name, ps in byname.items():
        nets[f(ps[0])]['names'].add(name)
    hit = 0
    for c in comps:
        if c['power']: continue
        for num, nm, ptype, p in c['pins']:
            r = f(p)
            nets[r]['nodes'].append(f"{c['ref']}.{num}({nm})")
    for s in sheets:
        for pn, p in s['pins']:
            nets[f(p)]['nodes'].append(f"[{s['name']}]:{pn}")
    return comps, nets, sheets, nc

if __name__ == '__main__':
    for path in sys.argv[1:]:
        comps, nets, sheets, nc = netlist(path)
        print(f"===== {os.path.basename(path)} =====")
        for c in sorted([c for c in comps if not c['power']], key=lambda c: c['ref'] or ''):
            print(f"  {c['ref']:8} {c['val'] or '':28} {c['mpn'] or ''} {'DNP' if c['dnp'] else ''}")
        for s in sheets:
            print(f"  SHEET [{s['name']}] -> {s['file']}")
        print("  -- nets --")
        for r, n in sorted(nets.items(), key=lambda kv: sorted(kv[1]['names']) or ['~']):
            if len(n['nodes']) + len(n['names']) < 2: continue
            nm = '/'.join(sorted(n['names'])) or '?'
            print(f"  {nm:24} : {' '.join(sorted(n['nodes']))}")
