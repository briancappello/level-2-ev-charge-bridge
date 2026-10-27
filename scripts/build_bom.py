import html
import re
from pathlib import Path

FX = 1.1188  # ECB EUR->USD, 2026-10-26 (frankfurter.dev)
DK = "https://www.digikey.com/en/products/result?keywords="
AD = "https://www.automationdirect.com/adc/shopping/catalog/"

# (ref, qty, part, mpn, vendor, url, unit, unit_currency, qty_for_ext, optional, notes)
G = []
def g(name): G.append(("group", name))
def r(ref, qty, part, mpn, vendor, url, unit, notes="", cur="USD", n=None, opt=False, alt=None, owned=False):
    G.append(("row", dict(ref=ref, qty=qty, part=part, mpn=mpn, vendor=vendor, url=url, unit=unit,
                          cur=cur, n=n if n is not None else (qty if isinstance(qty, (int, float)) else 1),
                          opt=opt, owned=owned, notes=notes, alt=alt or [])))

g("Already owned")
r("A1", 1, "ChargeBridge Evaluation Kit, EVSE side (CB-EVAL v1.2, CB-CCS-EVSE-LU module)", "CB-EVAL-CCS-EVSE-LU-KIT",
  "owned", "", 0.0, owned=True)
r("P1", 1, "NEMA 14-50 plug and cord", "", "owned", "", 0.0, owned=True,
  notes="Feeds L1, L2 and ground; N is landed on an isolated terminal and left unused. Its 50 A receptacle breaker is already GFCI.")
r("U1", 1, "x86 PC running EVerest", "", "owned", "", 0.0, owned=True,
  notes="Outside the enclosure, wired to the board's RJ45.")

g("Controller")
r("—", 1, "DIN-rail housing set for the 108 × 120 mm board", "Phoenix UM-PRO-SKT-B108-L120-7035 (1456980)",
  "WSU Industrials (DE)", "https://wsu-industrials.com/en/phoenix-contact-1456980-housing-set-um-pro-skt-b108-l120-7035", 11.49, cur="EUR",
  notes="Includes German VAT. US shipping not confirmed. Neff Automation (US) lists it without a price.",
  alt=[("Neff Automation", "https://shop.neffautomation.com/products/1456980")])
g("Power path")
r("TB1", 5, "Feed-through terminal, 16 mm², 76 A", "Phoenix UT 16 (3044199)", "Digi-Key", "https://www.digikey.com/en/products/detail/phoenix-contact/3044199/2426230", 2.44,
  notes="TB1-1 to TB1-5: L1, L1 tap, L2, L2 tap, N (isolated). 2,334 in stock.")
r("—", 2, "Plug-in bridge, 2-position, for UT 16", "Phoenix FBS 2-12 (3005950)", "Digi-Key", "https://www.digikey.com/en/products/detail/phoenix-contact/3005950/2525736", 2.66,
  notes="Joins TB1-1/TB1-2 and TB1-3/TB1-4 so the 24 V supply taps get their own clamps. 6,669 in stock.")
r("—", 1, "End cover for UT 16", "Phoenix D-UT 16 (3047206)", "Digi-Key", DK + "3047206", 0.74)
r("—", 4, "End clamp", "Phoenix E/UK (1201442)", "Digi-Key", DK + "1201442", 1.53)
r("PE1–PE3", 3, "Ground terminal, green-yellow", "Phoenix UT 16-PE (3044212)", "Digi-Key", "https://www.digikey.com/en/products/detail/phoenix-contact/3044212/2435394", None,
  notes="Cord G, J1772 PE, and the 0 V bond. Correct part number is 3044212. Price not shown when fetched.")
r("M1", 1, "Single-phase Modbus energy meter, 100 A", "SDM230-Modbus (non-MID)", "Amazon", "https://www.amazon.com/SDM230-Single-Energy-Bi-Directional-Function/dp/B0DKFF2Z83", 41.00,
  notes="Third-party seller shipping from overseas (Nov 5–13). Genuine Eastron not confirmed.")
r("K1", 1, "Installation contactor, 2 NO, 63 A AC-1, 24 V AC/DC coil", "ABB ESB63-20N-01 (1SAE351111R0120)", "TME (US site)",
  "https://www.tme.com/us/en-us/details/esb63-20n-01/contactors-installation-modular/abb/1sae351111r0120/", 115.48,
  notes="4 in stock; customs and tariffs included. Ships from Poland.")
r("K1 aux", 1, "Aux contact, 1 NO + 1 NC", "ABB EH04-11N (1SAE901901R1011)", "TME (US site)",
  "https://www.tme.com/us/en-us/details/eh04-11n/contactors-installation-modular/abb/1sae901901r1011/", 26.12,
  notes="105 in stock. Minimum load 17 V / 5 mA (reseller data).")
r("X1", 1, "J1772 tethered cable, 48 A, 25 ft", "Inteset 48 A replacement cable", "Amazon", "https://www.amazon.com/Inteset-Charger-Replacement-Original-Chargers/dp/B0FV116C88", 219.95,
  notes="Only 2 left. Listing doesn't say whether it has a latch sense wire. Alternative: Phoenix Contact cable at OpenEVSE, $229.00, 3–4 week backorder.",
  alt=[("OpenEVSE", "https://store.openevse.com/products/j1772-cable-48a-ultra-flexible")])
r("—", 1, "J1772 wall holster", "", "EVSE Adapters", "https://www.evseadapters.com/products/j1772-plug-holder", 9.95)
r("—", "15 ft", "8 AWG stranded THHN, black / red / green", "THN8 cut to length", "Wire & Cable Your Way", "https://www.wireandcableyourway.com/8-awg-thhn-building-wire", 0.87, n=15,
  notes="Price per ft; $20 minimum order. Red not confirmed in stock.")
r("—", 1, "Ferrule kit to 10 mm² with ratchet crimper", "LUNEY 1250 pc", "Amazon", "https://www.amazon.com/dp/B0B23V7ZQJ", 13.98)

g("Control supply and protection")
r("PS1", 1, "24 V DC DIN supply, 60 W", "Mean Well HDR-60-24", "Digi-Key", "https://www.digikey.com/en/products/detail/mean-well-usa-inc/HDR-60-24/7703804", 20.90,
  notes="No earth terminal (class II input). 2,367 in stock.")
r("F1, F2", 1, "2-pole 2 A C-curve supplementary protector", "Eaton FAZ-C2/2", "AutomationDirect", AD + "circuit_protection_-z-_fuses_-z-_disconnects/circuit_breakers_-a-_circuit_protectors/miniature_supplementary_protectors/faz-c2-2", 46.00,
  notes="94 available. UL 489 version FAZ-C2/2-NA costs $86.00.")
r("RCM1", 1, "6 mA DC residual current monitor, relay output", "Littelfuse / Western Automation RCM14-03", "Digi-Key", "https://www.digikey.com/en/products/detail/littelfuse-western-automation/RCM14-03/19183160", 36.38,
  opt=True, notes="97 in stock. RCM14-01 is the same price.")
r("—", 1, "Whole-home Type 2 surge protector", "Eaton CHSPT2ULTRA", "Amazon", "https://www.amazon.com/EATON-CHSPT2ULTRA-SURGE-PROTECTOR-108KA/dp/B00DJS8MGY", 180.00,
  opt=True, notes="Mounts in the CH panel, not the enclosure. Third-party seller.")

g("Sensors and operator")
r("TT1, TT2", 2, "PT1000 2-wire adhesive patch sensor, 2 ft PFA leads", "P2A-TAPE-REC-PK-1-PFXX-24-STWL", "Evolution Sensors",
  "https://evosensors.com/products/2-wire-rtd-pt1000-surface-temperature-sensor-with-self-adhesive-patch-and-with-2-4-or-8ft-of-lead-wire", 50.00,
  notes="Insulated, so the − leads float as the board requires.")
r("S1", 1, "22 mm E-stop, 40 mm mushroom, twist to release, 1 NC", "AutomationDirect GCX3131", "AutomationDirect", AD + "pushbuttons_-z-_switches_-z-_indicators/emergency_stop_pushbuttons/gcx3131", 12.00,
  opt=True, notes="455 available. Replaces the $121 Schneider. Omit it and unplug the 14-50 instead if you prefer.")
r("S1", 1, "Extra NC contact block for S1-a (2-pack)", "AutomationDirect ECX1030-2", "AutomationDirect", AD + "pushbuttons_-z-_switches_-z-_indicators/emergency_stop_pushbuttons/gcx3131", 8.75,
  opt=True, notes="Fits GCX. 607 available.")
r("R1, R2", 2, "2.2 kΩ 1% 0.5 W metal film", "Yageo MFR50SFTE52-2K2", "Digi-Key", DK + "MFR50SFTE52-2K2", 0.10,
  opt=True, notes="Only needed if S1 or RCM1 is fitted.")
r("S2", 1, "22 mm momentary pushbutton, black, 1 NO", "Schneider XB5AA31", "Digi-Key", DK + "XB5AA31", 28.30,
  notes="Replaces the key switch; the stop input needs a momentary contact.")
r("R3", 1, "3.3 kΩ 1% 0.5 W metal film", "Yageo MFR50SFTE52-3K3", "Digi-Key", DK + "MFR50SFTE52-3K3", 0.10,
  notes="7.3 mA through the aux contact, above its 5 mA minimum.")
r("H1", 1, "22 mm LED pilot light, 24 V, green", "Schneider XB5AVB3", "Digi-Key", DK + "XB5AVB3", 52.92, opt=True)

g("Mechanical")
r("—", 1, "NEMA 4X polycarbonate enclosure, 16 × 14 × 8.2 in, stainless latch", "Polycase ZH-161407-90", "Polycase", "https://www.polycase.com/zh-161407", 117.35,
  notes="313 in stock, ships in 1–2 business days (page saved 27 Oct).")
r("—", 2, "DIN rail kit, installed along the 16 in length", "Polycase DR-62", "Polycase", "https://www.polycase.com/dr-62", None,
  notes="Mounts on bosses in the base; no internal panel needed. The page shows only the bulk price (from $6.24); qty-1 price and rails per kit not shown. Two rails fit the parts list.",
  alt=[("DR-60 (across width)", "https://www.polycase.com/dr-60")])
r("—", 1, "M40 nylon gland, 19–28 mm, with locknut (2-pack)", "Bimed BM-ENX-15-W", "AutomationDirect", AD + "wire_-a-_cable_management/cable_glands/metric_thread", 9.25,
  notes="One for the EV cable, one for the 14-50 cord. Check both ODs fall in 19–28 mm.")
r("—", 1, "M20 nylon gland, 6–12 mm, with locknut (5-pack)", "Bimed BM-ENX-12-W", "AutomationDirect", AD + "wire_-a-_cable_management/cable_glands/metric_thread", 4.50,
  notes="For the Ethernet cable. An RJ45 plug won't pass through, so fit the plug after routing. 370 available.")
r("—", "~1 m each", "18 AWG MTW, black, red and green", "", "any", "", None,
  notes="For the 240 V taps to F1/F2 and PS1, the meter reference, and the 0 V bond. Offcuts are fine; not priced.")
r("—", "500 ft", "18 AWG MTW, blue", "Atlas MTW18BL", "AutomationDirect", AD + "bulk_wire_-a-_cable/single_conductor_wire_-a-_cable/mtw18bl", 49.00, n=1,
  notes="Price per spool. Backordered until Nov 12.")
r("—", "6 ft", "RS-485 shielded twisted pair, 120 Ω", "Belden 9841", "Wire & Cable Your Way", "https://www.wireandcableyourway.com/belden-9841-24-awg-1-pair-shielded-low-capacitance-computer-cable", 3.55, n=6,
  notes="Price per ft. Combine with the 8 AWG order to meet the $20 minimum.")

def money(v): return f"${v:,.2f}"
rows, req, opt_total, unpriced = [], 0.0, 0.0, 0
for kind, d in G:
    if kind == "group":
        rows.append(f'<tr class="group"><td colspan="7">{html.escape(d)}</td></tr>'); continue
    if d["owned"]:
        unit_s, ext_s, ext = "—", "$0.00", 0.0
    elif d["unit"] is None:
        unit_s, ext_s, ext = "not shown", "—", 0.0; unpriced += 1
    elif d["cur"] == "EUR":
        usd = d["unit"] * FX; ext = usd * d["n"]
        unit_s = f'€{d["unit"]:,.2f}<br><span class="fx">≈ {money(usd)}</span>'; ext_s = money(ext)
    else:
        ext = d["unit"] * d["n"]; unit_s = money(d["unit"]); ext_s = money(ext)
    if d["opt"]: opt_total += ext
    else: req += ext
    links = "Owned" if d["owned"] else (f'<a href="{html.escape(d["url"])}">{html.escape(d["vendor"])}</a>' if d["url"] else "Any supplier")
    for name, u in d["alt"]:
        links += f'<br><a class="alt" href="{html.escape(u)}">{html.escape(name)}</a>'
    part = html.escape(d["part"]) + (' <span class="opt">optional</span>' if d["opt"] else "")
    if d["mpn"]: part += f'<br><span class="mpn">{html.escape(d["mpn"])}</span>'
    rows.append(f'<tr><td>{html.escape(d["ref"])}</td><td>{d["qty"]}</td><td>{part}</td><td>{links}</td>'
                f'<td class="num">{unit_s}</td><td class="num">{ext_s}</td><td>{html.escape(d["notes"])}</td></tr>')
ship = 200 * FX
rows.append(f'<tr class="total"><td colspan="5">Required parts</td><td class="num">{money(req)}</td><td>Excludes tax, shipping, and items with no qty-1 price: the PE terminals, the DR-62 rail kits and the 18 AWG offcuts.</td></tr>')
rows.append(f'<tr class="total"><td colspan="5">Optional parts</td><td class="num">{money(opt_total)}</td><td>E-stop, RCM1, surge protector, H1.</td></tr>')
table = ('<div class="tablewrap">\n<table class="bom">\n<thead><tr><th>Ref</th><th>Qty</th><th>Part</th><th>Buy at</th>'
         '<th>Unit</th><th>Ext.</th><th>Notes</th></tr></thead>\n<tbody>\n' + "\n".join(rows) + '\n</tbody>\n</table>\n</div>')

p = str(Path(__file__).resolve().parent.parent / "cb-l2-evse.html")
s = open(p).read()
a = s.index('<h2>Bill of materials</h2>'); b = s.index('<h2>Build notes</h2>')
intro = ('<h2>Bill of materials</h2>\n<p class="hint">Prices were read from each vendor page on 26 Oct 2026, for quantity 1 '
         'shipped to the US, before tax and shipping. Euro prices are converted at the ECB rate of $1.1188. Stock changes daily; '
         'check before ordering.</p>\n')
s = s[:a] + intro + table + "\n\n" + s[b:]
css = ('table.bom{min-width:1040px}\ntable.bom td:nth-child(2){text-align:right}\n.num{text-align:right;white-space:nowrap}\n'
       '.mpn,.fx{color:var(--muted);font-size:.85rem}\na.alt{font-size:.85rem}\n'
       'tr.total td{font-weight:600;border-top:2px solid var(--ink)}\ntr.total td:first-child{text-align:right}\n')
if "table.bom" not in s:
    s = s.replace("tr.group td{", css + "tr.group td{", 1)
open(p, "w").write(s)
print(f"required {money(req)}  optional {money(opt_total)}  unpriced {unpriced}")
