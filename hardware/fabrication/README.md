# Fabrication files – Universal USB Flasher V2.1

Exported from EasyEDA Pro on 2026-11-13 (PCB1, DRC 0 errors). **Not built or tested yet.**

| File | What |
|---|---|
| `Gerber_Universal-USB-Flasher-V2.1.zip` | Gerber + drill files. Upload this zip as-is to JLCPCB, PCBWay or any other fab |
| `BOM_Universal-USB-Flasher-V2.1.csv` | Bill of materials, 34 lines / 66 parts, every line has an LCSC part number (UTF-16, tab-separated: EasyEDA format, opens in Excel) |
| `PickAndPlace_Universal-USB-Flasher-V2.1.csv` | Pick-and-place (centroid) for SMT assembly, all parts on the top side |

## Board order settings

2 layers · 80 × 40 mm · 1.6 mm FR-4 · 1 oz copper · min track/space 6/6 mil · min hole 0.3 mm · any mask colour (renders use blue) · white silkscreen · HASL lead-free, or ENIG for the 0.5 mm-pitch QFN (U2).

The zip also holds EasyEDA's flying-probe test data (`FlyingProbeTesting.json`) and `How-to-order-PCB.txt`. Fabs that don't use them ignore them.

## Assembly notes

- U2 (CH342F, QFN-24, 0.5 mm pitch): stencil + hot air or SMT service. Exposed pad = GND.
- Through-hole: H1, J2, J3, J4, J5, SJ1, SJ2 and the SW3 / SW4 slide switches. Fit them after the SMT parts.
- Fit jumper caps (C5305, not in the EasyEDA BOM) on SJ1 and SJ2 to turn auto-program on.
