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
  "Neff Automation (IN)", "https://shop.neffautomation.com/products/1456980", None,
  notes="Phoenix distributor in Indiana; price on request. The only US source found. WSU Industrials (Germany) lists it at €11.49 for reference.",
  alt=[("WSU Industrials (DE)", "https://wsu-industrials.com/en/phoenix-contact-1456980-housing-set-um-pro-skt-b108-l120-7035")])
g("Power path")
r("TB1", 5, "Feed-through terminal, 16 mm², 76 A", "Phoenix UT 16 (3044199)", "Digi-Key", "https://www.digikey.com/en/products/detail/phoenix-contact/3044199/2426230", 2.44,
  notes="TB1-1 to TB1-5: L1, L1 tap, L2, L2 tap, N (isolated). 2,334 in stock.")
r("—", 2, "Plug-in bridge, 2-position, for UT 16", "Phoenix FBS 2-12 (3005950)", "Digi-Key", "https://www.digikey.com/en/products/detail/phoenix-contact/3005950/2525736", 2.66,
  notes="Joins TB1-1/TB1-2 and TB1-3/TB1-4 so the 24 V supply taps get their own clamps. 6,669 in stock.")
r("—", 1, "End cover for UT 16", "Phoenix D-UT 16 (3047206)", "Digi-Key", DK + "3047206", 0.74)
r("—", 4, "End clamp", "Phoenix E/UK (1201442)", "Digi-Key", DK + "1201442", 1.53)
r("PE1–PE3", 3, "Ground terminal, green-yellow", "Phoenix UT 16-PE (3044212)", "Digi-Key", "https://www.digikey.com/en/products/detail/phoenix-contact/3044212/2435394", None,
  notes="Cord G, J1772 PE, and the 0 V bond. Correct part number is 3044212. Price not shown when fetched.")
r("M1", 1, "Wi-Fi energy meter, 2 CT channels, no display, 50 A clamp included", "Shelly EM Gen3 50A (S3EM-002CXCEU50), flashed with ESPHome", "Shelly USA",
  "https://us.shelly.com/products/shelly-em-gen3-50a", 69.99,
  notes="In stock. Runs open-source ESPHome after flashing (step 0) and reports to EVerest's powermeter_API over MQTT. ±2 % V and I. 37 × 42 × 16 mm, not DIN-mount. Rated −20 to 40 °C ambient. Needs 2 A upstream protection (F1/F2). Clamp: 60 cm lead; resellers give an 11 mm opening. No US listing (UL) found.",
  alt=[("SupplyHouse (NY)", "https://www.supplyhouse.com/Shelly-EM-GEN3-Gen3-Energy-Monitor-with-50A-Current-Transformer")])
r("K1", 1, "Modular contactor, 4 NO, 63 A, 24 V AC/DC coil (2 poles used)", "Finder 22.64.0.024.4310", "Digi-Key",
  "https://www.digikey.com/en/products/detail/finder-relays-inc/22-64-0-024-4310/10055799", 97.08,
  notes="53.5 mm wide. Coil 250 mA (6 W), operating range 20.4–26.4 V. Out of stock; Digi-Key expects it on 9 Nov. US alternative: ABB ESB63-20N-01 at Radwell, $266.85 new.",
  alt=[("ABB at Radwell", "https://www.radwell.com/Buy/ASEA%20BROWN%20BOVERI/ASEA%20BROWN%20BOVERI/1SAE351111R0120")])
r("K1 aux", 1, "Aux module for 22.44/22.64, 1 NO + 1 NC, mechanically linked", "Finder 022.65", "Digi-Key", DK + "022.65", 32.19,
  notes="Clips on K1's right side. NC 21-22 for weld detection, NO 33-34 for H1. Mechanically linked per EN 60947-5-1 Annex L. Minimum load 10 V / 10 mA.")
r("X1", 1, "J1772 tethered cable, 48 A, 25 ft", "Inteset 48 A replacement cable", "Amazon", "https://www.amazon.com/Inteset-Charger-Replacement-Original-Chargers/dp/B0FV116C88", 219.95,
  notes="Only 2 left. Listing doesn't say whether it has a latch sense wire. Alternative: Phoenix Contact cable at OpenEVSE, $229.00, 3–4 week backorder.",
  alt=[("OpenEVSE", "https://store.openevse.com/products/j1772-cable-48a-ultra-flexible")])
r("—", 1, "J1772 wall holster", "", "EVSE Adapters", "https://www.evseadapters.com/products/j1772-plug-holder", 9.95)
r("—", "15 ft", "8 AWG stranded THHN, black / red / green", "THN8 or equal", "Buy local", "", None,
  notes="Buy locally by the foot. For reference, Wire & Cable Your Way lists $0.87/ft but has a $20 minimum order.",
  alt=[("Wire & Cable Your Way", "https://www.wireandcableyourway.com/8-awg-thhn-building-wire")])
r("—", 1, "Ferrule kit to 10 mm² with ratchet crimper", "LUNEY 1250 pc", "Amazon", "https://www.amazon.com/dp/B0B23V7ZQJ", 13.98,
  notes="Fulfilled from Amazon's US warehouses.")

g("Control supply and protection")
r("PS1", 1, "24 V DC DIN supply, 60 W", "Mean Well HDR-60-24", "Digi-Key", "https://www.digikey.com/en/products/detail/mean-well-usa-inc/HDR-60-24/7703804", 20.90,
  notes="No earth terminal (class II input). Keep its output at or below 26.4 V, the top of K1's coil range. 2,367 in stock.")
r("F1, F2", 1, "2-pole 2 A C-curve supplementary protector", "Eaton FAZ-C2/2", "AutomationDirect", AD + "circuit_protection_-z-_fuses_-z-_disconnects/circuit_breakers_-a-_circuit_protectors/miniature_supplementary_protectors/faz-c2-2", 46.00,
  notes="94 available. UL 489 version FAZ-C2/2-NA costs $86.00.")
r("RCM1", 1, "Residual current monitor, UL 2231 CCID20 (20 mA AC / 56 mA DC), 14 mm aperture", "Western Automation / Littelfuse RCM14-04", "Digi-Key", DK + "RCM14-04", 36.38,
  notes="12 V supply, JST XH connector, open-drain output that holds K2 on. L1 and L2 of the J1772 cable pass through it.")
r("PS2", 1, "DIN DC-DC converter, 9–36 V in, 12 V 1.25 A", "Mean Well DDR-15G-12", "TRC Electronics", "https://www.trcelectronics.com/products/mean-well-ddr-15g-12", 26.27,
  notes="Powers RCM1 and K2's coil from PS1. 139 in stock.")
r("K2", 1, "DIN relay module, 12 V DC coil, 1 CO, gold-plated contacts", "Finder 38.51.7.012.5050", "Digi-Key", "https://www.digikey.com/en/products/detail/finder-relays-inc/38-51-7-012-5050/10822227", 21.36,
  notes="Contact 11–14 sits in the E-stop loop. 30 in stock (not normally stocked). Phoenix PLC-RSC-12DC/21AU is equivalent but backordered.")
r("—", 1, "JST XH 4-position housing for RCM1", "JST XHP-4", "Digi-Key", DK + "XHP-4", 0.10)
r("—", 4, "Pre-crimped JST XH lead, 22 AWG", "JST ASXHSXH22K (length to suit)", "Digi-Key", DK + "ASXHSXH22K", 0.76,
  notes="Price shown for the shortest length in the search; longer leads cost slightly more.")
r("S3", 1, "22 mm momentary pushbutton, black, 1 NO (RCM1 test)", "AutomationDirect GCX1100", "AutomationDirect", AD + "pushbuttons_-z-_switches_-z-_indicators/pushbuttons/gcx1100", 9.00,
  notes="693 available. Puts 12 V on RCM1's test input.")
r("—", 4, "Adhesive cable-tie mounts with ties", "any", "", "", None,
  notes="Two fix RCM1 to the enclosure base beside the J1772 gland, two fix M1 below the lower rail. Spare ties hold TT1 and TT2. Not priced.")

g("Meter flashing (one-off, on the bench)")
r("—", 1, "USB-to-serial adapter, 3.3 V logic and 3.3 V / 600 mA supply output", "SparkFun Serial Basic Breakout, CH340C, USB-C (DEV-15096)", "SparkFun (CO)",
  "https://www.sparkfun.com/sparkfun-serial-basic-breakout-ch340c-and-usb-c.html", 10.50,
  notes="In stock. Ships set to 3.3 V. Its regulator sources 600 mA, enough to run M1's ESP32-C3 on the bench. Pins: DTR, RXI, TXO, VCC, CTS, GND.")
r("—", 1, "7-position 1.27 mm male header, straight", "Sullins GRPB071VWVN-RC", "Digi-Key", "https://www.digikey.com/en/products/detail/sullins-connector-solutions/GRPB071VWVN-RC/1786443", 0.55,
  notes="5,668 in stock. Plugs into M1's 7-pin programming socket. The 1.27 mm pitch is what larger Shelly Gen2/Gen3 units use; check it against your unit before soldering.")
r("—", 1, "Female/female jumper wires, 6 in (pack of 10)", "SparkFun PRT-08430", "SparkFun (CO)", "https://www.sparkfun.com/jumper-wires-premium-6-f-f-pack-of-10.html", 4.95,
  notes="In stock. Cut five in half; solder the cut ends to the header pins for TX, RX, 3.3 V, GPIO0 and GND.")
r("—", 1, "USB cable, USB-C at the adapter end", "any", "", "", None,
  notes="To suit the PC's port. Not priced.")

g("Sensors and operator")
r("TT1, TT2", 2, "PT1000 2-wire probe, Ø3.2 × 30 mm fluorocarbon housing, 397 mm PTFE leads", "Yageo Nexensos 5016951 (EC3032-C)", "Digi-Key",
  "https://www.digikey.com/en/products/detail/yageo-nexensos/5016951/13583145", 11.70,
  notes="284 in stock. Class B (F 0.3), −50 to +200 °C. Housing rated 6 kV AC for 60 s, so the − leads float as the board requires, even on TB1-3. Held on with cable ties; no adhesive bonds to the housing.",
  alt=[("Newark", "https://www.newark.com/nexsensos/5016951/rtd-sensor-platinum-1-kohm-200deg/dp/31AM2566")])
r("S1", 1, "22 mm E-stop, 40 mm mushroom, twist to release, 1 NC", "AutomationDirect GCX3131", "AutomationDirect", AD + "pushbuttons_-z-_switches_-z-_indicators/emergency_stop_pushbuttons/gcx3131", 12.00,
  notes="455 available. Positive-opening contacts. Mounts in the right wall, 80 mm below S2.")
r("S1", 1, "Extra NC contact block for S1-a (2-pack)", "AutomationDirect ECX1030-2", "AutomationDirect", AD + "pushbuttons_-z-_switches_-z-_indicators/emergency_stop_pushbuttons/gcx3131", 8.75,
  notes="Second NC block for S1-a; clips beside the first. 607 available.")
r("R1, R2a, R2b", 3, "2.2 kΩ 1% 0.5 W metal film", "Yageo MFR50SFTE52-2K2", "Digi-Key", DK + "MFR50SFTE52-2K2", 0.10,
  notes="R1 in series to J4.11; R2a and R2b are parallel pull-downs, so either alone still trips.")
r("S2", 1, "22 mm momentary pushbutton, black, 1 NO", "AutomationDirect GCX1100", "AutomationDirect", AD + "pushbuttons_-z-_switches_-z-_indicators/pushbuttons/gcx1100", 9.00,
  notes="Same part as S3. Replaces the key switch; the stop input needs a momentary contact.")
r("R3a, R3b", 2, "3.9 kΩ 1% 0.5 W metal film", "Yageo MFR50SFTE52-3K9", "Digi-Key", DK + "MFR50SFTE52-3K9", 0.10,
  notes="In parallel across J5.12 and J5.9: 11.8 mA minimum through the aux contact, above the 022.65's 10 mA minimum. 0.18 W each at 26.4 V.")
r("H1", 1, "22 mm LED pilot light, 24 V AC/DC, green", "AutomationDirect ECX2052-24L", "AutomationDirect", AD + "pushbuttons_-z-_switches_-z-_indicators/indicating_lights/ecx2052-24l", 6.25,
  notes="1,230 available. Wired through K1's aux NO 33-34, so it lights whenever K1 is closed. No software needed.")

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
  notes="For the 240 V taps to F1/F2 and PS1, M1's L and N supply, and the 0 V bond. Offcuts are fine; not priced.")
r("—", "500 ft", "18 AWG MTW, blue", "Atlas MTW18BL", "AutomationDirect", AD + "bulk_wire_-a-_cable/single_conductor_wire_-a-_cable/mtw18bl", 49.00, n=1,
  notes="Price per spool. Backordered until Nov 12.")

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
    links = "Owned" if d["owned"] else (f'<a href="{html.escape(d["url"])}" target="_blank" rel="noopener">{html.escape(d["vendor"])}</a>' if d["url"]
                                         else html.escape(d["vendor"]) if d["vendor"] not in ("", "any") else "Any supplier")
    for name, u in d["alt"]:
        links += f'<br><a class="alt" href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(name)}</a>'
    part = html.escape(d["part"]) + (' <span class="opt">optional</span>' if d["opt"] else "")
    if d["mpn"]: part += f'<br><span class="mpn">{html.escape(d["mpn"])}</span>'
    rows.append(f'<tr><td>{html.escape(d["ref"])}</td><td>{d["qty"]}</td><td>{part}</td><td>{links}</td>'
                f'<td class="num">{unit_s}</td><td class="num">{ext_s}</td><td>{html.escape(d["notes"])}</td></tr>')
ship = 200 * FX
rows.append(f'<tr class="total"><td colspan="5">Total</td><td class="num">{money(req)}</td><td>Excludes tax, shipping, and items with no qty-1 price: the board housing (quote), the PE terminals, the DR-62 rail kits, the 8 AWG wire (bought locally), the 18 AWG offcuts, the tie mounts and the USB cable.</td></tr>')
if opt_total:
    rows.append(f'<tr class="total"><td colspan="5">Optional parts</td><td class="num">{money(opt_total)}</td><td></td></tr>')
table = ('<div class="tablewrap">\n<table class="bom">\n<thead><tr><th>Ref</th><th>Qty</th><th>Part</th><th>Buy at</th>'
         '<th>Unit</th><th>Ext.</th><th>Notes</th></tr></thead>\n<tbody>\n' + "\n".join(rows) + '\n</tbody>\n</table>\n</div>')

p = str(Path(__file__).resolve().parent.parent / "cb-l2-evse.html")
s = open(p).read()
a = s.index('<h2>Bill of materials</h2>'); b = s.index('<h2>Build notes</h2>')
intro = ('<h2>Bill of materials</h2>\n<p class="hint">Every vendor is US-based. Prices were read from each vendor page on 26–28 Oct 2026, '
         'for quantity 1 shipped to the US, before tax and shipping. Stock changes daily; check before ordering.</p>\n')
s = s[:a] + intro + table + "\n\n" + s[b:]
css = ('table.bom{min-width:1040px}\ntable.bom td:nth-child(2){text-align:right}\n.num{text-align:right;white-space:nowrap}\n'
       '.mpn,.fx{color:var(--muted);font-size:.85rem}\na.alt{font-size:.85rem}\n'
       'tr.total td{font-weight:600;border-top:2px solid var(--ink)}\ntr.total td:first-child{text-align:right}\n')
if "table.bom" not in s:
    s = s.replace("tr.group td{", css + "tr.group td{", 1)
open(p, "w").write(s)
print(f"required {money(req)}  optional {money(opt_total)}  unpriced {unpriced}")
