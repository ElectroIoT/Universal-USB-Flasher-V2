"""Wiring-by-section page (same style as the LED-dimmer / TankPilot docs).

    python tools/gen_wiring_sections.py        -> docs/wiring-by-section.html

One diagram per small section, grouped by the 8 EasyEDA schematic pages. Each box is a part
(reference, role, LCSC number) with its pins on the right; a coloured wire runs from each pin to a
vertical lane that joins every pin of the same net in that section. GND / +3V3 / +5V are drawn as
symbols at the pin. Nets that continue elsewhere show "-> also in". Data: tools/design.json.
"""
import collections, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'tools', 'design.json'), encoding='utf-8'))
PART = {p[0]: p for p in D['parts']}
BOM_DESC = {}
for b in D['bom'] + D.get('bom_extra', []):
    for r in b[0].split():
        BOM_DESC[r] = b

# ---------------------------------------------------------------- colours (dimmer palette)
C5, C3, CG, CVIO, CUSB, CDATA, CCTL, CLED, CPWR = '#ff4d94', '#4895ef', '#8a93a3', '#a78bfa', '#22d3ee', '#2fbf71', '#14b8a6', '#facc15', '#ff9f43'
def cls(n):
    if n == 'GND': return 'Ground', CG
    if n in ('+5V', '+5V_T', 'VBUS', 'VBUS_F'): return '5 V / USB power', C5
    if n in ('+3V3', '+3V3_T'): return '3.3 V', C3
    if n in ('VIO', 'Q3_B', 'Q3_C'): return 'VIO (logic level)', CVIO
    if n.startswith('USB_') or n in ('CC1', 'CC2'): return 'USB', CUSB
    if n in ('TXD', 'RXD', 'TX2', 'RX2', 'UPDI_R'): return 'UART data', CDATA
    if n in ('DTR_N', 'RTS_N', 'DTR_AP', 'RTS_AP', 'Q1_B', 'Q2_B', 'EN', 'IO0', 'RST', 'IO15', 'ESP01_RST', 'ESP01_IO2', 'DTR2_N', 'TPWR_EN'): return 'control / boot', CCTL
    if n.startswith('LED') or n == 'FAULT_N': return 'LED / fault', CLED
    return 'power-switch internals', CPWR
FLAG = {'GND', '+3V3', '+5V'}
THICK = {'+5V', '+5V_T', 'VBUS', 'VBUS_F', '+3V3', '+3V3_T'}

# ---------------------------------------------------------------- sections (page, title, refs, note)
G = [
 ('P1', 'POWER 1 - USB fuse F1, back-feed diode D1, bulk capacitors', ['F1', 'C1', 'D1', 'C5'],
  'VBUS -> F1 -> VBUS_F (C1 10 uF to GND). D1 anode (triangle side) on VBUS_F, cathode (bar) on +5V. C5 10 uF goes from +5V to GND - it must NOT sit across D1.'),
 ('P1', 'POWER 2 - 3.3 V regulator U1 (SGM2212)', ['U1', 'C6', 'C7'],
  'Pin 3 VIN = +5V, pin 1 GND, pins 2 and 4 VOUT = +3V3. C6 22 uF and C7 100 nF from +3V3 to GND, right at the regulator.'),
 ('P1', 'POWER 3 - 5V-IO warning LED (Q3, R16, R17, LED5)', ['Q3', 'R16', 'R17', 'LED5'],
  'Q3 is a PNP: emitter (arrow, bottom) on VIO, base through R16 4.7k to +3V3, collector (top) through R17 1k to LED5 anode; LED5 cathode (bar) to GND. LED5 lights only when SW3 selects 5 V. Net name is VIO (no space).'),
 ('P1', 'POWER 4 - ESP-01 bulk capacitor C8', ['C8'],
  'C8 22 uF between +3V3_T (switched target 3.3 V) and GND; on the PCB place it next to J2 VCC.'),
 ('P2', 'TARGET POWER 1 - 3.3 V target switch U4 (TPS2553) + PWR LED', ['U4', 'R18', 'C11', 'C12', 'R3', 'LED1'],
  'U4: pin 1 IN = +3V3 (C11 100 nF), pin 2 GND, pin 3 EN = TPWR_EN, pin 4 /FAULT = FAULT_N, pin 5 ILIM -> R18 43k -> GND, pin 6 OUT = +3V3_T (C12 10 uF). PWR LED: +3V3_T -> R3 1k -> LED1 anode, LED1 cathode (bar) -> GND.'),
 ('P2', 'TARGET POWER 2 - 5 V target switch U5 (TPS2553)', ['U5', 'R19', 'C13', 'C14'],
  'U5: pin 1 IN = +5V (C13 100 nF), pin 2 GND, pin 3 EN = TPWR_EN, pin 4 /FAULT = FAULT_N, pin 5 ILIM -> R19 51k -> GND, pin 6 OUT = +5V_T (C14 10 uF).'),
 ('P2', 'TARGET POWER 3 - enable line and POWER-CYCLE button', ['R20', 'SW5'],
  'TPWR_EN is shared by U4 pin 3 and U5 pin 3: R20 100k pulls it up to +3V3, SW5 pulls it to GND while pressed (both target rails off). Put a TPWR_EN net label on BOTH enable pins.'),
 ('P2', 'TARGET POWER 4 - OVERLOAD LED', ['R21', 'LED6'],
  '+5V -> R21 1k -> LED6 anode; LED6 cathode (bar) -> FAULT_N. FAULT_N is shared by U4 pin 4 and U5 pin 4 (open-drain, pulls low on overload) - put a FAULT_N label on both.'),
 ('P3', 'USB+ESD 1 - USB-C connector and CC resistors', ['USB1', 'R1', 'R2'],
  'Both VBUS pins = VBUS, all GND and shell (EH) pins = GND. DP1+DP2 = USB_DP, DN1+DN2 = USB_DM. CC1 -> R1 5.1k -> GND, CC2 -> R2 5.1k -> GND. SBU1 and SBU2 get No-Connect flags.'),
 ('P3', 'USB+ESD 2 - USB data ESD U3 (USBLC6-2SC6)', ['U3'],
  'Pins 1 and 6 = USB_DP, pins 3 and 4 = USB_DM, pin 5 = VBUS, pin 2 = GND.'),
 ('P3', 'USB+ESD 3 - header ESD arrays U6 / U7 (USBLC6-4SC6)', ['U6', 'U7'],
  'Pin 2 GND, pin 5 = +5V on both. U6: TXD, RXD, DTR_N, RTS_N. U7: EN, IO0, TX2, RX2. Their pin numbers are hidden in your symbol: left-middle = 2 (GND), right-middle = 5 (+5V).'),
 ('P4', 'USB-UART 1 - CH342F (U2) complete pin list', ['U2'],
  'Rename U8 to U2. Put a net label with exactly this name on each pin; the red-cross pins get No-Connect flags. EP (pin 25) = GND. VDD5 and VBUS = VBUS_F, VIO = VIO, V3 = V3 (only to C3).'),
 ('P4', 'USB-UART 2 - CH342F decoupling', ['C2', 'C3', 'C4'],
  'C2 100 nF VBUS_F-GND (at pin 7), C3 100 nF V3-GND (at pin 6), C4 100 nF VIO-GND (at pin 5).'),
 ('P4', 'USB-UART 3 - TX / RX / RX2 activity LEDs', ['R4', 'LED2', 'R5', 'LED3', 'R6', 'LED4'],
  'Each: VIO -> 2.2k -> LED anode, LED cathode (bar) on the data line. LED2 on TXD, LED3 on RXD, LED4 on RX2. The LED blinks when the line goes low (data).'),
 ('P5', 'AUTO-PROGRAM - SJ1 / SJ2 headers, Q1 / Q2, base resistors', ['SJ1', 'SJ2', 'R7', 'R8', 'Q1', 'Q2'],
  'SJ1: DTR_N - DTR_AP, SJ2: RTS_N - RTS_AP (2-pin headers C492401, jumper cap fitted = ON). Q1: base via R7 from DTR_AP, emitter (arrow) RTS_AP, collector EN. Q2: base via R8 from RTS_AP, emitter (arrow) DTR_AP, collector IO0.'),
 ('P6', 'TARGET I/O 1 - EN / IO0 pull-ups and IO15 pull-down', ['R9', 'C9', 'R10', 'R11'],
  'R9 10k +3V3_T -> EN and C9 100 nF EN -> GND; R10 10k +3V3_T -> IO0; R11 10k IO15 -> GND.'),
 ('P6', 'TARGET I/O 2 - Arduino auto-reset', ['C10', 'R14'],
  'C10 100 nF from DTR_N to RST; R14 10k from VIO to RST.'),
 ('P6', 'TARGET I/O 3 - UPDI resistor', ['R15'],
  'R15 4.7k from UPDI_R (SW4 common) to RXD. With SW4 on UPDI it links TX to RX.'),
 ('P6', 'TARGET I/O 4 - ESP-01 RST and GPIO2 pull-ups', ['R12', 'R13'],
  'R12 10k +3V3_T -> ESP01_RST (J2 pin 6); R13 10k +3V3_T -> ESP01_IO2 (J2 pin 3).'),
 ('P7', 'SWITCHES 1 - RESET and BOOT buttons', ['SW1', 'SW2'],
  'SW1: EN to GND (RESET). SW2: IO0 to GND (BOOT).'),
 ('P7', 'SWITCHES 2 - IO voltage SW3 and UART/UPDI SW4', ['SW3', 'SW4'],
  'SW3: pin 1 = +3V3, pin 2 (common) = VIO, pin 3 = +5V. SW4: pin 1 = TXD, pin 2 (common) = UPDI_R, pin 3 No-Connect. Pin 4 (metal tab) of both = GND.'),
 ('P8', 'CONNECTORS 1 - main header H1', ['H1'],
  'Pin order and colours match the silkscreen: 3V3 and 5V are the switched, current-limited target rails.'),
 ('P8', 'CONNECTORS 2 - ESP-01 socket J2', ['J2'],
  'Odd pins (top row): 1 GND, 3 GPIO2, 5 GPIO0, 7 RXD. Even pins (bottom row): 2 TXD, 4 CH_PD, 6 RST, 8 VCC. ESP TXD goes to the flasher RXD and ESP RXD to TXD.'),
 ('P8', 'CONNECTORS 3 - ESP-Prog ports J3 (1.27 mm) and J4 (2.54 mm)', ['J3', 'J4'],
  'Same pinout on both: 1 EN, 2 +3V3_T, 3 target TX -> RXD, 4 GND, 5 target RX -> TXD, 6 IO0.'),
 ('P8', 'CONNECTORS 4 - UART2 header J5', ['J5'],
  '1 GND, 2 TX2, 3 RX2, 4 DTR2_N.'),
]
assert sorted(r for g in G for r in g[2]) == sorted(PART), set(PART) ^ set(r for g in G for r in g[2])
PAGE_NAME = {p[0]: p[1].split('·')[1].strip() for p in D['pages']}
gid = [f"{g[0][1:]}.{i+1}" for i, g in enumerate(G)]  # temp
# number sections per page
cnt = collections.Counter(); SID = []
for g in G:
    cnt[g[0]] += 1; SID.append(f"{g[0][1:]}.{cnt[g[0]]}")
net_groups = collections.defaultdict(list)
for i, g in enumerate(G):
    for r in g[2]:
        for num, name, net in PART[r][5]:
            if net != 'NC' and i not in net_groups[net]: net_groups[net].append(i)

def pin_sort(p):
    m = re.match(r'(\d+)', p[0]); return (int(m.group(1)) if m else 999, p[0])

BW, ROW, HEAD, LANE = 250, 17, 34, 26
def flag(x, y, n, col):
    if n == 'GND':
        return (f'<line x1="{x}" y1="{y}" x2="{x+14}" y2="{y}" stroke="{col}" stroke-width="2"/><line x1="{x+14}" y1="{y-6}" x2="{x+14}" y2="{y+6}" stroke="{col}" stroke-width="2"/>'
                f'<line x1="{x+18}" y1="{y-4}" x2="{x+18}" y2="{y+4}" stroke="{col}" stroke-width="2"/><line x1="{x+22}" y1="{y-2}" x2="{x+22}" y2="{y+2}" stroke="{col}" stroke-width="2"/><text x="{x+28}" y="{y+3.5}" class="net" fill="{col}">GND</text>')
    if n in ('+3V3', '+5V'):
        return (f'<line x1="{x}" y1="{y}" x2="{x+16}" y2="{y}" stroke="{col}" stroke-width="2.4"/><line x1="{x+16}" y1="{y-7}" x2="{x+16}" y2="{y+7}" stroke="{col}" stroke-width="2.4"/><text x="{x+22}" y="{y+3.5}" class="net" fill="{col}">{n}</text>')
    if n == 'NC':
        return f'<path d="M{x+4} {y-5}L{x+14} {y+5}M{x+14} {y-5}L{x+4} {y+5}" stroke="#e5484d" stroke-width="2.4"/><text x="{x+20}" y="{y+3.5}" class="ext">No-Connect flag</text>'
    return (f'<line x1="{x}" y1="{y}" x2="{x+14}" y2="{y}" stroke="{col}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="3" fill="{col}"/>'
            f'<rect x="{x+14}" y="{y-7}" width="{8+7*len(n)}" height="14" rx="3" fill="{col}"/><text x="{x+18}" y="{y+3.5}" class="flag">{html.escape(n)}</text>')

def where(i_other):
    return f"{SID[i_other]} {G[i_other][1].split(' - ')[0].title()}"

def section_svg(i):
    page, title, refs, note = G[i]
    pins_of = {r: sorted(PART[r][5], key=pin_sort) for r in refs}
    c = collections.Counter(p[2] for r in refs for p in pins_of[r])
    single = {n for n, k in c.items() if k == 1 and n not in FLAG and n != 'NC'}
    lanes = []
    for r in refs:
        for p in pins_of[r]:
            n = p[2]
            if n not in FLAG and n != 'NC' and n not in single and n not in lanes: lanes.append(n)
    nb = min(len(lanes), 4); BAND = (14 + nb * 14) if lanes else 0
    y = 18 + BAND; boxes = {}; maxx = [0]
    for r in refs:
        h = HEAD + len(pins_of[r]) * ROW + 6; boxes[r] = (y, h); y += h + 14
    H = y + 10
    lx = {n: BW + 74 + k * LANE for k, n in enumerate(lanes)}
    lane_end = BW + 74 + len(lanes) * LANE
    out = []; ys = collections.defaultdict(list)
    for r in refs:
        by, bh = boxes[r]; b = BOM_DESC.get(r); p = PART[r]
        role = p[2]; lab = f"{b[4]}  [{b[6]}]" if b else ''
        out.append(f'<g class="box"><rect x="8" y="{by}" width="{BW}" height="{bh}" rx="7" fill="var(--card)" stroke="var(--line)"/>'
                   f'<text x="16" y="{by+15}" class="ref">{r}</text><text x="{20+8.5*len(r)}" y="{by+15}" class="role">{html.escape(role)}</text>'
                   f'<text x="16" y="{by+27}" class="lab">{html.escape(lab)}</text>')
        for k, (num, name, net) in enumerate(pins_of[r]):
            py = by + HEAD + k * ROW + 7
            txt = num if name == num else f"{num} {name}"
            nm, col = cls(net)
            out.append(f'<text x="{BW-6}" y="{py+3.5}" text-anchor="end" class="pin">{html.escape(txt)}</text>')
            xd = BW + 8
            if net in FLAG or net == 'NC':
                out.append(f'<g class="w" data-net="{html.escape(net)}">{flag(xd, py, net, CG if net=="GND" else col)}</g>')
            elif net in single:
                xf = (BW + 74 + len(lanes) * LANE + 6) if lanes else xd
                others = [where(j) for j in net_groups[net] if j != i]
                tx = xf+14+8+7*len(net)+8; nt = "→ " + ", ".join(others)
                note_t = f'<text x="{tx}" y="{py+3.5}" class="ext">{html.escape(nt)}</text>' if others else ''
                maxx[0] = max(maxx[0], tx + 6.2*len(nt) if others else xf + 30 + 7*len(net))
                lead = f'<line x1="{xd}" y1="{py}" x2="{xf}" y2="{py}" stroke="{col}" stroke-width="2"/>' if xf != xd else ''
                out.append(f'<g class="w" data-net="{html.escape(net)}">{lead}{flag(xf, py, net, col)}{note_t}</g>')
            else:
                ys[net].append(py)
                out.append(f'<g class="w" data-net="{html.escape(net)}"><line x1="{xd}" y1="{py}" x2="{lx[net]}" y2="{py}" stroke="{col}" stroke-width="{3 if net in THICK else 2}"/><circle cx="{xd}" cy="{py}" r="3" fill="{col}"/><circle cx="{lx[net]}" cy="{py}" r="2.6" fill="{col}"/></g>')
        out.append('</g>')
    for li, n in enumerate(lanes):
        nm, col = cls(n); x = lx[n]; yy = ys[n]
        ext = [where(j) for j in net_groups[n] if j != i]
        top = 22 + (li % 4) * 14   # label band above all boxes
        g = f'<g class="w lane" data-net="{html.escape(n)}"><line x1="{x}" y1="{top}" x2="{x}" y2="{max(yy)}" stroke="{col}" stroke-width="{3 if n in THICK else 2}"/>'
        if ext: g += f'<polygon points="{x-4},{top+2} {x+4},{top+2} {x},{top-5}" fill="{col}"/>'
        lab = n + ("   → also in: " + ", ".join(ext) if ext else "")
        g += f'<text x="{x+8}" y="{top+1}" class="net" fill="{col}">{html.escape(n)}</text>'
        if ext: g += f'<text x="{x+14+7.2*len(n)}" y="{top+1}" class="ext">→ also in: {html.escape(", ".join(ext))}</text>'
        maxx[0] = max(maxx[0], x + 14 + 7.2*len(n) + (6.2*len("→ also in: " + ", ".join(ext)) if ext else 0))
        out.append(g + '</g>')
    W = int(max(maxx[0], lane_end + 60, BW + 140) + 20)
    return W, H, ''.join(out), len(refs), len(lanes)

REVIEW = '''<section class="card review"><h2>Check of your pages 1 and 2 (PDF 2026-11-13)</h2>
<p class="mut">Everything else on these two pages is wired correctly (F1, C1, D1 direction, U1 pins, C6/C7, Q3 + R16 + R17 + LED5, C8, U4 IN/GND/EN/ILIM/FAULT, U5 IN/C13/GND/OUT/C14/ILIM, R20 + SW5, LED6 direction, C11, C12).</p>
<ol>
<li><b>Page 1 - C5 is across D1.</b> It connects VBUS_F to +5V, bypassing the diode. Move it: C5 between <b>+5V and GND</b> (see POWER 1).</li>
<li><b>Page 1 - net label "V IO"</b> on Q3's emitter has a space. Rename it to <b>VIO</b> or it will not connect to the CH342F and SW3.</li>
<li><b>Page 2 - LED1 is reversed.</b> Its cathode (bar) faces U4 OUT, so it can never light. Flip it: anode (triangle side) towards U4 OUT / +3V3_T, cathode (bar) towards R3 and GND (see TARGET POWER 1).</li>
<li><b>Page 2 - U4 pin 6 OUT has no +3V3_T label.</b> Without it, nothing gets the switched 3.3 V (H1 pin 1, ESP-01, J3/J4, the pull-ups). Add a <b>+3V3_T</b> net label on U4 OUT.</li>
<li><b>Page 2 - U5 pin 3 EN has no TPWR_EN label.</b> So U4's enable (labelled TPWR_EN) is floating, and R20/SW5 only control U5. Add <b>TPWR_EN</b> on the U5 EN node.</li>
<li><b>Page 2 - U5 pin 4 /FAULT has no FAULT_N label.</b> U4's FAULT_N does not reach LED6. Add <b>FAULT_N</b> on the U5 /FAULT node.</li>
<li><b>Both pages - "+3v3" (lower-case v).</b> Pick one spelling and use it on every page. These docs use <b>+3V3</b>; EasyEDA treats differently spelled names as different nets.</li>
</ol></section>'''

cards = []
cur = None
for i, g in enumerate(G):
    if g[0] != cur:
        cur = g[0]
        pg = next(p for p in D['pages'] if p[0] == cur)
        cards.append(f'<h2 class="pagehead" id="{cur}">{html.escape(pg[1])}</h2>')
    W, H, body, npart, nl = section_svg(i)
    cards.append(f'<section class="card" id="s{SID[i]}"><h3>{SID[i]} &middot; {html.escape(g[1])} <span class="cnt">{npart} parts, {nl} lanes</span></h3>'
                 f'<p class="mut">{html.escape(g[3])}</p><div class="scroll"><svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="dia">{body}</svg></div></section>')

legend = ''.join(f'<span><i style="background:{c}"></i>{n}</span>' for n, c in (('5 V / USB power (thick)', C5), ('3.3 V (thick)', C3), ('Ground', CG), ('VIO / logic level', CVIO), ('USB', CUSB), ('UART data', CDATA), ('control / boot', CCTL), ('LED / fault', CLED), ('switch internals', CPWR)))
nav = ''.join(f'<a href="#{p[0]}">{html.escape(p[1].split("·")[1].strip())}</a>' for p in D['pages'])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flasher Wiring by Section</title>
<style>:root{{--bg:#f4f6f9;--fg:#1c2330;--mut:#5b6677;--card:#fff;--line:#c9d1dc}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0e1116;--fg:#e6e9ef;--mut:#9aa5b5;--card:#171c24;--line:#323b49}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,Segoe UI,sans-serif}}main{{max-width:1300px;margin:0 auto;padding:16px}}
h1{{font-size:1.35rem;margin:0}}h3{{font-size:1.02rem;margin:0 0 6px}}.cnt{{font-weight:400;color:var(--mut);font-size:13px;margin-left:8px}}.mut{{color:var(--mut);font-size:13px}}
.pagehead{{font-size:1.15rem;margin:26px 0 4px;padding:8px 12px;border-radius:10px;background:#0d9488;color:#fff}}
.card{{background:var(--card);border-radius:12px;padding:12px;margin:12px 0}}.scroll{{overflow-x:auto}}
.review{{border-left:5px solid #f59e0b}}.review ol{{margin:6px 0 0 18px;padding:0}}.review li{{margin:5px 0}}
.top{{position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:3}}.legend span{{display:inline-block;margin-right:14px;font-size:13px;color:var(--mut)}}.legend i{{display:inline-block;width:22px;height:5px;border-radius:3px;margin-right:5px;vertical-align:middle}}
.nav a{{display:inline-block;margin:4px 8px 0 0;font-size:13px;color:#0d9488;text-decoration:none;font-weight:600}}
svg.dia text{{font-family:system-ui,Segoe UI,sans-serif;fill:var(--fg)}}.ref{{font-size:12.5px;font-weight:700}}.role{{font-size:10.5px;fill:var(--mut)!important}}.lab{{font-size:9.5px;fill:var(--mut)!important}}
.pin{{font-size:11px}}.net{{font-size:11px;font-weight:700}}.ext{{font-size:10.5px;fill:var(--mut)!important}}.flag{{font-size:9.5px;font-weight:700;fill:#10151c!important}}
.w{{cursor:pointer;transition:opacity .15s}}svg.hl .w{{opacity:.18}}svg.hl .w.on{{opacity:1}}.w.done line{{stroke-dasharray:4 4}}
</style></head><body><main>
<h1>Universal USB Flasher V2.1 - wiring by section</h1>
<p class="mut">One diagram per small section, grouped by your 8 EasyEDA pages. Each box is a part (reference, role, LCSC number) with its pins on the right; a coloured wire runs from the pin to a vertical lane that joins every pin of the same net. Ground, +3V3 and +5V are drawn as symbols at the pin. An arrow at the top of a lane, or a grey note after a flag, means the net continues in another section: use a net label with exactly that name. <b>Hover</b> a wire to highlight the whole net, <b>click</b> it to mark it as wired (dashed). LEDs and D1: <b>A</b> = triangle side (+), <b>K</b> = bar side (-).</p>
<div class="top"><div class="legend">{legend}</div><div class="nav">{nav} &middot; <a href="index.html">design page</a> <a href="build-guide.html">build guide</a></div></div>
{REVIEW}
{"".join(cards)}
<p class="mut">Generated by tools/gen_wiring_sections.py from tools/design.json. This is a connection diagram of the netlist, not a schematic: compare with hardware/netlist.csv (43 nets) after ERC.</p>
</main><script>
document.querySelectorAll('svg.dia').forEach(svg=>{{
 let st={{}};try{{st=JSON.parse(localStorage.getItem('uusbf-wdone')||'{{}}')}}catch(e){{}}
 svg.querySelectorAll('.w').forEach(w=>{{ if(st[w.dataset.net]) w.classList.add('done');
  w.addEventListener('mouseenter',()=>{{svg.classList.add('hl');svg.querySelectorAll('.w').forEach(o=>o.classList.toggle('on',o.dataset.net===w.dataset.net))}});
  w.addEventListener('mouseleave',()=>{{svg.classList.remove('hl');svg.querySelectorAll('.w').forEach(o=>o.classList.remove('on'))}});
  w.addEventListener('click',()=>{{const n=w.dataset.net;const d=!w.classList.contains('done');document.querySelectorAll('.w').forEach(o=>{{if(o.dataset.net===n)o.classList.toggle('done',d)}});
   let s={{}};try{{s=JSON.parse(localStorage.getItem('uusbf-wdone')||'{{}}')}}catch(e){{}};s[n]=d;try{{localStorage.setItem('uusbf-wdone',JSON.stringify(s))}}catch(e){{}}}});
 }});
}});
</script></body></html>'''
out = os.path.join(ROOT, 'docs', 'wiring-by-section.html')
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('wrote', out, len(page), 'sections', len(G))
