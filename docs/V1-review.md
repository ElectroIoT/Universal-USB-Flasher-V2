# V1 review: what V2 fixes

V1 is the CH340C board in [Universal-USB-To-Serial-Flasher](https://github.com/ElectroIoT/Universal-USB-To-Serial-Flasher). This review was done on 2026-11-12 from its schematic PNG, BOM and PCB images (not the live EasyEDA file).

| # | V1 issue | Effect | V2 fix |
|---|---|---|---|
| 1 | Q2 (IO0 transistor) drawn with **collector on DTR and emitter on IO0** | The NPN runs reverse-active at very low gain, so auto-boot is unreliable | Q2: C = IO0, B = RTS# via 10k, E = DTR# |
| 2 | "SJ_DTR / SJ_RTS" are 2-pin headers (PZ254V-11-02P), not solder jumpers | Auto-program does nothing until jumper caps are fitted, but the README says "closed by default" | Real solder jumpers, bridged by default |
| 3 | Header pin labelled "RST" is raw RTS | There's no correct Arduino reset; connecting it to RESET can hold the AVR in reset | RST pin = DTR# through 100 nF + 10k pull-up |
| 4 | CH340C runs at 3.3 V | A 5 V Arduino TX drives 5 V into a 3.3 V input | CH343G with VIO + 3.3/5 V switch |
| 5 | No fuse | A short on the 5V pin goes straight back to the PC's USB port | 500 mA polyfuse |
| 6 | Power LED 220 Ω from 5 V | ~13 mA, very bright | 1 kΩ from 3.3 V (~1.3 mA) |
| 7 | "PWD" silkscreen typo; README values don't match the BOM | Confusing for builders | Fixed |
| 8 | 100k base pull-downs R8/R9 | Not needed | Removed (also keeps the CH343 DTR pin free of a pull-down) |
| 9 | Three discrete ESD diodes | More parts | One USBLC6-2SC6 |

Before reordering V1 boards, open Q2 in EasyEDA and check whether the problem is only in the drawing or also in the PCB (symbol-to-footprint pin map).
