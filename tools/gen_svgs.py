"""Generate the animated SVG diagrams in images/ for Universal USB Flasher V2.

    python tools/gen_svgs.py            (writes to images/)

The board render is drawn from tools/design.json (placement), so it follows the design.
Animations use CSS keyframes and SMIL only (no JS), so they play inside <img> on GitHub."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'images')
os.makedirs(OUT, exist_ok=True)
D = json.load(open(os.path.join(ROOT, 'tools', 'design.json'), encoding='utf-8'))

FONT = "font-family:'Segoe UI',system-ui,-apple-system,Roboto,sans-serif"
BG = "#0b1622"; CARD = "#122235"; LINE = "#25405c"; INK = "#e6eef8"; MUTE = "#9cb0c6"; ACC = "#2dd4bf"
C = dict(v33="#f87171", v5="#c084fc", vio="#f472b6", gnd="#94a3b8", tx="#fb923c", rx="#4ade80",
         ctl="#60a5fa", esp="#facc15", usb="#22d3ee", tgt="#fb923c", red="#ef4444", blue="#3b82f6")

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
    open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(svg)
    print('wrote', name, len(svg))

DEFS = '''<defs><linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f7a4f"/><stop offset="1" stop-color="#07432b"/></linearGradient>
<linearGradient id="chipg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f36"/><stop offset="1" stop-color="#121418"/></linearGradient>
<radialGradient id="glow" cx="80%" cy="0%" r="70%"><stop offset="0" stop-color="#14b8a6" stop-opacity=".35"/><stop offset="1" stop-color="#14b8a6" stop-opacity="0"/></radialGradient></defs>'''

# ---------------------------------------------------------------- board render (data-driven)
PINLAB = [('3V3', '#ef4444'), ('5V', '#a855f7'), ('GND', '#475569'), ('TX', '#f97316'), ('RX/UPDI', '#16a34a'), ('DTR', '#2563eb'),
          ('RTS', '#2563eb'), ('RST', '#ca8a04'), ('EN', '#ca8a04'), ('IO0', '#ca8a04'), ('IO15', '#64748b')]
LEDCOL = {'LED1': ('#22c55e', 'pwr'), 'LED2': ('#fb923c', 'txl'), 'LED3': ('#facc15', 'rxl'), 'LED4': ('#3b82f6', 'rx2l'), 'LED5': ('#ef4444', 'off'), 'LED6': ('#ef4444', 'off')}

def board(ox, oy, k):
    W, H = D['board']['w'], D['board']['h']
    pl = {p[0]: p for p in D['placement']}
    o = [f'<g transform="translate({ox},{oy}) scale({k})">']
    o.append(f'<rect x="1" y="2" width="{W}" height="{H}" rx="2.4" fill="#021a10"/><rect width="{W}" height="{H}" rx="2.4" fill="url(#pg)" stroke="#2bd48f66" stroke-width=".25"/>')
    def c(r): return pl[r][1], pl[r][2]
    # decorative traces between real part positions
    tr = [('USB1', 'U3'), ('U3', 'U2'), ('U2', 'Q1'), ('U2', 'Q2'), ('Q1', 'U6'), ('Q2', 'U7'), ('U6', 'H1'), ('U7', 'H1'), ('U1', 'U4'), ('D1', 'U5'), ('U2', 'LED2'), ('U2', 'J5')]
    o.append('<g stroke="#2bd48f40" stroke-width=".45" fill="none">')
    for a, b in tr:
        (x1, y1), (x2, y2) = c(a), c(b)
        if a == 'USB1':
            x1 += 3.7
        o.append(f'<path d="M{x1} {y1}H{(x1+x2)/2:.1f}V{y2}H{x2}"/>')
    o.append('</g>')
    # moving data dots
    (ux, uy), (cx, cy), (hx, hy) = c('USB1'), c('U2'), c('U6')
    path = f'M{ux+3.7} {uy}H{cx}V{cy}H{hx}H{W-3}'
    o.append(f'<path id="dp" d="{path}" fill="none"/><circle r=".75" fill="{C["tx"]}"><animateMotion dur="2.4s" repeatCount="indefinite"><mpath href="#dp"/></animateMotion></circle>'
             f'<circle r=".75" fill="{C["rx"]}"><animateMotion dur="3.1s" repeatCount="indefinite" keyPoints="1;0" keyTimes="0;1" calcMode="linear"><mpath href="#dp"/></animateMotion></circle>')
    for r, x, y, w, h, g, lab in D['placement']:
        x0, y0 = x - w / 2, y - h / 2
        if r == 'USB1':
            o.append(f'<rect x="{x0-1.5}" y="{y0}" width="{w+1.5}" height="{h}" rx="1.2" fill="#c0c7d1" stroke="#8a94a3" stroke-width=".3"/><rect x="{x0-1.5}" y="{y-2.4}" width="2.4" height="4.8" rx="1" fill="#3a4150"/>')
        elif r in LEDCOL:
            col, cls = LEDCOL[r]
            o.append(f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="2.3" fill="{col}" opacity=".35"/><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx=".2" fill="{col}"/></g>')
        elif r[0] in 'RC' and not r.startswith('RS'):
            body = '#3b2f22' if r[0] == 'R' else '#b08d57'
            o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx=".15" fill="{body}"/><rect x="{x0}" y="{y0}" width=".45" height="{h}" fill="#d9dee5"/><rect x="{x0+w-.45}" y="{y0}" width=".45" height="{h}" fill="#d9dee5"/>')
        elif r in ('SW1', 'SW2', 'SW5'):
            o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx=".4" fill="#e5e7eb"/><circle cx="{x}" cy="{y}" r=".9" fill="#1f2937"/>')
        elif r in ('SW3', 'SW4'):
            o.append(f'<rect x="{x0}" y="{y0+.1}" width="{w}" height="{h-.2}" rx=".3" fill="#cbd5e1"/><rect x="{x-2.2}" y="{y-.8}" width="1.8" height="1.6" fill="#111827"/>')
        elif r == 'H1':
            for i, (lb, col) in enumerate(PINLAB):
                py = y - 12.7 + i * 2.54
                o.append(f'<rect x="{x-1.2}" y="{py-1.1:.2f}" width="2.4" height="2.2" fill="#111827"/><rect x="{x-.4}" y="{py-.35:.2f}" width=".8" height=".7" fill="#f4c542"/>'
                         f'<rect x="{x-8.6}" y="{py-.95:.2f}" width="6" height="1.9" rx=".4" fill="{col}"/><text x="{x-5.6}" y="{py+.48:.2f}" text-anchor="middle" fill="#fff" style="font-weight:800;font-size:1.1px">{lb}</text>')
        elif r in ('J2', 'J3', 'J4', 'J5'):
            rows, cols, pt = {'J2': (2, 4, 2.54), 'J3': (2, 3, 1.27), 'J4': (2, 3, 2.54), 'J5': (1, 4, 2.54)}[r]
            o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx=".4" fill="#111827"/>')
            if r == 'J3':
                o.append(f'<rect x="{x0+.6}" y="{y0+.6}" width="{w-1.2}" height="{h-1.2}" rx=".3" fill="#1f2937"/><rect x="{x0}" y="{y-.9}" width=".6" height="1.8" fill="{BG}"/>')
            for rr in range(rows):
                for cc in range(cols):
                    px, py = x - (cols - 1) * pt / 2 + cc * pt, y - (rows - 1) * pt / 2 + rr * pt
                    s = pt * .3
                    o.append(f'<rect x="{px-s/2:.2f}" y="{py-s/2:.2f}" width="{s:.2f}" height="{s:.2f}" fill="{"#f4c542" if r != "J2" else "#475569"}"/>')
        elif r.startswith('SJ'):
            o.append(f'<rect x="{x0}" y="{y0}" width="{w*.45}" height="{h}" fill="#d4a34a"/><rect x="{x0+w*.55}" y="{y0}" width="{w*.45}" height="{h}" fill="#d4a34a"/><rect x="{x0+w*.4}" y="{y-.2}" width="{w*.2}" height=".4" fill="#d4a34a"/>')
        else:  # ICs, transistors, diode, fuse
            o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx=".3" fill="url(#chipg)"/>')
            if r == 'U2':
                for i in range(6):
                    for (dx, dy) in ((x0 + .7 + i * .7, y0 - .25), (x0 + .7 + i * .7, y0 + h - .05), (x0 - .25, y0 + .7 + i * .7), (x0 + w - .05, y0 + .7 + i * .7)):
                        o.append(f'<rect x="{dx:.2f}" y="{dy:.2f}" width=".3" height=".3" fill="#cfd6df"/>')
                o.append(f'<circle cx="{x0+.6}" cy="{y0+.6}" r=".25" fill="#9ca3af"/><text x="{x}" y="{y+.45}" text-anchor="middle" fill="#d1d5db" style="font-weight:700;font-size:1.05px">CH342F</text>')
            elif r == 'U1':
                o.append(f'<rect x="{x0+.7}" y="{y0-1.6}" width="{w-1.4}" height="1.6" fill="#cfd6df"/>')
            elif w >= 3 and h >= 3:
                o.append(f'<text x="{x}" y="{y+.35}" text-anchor="middle" fill="#9ca3af" style="font-weight:700;font-size:.75px">{lab}</text>')
    for hx_, hy_ in D['board']['holes']:
        o.append(f'<circle cx="{hx_}" cy="{hy_}" r="1.6" fill="#d4a34a"/><circle cx="{hx_}" cy="{hy_}" r="1" fill="#02150d"/>')
    jx, jy = c('J2')
    o.append(f'<rect x="{jx-7.15}" y="{jy+2.4}" width="14.3" height="10" rx=".8" fill="#0f172a" opacity=".92" stroke="{C["esp"]}" stroke-width=".25" stroke-dasharray="1 .6"/><text x="{jx}" y="{jy+8.4}" text-anchor="middle" fill="{C["esp"]}" style="font-weight:700;font-size:1.4px">ESP-01</text>')
    o.append(f'<text x="8" y="{H-.9}" fill="#e5e7eb" style="font-weight:800;font-size:1.3px">USB FLASHER V2.1 · ElectroIoT</text>')
    o.append('</g>')
    return ''.join(o)

hero_style = '''
.txl{animation:blink .35s steps(2,start) infinite}
.rxl{animation:blink .45s steps(2,start) .2s infinite}
.rx2l{animation:blink .6s steps(2,start) .1s infinite}
.pwr{animation:breathe 4s ease-in-out infinite}
.off{opacity:.25}
@keyframes blink{0%{opacity:1}50%{opacity:.15}}
@keyframes breathe{50%{opacity:.6}}
.float{animation:float 5s ease-in-out infinite}
@keyframes float{50%{transform:translateY(-6px)}}
'''
body = DEFS + '<rect width="1200" height="560" rx="22" fill="url(#glow)"/>'
body += f'<text x="50" y="92" style="fill:{ACC};font-weight:800;font-size:15px;letter-spacing:3px">ELECTROIOT · OPEN HARDWARE</text>'
body += f'<text x="50" y="150" style="fill:{INK};font-weight:800;font-size:48px">Universal USB</text>'
body += f'<text x="50" y="204" style="fill:#5eead4;font-weight:800;font-size:48px">Flasher V2</text>'
body += f'<text x="50" y="248" class="s" style="font-size:17px">ESP32 · ESP8266 · ESP-01 · Arduino · UPDI AVR</text>'
body += f'<text x="50" y="274" class="s" style="font-size:17px">Dual UART. True 3.3 V / 5 V logic. Current-limited.</text>'
x, yb = 50, 300
for btxt in ['CH342F dual UART', 'Auto-program', 'ESP-Prog port', 'Target power switch', 'ESP-01 socket', 'SerialUPDI', 'ESD on every line']:
    w = 18 + len(btxt) * 7.9
    if x + w > 470:
        x, yb = 50, yb + 40
    body += f'<rect x="{x:.0f}" y="{yb}" width="{w:.0f}" height="30" rx="9" fill="#ffffff12" stroke="#ffffff30"/><text x="{x+w/2:.0f}" y="{yb+20}" text-anchor="middle" style="fill:{INK};font-weight:700;font-size:12.5px">{btxt}</text>'
    x += w + 9
body += f'<text x="50" y="{yb+72}" class="s" style="font-size:14px">{D["board"]["w"]} × {D["board"]["h"]} mm · 2-layer · LCSC parts · EasyEDA</text>'
body += f'<g class="float">{board(490, 70, 8.4)}</g>'
save('hero.svg', wrap(1200, 560, body, hero_style))

# ---------------------------------------------------------------- power flow (with target switches)
b = DEFS
b += '<text x="40" y="52" class="h">Power path</text><text x="40" y="78" class="s">USB 5 V → polyfuse → Schottky → LDO → current-limited target switches. The IO switch picks the CH342F logic level.</text>'
stages = [(30, 'USB-C', 'VBUS', '5.0 V', C['v5']), (190, 'F1 PTC', '500 mA hold', '5.0 V', C['v5']), (350, 'D1 Schottky', 'back-feed block', '≈4.65 V', C['v5']), (510, 'U1 LDO', 'SGM2212 800 mA', '3.30 V', C['v33'])]
for i, (x, t, sub, v, col) in enumerate(stages):
    b += f'<rect class="box" x="{x}" y="120" width="130" height="76" rx="14"/><text class="t" x="{x+65}" y="152" text-anchor="middle">{t}</text><text class="s" x="{x+65}" y="174" text-anchor="middle">{sub}</text>'
    b += f'<rect x="{x+33}" y="96" width="64" height="22" rx="11" fill="{col}22" stroke="{col}"/><text x="{x+65}" y="112" text-anchor="middle" style="fill:{col};font-weight:800;font-size:12.5px">{v}</text>'
    if i < 3:
        b += f'<path class="flow" d="M{x+132} 158H{x+158}" stroke="{col}"/>'
b += f'<path class="flow" d="M642 158H700" stroke="{C["v33"]}"/>'
b += f'<rect class="box" x="700" y="110" width="160" height="96" rx="14" style="stroke:{C["tgt"]}"/><text class="t" x="780" y="140" text-anchor="middle">U4 / U5</text><text class="s" x="780" y="160" text-anchor="middle">TPS2553 switches</text><text class="s" x="780" y="178" text-anchor="middle">0.61 A · 0.51 A limit</text><text class="s" x="780" y="196" text-anchor="middle">SW5 = power-cycle</text>'
b += f'<path class="flow" d="M862 158H900" stroke="{C["tgt"]}"/><rect class="box" x="900" y="120" width="80" height="76" rx="14"/><text class="t" x="940" y="152" text-anchor="middle">Target</text><text class="s" x="940" y="174" text-anchor="middle">+3V3_T</text><text class="s" x="940" y="190" text-anchor="middle">+5V_T</text>'
b += f'<path class="flow" d="M415 198V226H780V208" stroke="{C["v5"]}" style="animation-duration:1.6s"/><text x="600" y="220" text-anchor="middle" style="fill:{C["v5"]};font-weight:700;font-size:12px">+5V → U5</text>'
b += f'<path class="flow" d="M255 198V272H330" stroke="{C["v5"]}"/><rect class="box" x="330" y="244" width="180" height="56" rx="14"/><text class="t" x="420" y="268" text-anchor="middle">CH342F core</text><text class="s" x="420" y="288" text-anchor="middle">VDD5 + VBUS sense</text>'
b += f'<path class="flow" d="M575 198V272H620" stroke="{C["v33"]}" style="animation-duration:1.6s"/><rect class="box" x="620" y="244" width="170" height="56" rx="14" style="stroke:{C["vio"]}"/><text class="t" x="705" y="268" text-anchor="middle">SW3 → VIO</text><text class="s" x="705" y="288" text-anchor="middle">3V3 or 5V logic · LED5</text>'
b += f'<path class="flow" d="M705 302V330H420V302" stroke="{C["vio"]}" style="animation-duration:1.4s"/><text x="562" y="346" text-anchor="middle" style="fill:{C["vio"]};font-weight:700;font-size:12.5px">VIO → both UARTs</text>'
b += '<text x="30" y="384" class="s">A short on 3V3 or 5V: the TPS2553 limits current within microseconds and lights OVERLOAD. The PTC is the backup that protects the PC.</text>'
save('power-flow.svg', wrap(1000, 410, b))

# ---------------------------------------------------------------- auto-program timing (unchanged logic)
st = '''
.wave{fill:none;stroke-width:3.2;stroke-linejoin:round}
.cursor{animation:sweep 6s linear infinite}
@keyframes sweep{from{transform:translateX(0)}to{transform:translateX(700px)}}
.reveal{animation:reveal 6s linear infinite}
@keyframes reveal{from{width:0}to{width:700px}}
'''
b = '<defs><clipPath id="clipw"><rect class="reveal" x="200" y="100" width="0" height="300"/></clipPath></defs>'
b += '<text x="40" y="52" class="h">How auto-program works</text><text x="40" y="78" class="s">esptool toggles DTR/RTS of UART1. Q1 and Q2 turn that into a reset with IO0 held low, so the ESP enters the bootloader by itself.</text>'
x0, x1 = 200, 900
for a, cc, lab, col in [(200, 330, 'Idle', '#334155'), (330, 470, '① Reset', '#7f1d1d'), (470, 620, '② Boot', '#713f12'), (620, 900, '③ Flashing', '#064e3b')]:
    b += f'<rect x="{a}" y="100" width="{cc-a}" height="280" fill="{col}" opacity=".28"/><text x="{(a+cc)/2}" y="122" text-anchor="middle" style="fill:{INK};font-weight:800;font-size:13px">{lab}</text>'
rows = [('DTR#', C['ctl'], [(200, 1), (470, 0), (620, 1)]), ('RTS#', C['ctl'], [(200, 1), (330, 0), (470, 1)]),
        ('EN', C['esp'], [(200, 1), (330, 0), (470, 1)]), ('IO0', C['esp'], [(200, 1), (470, 0), (640, 1)])]
for r, (name, col, pts) in enumerate(rows):
    yb = 180 + r * 58
    hi, lo = yb - 22, yb + 14
    b += f'<text x="40" y="{yb}" class="t" style="fill:{col}">{name}</text><text x="120" y="{yb}" class="s">{"PC output" if r < 2 else "to ESP"}</text>'
    b += f'<path d="M{x0} {lo+6}H{x1}" stroke="{LINE}" stroke-width="1"/>'
    d = ''
    for i, (x, v) in enumerate(pts):
        y = hi if v else lo
        d = f'M{x} {y}' if i == 0 else d + f'H{x}V{y}'
    d += f'H{x1}'
    b += f'<path class="wave" d="{d}" stroke="{col}" opacity=".18"/><path class="wave" d="{d}" stroke="{col}" clip-path="url(#clipw)"/>'
b += f'<g class="cursor"><path d="M200 100V380" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 4"/><circle cx="200" cy="100" r="5" fill="{ACC}"/></g>'
b += '<text x="40" y="412" class="s">EN goes low (reset) → IO0 goes low while EN rises → the ESP boots into download mode. When a serial monitor asserts both lines, nothing resets.</text>'
save('auto-program.svg', wrap(960, 430, b, st))

# ---------------------------------------------------------------- VIO switch + 5V LED
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
b += '<text x="40" y="52" class="h">3.3 V / 5 V logic switch (SW3) + 5V-IO LED</text><text x="40" y="78" class="s">SW3 feeds the CH342F VIO pin, so both UARTs swing to the target\'s voltage. In 5 V mode Q3 lights the red 5V IO LED as a warning.</text>'
b += f'<circle cx="150" cy="190" r="12" fill="{C["vio"]}"/><path d="M150 190V290" stroke="{C["vio"]}" stroke-width="4"/><text x="150" y="312" text-anchor="middle" style="fill:{C["vio"]};font-weight:800">VIO</text>'
b += f'<circle cx="95" cy="125" r="9" fill="none" stroke="{C["v33"]}" stroke-width="3"/><text x="95" y="108" text-anchor="middle" style="fill:{C["v33"]};font-weight:800">3V3</text>'
b += f'<circle cx="205" cy="125" r="9" fill="none" stroke="{C["v5"]}" stroke-width="3"/><text x="205" y="108" text-anchor="middle" style="fill:{C["v5"]};font-weight:800">5V</text>'
b += f'<g class="lever"><path d="M150 190V122" stroke="{INK}" stroke-width="6" stroke-linecap="round"/></g>'
b += f'<g class="w5"><circle cx="250" cy="220" r="22" fill="{C["red"]}" opacity=".35"/><circle cx="250" cy="220" r="9" fill="{C["red"]}"/><text x="250" y="262" text-anchor="middle" style="fill:{C["red"]};font-weight:800;font-size:12px">5V IO!</text></g>'
b += f'<g class="w33"><circle cx="250" cy="220" r="9" fill="#3f1d1d"/><text x="250" y="262" text-anchor="middle" class="s" style="font-size:12px">LED5 off</text></g>'
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
b += f'<g class="w5"><path d="M330 136H930" stroke="{C["v5"]}" stroke-dasharray="4 6" opacity=".6"/><text x="320" y="140" text-anchor="end" style="fill:{C["v5"]};font-weight:800">≈4.6 V</text><text x="630" y="304" text-anchor="middle" class="t">5 V Arduino · 5 V Pro Mini · 5 V ATtiny</text></g>'
save('vio-switch.svg', wrap(960, 340, b, st))

# ---------------------------------------------------------------- UPDI (unchanged content)
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
b += f'<rect class="box" x="220" y="110" width="150" height="170" rx="16" style="stroke:{ACC}"/><text class="t" x="295" y="190" text-anchor="middle">CH342F</text><text class="s" x="295" y="210" text-anchor="middle">UART1</text>'
u = f'<path d="M370 160H760" stroke="{C["tx"]}" stroke-width="4"/><path d="M370 230H760" stroke="{C["rx"]}" stroke-width="4"/>'
u += f'<text x="390" y="150" style="fill:{C["tx"]};font-weight:800">TX →</text><text x="390" y="252" style="fill:{C["rx"]};font-weight:800">← RX</text>'
u += f'<circle r="6" fill="{C["tx"]}"><animateMotion dur="1.6s" repeatCount="indefinite" path="M380 160H750"/></circle><circle r="6" fill="{C["rx"]}"><animateMotion dur="1.6s" begin=".8s" repeatCount="indefinite" path="M750 230H380"/></circle>'
u += '<rect class="box" x="760" y="120" width="170" height="140" rx="16"/><text class="t" x="845" y="186" text-anchor="middle">ESP / Arduino</text><text class="s" x="845" y="208" text-anchor="middle">normal serial</text>'
b += f'<g class="uart">{u}</g>'
v = f'<path d="M370 160H470V190" stroke="{C["tx"]}" stroke-width="4"/><rect x="456" y="190" width="28" height="44" rx="4" fill="{CARD}" stroke="{INK}" stroke-width="2"/><text x="500" y="217" class="s">4.7 kΩ</text>'
v += f'<path d="M470 234V250" stroke="{C["rx"]}" stroke-width="4"/><path d="M370 250H760" stroke="{C["rx"]}" stroke-width="4"/><circle cx="470" cy="250" r="6" fill="{C["rx"]}"/>'
v += f'<text x="600" y="240" text-anchor="middle" style="fill:{C["rx"]};font-weight:800">UPDI (one wire, both ways)</text>'
v += f'<circle r="6" fill="{C["rx"]}"><animateMotion dur="1.4s" repeatCount="indefinite" path="M480 250H750"/></circle><circle r="6" fill="{C["esp"]}"><animateMotion dur="1.4s" begin=".7s" repeatCount="indefinite" path="M750 250H480"/></circle>'
v += f'<rect class="box" x="760" y="120" width="170" height="160" rx="16" style="stroke:{C["rx"]}"/><text class="t" x="845" y="190" text-anchor="middle">ATtiny1614</text><text class="s" x="845" y="212" text-anchor="middle">AVR-DA / DB / DD</text><text class="s" x="845" y="234" text-anchor="middle">UPDI pin</text>'
b += f'<g class="updi">{v}</g>'
b += '<text x="40" y="318" class="s">Arduino IDE: megaTinyCore / DxCore → Programmer "SerialUPDI - 230400 baud". Or: pymcuprog -t uart -u COMx -d attiny1614 write -f app.hex</text>'
save('updi-mode.svg', wrap(960, 340, b, st))

# ---------------------------------------------------------------- targets
st = '.pulse{animation:pulse 2s ease-in-out infinite}@keyframes pulse{50%{opacity:.45}}'
b = '<text x="40" y="52" class="h">One board, every common target</text><text x="40" y="78" class="s">PC software sees two COM ports. UART1 flashes the module you plug in or wire up; UART2 watches a second device.</text>'
b += f'<rect x="50" y="140" width="150" height="96" rx="8" fill="{CARD}" stroke="{LINE}" stroke-width="2"/><rect x="62" y="152" width="126" height="72" rx="4" fill="#0f2a3d"/><path d="M30 244H220L208 258H42Z" fill="{LINE}"/>'
b += f'<text x="125" y="186" text-anchor="middle" style="fill:{ACC};font-weight:800;font-size:13px">esptool</text><text x="125" y="204" text-anchor="middle" class="s">Arduino IDE · PIO</text>'
b += f'<path class="flow" d="M222 200H330" stroke="{C["usb"]}"/><text x="276" y="190" text-anchor="middle" class="s">USB-C</text>'
b += f'<rect class="box" x="330" y="146" width="170" height="108" rx="16" style="stroke:{ACC}"/><text class="t" x="415" y="190" text-anchor="middle">Flasher V2</text><text class="s" x="415" y="212" text-anchor="middle">CH342F · auto-program</text>'
targets = [('ESP32 / S3 / C3', 'auto-program · H1 or J3', C['esp']), ('ESP-Prog boards', 'J3 1.27 mm cable', C['ctl']), ('ESP8266 / ESP-12F', 'IO15 pull-down', C['esp']), ('ESP-01 / 01S', 'plug into J2', C['esp']),
           ('Arduino / ATmega', 'RST pin (DTR+cap)', C['tx']), ('ATtiny / AVR-Dx', 'UPDI mode', C['rx']), ('2nd device log', 'UART2 on J5', C['blue'])]
for i, (t, sub, col) in enumerate(targets):
    y = 96 + i * 50
    b += f'<path class="flow" d="M502 200C560 200 560 {y+20} 620 {y+20}" stroke="{col}" style="animation-duration:{1.1+i*.12:.2f}s"/>'
    b += f'<rect class="box" x="620" y="{y}" width="300" height="40" rx="12"/><circle class="pulse" cx="642" cy="{y+20}" r="7" fill="{col}" style="animation-delay:{i*.3:.1f}s"/><text class="t" x="660" y="{y+18}" style="font-size:14px">{t}</text><text class="s" x="660" y="{y+34}" style="font-size:11.5px">{sub}</text>'
save('targets.svg', wrap(960, 460, b, st))

# ---------------------------------------------------------------- NEW: target power switch animation
st = '''
.btn{animation:press 8s step-end infinite}
@keyframes press{0%{transform:translateY(0)}25%{transform:translateY(5px)}40%{transform:translateY(0)}}
.rail{animation:rail 8s step-end infinite}
@keyframes rail{0%{opacity:1}25%{opacity:.12}40%{opacity:1}}
.ovl{animation:ovl 8s step-end infinite;opacity:.15}
@keyframes ovl{0%{opacity:.15}60%{opacity:1}85%{opacity:.15}}
.short{animation:short 8s step-end infinite;opacity:0}
@keyframes short{0%{opacity:0}60%{opacity:1}85%{opacity:0}}
.cur{animation:cur 8s linear infinite;transform-origin:0 0}
.lab{animation:lab 8s step-end infinite}
.lab2{animation:lab2 8s step-end infinite;opacity:0}
.lab3{animation:lab3 8s step-end infinite;opacity:0}
@keyframes lab{0%{opacity:1}25%{opacity:0}40%{opacity:1}60%{opacity:0}85%{opacity:1}}
@keyframes lab2{0%{opacity:0}25%{opacity:1}40%{opacity:0}}
@keyframes lab3{0%{opacity:0}60%{opacity:1}85%{opacity:0}}
'''
b = '<text x="40" y="52" class="h">Current-limited target power (U4/U5 + SW5)</text><text x="40" y="78" class="s">Hold POWER-CYCLE to switch the target off. On a short, the TPS2553 clamps the current and the OVERLOAD LED lights; the PC never sees it.</text>'
b += f'<rect class="box" x="40" y="130" width="140" height="80" rx="14"/><text class="t" x="110" y="166" text-anchor="middle">+3V3 / +5V</text><text class="s" x="110" y="188" text-anchor="middle">from LDO / USB</text>'
b += f'<path class="flow" d="M182 170H300" stroke="{C["v33"]}"/>'
b += f'<rect class="box" x="300" y="120" width="190" height="100" rx="16" style="stroke:{C["tgt"]}"/><text class="t" x="395" y="160" text-anchor="middle">TPS2553</text><text class="s" x="395" y="182" text-anchor="middle">U4 ≈0.61 A · U5 ≈0.51 A</text><text class="s" x="395" y="200" text-anchor="middle">EN · FAULT# · ILIM</text>'
b += f'<g class="rail"><path class="flow" d="M492 170H640" stroke="{C["tgt"]}"/></g>'
b += f'<rect class="box" x="640" y="120" width="160" height="100" rx="16"/><text class="t" x="720" y="160" text-anchor="middle">Target</text><text class="s" x="720" y="182" text-anchor="middle">+3V3_T · +5V_T</text>'
b += f'<g class="short"><path d="M700 196l12-10l6 8l12-10" stroke="{C["red"]}" stroke-width="4" fill="none"/><text x="720" y="214" text-anchor="middle" style="fill:{C["red"]};font-weight:800;font-size:12px">SHORT</text></g>'
b += f'<rect x="355" y="262" width="80" height="38" rx="8" fill="#e5e7eb"/><g class="btn"><circle cx="395" cy="281" r="12" fill="#1f2937"/></g><text x="395" y="322" text-anchor="middle" class="t" style="font-size:13px">SW5 POWER</text>'
b += f'<path d="M395 262V222" stroke="{C["ctl"]}" stroke-width="3"/><text x="402" y="246" class="s">EN</text>'
b += f'<circle class="ovl" cx="560" cy="282" r="22" fill="{C["red"]}"/><circle cx="560" cy="282" r="9" fill="{C["red"]}"/><text x="560" y="322" text-anchor="middle" class="t" style="font-size:13px">OVERLOAD</text>'
b += f'<path d="M490 200C530 200 560 230 560 260" stroke="{C["red"]}" stroke-width="2.5" fill="none" stroke-dasharray="4 4"/><text x="540" y="226" class="s">FAULT#</text>'
b += f'<rect class="box" x="820" y="120" width="120" height="200" rx="16"/><text class="s" x="880" y="146" text-anchor="middle">state</text>'
b += f'<g class="lab"><text class="t" x="880" y="216" text-anchor="middle" style="fill:{C["rx"]}">ON</text><text class="s" x="880" y="238" text-anchor="middle">normal</text></g>'
b += f'<g class="lab2"><text class="t" x="880" y="216" text-anchor="middle" style="fill:{MUTE}">OFF</text><text class="s" x="880" y="238" text-anchor="middle">SW5 held</text></g>'
b += f'<g class="lab3"><text class="t" x="880" y="216" text-anchor="middle" style="fill:{C["red"]}">LIMIT</text><text class="s" x="880" y="238" text-anchor="middle">≈0.6 A clamp</text></g>'
save('power-switch.svg', wrap(980, 350, b, st))

# ---------------------------------------------------------------- NEW: dual UART
st = '.pulse{animation:pulse 1.6s ease-in-out infinite}@keyframes pulse{50%{opacity:.35}}'
b = '<text x="40" y="52" class="h">Dual UART (CH342F)</text><text x="40" y="78" class="s">One USB cable, two COM ports with one shared VIO. Flash on UART1 while UART2 shows another device\'s log.</text>'
b += f'<rect class="box" x="40" y="130" width="170" height="150" rx="14"/><text class="t" x="125" y="166" text-anchor="middle">PC</text>'
b += f'<rect x="60" y="184" width="130" height="34" rx="8" fill="#0f2a3d" stroke="{C["tx"]}"/><text x="125" y="206" text-anchor="middle" style="fill:{C["tx"]};font-weight:700;font-size:13px">COM7 · esptool</text>'
b += f'<rect x="60" y="228" width="130" height="34" rx="8" fill="#0f2a3d" stroke="{C["blue"]}"/><text x="125" y="250" text-anchor="middle" style="fill:{C["blue"]};font-weight:700;font-size:13px">COM8 · monitor</text>'
b += f'<path class="flow" d="M212 205H330" stroke="{C["usb"]}"/><text x="270" y="196" text-anchor="middle" class="s">USB</text>'
b += f'<rect class="box" x="330" y="120" width="180" height="170" rx="16" style="stroke:{ACC}"/><text class="t" x="420" y="160" text-anchor="middle">CH342F</text><text class="s" x="420" y="180" text-anchor="middle">VIO 1.8–5 V</text>'
b += f'<text x="500" y="214" text-anchor="end" style="fill:{C["tx"]};font-weight:800;font-size:12px">UART1</text><text x="500" y="262" text-anchor="end" style="fill:{C["blue"]};font-weight:800;font-size:12px">UART2</text>'
b += f'<path d="M512 210H700" stroke="{C["tx"]}" stroke-width="4"/><circle r="6" fill="{C["tx"]}"><animateMotion dur="1.2s" repeatCount="indefinite" path="M515 210H695"/></circle>'
b += f'<path d="M512 258H700" stroke="{C["blue"]}" stroke-width="4"/><circle r="6" fill="{C["blue"]}"><animateMotion dur="1.9s" repeatCount="indefinite" path="M695 258H515"/></circle>'
b += f'<text x="606" y="200" text-anchor="middle" class="s">TX/RX + DTR/RTS (auto-program)</text><text x="606" y="282" text-anchor="middle" class="s">TX2/RX2 + DTR2 on J5</text>'
b += f'<rect class="box" x="700" y="170" width="230" height="62" rx="14"/><text class="t" x="815" y="198" text-anchor="middle">Target being flashed</text><text class="s" x="815" y="218" text-anchor="middle">H1 · J3 · J4 · J2</text>'
b += f'<rect class="box" x="700" y="240" width="230" height="44" rx="14"/><circle class="pulse" cx="724" cy="262" r="7" fill="{C["blue"]}"/><text class="t" x="822" y="268" text-anchor="middle" style="font-size:14px">Gateway / 2nd board log</text>'
save('dual-uart.svg', wrap(980, 320, b, st))

# ---------------------------------------------------------------- NEW: PROG pogo pad standard
st = '''
.jig{animation:jig 5s ease-in-out infinite}
@keyframes jig{0%,15%{transform:translateY(-40px)}35%,75%{transform:translateY(0)}95%,100%{transform:translateY(-40px)}}
.ok{animation:ok 5s step-end infinite;opacity:0}
@keyframes ok{0%{opacity:0}38%{opacity:1}75%{opacity:0}}
'''
b = '<text x="40" y="52" class="h">ElectroIoT PROG pad standard (pogo)</text><text x="40" y="78" class="s">6 bare pads in ESP-Prog order at 2.54 mm on every new board. A pogo jig on J4 presses on, and EN/IO0 auto-program does the rest.</text>'
pins = [('1', 'EN', C['esp']), ('2', 'VDD', C['v33']), ('3', 'TXD', C['tx']), ('4', 'GND', '#64748b'), ('5', 'RXD', C['rx']), ('6', 'IO0', C['esp'])]
b += f'<rect x="80" y="230" width="360" height="110" rx="10" fill="url(#pg)"/><text x="100" y="330" style="fill:#e5e7eb;font-weight:700;font-size:12px">target board (no header)</text>'
b = DEFS + b
for i, (n, lab, col) in enumerate(pins):
    r, cc = divmod(i, 2)
    x, y = 220 + cc * 50, 250 + r * 0  # 2x3 drawn as 3 columns x 2 rows on the board edge view
for i, (n, lab, col) in enumerate(pins):
    cc, r = divmod(i, 2)
    x, y = 200 + cc * 50, 258 + r * 40
    b += f'<circle cx="{x}" cy="{y}" r="14" fill="#d4a34a"/><text x="{x}" y="{y+4}" text-anchor="middle" style="fill:#1f2937;font-weight:800;font-size:12px">{n}</text><text x="{x+20}" y="{y+4}" style="fill:#e5e7eb;font-weight:700;font-size:11px">{lab}</text>'
jig = f'<rect x="170" y="110" width="180" height="60" rx="10" fill="{CARD}" stroke="{LINE}" stroke-width="2"/><text x="260" y="146" text-anchor="middle" class="t" style="font-size:14px">pogo jig → J4</text>'
for cc in range(3):
    for r in range(2):
        x = 200 + cc * 50
        jig += f'<path d="M{x} 170V{232 + r*40 - 10}" stroke="#cbd5e1" stroke-width="4"/>'
b += f'<g class="jig">{jig}</g>'
b += f'<g class="ok"><text x="260" y="220" text-anchor="middle" style="fill:{C["rx"]};font-weight:800;font-size:13px">contact ✓</text></g>'
spec = [('Pitch', '2.54 mm, 2 × 3'), ('Pad', 'Ø 1.5–1.8 mm, no paste'), ('Order', 'ESP-Prog: 1 EN · 2 VDD · 3 TXD · 4 GND · 5 RXD · 6 IO0'), ('Keep-out', '1 mm around pads, no parts'), ('Optional', '2 × Ø 1.0 mm NPTH locating holes'), ('Silk', '"PROG" + pin 1 dot')]
for i, (k, v) in enumerate(spec):
    y = 130 + i * 34
    b += f'<text x="500" y="{y}" class="t" style="fill:{ACC};font-size:13px">{k}</text><text x="600" y="{y}" class="s" style="font-size:13px">{v}</text>'
save('prog-pad.svg', wrap(980, 360, b, st))
