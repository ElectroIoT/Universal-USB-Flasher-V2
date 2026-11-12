"""Generate animated SVGs for the Universal USB Flasher V2 repo.
Usage: python gen_svgs.py OUT_DIR
Animations use CSS keyframes and SMIL only (no JS), so they play inside <img> on GitHub."""
import sys, os
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "font-family:'Segoe UI',system-ui,-apple-system,Roboto,sans-serif"
BG = "#0b1622"; CARD = "#122235"; LINE = "#25405c"; INK = "#e6eef8"; MUTE = "#9cb0c6"; ACC = "#2dd4bf"
C = dict(v33="#f87171", v5="#c084fc", vio="#f472b6", gnd="#94a3b8", tx="#fb923c", rx="#4ade80",
         ctl="#60a5fa", esp="#facc15", usb="#22d3ee")

def wrap(w, h, body, style=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
<style>
text{{{FONT}}}
.t{{fill:{INK};font-weight:700;font-size:15px}}
.s{{fill:{MUTE};font-size:12.5px}}
.h{{fill:{INK};font-weight:800;font-size:22px}}
.box{{fill:{CARD};stroke:{LINE};stroke-width:2}}
.flow{{fill:none;stroke-width:4;stroke-linecap:round;stroke-dasharray:10 12;animation:flow 1.2s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-44}}}}
{style}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect width="{w}" height="{h}" rx="22" fill="{BG}"/>
{body}
</svg>'''

def save(name, svg):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(svg)
    print('wrote', name, len(svg))

# ---------------------------------------------------------------- hero board
PINS = [('3V3', C['v33']), ('5V', C['v5']), ('GND', '#475569'), ('TX', C['tx']), ('RX/UPDI', '#16a34a'), ('DTR', '#2563eb'),
        ('RTS', '#2563eb'), ('RST', '#ca8a04'), ('EN', '#ca8a04'), ('IO0', '#ca8a04'), ('IO15', '#64748b')]
def board(ox, oy, k):
    """board in mm scaled by k at offset"""
    def X(v): return ox + v * k
    def Y(v): return oy + v * k
    b = []
    b.append(f'<rect x="{X(1)}" y="{Y(2)}" width="{72*k}" height="{34*k}" rx="{2.4*k}" fill="#021a10"/>')
    b.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{72*k}" height="{34*k}" rx="{2.4*k}" fill="url(#pg)" stroke="#2bd48f66" stroke-width="2"/>')
    # traces
    tr = ["M8 16H20V18H30", "M8 18H19V20H22", "M30 18H36V15H44", "M30 19H36V20H44", "M46 15H60V9H66", "M46 20H62V24H66", "M14 29H26V10", "M30 22H40V26H66"]
    b.append(f'<g transform="translate({ox},{oy}) scale({k})" stroke="#2bd48f40" stroke-width=".45" fill="none">' + ''.join(f'<path d="{d}"/>' for d in tr) + '</g>')
    # data packets moving along a trace
    b.append(f'<g transform="translate({ox},{oy}) scale({k})"><path id="dp" d="M8 16H20V18H30M30 18H36V15H44H60V9H66" fill="none"/>'
             f'<circle r=".7" fill="{C["tx"]}"><animateMotion dur="2.4s" repeatCount="indefinite" rotate="auto"><mpath href="#dp"/></animateMotion></circle>'
             f'<circle r=".7" fill="{C["rx"]}"><animateMotion dur="3.1s" repeatCount="indefinite" keyPoints="1;0" keyTimes="0;1" calcMode="linear"><mpath href="#dp"/></animateMotion></circle></g>')
    g = [f'<g transform="translate({ox},{oy}) scale({k})">']
    g.append('<rect x="-1.5" y="12.5" width="9" height="9" rx="1.2" fill="#c0c7d1" stroke="#8a94a3" stroke-width=".3"/><rect x="-1.5" y="14.6" width="2.4" height="4.8" rx="1" fill="#3a4150"/>')
    g.append('<rect x="20" y="15" width="10" height="6" rx=".5" fill="url(#chipg)"/>')
    for i in range(8):
        g.append(f'<rect x="{20.6+i*1.27:.2f}" y="13.9" width=".5" height="1.1" fill="#cfd6df"/><rect x="{20.6+i*1.27:.2f}" y="21" width=".5" height="1.1" fill="#cfd6df"/>')
    g.append('<text x="25" y="18.6" text-anchor="middle" fill="#d1d5db" style="font-weight:700;font-size:1.2px">CH343G</text>')
    g.append('<rect x="20.8" y="4" width="6.5" height="3.5" rx=".3" fill="url(#chipg)"/><rect x="21.5" y="2.2" width="5" height="1.8" fill="#cfd6df"/><rect x="21" y="7.5" width="1" height="1.6" fill="#cfd6df"/><rect x="23.5" y="7.5" width="1" height="1.6" fill="#cfd6df"/><rect x="26" y="7.5" width="1" height="1.6" fill="#cfd6df"/>')
    g.append('<rect x="10.5" y="15.5" width="3" height="3" rx=".3" fill="url(#chipg)"/>')
    for x, y in [(11,11),(11,23),(17,13.5),(21,23.5),(25,23.5),(29,23.5),(30,4),(30,8),(18,5),(40,15),(40,20),(47,12.5),(51,12.5),(55,12.5),(35,24.5),(39,24.5),(43,24.5),(47,24.5),(51,24.5),(55,24.5),(50,17.5),(54,17.5),(58,17.5),(17,29.5),(43,30.5)]:
        g.append(f'<rect x="{x-1}" y="{y-.62}" width="2" height="1.25" rx=".15" fill="#3b2f22"/><rect x="{x-1}" y="{y-.62}" width=".45" height="1.25" fill="#d9dee5"/><rect x="{x+.55}" y="{y-.62}" width=".45" height="1.25" fill="#d9dee5"/>')
    for x, y in [(36,15),(36,20)]:
        g.append(f'<rect x="{x-1.4}" y="{y-.7}" width="2.8" height="1.4" rx=".2" fill="url(#chipg)"/>')
    for x, y, col, cls in [(17,11,'#ef4444','pwr'),(47,9.5,'#fb923c','txl'),(51,9.5,'#facc15','rxl'),(55,9.5,'#22c55e','act')]:
        g.append(f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="2.4" fill="{col}" opacity=".35"/><rect x="{x-1}" y="{y-.62}" width="2" height="1.25" rx=".2" fill="{col}"/></g>')
    for x, y in [(36,3.5),(42.5,3.5)]:
        g.append(f'<rect x="{x-2.5}" y="{y-1.5}" width="5" height="3" rx=".4" fill="#e5e7eb"/><circle cx="{x}" cy="{y}" r=".9" fill="#1f2937"/>')
    for x, y in [(50,3.5),(59,3.5)]:
        g.append(f'<rect x="{x-3.5}" y="{y-1.4}" width="7" height="2.8" rx=".3" fill="#cbd5e1"/><rect x="{x-2.2}" y="{y-.8}" width="1.8" height="1.6" fill="#111827" class="slide"/>')
    for i, (lab, col) in enumerate(PINS):
        y = 5.3 + i * 2.54
        g.append(f'<rect x="68.3" y="{y-1.1:.2f}" width="2.4" height="2.2" fill="#111827"/><rect x="69.1" y="{y-.35:.2f}" width=".8" height=".7" fill="#f4c542"/><rect x="61.6" y="{y-.95:.2f}" width="5.6" height="1.9" rx=".4" fill="{col}"/><text x="64.4" y="{y+.48:.2f}" text-anchor="middle" fill="#fff" style="font-weight:800;font-size:1.15px">{lab}</text>')
    g.append('<rect x="46.9" y="28" width="10.2" height="5.1" rx=".4" fill="#111827"/>')
    for r in range(2):
        for i in range(4):
            g.append(f'<rect x="{48.2+i*2.54-.4:.2f}" y="{29.27+r*2.54-.4:.2f}" width=".8" height=".8" fill="#475569"/>')
    g.append(f'<rect x="44.85" y="32" width="14.3" height="11" rx=".8" fill="#0f172a" opacity=".9" stroke="{C["esp"]}" stroke-width=".25" stroke-dasharray="1 .6"/><text x="52" y="38.6" text-anchor="middle" fill="{C["esp"]}" style="font-weight:700;font-size:1.4px">ESP-01</text>')
    for x, y in [(4,3.5),(4,30.5),(38.5,30.5)]:
        g.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#d4a34a"/><circle cx="{x}" cy="{y}" r="1" fill="#02150d"/>')
    g.append('<text x="8" y="33.1" fill="#e5e7eb" style="font-weight:800;font-size:1.3px">USB FLASHER V2 · ElectroIoT</text></g>')
    return ''.join(b) + ''.join(g)

defs = '''<defs><linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f7a4f"/><stop offset="1" stop-color="#07432b"/></linearGradient>
<linearGradient id="chipg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f36"/><stop offset="1" stop-color="#121418"/></linearGradient>
<radialGradient id="glow" cx="80%" cy="0%" r="70%"><stop offset="0" stop-color="#14b8a6" stop-opacity=".35"/><stop offset="1" stop-color="#14b8a6" stop-opacity="0"/></radialGradient></defs>'''
hero_style = '''
.txl{animation:blink .35s steps(2,start) infinite}
.rxl{animation:blink .45s steps(2,start) .2s infinite}
.act{animation:breathe 2.4s ease-in-out infinite}
.pwr{animation:breathe 4s ease-in-out infinite}
@keyframes blink{0%{opacity:1}50%{opacity:.15}}
@keyframes breathe{50%{opacity:.55}}
.float{animation:float 5s ease-in-out infinite}
@keyframes float{50%{transform:translateY(-6px)}}
'''
body = defs + '<rect width="1200" height="560" rx="22" fill="url(#glow)"/>'
body += f'<text x="56" y="92" style="fill:{ACC};font-weight:800;font-size:15px;letter-spacing:3px">ELECTROIOT · OPEN HARDWARE</text>'
body += f'<text x="56" y="150" style="fill:{INK};font-weight:800;font-size:50px">Universal USB</text>'
body += f'<text x="56" y="206" style="fill:#5eead4;font-weight:800;font-size:50px">Flasher V2</text>'
body += f'<text x="56" y="252" class="s" style="font-size:18px">ESP32 · ESP8266 · ESP-01 · Arduino · UPDI AVR</text>'
body += f'<text x="56" y="280" class="s" style="font-size:18px">One USB-C board. True 3.3 V / 5 V logic. No buttons.</text>'
badges = ['CH343G + VIO', 'Auto-program', 'ESP-01 socket', 'SerialUPDI', 'USB-C + PTC + ESD']
x, yb = 56, 312
for btxt in badges:
    w = 18 + len(btxt) * 8.0
    if x + w > 500:
        x, yb = 56, yb + 42
    body += f'<rect x="{x:.0f}" y="{yb}" width="{w:.0f}" height="32" rx="9" fill="#ffffff12" stroke="#ffffff30"/><text x="{x+w/2:.0f}" y="{yb+21}" text-anchor="middle" style="fill:{INK};font-weight:700;font-size:13px">{btxt}</text>'
    x += w + 10
body += f'<text x="56" y="{yb+84}" class="s" style="font-size:14px">72 × 34 mm · 2-layer · LCSC parts · EasyEDA</text>'
body += f'<g class="float">{board(530, 90, 8.8)}</g>'
save('hero.svg', wrap(1200, 560, body, hero_style))

# ---------------------------------------------------------------- power flow
st = ''
b = defs
b += '<text x="40" y="52" class="h">Power path</text><text x="40" y="78" class="s">USB 5 V → polyfuse → Schottky → 3.3 V LDO. The IO switch picks the logic level for the CH343G.</text>'
stages = [(40, 'USB-C', 'VBUS', '5.0 V', C['v5']), (220, 'F1 PTC', '500 mA hold', '5.0 V', C['v5']), (400, 'D1 Schottky', 'back-feed block', '≈4.65 V', C['v5']), (580, 'U1 LDO', 'SGM2212 800 mA', '3.30 V', C['v33'])]
for i, (x, t, sub, v, col) in enumerate(stages):
    b += f'<rect class="box" x="{x}" y="120" width="140" height="76" rx="14"/><text class="t" x="{x+70}" y="152" text-anchor="middle">{t}</text><text class="s" x="{x+70}" y="174" text-anchor="middle">{sub}</text>'
    b += f'<rect x="{x+38}" y="96" width="64" height="22" rx="11" fill="{col}22" stroke="{col}"/><text x="{x+70}" y="112" text-anchor="middle" style="fill:{col};font-weight:800;font-size:12.5px">{v}</text>'
    if i < 3:
        b += f'<path class="flow" d="M{x+142} 158H{x+178}" stroke="{col}"/>'
b += f'<path class="flow" d="M722 158H800" stroke="{C["v33"]}"/><rect class="box" x="800" y="120" width="150" height="76" rx="14"/><text class="t" x="875" y="152" text-anchor="middle">+3V3 rail</text><text class="s" x="875" y="174" text-anchor="middle">H1 · ESP-01 · pull-ups</text>'
# branches
b += f'<path class="flow" d="M290 198V262H360" stroke="{C["v5"]}"/><rect class="box" x="360" y="232" width="180" height="60" rx="14"/><text class="t" x="450" y="258" text-anchor="middle">CH343G core</text><text class="s" x="450" y="278" text-anchor="middle">VDD5 + VBUS sense</text>'
b += f'<path class="flow" d="M470 198V214H640V262H690" stroke="{C["v5"]}" style="animation-duration:1.6s"/>'
b += f'<path class="flow" d="M875 198V262H840" stroke="{C["v33"]}" style="animation-duration:1.6s"/>'
b += f'<rect class="box" x="690" y="232" width="150" height="60" rx="14" style="stroke:{C["vio"]}"/><text class="t" x="765" y="258" text-anchor="middle">SW3 → VIO</text><text class="s" x="765" y="278" text-anchor="middle">3V3 or 5V logic</text>'
b += f'<path class="flow" d="M765 294V330H450V294" stroke="{C["vio"]}" style="animation-duration:1.4s"/><text x="610" y="324" text-anchor="middle" style="fill:{C["vio"]};font-weight:700;font-size:12.5px">VIO → CH343G I/O pins</text>'
b += '<text x="40" y="372" class="s">Short on the 5V pin? The PTC heats up and limits current, so the PC port stays safe. It resets on its own once the short is removed.</text>'
save('power-flow.svg', wrap(1000, 400, b, st))

# ---------------------------------------------------------------- auto-program timing
st = '''
.wave{fill:none;stroke-width:3.2;stroke-linejoin:round}
.cursor{animation:sweep 6s linear infinite}
@keyframes sweep{from{transform:translateX(0)}to{transform:translateX(700px)}}
.reveal{animation:reveal 6s linear infinite}
@keyframes reveal{from{width:0}to{width:700px}}
.ph{opacity:.0;animation:ph 6s linear infinite}
@keyframes ph{0%,100%{opacity:.25}}
'''
b = '<defs><clipPath id="clipw"><rect class="reveal" x="200" y="100" width="0" height="300"/></clipPath></defs>'
b += '<text x="40" y="52" class="h">How auto-program works</text><text x="40" y="78" class="s">esptool toggles DTR/RTS. Q1 and Q2 turn that into a reset with IO0 held low, so the ESP enters the bootloader by itself.</text>'
x0, x1 = 200, 900
phases = [(200, 330, 'Idle', '#334155'), (330, 470, '① Reset', '#7f1d1d'), (470, 620, '② Boot', '#713f12'), (620, 900, '③ Flashing', '#064e3b')]
for a, c, lab, col in phases:
    b += f'<rect x="{a}" y="100" width="{c-a}" height="280" fill="{col}" opacity=".28"/><text x="{(a+c)/2}" y="122" text-anchor="middle" style="fill:{INK};font-weight:800;font-size:13px">{lab}</text>'
rows = [('DTR#', C['ctl'], [(200,1),(470,0),(620,1)]), ('RTS#', C['ctl'], [(200,1),(330,0),(470,1)]),
        ('EN', C['esp'], [(200,1),(330,0),(470,1)]), ('IO0', C['esp'], [(200,1),(470,0),(640,1)])]
for r, (name, col, pts) in enumerate(rows):
    yb = 180 + r * 58
    hi, lo = yb - 22, yb + 14
    b += f'<text x="40" y="{yb}" class="t" style="fill:{col}">{name}</text><text x="120" y="{yb}" class="s">{"PC output" if r < 2 else "to ESP"}</text>'
    b += f'<path d="M{x0} {lo+6}H{x1}" stroke="{LINE}" stroke-width="1"/>'
    d = ''
    lvl = None
    for i, (x, v) in enumerate(pts):
        y = hi if v else lo
        if i == 0:
            d = f'M{x} {y}'
        else:
            d += f'H{x}V{y}'
    d += f'H{x1}'
    b += f'<path class="wave" d="{d}" stroke="{col}" opacity=".18"/>'
    b += f'<path class="wave" d="{d}" stroke="{col}" clip-path="url(#clipw)"/>'
b += f'<g class="cursor"><path d="M200 100V380" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 4"/><circle cx="200" cy="100" r="5" fill="{ACC}"/></g>'
b += f'<text x="40" y="412" class="s">EN goes low (reset) → IO0 goes low while EN rises → the ESP boots into download mode. When a serial monitor asserts both lines, nothing resets.</text>'
save('auto-program.svg', wrap(960, 430, b, st))

# ---------------------------------------------------------------- VIO switch
st = '''
.lever{transform-origin:150px 190px;animation:lever 6s ease-in-out infinite}
@keyframes lever{0%,40%{transform:rotate(-28deg)}50%,90%{transform:rotate(28deg)}100%{transform:rotate(-28deg)}}
.w33{animation:w33 6s step-end infinite}.w5{animation:w5 6s step-end infinite}
@keyframes w33{0%{opacity:1}45%{opacity:0}95%{opacity:1}}
@keyframes w5{0%{opacity:0}45%{opacity:1}95%{opacity:0}}
.scroll{animation:scroll 1.5s linear infinite}
@keyframes scroll{to{transform:translateX(-80px)}}
'''
b = '<defs><clipPath id="cv"><rect x="330" y="110" width="600" height="170"/></clipPath></defs>'
b += '<text x="40" y="52" class="h">3.3 V / 5 V logic switch (SW3)</text><text x="40" y="78" class="s">SW3 feeds the CH343G VIO pin, so TX, RX, DTR and RTS swing to the target\'s own voltage. No level shifter is needed.</text>'
b += f'<circle cx="150" cy="190" r="12" fill="{C["vio"]}"/><path d="M150 190V290" stroke="{C["vio"]}" stroke-width="4"/><text x="150" y="312" text-anchor="middle" style="fill:{C["vio"]};font-weight:800">VIO</text>'
b += f'<circle cx="95" cy="125" r="9" fill="none" stroke="{C["v33"]}" stroke-width="3"/><text x="95" y="108" text-anchor="middle" style="fill:{C["v33"]};font-weight:800">3V3</text>'
b += f'<circle cx="205" cy="125" r="9" fill="none" stroke="{C["v5"]}" stroke-width="3"/><text x="205" y="108" text-anchor="middle" style="fill:{C["v5"]};font-weight:800">5V</text>'
b += f'<g class="lever"><path d="M150 190V122" stroke="{INK}" stroke-width="6" stroke-linecap="round"/></g>'
# waveforms
def sq(amp, y0):
    d = f'M330 {y0}'
    x = 330
    for i in range(10):
        d += f'H{x+40}V{y0-amp}H{x+80}V{y0}'
        x += 80
    return d
b += f'<path d="M330 260H930" stroke="{LINE}"/><text x="320" y="264" text-anchor="end" class="s">0 V</text>'
b += f'<g clip-path="url(#cv)"><g class="w33"><path class="scroll" d="{sq(66,260)}" fill="none" stroke="{C["v33"]}" stroke-width="3.5"/></g><g class="w5"><path class="scroll" d="{sq(124,260)}" fill="none" stroke="{C["v5"]}" stroke-width="3.5"/></g></g>'
b += f'<g class="w33"><path d="M330 194H930" stroke="{C["v33"]}" stroke-dasharray="4 6" opacity=".6"/><text x="320" y="198" text-anchor="end" style="fill:{C["v33"]};font-weight:800">3.3 V</text><text x="630" y="304" text-anchor="middle" class="t">ESP32 · ESP8266 · ESP-01 · 3.3 V Pro Mini</text></g>'
b += f'<g class="w5"><path d="M330 136H930" stroke="{C["v5"]}" stroke-dasharray="4 6" opacity=".6"/><text x="320" y="140" text-anchor="end" style="fill:{C["v5"]};font-weight:800">≈4.6 V</text><text x="630" y="304" text-anchor="middle" class="t">Arduino Uno chip · 5 V Pro Mini · 5 V ATtiny</text></g>'
save('vio-switch.svg', wrap(960, 340, b, st))

# ---------------------------------------------------------------- UPDI mode
st = '''
.uart{animation:m1 8s step-end infinite}.updi{animation:m2 8s step-end infinite}
@keyframes m1{0%{opacity:1}50%{opacity:0}}
@keyframes m2{0%{opacity:0}50%{opacity:1}}
.knob{animation:knob 8s step-end infinite}
@keyframes knob{0%{transform:translateX(0)}50%{transform:translateX(34px)}}
'''
b = '<text x="40" y="52" class="h">UART ⇄ UPDI mode (SW4)</text><text x="40" y="78" class="s">Slide SW4 to UPDI: TX is linked to RX through 4.7 kΩ, and RX/UPDI becomes a one-wire programmer for ATtiny 0/1/2-series and AVR-Dx.</text>'
b += f'<rect x="60" y="130" width="80" height="34" rx="8" fill="#cbd5e1"/><g class="knob"><rect x="66" y="135" width="34" height="24" rx="5" fill="#111827"/></g><text x="100" y="188" text-anchor="middle" class="t">SW4</text>'
b += f'<g class="uart"><text x="100" y="118" text-anchor="middle" style="fill:{C["tx"]};font-weight:800">UART</text></g><g class="updi"><text x="100" y="118" text-anchor="middle" style="fill:{C["rx"]};font-weight:800">UPDI</text></g>'
b += f'<rect class="box" x="220" y="110" width="150" height="170" rx="16" style="stroke:{ACC}"/><text class="t" x="295" y="200" text-anchor="middle">CH343G</text>'
# UART group
u = f'<path d="M370 160H760" stroke="{C["tx"]}" stroke-width="4"/><path d="M370 230H760" stroke="{C["rx"]}" stroke-width="4"/>'
u += f'<text x="390" y="150" style="fill:{C["tx"]};font-weight:800">TX →</text><text x="390" y="252" style="fill:{C["rx"]};font-weight:800">← RX</text>'
u += f'<circle r="6" fill="{C["tx"]}"><animateMotion dur="1.6s" repeatCount="indefinite" path="M380 160H750"/></circle><circle r="6" fill="{C["rx"]}"><animateMotion dur="1.6s" begin=".8s" repeatCount="indefinite" path="M750 230H380"/></circle>'
u += f'<rect class="box" x="760" y="120" width="170" height="140" rx="16"/><text class="t" x="845" y="186" text-anchor="middle">ESP / Arduino</text><text class="s" x="845" y="208" text-anchor="middle">normal serial</text>'
b += f'<g class="uart">{u}</g>'
# UPDI group
v = f'<path d="M370 160H470V190" stroke="{C["tx"]}" stroke-width="4"/><rect x="456" y="190" width="28" height="44" rx="4" fill="{CARD}" stroke="{INK}" stroke-width="2"/><text x="500" y="217" class="s">4.7 kΩ</text>'
v += f'<path d="M470 234V250" stroke="{C["rx"]}" stroke-width="4"/><path d="M370 250H760" stroke="{C["rx"]}" stroke-width="4"/><circle cx="470" cy="250" r="6" fill="{C["rx"]}"/>'
v += f'<text x="600" y="240" text-anchor="middle" style="fill:{C["rx"]};font-weight:800">UPDI (one wire, both ways)</text>'
v += f'<circle r="6" fill="{C["rx"]}"><animateMotion dur="1.4s" repeatCount="indefinite" path="M480 250H750"/></circle><circle r="6" fill="{C["esp"]}"><animateMotion dur="1.4s" begin=".7s" repeatCount="indefinite" path="M750 250H480"/></circle>'
v += f'<rect class="box" x="760" y="120" width="170" height="160" rx="16" style="stroke:{C["rx"]}"/><text class="t" x="845" y="190" text-anchor="middle">ATtiny1614</text><text class="s" x="845" y="212" text-anchor="middle">AVR-DA / DB / DD</text><text class="s" x="845" y="234" text-anchor="middle">UPDI pin</text>'
b += f'<g class="updi">{v}</g>'
b += '<text x="40" y="318" class="s">Arduino IDE: megaTinyCore / DxCore → Programmer "SerialUPDI - 230400 baud". Or: pymcuprog -t uart -u COMx -d attiny1614 write -f app.hex</text>'
save('updi-mode.svg', wrap(960, 340, b, st))

# ---------------------------------------------------------------- data flow / targets
st = '''
.pulse{animation:pulse 2s ease-in-out infinite}
@keyframes pulse{50%{opacity:.45}}
'''
b = '<text x="40" y="52" class="h">One board, every common target</text><text x="40" y="78" class="s">PC software talks to a COM port. The flasher turns it into UART plus control lines for the module you plug in or wire up.</text>'
# laptop
b += f'<rect x="50" y="140" width="150" height="96" rx="8" fill="{CARD}" stroke="{LINE}" stroke-width="2"/><rect x="62" y="152" width="126" height="72" rx="4" fill="#0f2a3d"/><path d="M30 244H220L208 258H42Z" fill="{LINE}"/>'
b += f'<text x="125" y="186" text-anchor="middle" style="fill:{ACC};font-weight:800;font-size:13px">esptool</text><text x="125" y="204" text-anchor="middle" class="s">Arduino IDE · PIO</text>'
b += f'<path class="flow" d="M222 200H330" stroke="{C["usb"]}"/><text x="276" y="190" text-anchor="middle" class="s">USB-C</text>'
b += f'<rect class="box" x="330" y="146" width="170" height="108" rx="16" style="stroke:{ACC}"/><text class="t" x="415" y="190" text-anchor="middle">Flasher V2</text><text class="s" x="415" y="212" text-anchor="middle">CH343G + auto-program</text>'
targets = [('ESP32 / S3 / C3', 'auto-program', C['esp']), ('ESP8266 / ESP-12F', 'IO15 pull-down', C['esp']), ('ESP-01 / 01S', 'plug into J2', C['esp']), ('Arduino / ATmega', 'RST pin (DTR+cap)', C['tx']), ('ATtiny / AVR-Dx', 'UPDI mode', C['rx'])]
for i, (t, sub, col) in enumerate(targets):
    y = 104 + i * 62
    b += f'<path class="flow" d="M502 200C560 200 560 {y+24} 620 {y+24}" stroke="{col}" style="animation-duration:{1.1+i*.15:.2f}s"/>'
    b += f'<rect class="box" x="620" y="{y}" width="300" height="48" rx="12"/><circle class="pulse" cx="644" cy="{y+24}" r="7" fill="{col}" style="animation-delay:{i*.3:.1f}s"/><text class="t" x="664" y="{y+22}">{t}</text><text class="s" x="664" y="{y+40}">{sub}</text>'
save('targets.svg', wrap(960, 430, b, st))
