"""Universal USB Flasher V2.1 - the 4 HTML pages in the TankPilot style. Run from the repo root:
    python -I tools/gen_docs.py
Writes docs/bom.html, docs/wiring-by-section.html, docs/schematic-sections.html, docs/pcb-floorplan.html.
Data: tools/design.json (parts, pins, nets, BOM, placement, blocks). Drawings: tools/flasher_sheets.py."""
import collections, html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flasher_sheets as SH

e = html.escape
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
D = json.load(open(os.path.join(HERE, "design.json"), encoding="utf-8"))
CSS = open(os.path.join(HERE, "tp_style.css"), encoding="utf-8").read()
PART = {p[0]: p for p in D["parts"]}
BOMALL = D["bom"] + D.get("bom_extra", [])
BYREF = {}
for b in BOMALL:
    for r in b[0].split():
        BYREF[r] = b
BW, BH = D["board"]["w"], D["board"]["h"]
PAGE_COL = {"P1": "#ff9f43", "P2": "#ef4444", "P3": "#4895ef", "P4": "#14b8a6", "P5": "#a66cff", "P6": "#ca8a04", "P7": "#ec407a", "P8": "#64748b"}

# ------------------------------------------------------------------ sections (per sheet)
SECTIONS = [
 ("P1", "USB fuse F1, back-feed diode D1, bulk capacitors", ["F1", "C1", "D1", "C5"], "VBUS -> F1 -> VBUS_F (C1 10 uF to GND). D1 anode (triangle) on VBUS_F, cathode (bar) on +5V. C5 10 uF from +5V to GND - never across D1."),
 ("P1", "3.3 V regulator U1 (SGM2212)", ["U1", "C6", "C7"], "Pin 3 VIN = +5V, pin 1 GND, pins 2 and 4 VOUT = +3V3. C6 22 uF and C7 100 nF on +3V3."),
 ("P1", "5V-IO warning LED (Q3, R16, R17, LED5)", ["Q3", "R16", "R17", "LED5"], "PNP Q3: emitter (arrow, bottom) on VIO, base via R16 4.7k to +3V3, collector via R17 1k to LED5 anode; LED5 cathode (bar) to GND. Net name VIO - no space."),
 ("P1", "ESP-01 bulk capacitor C8", ["C8"], "C8 22 uF from +3V3_T to GND; on the PCB next to J2 VCC."),
 ("P2", "3.3 V target switch U4 + PWR LED", ["U4", "R18", "C11", "C12", "R3", "LED1"], "U4: 1 IN = +3V3 (C11), 2 GND, 3 EN = TPWR_EN, 4 /FAULT = FAULT_N, 5 ILIM -> R18 43k -> GND, 6 OUT = +3V3_T (C12). PWR LED: +3V3_T -> R3 1k -> LED1 anode, cathode (bar) -> GND."),
 ("P2", "5 V target switch U5", ["U5", "R19", "C13", "C14"], "U5: 1 IN = +5V (C13), 2 GND, 3 EN = TPWR_EN, 4 /FAULT = FAULT_N, 5 ILIM -> R19 51k -> GND, 6 OUT = +5V_T (C14)."),
 ("P2", "Enable line + POWER-CYCLE button", ["R20", "SW5"], "TPWR_EN: R20 100k to +3V3, SW5 to GND. Put a TPWR_EN label on U4 pin 3 AND U5 pin 3."),
 ("P2", "OVERLOAD LED", ["R21", "LED6"], "+5V -> R21 1k -> LED6 anode; LED6 cathode (bar) -> FAULT_N. FAULT_N label on U4 pin 4 AND U5 pin 4."),
 ("P3", "USB-C connector + CC resistors", ["USB1", "R1", "R2"], "Both VBUS pins = VBUS, GND + shell = GND, DP1+DP2 = USB_DP, DN1+DN2 = USB_DM, CC1/CC2 -> 5.1k -> GND, SBU1/SBU2 No-Connect."),
 ("P3", "USB data ESD U3", ["U3"], "Pins 1, 6 = USB_DP; 3, 4 = USB_DM; 5 = VBUS; 2 = GND."),
 ("P3", "Header ESD U6 / U7", ["U6", "U7"], "Pin 2 GND, pin 5 +5V. U6: TXD, RXD, DTR_N, RTS_N. U7: EN, IO0, TX2, RX2."),
 ("P4", "CH342F U2 (rename U8 -> U2)", ["U2"], "A net label on every pin, No-Connect on the 10 unused modem pins, EP (25) = GND."),
 ("P4", "CH342F decoupling", ["C2", "C3", "C4"], "C2 VBUS_F (pin 7), C3 V3 (pin 6, nothing else on V3), C4 VIO (pin 5). 100 nF each."),
 ("P4", "TX / RX / RX2 activity LEDs", ["R4", "LED2", "R5", "LED3", "R6", "LED4"], "VIO -> 2.2k -> LED anode, cathode (bar) on TXD / RXD / RX2."),
 ("P5", "Auto-program: SJ1/SJ2, Q1/Q2", ["SJ1", "SJ2", "R7", "R8", "Q1", "Q2"], "SJ1 DTR_N - DTR_AP, SJ2 RTS_N - RTS_AP (jumper caps fitted). Q1: B via R7 from DTR_AP, E = RTS_AP, C = EN. Q2: B via R8 from RTS_AP, E = DTR_AP, C = IO0."),
 ("P6", "EN / IO0 pull-ups, IO15 pull-down", ["R9", "C9", "R10", "R11"], "R9 +3V3_T -> EN, C9 EN -> GND, R10 +3V3_T -> IO0, R11 IO15 -> GND."),
 ("P6", "Arduino auto-reset", ["C10", "R14"], "C10 100 nF DTR_N -> RST, R14 10k VIO -> RST."),
 ("P6", "UPDI resistor", ["R15"], "R15 4.7k UPDI_R -> RXD."),
 ("P6", "ESP-01 RST / GPIO2 pull-ups", ["R12", "R13"], "R12 +3V3_T -> ESP01_RST, R13 +3V3_T -> ESP01_IO2."),
 ("P7", "RESET and BOOT buttons", ["SW1", "SW2"], "SW1 EN to GND, SW2 IO0 to GND."),
 ("P7", "IO voltage SW3 and UART/UPDI SW4", ["SW3", "SW4"], "SW3: 1 +3V3, 2 VIO, 3 +5V. SW4: 1 TXD, 2 UPDI_R, 3 No-Connect. Pin 4 of both = GND."),
 ("P8", "Main header H1", ["H1"], "3V3 and 5V are the switched, current-limited target rails."),
 ("P8", "ESP-01 socket J2", ["J2"], "Odd pins top row (1 GND, 3 GPIO2, 5 GPIO0, 7 RXD), even pins bottom row (2 TXD, 4 CH_PD, 6 RST, 8 VCC)."),
 ("P8", "ESP-Prog J3 (1.27 mm) and J4 (2.54 mm)", ["J3", "J4"], "1 EN, 2 +3V3_T, 3 target TX -> RXD, 4 GND, 5 target RX -> TXD, 6 IO0."),
 ("P8", "UART2 header J5", ["J5"], "1 GND, 2 TX2, 3 RX2, 4 DTR2_N."),
]
assert sorted(r for s in SECTIONS for r in s[2]) == sorted(PART)
SEC = {}
cnt = collections.Counter()
for s in SECTIONS:
    cnt[s[0]] += 1
    SEC[f"{s[0]}s{cnt[s[0]]}"] = s
PAGES = [(p[0], f"Sheet {p[0][1:]}: {p[1].split('·')[1].strip()} ({p[2]})", [k for k in SEC if SEC[k][0] == p[0]]) for p in D["pages"]]
REFSEC = {r: k for k, s in SEC.items() for r in s[2]}
NETS = collections.defaultdict(list)
for p in D["parts"]:
    for num, name, net in p[5]:
        if net != "NC":
            NETS[net].append((p[0], num, p[1]))

NAV = [("bom.html", "BOM"), ("wiring-by-section.html", "Wiring"), ("schematic-sections.html", "Schematic"), ("pcb-floorplan.html", "PCB floorplan")]
HEAD_SUB = "CH342F dual-UART USB-C flasher for ESP32 / ESP8266 / ESP-01 / Arduino / UPDI &middot; LCSC listings read 2026-11-12/13 &middot; Sheet N here = Sheet N in your EasyEDA project"


def head(title, sub, nav="", active="bom.html", stats=""):
    nv = "".join(f'<a class="{"on" if f == active else ""}" href="{f}">{n}</a>' for f, n in NAV)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{CSS}</style></head><body>'
            f'<header><div class="wrap"><h1>{e(title)}</h1><p>{sub}</p><nav>{nv}</nav></div></header><div class="wrap">' + stats +
            '<div class="warn"><b>Design stage.</b> Planned design: nets come from tools/design.json and match your EasyEDA sheets (2026-11-13). Check pin numbers and footprints in EasyEDA and against the datasheets. Nothing has been built or tested yet.</div>' + nav)


def links():
    return '<footer>Generated by <code>tools/gen_docs.py</code> from <code>tools/design.json</code>. Prices are the first LCSC tier seen and change daily; stock is from the check date.</footer>'


def ncol(n):
    if n == "GND": return "#8a93a3"
    if n in ("+5V", "VBUS", "VBUS_F"): return "#fb8c00"
    if n == "+3V3": return "#f4b400"
    if n in ("+3V3_T", "+5V_T"): return "#e11d48"
    if n == "VIO": return "#db2777"
    if n.startswith("USB_") or n in ("CC1", "CC2"): return "#8e24aa"
    if n in ("TXD", "RXD", "TX2", "RX2", "UPDI_R"): return "#2fbf71"
    if n in ("DTR_N", "RTS_N", "DTR_AP", "RTS_AP", "Q1_B", "Q2_B", "EN", "IO0", "RST", "IO15", "ESP01_RST", "ESP01_IO2", "DTR2_N", "TPWR_EN"): return "#a66cff"
    return "#00bcd4"


RAILS = {"+5V", "+3V3", "VBUS", "VBUS_F", "+3V3_T", "+5V_T", "VIO"}
LEGEND = ('<p class="legend"><span><i style="background:#fb8c00"></i>5 V / VBUS</span><span><i style="background:#f4b400"></i>3.3 V</span><span><i style="background:#e11d48"></i>switched target rails</span>'
          '<span><i style="background:#db2777"></i>VIO</span><span><i style="background:#8a93a3"></i>GND</span><span><i style="background:#8e24aa"></i>USB</span><span><i style="background:#2fbf71"></i>UART data</span>'
          '<span><i style="background:#a66cff"></i>control / boot</span><span><i style="background:#00bcd4"></i>LED / internal nets</span></p>')


def info(ref):
    b = BYREF[ref]
    status = {"ok": "IN STOCK", "v1": "FROM V1 BOM", "warn": "CHECK", "info": "PCB ONLY"}[b[9]]
    cls = {"ok": "VERIFIED", "v1": "LISTING", "warn": "LISTING", "info": "opt"}[b[9]]
    return b, status, cls


def gnd_sym(x, y, c):
    return (f'<line x1="{x}" y1="{y}" x2="{x+12}" y2="{y}" stroke="{c}" stroke-width="2"/><line x1="{x+12}" y1="{y-7}" x2="{x+12}" y2="{y+7}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+16}" y1="{y-4}" x2="{x+16}" y2="{y+4}" stroke="{c}" stroke-width="2"/><line x1="{x+20}" y1="{y-2}" x2="{x+20}" y2="{y+2}" stroke="{c}" stroke-width="2"/>')


# ------------------------------------------------------------------ wiring diagram per section
def section_svg(sid):
    refs = SEC[sid][2]
    PXR = 300
    y = 16
    boxes, pinpos = [], []
    for ref in refs:
        pl = PART[ref][5]
        h = 34 + 16 * len(pl)
        boxes.append((ref, y, h))
        for k, (num, name, net) in enumerate(pl):
            pinpos.append((ref, num if name == num else f"{num} {name}", net, y + 40 + 16 * k))
        y += h + 14
    lanes = []
    for ref, pin, net, py in pinpos:
        if net not in RAILS and net not in ("GND", "NC") and net not in lanes:
            lanes.append(net)
    lx = {n: 520 + 24 * i for i, n in enumerate(lanes)}
    Wd, Ht = 520 + 24 * len(lanes) + 40, y + 20
    o = [f'<svg viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}" class="dia" data-sec="{sid}">']
    for ref, by, bh in boxes:
        b = BYREF.get(ref)
        o.append(f'<g class="bx" data-ref="{ref}"><rect x="8" y="{by}" width="{PXR-8}" height="{bh}" rx="7" fill="var(--card)" stroke="var(--line)" stroke-width="2"/>'
                 f'<text x="16" y="{by+14}" class="ref">{e(ref)}</text><text x="{16+8*len(ref)+8}" y="{by+14}" class="role">{e(PART[ref][2][:44])}</text><text x="16" y="{by+27}" class="lab">{e(b[4])} [{e(b[6])}]</text></g>')
    for ref, pin, net, py in pinpos:
        o.append(f'<text x="{PXR-14}" y="{py+3.5}" text-anchor="end" class="pin">{e(pin)}</text>')
        if net == "NC":
            o.append(f'<g class="w"><line x1="{PXR}" y1="{py}" x2="{PXR+10}" y2="{py}" stroke="#9aa5b5" stroke-width="2"/><line x1="{PXR+10}" y1="{py-4}" x2="{PXR+18}" y2="{py+4}" stroke="#dc2626" stroke-width="2.2"/><line x1="{PXR+18}" y1="{py-4}" x2="{PXR+10}" y2="{py+4}" stroke="#dc2626" stroke-width="2.2"/><text x="{PXR+24}" y="{py+3.5}" class="lab">No-Connect flag</text></g>')
            continue
        c = ncol(net)
        if net == "GND":
            o.append(f'<g class="w" data-net="GND">{gnd_sym(PXR, py, c)}<text x="{PXR+28}" y="{py+3.5}" class="net" fill="{c}">GND</text></g>')
        elif net in RAILS:
            wd = 7 * len(net) + 10
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{PXR}" y1="{py}" x2="{PXR+14}" y2="{py}" stroke="{c}" stroke-width="3"/><rect x="{PXR+14}" y="{py-8}" width="{wd}" height="16" rx="4" fill="{c}"/><text x="{PXR+19}" y="{py+3.5}" class="flag">{e(net)}</text></g>')
        else:
            x2 = lx[net]
            pw = 6.6 * len(net) + 14
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{PXR}" y1="{py}" x2="{x2}" y2="{py}" stroke="{c}" stroke-width="2"/><circle cx="{PXR}" cy="{py}" r="3" fill="{c}"/><circle cx="{x2}" cy="{py}" r="2.6" fill="{c}"/><rect x="{PXR+14}" y="{py-9}" width="{pw:.0f}" height="18" rx="9" fill="{c}"/><text x="{PXR+22}" y="{py+4}" class="pill">{e(net)}</text></g>')
    for net in lanes:
        ys = [py for _, _, n, py in pinpos if n == net]
        if len(ys) > 1:
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{lx[net]}" y1="{min(ys)}" x2="{lx[net]}" y2="{max(ys)}" stroke="{ncol(net)}" stroke-width="2"/></g>')
    o.append("</svg>")
    return "".join(o)


# ------------------------------------------------------------------ BOM page
def page_bom():
    pieces = sum(b[1] for b in BOMALL if b[6].startswith("C"))
    cost = sum((b[8] or 0) * b[1] for b in BOMALL)
    stats = ('<div class="stats top">'
             f'<div class="stat"><b>{pieces}</b><span>parts per board</span></div><div class="stat"><b>{len(PAGES)}</b><span>schematic sheets</span></div>'
             f'<div class="stat"><b id="cost">${cost:.2f}</b><span>captured LCSC prices</span></div><div class="stat"><b id="ticked">0%</b><span>ticked off</span></div></div>')
    o = [head("Universal USB Flasher V2.1 - Bill of materials", HEAD_SUB, "", "bom.html", stats)]
    o.append('<div class="bar"><input type="search" id="q" placeholder="Search ref, MPN, C-number, function..."><label>Boards <input type="number" id="boards" min="1" value="1"></label>'
             '<button id="copy">Copy all C-numbers</button><button class="ghost" id="reset">Clear ticks</button></div><div class="prog"><i id="pbar"></i></div>')
    o.append(f'<div class="rec"><b>About USD {cost:.2f} of parts per board</b> with the prices captured on LCSC ({pieces} pieces); lines marked FROM V1 BOM have no captured price (cheap passives) and add a little. PCB, cables and shipping not included. <b>U2 CH342F is QFN-24</b>: JLC assembly or hot air.</div>')
    for pid, ptitle, secs in PAGES:
        refs = [r for s in secs for r in SEC[s][2]]
        c = sum((BYREF[r][8] or 0) for r in refs)
        o.append(f'<section class="card" id="{pid}" style="--c:{PAGE_COL[pid]}"><h2>{e(ptitle)}<span class="cnt">{len(refs)} parts, about ${c:.2f}</span></h2>')
        o.append('<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Function</th><th>Part</th><th>LCSC #</th><th>Qty</th><th>Stock</th><th>$ each</th></tr></thead><tbody>')
        for sid in secs:
            o.append(f'<tr><td colspan="8" style="background:{PAGE_COL[pid]}22"><b>{e(SEC[sid][1])}</b></td></tr>')
            for r in SEC[sid][2]:
                b, st, cl = info(r)
                pr = b[8]
                cnum = b[6]
                link = f'<a href="https://www.lcsc.com/product-detail/{cnum}.html" target="_blank" rel="noopener">{cnum}</a>' if cnum.startswith("C") else "PCB"
                o.append(f'<tr data-ref="{r}" data-sub="{(pr or 0):.4f}" data-c="{cnum}" data-q="1"><td><input type="checkbox" class="ck" data-k="{r}"></td><td class="ref"><b>{r}</b></td>'
                         f'<td class="f">{e(PART[r][2])}</td><td><span class="mpn">{e(b[4])}</span><span class="note">{e(b[5])}</span><span class="tag {cl}">{st}</span>{f"<span class=note>{e(b[11])}</span>" if b[11] else ""}</td>'
                         f'<td>{link}</td><td class="n">1</td><td class="n">{e(b[7] or "-")}</td><td class="n">{f"{pr:.4f}" if pr is not None else "-"}</td></tr>')
        o.append("</tbody></table></div></section>")
    ex = D.get("bom_extra", [])
    if ex:
        o.append('<section class="card" id="extra" style="--c:#475569"><h2>Not on the schematic (order with the parts)<span class="cnt">jumper caps</span></h2><div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Function</th><th>Part</th><th>LCSC #</th><th>Qty</th><th>Stock</th><th>$ each</th></tr></thead><tbody>')
        for b in ex:
            o.append(f'<tr data-ref="{b[0]}" data-sub="{(b[8] or 0)*b[1]:.4f}" data-c="{b[6]}" data-q="{b[1]}"><td><input type="checkbox" class="ck" data-k="{b[0]}"></td><td class="ref"><b>{b[0]}</b></td><td class="f">{e(b[2])}</td>'
                     f'<td><span class="mpn">{e(b[4])}</span><span class="note">{e(b[5])}</span></td><td><a href="https://www.lcsc.com/product-detail/{b[6]}.html" target="_blank" rel="noopener">{b[6]}</a></td><td class="n">{b[1]}</td><td class="n">{e(b[7])}</td><td class="n">{b[8]:.4f}</td></tr>')
        o.append("</tbody></table></div></section>")
    o.append(links() + """<script>
const K='uusbf-tp-bom';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const rows=[...document.querySelectorAll('tr[data-ref]')],cks=[...document.querySelectorAll('.ck')];
function money(){const b=Math.max(1,+document.getElementById('boards').value||1);let s=0;rows.forEach(r=>{s+=+r.dataset.sub});document.getElementById('cost').textContent='$'+(s*b).toFixed(2)}
function upd(){const n=cks.filter(c=>c.checked).length;document.getElementById('ticked').textContent=Math.round(100*n/cks.length)+'%';document.getElementById('pbar').style.width=(100*n/cks.length)+'%';
 rows.forEach(r=>r.classList.toggle('done',r.querySelector('.ck').checked));try{localStorage.setItem(K,JSON.stringify(Object.fromEntries(cks.filter(c=>c.checked).map(c=>[c.dataset.k,1]))))}catch(e){}}
cks.forEach(c=>{c.checked=!!st[c.dataset.k];c.addEventListener('change',upd)});
document.getElementById('reset').onclick=()=>{cks.forEach(c=>c.checked=false);upd()};document.getElementById('boards').oninput=money;
document.getElementById('q').oninput=ev=>{const v=ev.target.value.toLowerCase();rows.forEach(r=>r.style.display=r.innerText.toLowerCase().includes(v)?'':'none')};
document.getElementById('copy').onclick=()=>{const b=Math.max(1,+document.getElementById('boards').value||1),m={};
 rows.forEach(r=>{if(!r.dataset.c.startsWith('C'))return;m[r.dataset.c]=(m[r.dataset.c]||0)+(+r.dataset.q)*b});
 const t=Object.entries(m).map(([c,q])=>c+','+q).join('\\n');const btn=document.getElementById('copy');
 (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{btn.textContent='Copied '+Object.keys(m).length+' lines (C#,qty)'},()=>{prompt('Copy:',t)})};
upd();money();
</script></div></body></html>""")
    return "".join(o)


# ------------------------------------------------------------------ connection map + wiring page
def box(x, y, w, h, col, title, lines):
    s = f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" fill-opacity=".09" stroke="{col}" stroke-width="2"/><rect x="{x}" y="{y}" width="{w}" height="26" rx="12" fill="{col}" fill-opacity=".9"/><text x="{x+12}" y="{y+18}" font-size="13" font-weight="700" fill="#fff">{e(title)}</text>'
    for i, l in enumerate(lines):
        s += f'<text x="{x+12}" y="{y+46+i*17}" font-size="12" fill="currentColor">{e(l)}</text>'
    return s + "</g>"


def arrow(pts, col, lab="", lx=None, ly=None):
    d = " ".join(("M" if i == 0 else "L") + f"{a},{b}" for i, (a, b) in enumerate(pts))
    mid = pts[len(pts) // 2]
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3" marker-end="url(#ah{col[1:]})"/>'
    if lab:
        s += f'<text x="{lx if lx is not None else mid[0]+6}" y="{ly if ly is not None else mid[1]-6}" font-size="11" font-weight="700" fill="{col}">{e(lab)}</text>'
    return s


def map_body():
    cols = ["#fb8c00", "#f4b400", "#e11d48", "#8e24aa", "#2fbf71", "#a66cff", "#db2777"]
    s = ['<svg viewBox="0 0 1240 640" width="1240" class="dia" style="color:var(--fg)"><defs>']
    for c in cols:
        s.append(f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    s.append("</defs>")
    s.append(box(20, 20, 330, 130, "#4895ef", "USB-C INPUT (sheet 3)", ["USB1 USB-C 16P, R1 / R2 5.1k on CC1 / CC2", "U3 USBLC6-2SC6 on D+ / D-", "VBUS to the power sheet"]))
    s.append(box(20, 200, 330, 150, "#ff9f43", "POWER (sheet 1)", ["F1 PTC 500 mA -> VBUS_F (C1)", "D1 Schottky -> +5V (C5)", "U1 SGM2212 -> +3V3 (C6, C7)", "Q3 + LED5: 5V-IO warning"]))
    s.append(box(20, 400, 330, 170, "#ef4444", "TARGET POWER (sheet 2)", ["U4 TPS2553: +3V3 -> +3V3_T (0.61 A)", "U5 TPS2553: +5V -> +5V_T (0.51 A)", "SW5 POWER-CYCLE on TPWR_EN", "LED1 PWR, LED6 OVERLOAD (FAULT_N)"]))
    s.append(box(430, 20, 380, 190, "#14b8a6", "CH342F DUAL UART (sheet 4)", ["U2 CH342F, VDD5 + VBUS from VBUS_F", "VIO from SW3 (3V3 or 5V)", "UART0: TXD RXD DTR_N RTS_N", "UART1: TX2 RX2 DTR2_N", "LEDs TX / RX / RX2 from VIO", "C2 / C3 / C4 decoupling"]))
    s.append(box(430, 260, 380, 120, "#a66cff", "AUTO-PROGRAM (sheet 5)", ["SJ1 / SJ2 headers + caps", "Q1 -> EN, Q2 -> IO0 (R7 / R8 10k)"]))
    s.append(box(430, 420, 380, 150, "#ca8a04", "TARGET I/O + SWITCHES (sheets 6, 7)", ["EN / IO0 pull-ups, IO15 pull-down", "C10 + R14 Arduino RST, R15 UPDI", "SW1 RESET, SW2 BOOT", "SW3 IO 3V3|5V, SW4 UART|UPDI"]))
    s.append(box(890, 20, 330, 110, "#4895ef", "HEADER ESD (sheet 3)", ["U6: TXD RXD DTR_N RTS_N", "U7: EN IO0 TX2 RX2"]))
    s.append(box(890, 180, 330, 200, "#64748b", "CONNECTORS (sheet 8)", ["H1 1x11 main header", "J2 ESP-01 socket", "J3 ESP-Prog 2x3 1.27 mm", "J4 PROG 2x3 2.54 mm (pogo jig)", "J5 UART2 1x4"]))
    s.append(arrow([(185, 150), (185, 200)], cols[0], "VBUS", lx=192, ly=180))
    s.append(arrow([(350, 80), (430, 80)], cols[3], "D+ D-", lx=360, ly=72))
    s.append(arrow([(350, 230), (390, 230), (390, 120), (430, 120)], cols[0], "VBUS_F", lx=354, ly=222))
    s.append(arrow([(185, 350), (185, 400)], cols[1], "+3V3 +5V", lx=192, ly=380))
    s.append(arrow([(350, 300), (400, 300), (400, 470), (430, 470)], cols[6], "SW3 -> VIO", lx=356, ly=292))
    s.append(arrow([(620, 210), (620, 260)], cols[5], "DTR_N RTS_N", lx=628, ly=240))
    s.append(arrow([(810, 70), (890, 70)], cols[4], "UART", lx=822, ly=62))
    s.append(arrow([(1055, 130), (1055, 180)], cols[4], "", lx=0, ly=0))
    s.append(arrow([(810, 320), (890, 320)], cols[5], "EN IO0", lx=822, ly=312))
    s.append(arrow([(810, 480), (850, 480), (850, 360), (890, 360)], cols[5], "RST IO15 pulls", lx=818, ly=500))
    s.append(arrow([(350, 520), (380, 520), (380, 600), (1080, 600), (1080, 380)], cols[2], "+3V3_T +5V_T", lx=600, ly=594))
    s.append("</svg>")
    leg = LEGEND
    pins = [("21", "TXD0", "TXD", "U6, H1-4, J2-7, J3/J4-5, LED2, SW4-1"), ("20", "RXD0", "RXD", "U6, H1-5, J2-2, J3/J4-3, LED3, R15"), ("23", "DTR0#", "DTR_N", "SJ1, C10, U6, H1-6"),
            ("19", "RTS0#", "RTS_N", "SJ2, U6, H1-7"), ("13", "TXD1", "TX2", "U7, J5-2"), ("12", "RXD1", "RX2", "U7, J5-3, LED4"), ("15", "DTR1#", "DTR2_N", "J5-4"),
            ("3 / 4", "UD+ / UD-", "USB_DP / USB_DM", "U3, USB1"), ("5", "VIO", "VIO", "SW3 common, C4, LED resistors, R14, Q3"), ("6", "V3", "V3", "C3 only"),
            ("7 / 8", "VDD5 / VBUS", "VBUS_F", "F1, C1, C2, D1"), ("2, 25", "GND, EP", "GND", "-"), ("1, 9, 10, 11, 14, 16, 17, 18, 22, 24", "unused", "NC", "No-Connect flags")]
    tab = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in pins)
    return (leg + f'<div class="scroll" style="background:var(--card);border-radius:12px;padding:8px">{"".join(s)}</div>'
            f'<h3>CH342F (U2) pin assignment</h3><div class="scroll"><table><thead><tr><th>Pin</th><th>Name</th><th>Net</th><th>Goes to</th></tr></thead><tbody>{tab}</tbody></table></div>'
            '<p class="mut">DTR0# and DTR1# must not get a pull-down resistor: a 3-8k pull-down at power-up switches them to RS485 TNOW mode.</p>')


EXTERNAL = [
    ("USB-C (USB1)", "To the PC. Two COM ports appear: UART1 = H1 / J3 / J4 / J2, UART2 = J5."),
    ("Main header H1", "Pin 1 3V3, 2 5V (both switched, current-limited), 3 GND, 4 TX -> target RX, 5 RX/UPDI <- target TX, 6 DTR, 7 RTS, 8 RST (Arduino), 9 EN, 10 IO0, 11 IO15."),
    ("ESP-Prog cable (J3)", "1.27 mm 2x3 cable to boards with Espressif's PROG header. Same order as ESP-Prog: EN, VDD, TXD, GND, RXD, IO0."),
    ("Pogo jig / 2.54 cable (J4)", "Same pinout as J3 at 2.54 mm; the PROG pogo jig plugs in here."),
    ("ESP-01 (J2)", "Plug the module in, antenna away from the header. <b>SW3 must be on 3V3.</b>"),
    ("UART2 (J5)", "1 GND, 2 TX2 -> device RX, 3 RX2 <- device TX, 4 DTR2 (raw)."),
    ("SW3 / SW4", "SW3 = logic level 3V3 or 5V (5V lights LED5). SW4 = UART or UPDI (TX linked to RX through R15)."),
    ("SW5 POWER", "Hold to switch both target rails off (power-cycle)."),
]
ASBUILT = [
    ("Sheet 1 Power", "F1, D1, U1, C1, C5, C6, C7, C8, Q3, R16, R17, LED5"), ("Sheet 2 Target Power", "U4, U5, R18-R21, R3, C11-C14, SW5, LED1, LED6"),
    ("Sheet 3 USB+ESD", "USB1, R1, R2, U3, U6, U7"), ("Sheet 4 USB-UART", "U2 (shown as U8 in your file), C2-C4, R4-R6, LED2-LED4"),
    ("Sheet 5 Auto-program", "Q1, Q2, R7, R8 - SJ1 / SJ2 still to add"), ("Sheet 6 Target I/O", "R9-R15, C9, C10"), ("Sheet 7 LEDs + Switches", "SW1-SW4"), ("Sheet 8 Connectors", "H1, J2, J3, J4, J5"),
]
CHECKS = [
    "<b>All earlier issues fixed</b> (4th PDF, 2026-11-13): +5V on the D1 / U1 VIN node, VIO, +3V3_T on U4 OUT, +3V3 spelling, SJ2 = RTS_N, SW3/SW4 pin 4 to GND, LED6 named. Schematic matches the netlist - next: Update PCB from schematic and place parts by the floor plan.",
    "<b>Tidy only (optional):</b> sheet 7 the VIO and +5V labels on SW3 pins 2/3 touch - move one label a little so they are easy to read.",
]


def page_wiring():
    o = [head("Universal USB Flasher V2.1 - Wiring by section", HEAD_SUB.replace("LCSC listings read 2026-11-12/13 &middot; ", ""), "", "wiring-by-section.html")]
    o.append(LEGEND)
    o.append('<section class="card" style="--c:#1e3a8a"><h2>System wiring (connection map)</h2>' + map_body() + '</section>')
    o.append('<section class="card" style="--c:#dc2626"><h2>External wiring (what you connect by hand)</h2><div class="scroll"><table><thead><tr><th>Connection</th><th>How</th></tr></thead><tbody>'
             + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in EXTERNAL) + '</tbody></table></div></section>')
    o.append('<section class="card" style="--c:#0f766e"><h2>Your EasyEDA schematic (read 2026-11-13)</h2><p class="mut">All 64 real parts are placed on 8 sheets with the right values and LCSC parts. All 8 sheets are wired (PDF read 2026-11-13, 4th version); this is what is on each sheet:</p>'
             '<div class="scroll"><table><thead><tr><th>Sheet</th><th>Parts</th></tr></thead><tbody>' + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in ASBUILT) + '</tbody></table></div>'
             '<div class="warn"><b>Checks found in your schematic:</b><ol style="margin:6px 0 0 18px;padding:0">' + "".join(f"<li>{c}</li>" for c in CHECKS) + '</ol></div></section>')
    o.append('<div class="bar"><progress id="pg" value="0" max="1" style="width:240px"></progress><span id="pt" class="mut"></span><button class="ghost" id="rs">Clear ticks</button></div><p class="mut">Pin-to-net per section: each box is a part; the flag on a pin is the net name - put the same net label in EasyEDA and the pins join. Hover a wire to highlight its net, click to mark it wired (saved in this browser).</p>')
    for pid, ptitle, secs in PAGES:
        o.append(f'<section class="card" id="{pid}" style="--c:{PAGE_COL[pid]}"><h2>{e(ptitle)}</h2>')
        for sid in secs:
            _, title, refs, desc = SEC[sid]
            o.append(f'<div data-sec="{sid}" class="sec"><h3 style="color:{PAGE_COL[pid]}">{e(title)} <span class="mut secprog"></span></h3><p class="mut">{e(desc)}</p><div class="scroll">{section_svg(sid)}</div></div>')
        o.append("</section>")
    o.append(links() + """<script>
const K='uusbf-tp-wiring';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const svgs=[...document.querySelectorAll('svg.dia[data-sec]')];
function nets(svg){return [...new Set([...svg.querySelectorAll('.w[data-net]')].map(w=>w.dataset.net))]}
function apply(){let done=0,total=0;svgs.forEach(svg=>{const sid=svg.dataset.sec,ns=nets(svg);let d=0;
 svg.querySelectorAll('.w[data-net]').forEach(w=>w.classList.toggle('done',!!st[sid+'|'+w.dataset.net]));ns.forEach(n=>{if(st[sid+'|'+n])d++});
 svg.closest('.sec').querySelector('.secprog').textContent=d+' / '+ns.length+' nets wired';done+=d;total+=ns.length});
 document.getElementById('pg').max=total;document.getElementById('pg').value=done;document.getElementById('pt').textContent=done+' / '+total+' nets wired';try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
svgs.forEach(svg=>{const sid=svg.dataset.sec;svg.querySelectorAll('.w[data-net]').forEach(w=>{
 w.addEventListener('mouseenter',()=>{svg.classList.add('hl');svg.querySelectorAll('.w[data-net="'+w.dataset.net+'"]').forEach(x=>x.classList.add('on'))});
 w.addEventListener('mouseleave',()=>{svg.classList.remove('hl');svg.querySelectorAll('.w.on').forEach(x=>x.classList.remove('on'))});
 w.addEventListener('click',()=>{const k=sid+'|'+w.dataset.net;if(st[k])delete st[k];else st[k]=1;apply()})})});
document.getElementById('rs').onclick=()=>{if(confirm('Clear all net ticks?')){st={};apply()}};apply();
</script></div></body></html>""")
    return "".join(o)


# ------------------------------------------------------------------ schematic page
SETUP = ["Open your EasyEDA Pro project (one schematic, 8 sheets, one PCB).", "Sheet names: Power, Target Power, USB+ESD, USB-UART, Auto-program, Target I/O, LEDs + Switches, Connectors.",
         "Parts are placed by LCSC number (done). Set each Designator to the Ref in the tables below (rename U8 to U2).", "Use net labels for every connection that leaves a sheet; the same name on both sheets. Names are case-sensitive (+3V3, not +3v3).",
         "GND, +3V3 and +5V can be power flags; every other rail (VBUS_F, VIO, +3V3_T, +5V_T) is a normal net label.", "Run the schematic check (ERC) after each sheet and fix every warning."]
FINAL = ["Every net label is used at least twice (single-use labels are typos).", f"13 No-Connect flags: USB1 SBU1/SBU2, U2 pins 1, 9, 10, 11, 14, 16, 17, 18, 22, 24, SW4 pin 3.",
         "Export the netlist (Design > Netlist) and compare with hardware/netlist.csv: 43 nets.", f"Part count: {len(PART)} references (66) - BOM page.", "Export the schematic PDF and send it for a check."]


def sheet_parts_table(secs):
    groups, order = {}, []
    for s in secs:
        for r in SEC[s][2]:
            c = BYREF[r][6]
            if c not in groups:
                groups[c] = [[], BYREF[r]]
                order.append(c)
            groups[c][0].append(r)
    body = ""
    for c in order:
        refs, b = groups[c]
        link = f'<a href="https://www.lcsc.com/product-detail/{c}.html" target="_blank" rel="noopener">{c}</a>' if c.startswith("C") else "PCB"
        body += f'<tr><td><b>{e(", ".join(refs))}</b></td><td class="n">{len(refs)}</td><td>{e(b[2])}</td><td><span class="mpn">{e(b[4])}</span></td><td>{link}</td></tr>'
    return f'<div class="scroll"><table><thead><tr><th>Ref</th><th>Qty</th><th>Function</th><th>Part</th><th>LCSC</th></tr></thead><tbody>{body}</tbody></table></div>'


def u2_table():
    rows = ""
    for num, name, net in sorted(PART["U2"][5], key=lambda x: int(x[0])):
        what = '<b style="color:#dc2626">No-Connect flag</b>' if net == "NC" else ("GND" if net == "GND" else f'net label <b>{e(net)}</b>')
        rows += f"<tr><td><b>{num}</b></td><td>{e(name)}</td><td>{what}</td></tr>"
    return f'<div class="scroll"><table><thead><tr><th>Pin</th><th>Name</th><th>What to put on the pin</th></tr></thead><tbody>{rows}</tbody></table></div>'


def esd_table():
    rows = ""
    for ref in ("U3", "U6", "U7"):
        for num, name, net in PART[ref][5]:
            rows += f"<tr><td><b>{ref}</b></td><td>{num}</td><td>{e(name)}</td><td>{e(net)}</td></tr>"
    return f'<div class="scroll"><table><thead><tr><th>Ref</th><th>Pin</th><th>Name</th><th>Net</th></tr></thead><tbody>{rows}</tbody></table></div>'


def page_schem():
    o = [head("Universal USB Flasher V2.1 - Schematic by section", "Eight sheets, simplified symbols, with the parts of each sheet; the same Sheet 1-8 as on the BOM and Wiring pages and in your EasyEDA project.", "", "schematic-sections.html")]
    o.append('<p class="mut">Jump to: <a href="#u2pins">U2 CH342F pin guide (with No-Connect flags)</a> &middot; <a href="#esdpins">U3 / U6 / U7 ESD pin guide</a></p><div class="warn"><b>Planning drawing.</b> Symbols are simplified: draw the real schematic in EasyEDA from this page and the Wiring page. LEDs and diodes: triangle = anode (A), bar = cathode (K).</div>')
    o.append(LEGEND)
    total = len(SETUP) + len(FINAL) + sum(len(secs) for _, _, secs in PAGES)
    o.append(f'<div class="bar"><progress id="pg" value="0" max="{total}" style="width:240px"></progress><span id="pt" class="mut"></span><button class="ghost" id="rs">Clear ticks</button></div>')
    o.append('<section class="card" id="setup" style="--c:#475569"><h2>Setup in EasyEDA</h2>' + "".join(f'<div class="step"><input type="checkbox" class="ck" data-k="setup{i}"><span><b>{i}.</b> {e(s)}</span></div>' for i, s in enumerate(SETUP, 1)) + "</section>")
    for pid, ptitle, secs in PAGES:
        refs = [r for s in secs for r in SEC[s][2]]
        nets = sorted({x[2] for r in refs for x in PART[r][5]} - {"NC"})
        leave = [n for n in nets if len({pg for _, _, pg in NETS[n]}) > 1]
        o.append(f'<section class="card" id="{pid}" style="--c:{PAGE_COL[pid]}"><h2>{e(ptitle)}</h2><div class="scroll">{SH.SHEETS[pid]()}</div>')
        o.append(f'<p class="mut">Nets leaving this sheet (net labels): {e(", ".join(leave)) or "none"}.</p>')
        o.append('<h3>Parts of this sheet</h3>' + sheet_parts_table(secs))
        o.append('<details open><summary><b>Build steps</b> (tick as you draw this sheet)</summary>')
        for i, s in enumerate(secs, 1):
            o.append(f'<div class="step"><input type="checkbox" class="ck" data-k="{pid}-s{i}"><span><b>{i}. {e(SEC[s][1])}:</b> {e(SEC[s][3])}</span></div>')
        o.append("</details></section>")
    o.append('<section class="card" id="u2pins" style="--c:#14b8a6"><h2>Pin guide: U2 CH342F (QFN-24, all 25 pins)</h2><p class="mut">Your symbol: pins 1-6 on the left, 7-12 on the bottom, 13-18 on the right (bottom to top) plus EP 25, 19-24 along the top. '
             '<b style="color:#dc2626">No-Connect flag</b> on the 10 unused modem pins.</p>' + u2_table() + '</section>')
    o.append('<section class="card" id="esdpins" style="--c:#4895ef"><h2>Pin guide: USBLC6-2SC6 (U3) and USBLC6-4SC6 (U6, U7)</h2><p class="mut">The pin numbers are hidden in your symbols: left-middle = pin 2 (GND), right-middle = pin 5 (VBUS / +5V).</p>' + esd_table() + '</section>')
    o.append('<section class="card" id="final" style="--c:#10b981"><h2>Final checks</h2>' + "".join(f'<div class="step"><input type="checkbox" class="ck" data-k="final{i}"><span><b>{i}.</b> {e(s)}</span></div>' for i, s in enumerate(FINAL, 1)) + "</section>")
    o.append(links() + """<script>
const K='uusbf-tp-schem';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const cks=[...document.querySelectorAll('.ck')];
function upd(){const n=cks.filter(c=>c.checked).length;document.getElementById('pg').value=n;document.getElementById('pt').textContent=n+' / '+cks.length+' done';cks.forEach(c=>{const r=c.closest('.step');if(r)r.classList.toggle('ok',c.checked)});try{localStorage.setItem(K,JSON.stringify(Object.fromEntries(cks.filter(c=>c.checked).map(c=>[c.dataset.k,1]))))}catch(e){}}
cks.forEach(c=>{c.checked=!!st[c.dataset.k];c.addEventListener('change',upd)});document.getElementById('rs').onclick=()=>{cks.forEach(c=>c.checked=false);upd()};upd();
</script></div></body></html>""")
    return "".join(o)


# ------------------------------------------------------------------ PCB page (origin top-left, y down)
PL = {r[0]: r for r in D["placement"]}
BLOCKS = D["blocks"]
REFBLK = {r: b[0] for b in BLOCKS for r in b[4]}
NETW = [("VBUS, VBUS_F, +5V, +5V_T", "0.8 mm", "Up to 0.5 A plus the board itself."), ("+3V3, +3V3_T", "0.6 mm", "ESP32 Wi-Fi peaks about 0.5 A."), ("VIO", "0.3 mm", "Logic supply, a few mA."),
        ("GND", "pour on both layers", "Stitching vias, especially around U2, U4, U5 and USB1."), ("USB_DP / USB_DM", "0.2-0.3 mm pair", "Short, side by side, no vias, over solid GND (USB full-speed)."),
        ("ILIM3 / ILIM5", "0.25 mm, < 3 mm", "R18 / R19 right at the ILIM pin."), ("Signals", "0.25 mm", "TXD, RXD, DTR, RTS, EN, IO0 and the rest.")]
STEPS = [f"Draw the outline {BW:.0f} x {BH:.0f} mm with 2 mm corners and the M3 holes at " + ", ".join(f"({x:g}, {y:g})" for x, y in D["board"]["holes"]) + " mm (3.2 mm, non-plated).",
         "Update the PCB from the schematic. Check every footprint against its datasheet first (U2 QFN-24, U4/U5 SOT-23-6, USB1, J3 box header).",
         "Place block by block with the X / Y tables (origin top-left, Y down), ticking each part here.", "Draw one dashed rectangle per block on the Top Silkscreen layer with its title.",
         "Route USB D+/D- first, then power (wide traces), then signals. Pour GND on both layers.",
         "Silkscreen: H1 colour labels, POWER / RESET / BOOT / IO 3V3|5V / UART|UPDI, 5V IO!, OVERLOAD, AUTO-PROG (cap = ON), J5 pin names, ESP-01 outline.", "Run DRC, export Gerber, order (see the build guide)."]


def part_svg(ref, dim=False):
    _, x, y, w, h, g, lab = PL[ref]
    col = next(b[2] for b in BLOCKS if b[0] == REFBLK[ref])
    f = 1.4 if min(w, h) > 3.2 else 1.0
    b = BYREF[ref]
    return (f'<g class="pt" data-ref="{ref}" opacity="{".22" if dim else "1"}"><title>{e(ref)}: {e(PART[ref][2])} [{e(b[6])}] x={x:g} y={y:g} mm</title>'
            f'<rect x="{x-w/2:.2f}" y="{y-h/2:.2f}" width="{w:.2f}" height="{h:.2f}" rx="0.3" fill="{col}" fill-opacity=".30" stroke="{col}" stroke-width="0.2"/>'
            f'<text x="{x:.2f}" y="{y+f/3:.2f}" text-anchor="middle" font-size="{f}" font-weight="700" fill="var(--fg)" style="pointer-events:none">{e(ref)}</text></g>')


def board_inner(full, active=None):
    o = [f'<rect x="0" y="0" width="{BW}" height="{BH}" rx="2" fill="var(--board)" stroke="var(--fg)" stroke-width="0.3"/>']
    for gx in range(10, int(BW), 10):
        o.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{BH}" stroke="var(--line)" stroke-width="0.08" stroke-dasharray="0.5 1"/>')
        if full: o.append(f'<text x="{gx}" y="-0.8" text-anchor="middle" font-size="1.3" fill="#5b6677">{gx}</text>')
    for gy in range(10, int(BH), 10):
        o.append(f'<line x1="0" y1="{gy}" x2="{BW}" y2="{gy}" stroke="var(--line)" stroke-width="0.08" stroke-dasharray="0.5 1"/>')
        if full: o.append(f'<text x="-0.8" y="{gy+0.5}" text-anchor="end" font-size="1.3" fill="#5b6677">{gy}</text>')
    for hx, hy in D["board"]["holes"]:
        o.append(f'<circle cx="{hx}" cy="{hy}" r="3" fill="none" stroke="#9aa5b5" stroke-width="0.2" stroke-dasharray="0.6 0.4"/><circle cx="{hx}" cy="{hy}" r="1.6" fill="var(--board)" stroke="#9aa5b5" stroke-width="0.2"/>')
    j2 = PL["J2"]
    o.append(f'<rect x="{j2[1]-7.15:.2f}" y="{j2[2]-3:.2f}" width="14.3" height="24.8" rx="0.8" fill="none" stroke="#ca8a04" stroke-width="0.2" stroke-dasharray="0.8 0.5"/><text x="{j2[1]:.2f}" y="{j2[2]+15:.2f}" text-anchor="middle" font-size="1.4" fill="#ca8a04">ESP-01 overhang</text>')
    for b in BLOCKS:
        x0, y0, x1, y1 = b[3]
        dim = active is not None and b[0] != active
        tw = len(b[1]) * 0.78 + 1.0
        o.append(f'<g opacity="{".35" if dim else "1"}"><rect x="{x0}" y="{y0}" width="{x1-x0:.2f}" height="{y1-y0:.2f}" rx="0.5" fill="none" stroke="{b[2]}" stroke-width="0.25" stroke-dasharray="1.1 0.6"/>'
                 f'<rect x="{x0+0.6:.2f}" y="{y0-0.7:.2f}" width="{tw:.2f}" height="1.3" fill="var(--board)"/><text x="{x0+1.0:.2f}" y="{y0+0.3:.2f}" font-size="1.15" font-weight="700" fill="{b[2]}">{e(b[1])}</text></g>')
    for ref in PL:
        o.append(part_svg(ref, dim=(active is not None and REFBLK[ref] != active)))
    return "".join(o)


def board_svg(view=None, active=None, width_px=860):
    vx0, vy0, vx1, vy1 = view or (-3, -3, BW + 3, BH + 24)
    w, h = vx1 - vx0, vy1 - vy0
    return f'<svg viewBox="{vx0:.2f} {vy0:.2f} {w:.2f} {h:.2f}" width="{width_px:.0f}" height="{width_px*h/w:.0f}" class="plan" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif">{board_inner(view is None, active)}</svg>'


def parts_table(b):
    t = '<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Part</th><th>LCSC</th><th>X mm</th><th>Y mm</th><th>Size mm (est.)</th></tr></thead><tbody>'
    for r in b[4]:
        _, x, y, w, h, g, lab = PL[r]
        t += f'<tr data-ref="{r}"><td><input type="checkbox" class="ck" data-k="{r}"></td><td><b>{r}</b></td><td>{e(PART[r][2])}</td><td>{e(BYREF[r][6])}</td><td class="num">{x:g}</td><td class="num">{y:g}</td><td>{w:g} x {h:g}</td></tr>'
    return t + "</tbody></table></div>"


def page_pcb():
    total = len(PL)
    used = sum(r[3] * r[4] for r in D["placement"])
    chips = ('<div class="chips"><a style="background:#607d8b" href="#size">Board size</a><a style="background:#607d8b" href="#plan">Floor plan</a>'
             + "".join(f'<a style="background:{b[2]}" href="#{b[0]}">{e(b[1])}</a>' for b in BLOCKS)
             + f'<a style="background:#607d8b" href="#nets">Nets</a><a style="background:#607d8b" href="#steps">Steps</a><span class="mut">placed <b id="tot">0</b> / {total}</span><div class="pbar"><div id="barfill"></div></div><button class="ghost" id="reset">Reset ticks</button></div>')
    o = [head(f"Universal USB Flasher V2.1 - PCB floorplan {BW:.0f} x {BH:.0f} mm", f"{BW:.0f} x {BH:.0f} mm, 2 layers. One zoomed drawing, one dashed silkscreen box and one X / Y table per block; tick each part as you place it in EasyEDA (saved in this browser).", chips, "pcb-floorplan.html")]
    o.append(f'<section class="card" id="size"><h2>Board size: {BW:.0f} x {BH:.0f} mm</h2><div class="rec"><b>2 layers, 1.6 mm FR-4, 1 oz copper, {BW:.0f} x {BH:.0f} mm, 2 mm corners, two M3 holes (3.2 mm, non-plated).</b> Parts use about {used:.0f} mm&sup2; of {BW*BH:.0f} mm&sup2; ({100*used/(BW*BH):.0f} %). Under 100 x 100 mm, the cheapest PCB tier. The ESP-01 module hangs off the bottom edge.</div>'
             '<h3>Outline and holes</h3><div class="scroll"><table><thead><tr><th>Item</th><th>X mm</th><th>Y mm</th><th>Size</th></tr></thead><tbody>'
             f'<tr><td>Board outline</td><td class="num">0 - {BW:.0f}</td><td class="num">0 - {BH:.0f}</td><td>{BW:.0f} x {BH:.0f}, corner radius 2 mm (origin top-left, Y down)</td></tr>'
             + "".join(f'<tr><td>MH{i} M3 hole</td><td class="num">{hx:g}</td><td class="num">{hy:g}</td><td>3.2 mm, non-plated</td></tr>' for i, (hx, hy) in enumerate(D["board"]["holes"], 1))
             + '</tbody></table></div><h3>Edge plan</h3><ul class="rules"><li><b>Left edge:</b> USB-C (USB1).</li><li><b>Top edge:</b> SW5 POWER, SW1 RESET, SW2 BOOT, SW3 IO 3V3|5V, SW4 UART|UPDI.</li>'
             '<li><b>Right edge:</b> H1 main header (pin 1 3V3 at the top).</li><li><b>Bottom edge:</b> J3 ESP-Prog, J2 ESP-01 (module overhangs), J4 PROG 2.54, J5 UART2.</li></ul>'
             '<p class="mut">The placement checker confirms: every part inside its own block box, no two boxes overlapping, no part overlapping another, nothing within 3 mm of a mounting hole.</p></section>')
    o.append('<section class="card" id="plan"><h2>Floor plan<span class="cnt">dashed boxes = silkscreen boxes; click a part to tick it</span></h2><div class="scroll">' + board_svg() + '</div></section>')
    for b in BLOCKS:
        x0, y0, x1, y1 = b[3]
        crop = (max(x0 - 3, -2), max(y0 - 3, -2), min(x1 + 3, BW + 2), min(y1 + 3, BH + 2))
        wpx = int(min(900, max(520, (crop[2] - crop[0]) * 16)))
        o.append(f'<section class="card" id="{b[0]}" style="--c:{b[2]}"><h2>{e(b[1])}<span class="cnt"><span class="done">0</span> / {len(b[4])} placed &middot; box x {x0:g} to {x1:g}, y {y0:g} to {y1:g} mm</span></h2><ul class="rules">'
                 + "".join(f"<li>{e(t)}</li>" for t in b[5]) + f'</ul><div class="scroll">{board_svg(view=crop, active=b[0], width_px=wpx)}</div>{parts_table(b)}</section>')
    o.append('<section class="card" id="nets"><h2>Nets and trace widths<span class="cnt">1 oz copper, with margin</span></h2><div class="scroll"><table><thead><tr><th>Net</th><th>Width</th><th>Notes</th></tr></thead><tbody>' + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in NETW) + '</tbody></table></div></section>')
    o.append('<section class="card" id="steps"><h2>Order of work</h2><ol class="steps">' + "".join(f"<li>{e(t)}</li>" for t in STEPS) + "</ol></section>" + links())
    o.append("""<script>
const K='uusbf-tp-pcb';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
function apply(){const total=document.querySelectorAll('#plan .pt').length;document.querySelectorAll('.pt').forEach(g=>g.classList.toggle('ok',!!st[g.dataset.ref]));
 document.querySelectorAll('tr[data-ref]').forEach(r=>{const on=!!st[r.dataset.ref];r.classList.toggle('ok',on);r.querySelector('.ck').checked=on});
 const n=Object.keys(st).length;document.getElementById('tot').textContent=n;document.getElementById('barfill').style.width=(100*n/total)+'%';
 document.querySelectorAll('section.card[id]').forEach(sec=>{const rows=sec.querySelectorAll('tr[data-ref]');if(!rows.length)return;const d=[...rows].filter(r=>st[r.dataset.ref]).length;const c=sec.querySelector('.done');if(c)c.textContent=d});
 try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
function tog(r){if(st[r])delete st[r];else st[r]=1;apply()}
document.querySelectorAll('.pt').forEach(g=>g.addEventListener('click',()=>tog(g.dataset.ref)));document.querySelectorAll('input.ck').forEach(c=>c.addEventListener('change',()=>tog(c.dataset.k)));
document.getElementById('reset').onclick=()=>{st={};apply()};apply();
</script></div></body></html>""")
    return "".join(o)


def check_layout():
    errs = []
    for b in BLOCKS:
        x0, y0, x1, y1 = b[3]
        for r in b[4]:
            _, x, y, w, h, *_ = PL[r]
            if r != "USB1" and (x - w / 2 < x0 or x + w / 2 > x1 or y - h / 2 < y0 or y + h / 2 > y1):
                errs.append(f"{r} outside {b[0]}")
    for i in range(len(BLOCKS)):
        for j in range(i + 1, len(BLOCKS)):
            a, c = BLOCKS[i][3], BLOCKS[j][3]
            if a[0] < c[2] and c[0] < a[2] and a[1] < c[3] and c[1] < a[3]:
                errs.append(f"block overlap {BLOCKS[i][0]} / {BLOCKS[j][0]}")
    if set(REFBLK) != set(PART):
        errs.append(f"block refs mismatch {set(REFBLK) ^ set(PART)}")
    return errs


def main():
    errs = check_layout()
    if errs:
        print("LAYOUT ERRORS:", errs); sys.exit(1)
    for name, fn in (("bom.html", page_bom), ("wiring-by-section.html", page_wiring), ("schematic-sections.html", page_schem), ("pcb-floorplan.html", page_pcb)):
        open(os.path.join(DOCS, name), "w", encoding="utf-8", newline="\n").write(fn())
    print("pages written: bom, wiring-by-section, schematic-sections, pcb-floorplan; blocks", len(BLOCKS), "sections", len(SEC))


if __name__ == "__main__":
    main()
