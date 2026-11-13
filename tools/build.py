"""Build all hardware outputs from tools/design.json (single source of truth).

    python tools/build.py

Writes hardware/netlist.csv, hardware/BOM_V2_LCSC.csv, hardware/schematic-pages.md,
hardware/placement.csv and injects the design data into docs/index.html
(between /*DESIGN-START*/ and /*DESIGN-END*/). Fails loudly on inconsistencies.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'tools', 'design.json'), encoding='utf-8'))
HW = os.path.join(ROOT, 'hardware')
POWER = ('GND', '+3V3', '+5V')
errors = []

parts = {p[0]: p for p in D['parts']}
if len(parts) != len(D['parts']):
    errors.append('duplicate part refs')
pages = [p[0] for p in D['pages']]

# --- nets
nets = {}
for p in D['parts']:
    if p[1] not in pages:
        errors.append(f'{p[0]}: unknown page {p[1]}')
    seen = set()
    for num, name, net in p[5]:
        if num in seen:
            errors.append(f'{p[0]}: duplicate pin {num}')
        seen.add(num)
        if net != 'NC':
            nets.setdefault(net, []).append((p[0], num, name, p[1]))
for n, pins in nets.items():
    if len(pins) < 2:
        errors.append(f'net {n} has only one pin: {pins}')

# --- BOM coverage
bom_refs = []
for line in D['bom']:
    refs = line[0].split()
    if len(refs) != line[1]:
        errors.append(f'BOM qty mismatch: {line[0]} qty {line[1]}')
    bom_refs += refs
for r in bom_refs:
    if r not in parts:
        errors.append(f'BOM ref {r} not in parts')
for r in parts:
    if bom_refs.count(r) != 1:
        errors.append(f'part {r} appears {bom_refs.count(r)}x in BOM')
for line in D['bom']:
    for r in line[0].split():
        if r in parts and line[6] not in ('—', parts[r][4]) and parts[r][4] != '-':
            errors.append(f'{r}: LCSC {parts[r][4]} in parts vs {line[6]} in BOM')

# --- placement coverage
pl_refs = [p[0] for p in D['placement']]
for r in parts:
    if r not in pl_refs:
        errors.append(f'part {r} missing from placement')
for r in pl_refs:
    if r not in parts:
        errors.append(f'placement ref {r} not a part')
W, H = D['board']['w'], D['board']['h']
for r, x, y, w, h, g, lab in D['placement']:
    if g not in D['groups']:
        errors.append(f'{r}: unknown group {g}')
    if r != 'USB1' and (x - w / 2 < 0 or x + w / 2 > W or y - h / 2 < 0 or y + h / 2 > H):
        errors.append(f'{r}: outside board')
# simple overlap check
pl = D['placement']
for i in range(len(pl)):
    for j in range(i + 1, len(pl)):
        a, b = pl[i], pl[j]
        if abs(a[1] - b[1]) * 2 < (a[3] + b[3]) and abs(a[2] - b[2]) * 2 < (a[4] + b[4]):
            errors.append(f'overlap: {a[0]} / {b[0]}')

if errors:
    print('DESIGN ERRORS:')
    for e in errors:
        print('  -', e)
    sys.exit(1)

# --- BOM extras (not schematic parts, e.g. jumper caps) are added after validation
D['bom'] = D['bom'] + D.get('bom_extra', [])

# --- netlist.csv
with open(os.path.join(HW, 'netlist.csv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('Net,Connections (Ref.pin),Pages\n')
    for n in sorted(nets, key=lambda k: (k not in POWER, k)):
        pins = nets[n]
        f.write(f'{n},"' + '; '.join(f'{r}.{num}({name})' for r, num, name, _ in pins) + '",' + ' '.join(sorted({pg for *_, pg in pins})) + '\n')
    nc = [f'{p[0]}.{num}({name})' for p in D['parts'] for num, name, net in p[5] if net == 'NC']
    f.write('NC (No-Connect flag),"' + '; '.join(nc) + '",\n')

# --- BOM csv
def q(s):
    s = str(s)
    return '"' + s.replace('"', '""') + '"' if (',' in s or '"' in s) else s
G = D['groups']
with open(os.path.join(HW, 'BOM_V2_LCSC.csv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('Ref,Qty,Description,Package,MPN,Manufacturer,LCSC Part #,Stock (2026-11-12/13),Unit price (USD),Block,Notes\n')
    for r, qty, desc, pkg, mpn, mfr, lcsc, stock, price, st, g, note in D['bom']:
        f.write(','.join(q(x) for x in [r, qty, desc, pkg, mpn, mfr, lcsc, stock or 'not rechecked', '' if price is None else price, G[g][0], note]) + '\n')

# --- placement.csv
NOTES = D.get('notes', {})
with open(os.path.join(HW, 'placement.csv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(f'# Board {W} x {H} mm, origin top-left, Y down, part centres\n')
    f.write('Ref,X_mm,Y_mm,Body_W_mm,Body_H_mm,Block,Label,Note\n')
    for r, x, y, w, h, g, lab in D['placement']:
        f.write(','.join(q(v) for v in [r, x, y, w, h, G[g][0], lab, NOTES.get(r, '')]) + '\n')

# --- schematic-pages.md
L = ['# EasyEDA schematic: page-by-page connection list', '',
     f'Generated from `tools/design.json` ({D["version"]}). {len(D["parts"])} parts · {sum(len(p[5]) for p in D["parts"])} pins · {len(nets)} nets.', '',
     'For every part: place the symbol (by LCSC number), then wire each pin to the net shown. Pins marked **NC** get an EasyEDA **No-Connect flag**. '
     'GND, +3V3 and +5V use global power symbols. Every other net that appears on more than one page needs a net label with exactly the same name.', '',
     '> Check before you trust a pin number: D1 and LED1–LED6 (which symbol pin is K), Q1/Q2/Q3 (SOT-23: 1=B, 2=E, 3=C), U2 (QFN-24 pin 25 = exposed pad EP), J2 (odd pins top row assumed). R/C/PTC pins are interchangeable.', '',
     'An interactive version with tick boxes is in [docs/index.html](../docs/index.html#sch-check).', '']
for pid, title, sub in D['pages']:
    pp = [p for p in D['parts'] if p[1] == pid]
    pn = {x[2] for p in pp for x in p[5]} - {'NC', *POWER}
    cross = sorted(n for n in pn if len({pg for *_, pg in nets[n]}) > 1)
    ncs = [f'{p[0]}.{x[0]} ({x[1]})' for p in pp for x in p[5] if x[2] == 'NC']
    L += [f'## {title}', '', f'_{sub}_', '',
          f'**Net labels on this page:** {", ".join("`" + n + "`" for n in cross) or "none"}  ',
          f'**No-Connect flags:** {", ".join("`" + n + "`" for n in ncs) or "none"}', '']
    for p in pp:
        L += [f'### {p[0]}: {p[2]}', '', f'Footprint `{p[3]}` · LCSC {p[4]}', '', '| ✓ | Pin | Name | Net | Also on this net |', '|---|---|---|---|---|']
        for num, name, net in p[5]:
            if net == 'NC':
                other = '**No-Connect flag**'
            elif net in POWER:
                other = f'power symbol ({len(nets[net])} pins)'
            else:
                other = ', '.join(f'{r}.{n2}' + (f' ({pg})' if pg != pid else '') for r, n2, _, pg in nets[net] if not (r == p[0] and n2 == num))
            L.append(f'| ☐ | {num} | {name} | `{net}` | {other} |')
        L.append('')
open(os.path.join(HW, 'schematic-pages.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L))

# --- inject into every docs/*.html that has DESIGN markers
import glob
blob = '/*DESIGN-START*/\nconst DESIGN=' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n/*DESIGN-END*/'
pages = 0
for idx in sorted(glob.glob(os.path.join(ROOT, 'docs', '*.html'))):
    html = open(idx, encoding='utf-8').read()
    new, n = re.subn(r'/\*DESIGN-START\*/.*?/\*DESIGN-END\*/', lambda m: blob, html, flags=re.S)
    if n:
        open(idx, 'w', encoding='utf-8', newline='\n').write(new); pages += 1
if pages < 2:
    print('docs: expected DESIGN markers in index.html and build-guide.html'); sys.exit(1)

# --- README tables (between markers)
rd = os.path.join(ROOT, 'README.md')
readme = open(rd, encoding='utf-8').read()
def lc(c):
    return f'[{c}](https://www.lcsc.com/product-detail/{c}.html)' if c.startswith('C') else c
rows = ['| Ref | Qty | Part | Package | LCSC | Notes |', '|---|:-:|---|---|---|---|']
for r, qty, desc, pkg, mpn, mfr, lcsc, stock, price, st, g, note in D['bom']:
    warn = '⚠️ ' if st == 'warn' else ''
    rows.append(f'| {r.replace(" ", ", ")} | {qty} | {mpn}: {desc} | {pkg} | {lc(lcsc)} | {warn}{note} |')
known = sum((x[8] or 0) * x[1] for x in D['bom'])
rows += ['', f'**{sum(x[1] for x in D["bom"] if x[6].startswith("C"))} parts · {len({x[6] for x in D["bom"] if x[6].startswith("C")})} unique LCSC numbers · ≈${known:.2f} in captured LCSC prices per board** (plus a little for lines without a captured price; no PCB or shipping).']
pg = ['| Page | Parts | No-Connect flags |', '|---|---|---|']
for pid, title, sub in D['pages']:
    pp = [p for p in D['parts'] if p[1] == pid]
    ncs = [f'{p[0]}.{x[0]} {x[1]}' for p in pp for x in p[5] if x[2] == 'NC']
    pg.append(f'| {title} | {", ".join(p[0] for p in pp)} | {", ".join(ncs) or "none"} |')
for tag, body in (('BOM', rows), ('PAGES', pg)):
    readme, n = re.subn(rf'<!-- {tag}:START -->.*?<!-- {tag}:END -->', lambda m: f'<!-- {tag}:START -->\n' + '\n'.join(body) + f'\n<!-- {tag}:END -->', readme, flags=re.S)
    if n != 1:
        print(f'README: {tag} markers not found'); sys.exit(1)
open(rd, 'w', encoding='utf-8', newline='\n').write(readme)

nc_count = sum(1 for p in D['parts'] for x in p[5] if x[2] == 'NC')
print(f'OK: {len(D["parts"])} parts, {sum(len(p[5]) for p in D["parts"])} pins, {len(nets)} nets, {nc_count} NC pins, {len(D["bom"])} BOM lines, board {W}x{H} mm')

# --- wiring-by-section page (LED-dimmer style)
import subprocess
subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tools', 'gen_docs.py')], check=True)
