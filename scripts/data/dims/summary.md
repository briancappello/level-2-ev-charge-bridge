# DIN-rail part dimensions & terminal layouts (gathered 2026-10-27)

Conventions: **W** = width along the DIN rail, **H** = height across the rail as seen from the front, **D** = depth (front-to-back). "Top/bottom" = as seen from the front with the rail horizontal. All numbers come from the cited source; "not found" means I didn't find it in a source.

## Summary table

| # | Part | W along rail (mm) | H across rail (mm) | D (mm) | Modules | Source |
|---|---|---|---|---|---|---|
| 1 | Phoenix UT 16 (3044199) | 12.2 (pitch) | 55.5 ("Length") | 55 on NS35/7.5; 62.5 on NS35/15 | – | https://www.farnell.com/datasheets/1514100.pdf |
| 1b | Phoenix FBS 2-12 bridge (**3005950**) | 2-pos, 12 mm pitch | – | – | – | Listed as the UT 16 bridge in the UT 16 datasheet (above); DigiKey 277-3343-ND, **$2.66 @ qty 1**, 6,669 in stock: https://www.digikey.com/en/products/detail/phoenix-contact/3005950/2525736 |
| 2 | Phoenix UT 16-PE (3044212) | 12.2 | 55.5 | 55 on NS35/7.5; 62.5 on NS35/15 | – | https://media.digikey.com/PDF/Data%20Sheets/Phoenix%20Contact%20PDFs/3044212.pdf |
| 3a | Phoenix D-UT 16 end cover (3047206) | **2.2** thick | 55.5 (L) | 54.8 (H) | – | Accessory list in the 3044212 datasheet above. The older UT 16 datasheet (Farnell, 2005) lists 2.2 W × 52.8 L × 47.3 H. |
| 3b | Phoenix E/UK end clamp (1201442) | **9.5** | 50.5 (length) | 35.3 (height) | – | Mouser PDF / Phoenix search snippets: https://www.mouser.com/datasheet/2/324/3/1201442-1403160.pdf , https://www.phoenixcontact.com/en-ro/products/end-block-euk-1201442 (search snippets only; Phoenix site blocks bots) |
| 4 | ABB ESB63-20N-01 (1SAE351111R0120) | **54** | **85** | 65 (product data); drawing shows 58 / 43.5 / 6.8 | **3** | https://www.cse-distributors.co.uk/sites/admin/plugins/elfinder/files/cse/ExtraDocs/ESB63-20N-01/ESB63-20N-01.pdf ; catalog p.16: https://new.abb.com/docs/librariesprovider22/default-document-library/2cdc103051c0201_en_i_catalog_installation_contactors.pdf?sfvrsn=9dc5c60a_0 |
| 5 | ABB EH04-11N (1SAE901901R1011) | **9** | **85** | 65 (product data); drawing 58 / 43.5 / 6.8 | (½ module) | https://media.distrelec.com/Web/Downloads/_t/ds/1SAE901901M1011_eng_tds.pdf ; catalog p.21 (same URL as row 4) |
| 6 | Eastron SDM230-Modbus | **36** | **100** | **63** | 2 ("Two Module") | Manual V1.9: https://www.eastrongroup.com/eastrongroup/2026/07/28/EastronSDM230-ModbususermanualV19.pdf (older Eastron Europe manual says 36x99x63) |
| 7 | Mean Well HDR-60-24 | **52.5** | **90** | **54.5** (drawing also shows 58.4 overall incl. rail clip) | (3, inferred from 52.5 mm) | https://www.meanwell.com/Upload/PDF/HDR-60/HDR-60-SPEC.PDF (pages 2 and 4) |
| 8 | Eaton FAZ-C2/2 (278748) | **35** (17.5/pole) | **80** | 60 rail to front face + 8 toggle; ETIM "built-in depth" 70.5 | **2** | https://efobasen.no/mime_root/57/Eaton-DS-278748-FAZ-C2_2-20190307.pdf (p.1, 6, 9) |
| 9 | Phoenix UM-PRO-SKT-B108-L120-7035 (1456980) | **123.8** | **127.8** | **39.45** (32.45 above the top edge of the rail) | – | http://datasheets.nexxconn.com/phoenix-contact/1545284.pdf |
| 10a | Schneider XB5AA31 | cutout Ø22.5 rec. (Ø22.3 +0.4/0) | body 30 W × 41.5 H | 43 behind panel (+23.6 per extra contact row); 9 in front | – | se.com datasheet PDF: https://www.se.com/us/en/product/download-pdf/XB5AA31 |
| 10b | Schneider XB5AVB3 | cutout Ø22.5 rec. (Ø22.3 +0.4/0) | body 30 × 41.5 | 43 behind panel; 11 in front | – | https://www.se.com/us/en/product/download-pdf/XB5AVB3 |
| 10c | AutomationDirect GCX3131 | mounting hole Ø22.5 | mushroom **Ø40** | 45.0 behind panel with 1 contact-block layer (+26.0 per added layer); generic GCX plastic drawing | – | https://cdn.automationdirect.com/static/specs/gcx22mmpb.pdf (p. tPIL-3); product page: https://www.automationdirect.com/adc/shopping/catalog/pushbuttons_-a-_switches_-a-_indicators/22mm_round_metal_pushbuttons_-a-_switches_-a-_indicators/emergency_stop_pushbuttons/gcx3131 |
| 11 | Polycase DR-62 | 1 rail, 35 × 7.5 × **375** mm | – | – | – | Polycase DR-62 page, from the search snippet only (site blocks bots): https://www.polycase.com/dr-62 |
| 12a | Bimed BM-ENX-15-W (M40×1.5) | see gland table | | | | |
| 12b | Bimed BM-ENX-12-W (M20×1.5) | see gland table | | | | |

---

## 1–3. Phoenix UT 16 family
- **UT 16 (3044199):** W 12.2, L 55.5, H 55 (NS 35/7.5) / 62.5 (NS 35/15). Wire range: 1.5–25 mm² solid or stranded, AWG 16–4. With ferrule: 1–16 mm². Two equal conductors: 1–6 mm² (solid). Strip length 14 mm. Feed-through block with one screw at each end, so one terminal on the top edge and one on the bottom edge. Source: Farnell copy of the Phoenix datasheet (dated 2005). The DigiKey page lists 3044199 at $2.44.
- **Bridge:** both the UT 16 and UT 16-PE datasheets list **FBS 2-12, part no. 3005950** (2-pos, red) under "Bridges". Other options in the same list: RB UT 16-(2,5/4) 3047073 and RB UT 16-ST(2,5/4) 3047099 (reducing bridges). DigiKey: 277-3343-ND, $2.66 each at qty 1, manufacturer pack 10, pitch 12.00 mm.
- **UT 16-PE (3044212):** W 12.2, L 55.5, H 55 / 62.5. Same wire range and strip length (14 mm) as UT 16.
- **D-UT 16 (3047206):** the two datasheets disagree on length and height, but both give width **2.2 mm**:
  - Current 3044212 datasheet: 55.5 L × 54.8 H.
  - 2005 UT 16 datasheet: 52.8 L × 47.3 H.
- **E/UK (1201442):** W 9.5, H 35.3, L 50.5.

## 4. ABB ESB63-20N-01
- 54 W × 85 H. Product-data depth is 65 mm. The catalog dimension drawing shows 58, 43.5 and 6.8 mm (the drawing doesn't say which is the overall depth). 3 module spacings.
- **Terminals** (catalog p.16 symbol for ESB63-20N-01): top row **A1, 1, 3**; bottom row **A2, 2, 4**.
- The ESB63..N front-view drawing (4-pole housing) shows 4 main screws on the top edge and 4 on the bottom edge. A smaller coil screw sits in the middle of each edge, between poles 2 and 3: A1 at the top, A2 at the bottom. I didn't find which screw positions the 2-pole 20N variant actually uses.
- Wire range, main: 1×1.5–25 mm² rigid; 1×1.5–16 mm² flexible (with or without ferrule); 2×1.5–10 mm². Wire range, control: 1×0.75–2.5 mm² ferrule; 1×1–4 mm² rigid. Strip length: 13 mm main, 7 mm control.
- An ESB-DIS distance piece (½ module) is recommended between adjacent ESB63s when they run for more than 1 h and ambient is above 40 °C (catalog p.21).

## 5. ABB EH04-11N
- 9 W × 85 H × 65 D (product data). The catalog drawing gives terminal pitch: 69 mm between the outer top and bottom screws, 53 mm between the inner ones.
- **Mounting side:** "mounted on the **left side** of the contactors … clip-on the left side" (catalog pp. 9 and 11).
- **Terminal numbers are 21-22 (NC) and 33-34 (NO), not 13-14.** EH04-20N is 23-24 + 33-34. The catalog symbol shows **21 and 33 on the top edge** and **22 and 34 on the bottom edge**.
- The drawing shows 2 screws stacked on the top edge (one behind the other across the rail) and 2 on the bottom edge. Which number is the outer screw vs. the inner one isn't legible in the drawing (not found).

## 6. Eastron SDM230-Modbus (wiring diagram, manual V1.9 p.12)
- 36 W × 100 H × 63 D, DIN 43880, "Two Module". The drawing also shows 45 mm (front-face step height) and 35 mm (rail).
- **Top edge:** large terminals **1 = L-in** (left) and **2 = L-out** (right). A strip of 6 small screws sits just below them (unlabelled in the drawing).
- **Bottom edge:** the small terminals sit just above the large ones, left to right: **5 = A, 6 = B, 7 = GND, 8 = pulse 1 +, 9 = COM, 10 = pulse 2 +**. The large terminals are **3 = N-in** (left) and **4 = N-out** (right).
- Older Eastron Europe series manual: the same layout is called "SDM230-V1". A "V2" variant puts 1 L-in / 2 N-in on top and 3 L-out / 4 N-out on the bottom, so **check the label on the unit you have**. Source: https://www.eastroneurope.com/images/uploads/products/manuals/SDM230_Sereis_Manual.pdf
- Main conductor: 16–25 mm² with lug or ferrule, torque 2.0 N·m (V1.9 manual).

## 7. Mean Well HDR-60-24
- 52.5 W × 90 H × 54.5 D; the side view shows 58.4 overall. Fits TS35/7.5 or TS35/15.
- **Top edge**, left to right: pins **1 −V, 2 −V, 3 +V, 4 +V**, then the Vo-adjust pot to the right.
- **Bottom edge**, at the left: **5 AC/L, 6 AC/N**.
- **There is no FG/PE terminal.** The pin table lists only pins 1–6.
- Wire range: not found in the spec. The front label reads "Terminal torque 4.4 Lb-in" (top) and "3.0 Lb-in" (bottom).

## 8. Eaton FAZ-C2/2
- 35 W × 80 H. Side view: 60 mm from the mounting face to the front face, 8 mm toggle protrusion, 5.5 mm rail-clip offset, 45 mm front-face height, 44 mm rear body. ETIM built-in depth: 70.5 mm. 2 module spacings.
- **Terminals:** **1, 3 on top**, **2, 4 on the bottom** (Eaton FAZ "Connection Diagrams – Two-Pole", AutomationDirect Eaton FAZ spec p. tCPR-110: https://cdn.automationdirect.com/static/specs/eatonfaz.pdf). Supply direction "as required".
- Wire range: 1×25 / 2×10 mm² (Eaton). AutomationDirect lists 1 wire 0.75–25 mm² (18–4 AWG) and 2 wires 0.75–10 mm².

## 9. Phoenix UM-PRO-SKT-B108-L120-7035 (1456980)
- "Dimensions on the DIN rail: width 123.8, height 127.8, depth 39.45"; depth from the top edge of the DIN rail is 32.45. PCB 108 × 120 mm, 1.4–1.8 mm thick, 3 PCB holders. "Mounting position: parallel to the DIN rail".
- **PCB orientation vs. rail: not explicitly stated.** The product photo shows an extruded profile closed by two black lateral end elements that carry the rail feet. That suggests the profile axis (the L120 direction) runs along the rail (120 + end elements → 123.8), but no source states this, so treat it as unconfirmed. Confirm with the Phoenix CAD/drawing (Phoenix site blocked the bot).

## 10. Panel devices
| Part | Cutout | In front of panel | Behind panel | Body (W × H) | Panel thickness | Spacing |
|---|---|---|---|---|---|---|
| XB5AA31 | Ø22.5 rec. (Ø22.3 +0.4/0) | 9 | 43 (+23.6 per extra contact row) | 30 × 41.5 | 1–6 | Screw-clamp: a = 40, b = 30 centre-to-centre |
| XB5AVB3 | Ø22.5 rec. | 11 | 43 | 30 × 41.5 | 1–6 | same |
| GCX3131 | Ø22.5 | (not given for the mushroom) | 45.0 with 1 layer (+26 per layer) | mushroom Ø40 | 1–6 | 40 × 30 (same polarity ≤ 230 V) or 50 × 40 (≤ 400 V, different polarity) |

GCX3131 is a plastic-base, 1 NC, twist-to-release E-stop with a 40 mm mushroom (AutomationDirect product page). The depth comes from the generic GCX plastic pushbutton drawing, not a part-specific one.

## 11. Polycase DR-62
- "(1) 35 mm × 7.5 mm × **375 mm** din rail and (2) screws". Mounts "along the length of the ZH-161407, ZQ-161407". **One rail per kit.**
- For comparison, DR-60 is the 325 mm rail that mounts "along the width of the ZH-161407".
- Source: Polycase page snippets via DuckDuckGo (https://www.polycase.com/dr-62 , https://www.polycase.com/dr-60). I couldn't fetch the pages themselves (bot-blocked).

## 12. Bimed glands (AutomationDirect catalog + 2D drawings; Bimed catalog agrees for M40)
| Part | Thread | Cable range | Hex SW (cap/body) | Across corners D | Max Ø in drawing | Height above wall H | Thread length TL | Thread Ø TD |
|---|---|---|---|---|---|---|---|---|
| BM-ENX-15-W | M40×1.5 | 19–28 | **46** | 52.4 | **Ø55.3** (top view, overall); 50.0 lock nut | 45.5 | 10.0 | 40.0 |
| BM-ENX-12-W | M20×1.5 | 6–12 | **24** | 27.7 | **28.6** (section, overall); 26.0 lock nut | 29.0 | 10.0 | 20.0 |

- Clearance hole / drill size: **not found** in any of these sources.
- Sources:
  - https://cdn.automationdirect.com/static/specs/bimedglands.pdf (table p. tWIR-142)
  - https://cdn.automationdirect.com/static/drawings/BM-ENX-15-W.pdf
  - https://cdn.automationdirect.com/static/drawings/BM-ENX-12-W.pdf
  - https://www.bimedteknik.com/documents/Standard%20Glands%20with%20Thread,%20Polyamide.pdf : BM-EN-15 is SW 46 / D 52.4 / H 47.4. BM-EN-12 isn't in that table; BM-12 there is SW 24 / D 27.0.
