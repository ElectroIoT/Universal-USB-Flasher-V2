# Feature ideas

## Done in V2.1 (2026-11-13)
| Feature | How it is implemented |
|---|---|
| ESP-Prog compatible header | J3: 2×3 1.27 mm box header in ESP-Prog PROG order; J4: same pinout at 2.54 mm |
| Current-limited target power | U4/U5 TPS2553 (≈0.61 A on 3V3, ≈0.51 A on 5V), SW5 POWER-CYCLE, LED6 OVERLOAD from FAULT# |
| ESD on header pins | U6/U7 USBLC6-4SC6 on TX, RX, DTR, RTS, EN, IO0, TX2, RX2 |
| 5V-IO warning LED | Q3 MMBT3906 compares VIO with +3V3 and lights LED5 in 5 V mode (no DPDT switch needed) |
| Dual UART | CH342F replaces CH343G; UART2 on J5, blue LED4 on RX2 |
| Pogo-pad standard | [prog-pad-standard.md](prog-pad-standard.md); pogo jig plugs into J4 |

## Still open
### Pogo jig adapter board
A small PCB with 6 pogo pins in the PROG pattern, 2 locating pins and a 2×3 2.54 mm female header that plugs into J4.

### Enclosure
A 3D-printed or acrylic sandwich case that protects the bottom side and supports the ESP-01 overhang.

### Stand-alone offline programmer (separate project)
An ESP32-S3 with an SD card and a "Flash" button that writes a stored image to targets without a PC, for small production runs.
