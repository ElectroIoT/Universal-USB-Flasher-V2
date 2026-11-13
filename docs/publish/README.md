# Posting the project (OSHWLab, PCBWay, others)

Ready-to-paste text for each site, plus a checklist. Nothing here is posted automatically: you post it from your own account.

| File | Use |
|---|---|
| [oshwlab.md](oshwlab.md) | OSHWLab (EasyEDA) project page: title, summary, tags, description |
| [pcbway.md](pcbway.md) | PCBWay Shared Projects: title, description, board options to pick at upload |
| [`../../images/`](../../images/) | Cover and gallery images (list below) |

## Images to upload

| Image | Where |
|---|---|
| `images/pcb-3d.png` | **Cover image** on every site |
| `images/pcb-3d-top.png`, `images/pcb-3d-bottom.png` | Gallery |
| `images/pcb-2d-top.png`, `images/pcb-2d-bottom.png` | Gallery / PCB preview |
| `images/hero.svg`, `images/targets.svg`, `images/how-it-works.svg` | Description images (convert to PNG if the site does not take SVG) |

## Fabrication files (already in the repo)

Exported 2026-11-13 into [`hardware/fabrication/`](../../hardware/fabrication/): attach these on OSHWLab / PCBWay.

| File | Attach as |
|---|---|
| `Gerber_Universal-USB-Flasher-V2.1.zip` | Gerber (PCBWay: upload this zip) |
| `BOM_Universal-USB-Flasher-V2.1.csv` | BOM |
| `PickAndPlace_Universal-USB-Flasher-V2.1.csv` | Pick-and-place / centroid |

Still to export yourself if you want them: **schematic PDF** (Schematic1 → Export → PDF, all 8 pages) and a **3D STEP** (3D view → Export → 3D File). After any PCB change, export the Gerber, BOM and pick-and-place again (EasyEDA: Export menu) and replace the files.

## Checklist before posting

- [ ] DRC 0 errors (checked 2026-11-13); press Shift+B to rebuild the pours after any later edit
- [ ] Gerber viewer: top and bottom silkscreen readable, nothing printed on pads
- [ ] Say clearly on every site: **design only, not built or tested yet**
- [ ] Licence: CERN-OHL-P-2.0
- [ ] Link back to https://github.com/ElectroIoT/Universal-USB-Flasher-V2
- [ ] After the first boards work: update the status line everywhere and add real photos
