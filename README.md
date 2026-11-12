<p align="center"><img src="images/hero.svg" alt="Universal USB Flasher V2 board" width="100%"></p>

# Universal USB Flasher V2

**One USB-C board to flash ESP32, ESP8266 (ESP-12F, ESP-01), Arduino/ATmega and UPDI AVR chips.**
True 3.3 V / 5 V logic, a plug-in ESP-01 socket, automatic reset/boot, and USB overcurrent protection.

> **Status: design stage.** The plan, netlist, LCSC BOM and placement are done. The schematic and PCB are being drawn in EasyEDA. **Nothing has been built or tested on hardware yet.** This is V2 of [Universal-USB-To-Serial-Flasher](https://github.com/ElectroIoT/Universal-USB-To-Serial-Flasher) (CH340C). See [what V2 fixes](docs/V1-review.md).

| | |
|---|---|
| USB-UART | **WCH CH342F dual UART** (QFN-24), VIO 1.8–5 V, up to 3 Mbaud, two COM ports, native CDC driver |
| Logic level | **SW3**: 3.3 V or ~4.6 V (5 V rail after Schottky) |
| Targets | ESP32 / S2 / S3 / C3, ESP8266, ESP-12F, ESP-01/01S, ATmega328P, Pro Mini, LGT8F328P, ATtiny 0/1/2-series, AVR-DA/DB/DD |
| Power out | 3.3 V and 5 V through **current-limited TPS2553 switches** (≈0.61 A / ≈0.51 A), POWER-CYCLE button, OVERLOAD LED |
| Ports | H1 1×11 · **ESP-Prog 2×3 1.27 mm (J3)** · 2×3 2.54 mm pogo/cable (J4) · UART2 (J5) · ESP-01 socket (J2) |
| Board | 80 × 40 mm, 2-layer, 1.6 mm. All parts on LCSC |
| Interactive guide | [`docs/index.html`](docs/index.html): BOM, schematic and placement **tick-lists** for EasyEDA |

---

## Contents
- [Features](#features)
- [How it works](#how-it-works)
- [Pinout](#pinout)
- [Wiring cheat-sheet](#wiring-cheat-sheet)
- [Bill of materials](#bill-of-materials)
- [Schematic pages (EasyEDA)](#schematic-pages-easyeda)
- [PCB placement](#pcb-placement)
- [Bring-up test plan](#bring-up-test-plan)
- [Roadmap / feature ideas](#roadmap--feature-ideas)
- [Repository layout](#repository-layout)

---

## Features

> **V2.1 update (2026-11-13):** CH342F dual UART, ESP-Prog port, current-limited target power with power-cycle button, ESD on all header lines, 5V-IO warning LED and the PROG pogo-pad standard. Current data: [`hardware/`](hardware/) (generated from `tools/design.json`). Some sections below still describe V2.0 details and will be refreshed.

<p align="center"><img src="images/power-switch.svg" width="100%"></p>
<p align="center"><img src="images/dual-uart.svg" width="100%"></p>
<p align="center"><img src="images/prog-pad.svg" width="100%"></p>

<p align="center"><img src="images/targets.svg" alt="Supported targets" width="100%"></p>

- ⚡ **3.3 V / 5 V logic switch.** CH343G VIO follows SW3, so no level shifters are needed.
- 🔁 **ESP auto-program.** Two MMBT3904 transistors (NodeMCU circuit) drive EN and IO0, so esptool, Arduino IDE and PlatformIO flash with no button pressing.
- 📡 **ESP-01 socket (J2).** Plug in an ESP-01/01S and flash, with no wires. GPIO2/RST/CH_PD pull-ups are on the board.
- 🧩 **Bare ESP-12F / WROOM support.** EN and IO0 pull-ups, plus an IO15 pin with a 10k pull-down.
- ♾️ **Arduino auto-reset pin.** RST = DTR# through 100 nF, with a 10k pull-up.
- 🔧 **UPDI mode (SW4).** TX→4.7k→RX turns the RX pin into a SerialUPDI programmer.
- 🛡️ **Protected USB-C.** 5.1k CC, USBLC6-2SC6 ESD, 500 mA PTC, Schottky back-feed diode.
- 🔌 **SJ1/SJ2 solder jumpers**, bridged by default. Cut them to turn the board into a plain USB-UART.
- 💡 **4 LEDs.** PWR, USB-ACT (enumerated), TX, RX. They run from VIO, so they work at both logic levels.
- 🎨 **Colour-coded silkscreen**, kept from V1.

---

## How it works

### 1. Power path
<p align="center"><img src="images/power-flow.svg" alt="Power path animation" width="100%"></p>

USB VBUS goes through the **500 mA polyfuse F1** (`VBUS_F`). That feeds the CH343G core (VDD5 + VBUS sense) and, via the **Schottky D1**, the `+5V` rail (~4.65 V). The **SGM2212 LDO** makes `+3V3` (800 mA) for the header, the ESP-01 socket and the pull-ups. D1 stops a self-powered 5 V target from back-feeding the PC.

### 2. Auto-program (ESP32 / ESP8266)
<p align="center"><img src="images/auto-program.svg" alt="Auto-program timing animation" width="100%"></p>

| DTR# pin | RTS# pin | EN | IO0 | Meaning |
|:-:|:-:|:-:|:-:|---|
| 1 | 1 | high | high | idle / run |
| 1 | 0 | **low** | high | reset |
| 0 | 1 | high | **low** | boot (download) mode |
| 0 | 0 | high | high | both asserted (serial monitor), no reset |

- Q1: B ← DTR# via 10k, E = RTS#, C = EN.
- Q2: B ← RTS# via 10k, E = DTR#, **C = IO0**. In V1 this transistor was drawn with C and E swapped.

### 3. Logic-level switch
<p align="center"><img src="images/vio-switch.svg" alt="VIO switch animation" width="100%"></p>

The CH343G has a separate **VIO** pin for its UART and modem I/O. SW3 connects VIO to +3V3 or +5V, so TX/RX/DTR/RTS swing to the target's own supply. **Set SW3 to 3V3 before plugging in an ESP-01** (the ESP8266 is not 5 V tolerant).

### 4. UPDI mode
<p align="center"><img src="images/updi-mode.svg" alt="UPDI mode animation" width="100%"></p>

SW4 in UPDI links TX to RX through R15 (4.7k). This is the standard **SerialUPDI** adapter. Connect `RX/UPDI`, `GND` and `VCC` to the AVR and set SW3 to the AVR's voltage.

```bash
# Arduino IDE: megaTinyCore / DxCore → Programmer "SerialUPDI - 230400 baud"
pymcuprog -t uart -u COM7 -d attiny1614 write -f app.hex --erase --verify
```

### 5. Arduino reset
`DTR#` → C10 100 nF → `RST`, with R14 10k to VIO. The falling edge of DTR when the IDE opens the port gives the classic Arduino auto-reset. It works on a bare ATmega328P, which has no DTR capacitor of its own.

---

## Pinout

**H1, 1×11, 2.54 mm** (silkscreen colours in brackets)

| Pin | Label | Net | Use |
|---:|---|---|---|
| 1 | 3V3 (red) | +3V3 | 3.3 V out |
| 2 | 5V (purple) | +5V | ~4.6 V out, 500 mA PTC |
| 3 | GND (black) | GND | ground |
| 4 | TX (orange) | TXD | flasher TX → target RX |
| 5 | RX/UPDI (green) | RXD | flasher RX ← target TX; UPDI pin in UPDI mode |
| 6 | DTR (blue) | DTR_N | raw DTR# |
| 7 | RTS (blue) | RTS_N | raw RTS# |
| 8 | RST (yellow) | RST | Arduino reset (DTR# via 100 nF) |
| 9 | EN (yellow) | EN | ESP EN/CH_PD (auto-program) |
| 10 | IO0 (yellow) | IO0 | ESP boot strap (auto-program) |
| 11 | IO15 (grey) | IO15 | 10k pull-down for bare ESP8266 |

**J2, ESP-01 socket (2×4 female)**, component side up, antenna pointing away from the header:
```
 GND   GPIO2  GPIO0  RXD
 TXD   CH_PD  RST    VCC
```

**CH343G (U2)**: 1 GND · 2 TXD · 3 RXD · 4 V3 (100 nF only) · 5 UD+ · 6 UD− · 7 VBUS · 8 ACT# · 9 DCD# (NC) · 10 TNOW/DTR# (**no pull-down!**) · 11 RTS# · 12 DSR# (NC) · 13 CTS# (NC) · 14 RI# (NC) · 15 VIO · 16 VDD5

---

## Wiring cheat-sheet

| Target | SW3 | SW4 | Connect |
|---|:-:|:-:|---|
| ESP32 / ESP8266 dev board | 3V3 | UART | 3V3 · GND · TX→RX · RX←TX · EN · IO0 |
| Bare ESP-12F | 3V3 | UART | 3V3 · GND · TX · RX · EN · IO0 · IO15 |
| Bare ESP32-WROOM / C3 / S3 | 3V3 | UART | 3V3 · GND · TX · RX · EN · IO0 |
| ESP-01 / 01S | **3V3** | UART | plug into J2 |
| Arduino Pro Mini 5 V / bare ATmega328P | 5V | UART | 5V · GND · TX · RX · RST |
| Arduino Pro Mini 3.3 V | 3V3 | UART | 3V3 · GND · TX · RX · RST |
| ATtiny1614 / AVR-Dx | target V | **UPDI** | VCC · GND · RX/UPDI |

```bash
esptool.py --port COM7 --baud 921600 write_flash 0x0 firmware.bin
```

---

## Bill of materials

Full CSV: [`hardware/BOM_V2_LCSC.csv`](hardware/BOM_V2_LCSC.csv). LCSC numbers were looked up on 2026-11-12. The interactive BOM with tick boxes is in [`docs/index.html`](docs/index.html#bom).

| Ref | Qty | Part | Package | LCSC | Notes |
|---|:-:|---|---|---|---|
| U2 | 1 | CH343G USB-UART (VIO) | SOP-16 | [C2844153](https://www.lcsc.com/product-detail/C2844153.html) | ⚠️ 500 in stock; alt CH343P C2846043 (QFN, different pinout) |
| U1 | 1 | SGM2212-3.3 LDO 800 mA | SOT-223 | [C3294699](https://www.lcsc.com/product-detail/C3294699.html) | |
| U3 | 1 | USBLC6-2SC6 ESD | SOT-23-6 | [C7519](https://www.lcsc.com/product-detail/C7519.html) | |
| F1 | 1 | JK-nSMD050-16 PTC 500 mA | 1206 | [C2680506](https://www.lcsc.com/product-detail/C2680506.html) | 1 A trip |
| D1 | 1 | 1N5819HW Schottky | SOD-123 | [C82544](https://www.lcsc.com/product-detail/C82544.html) | |
| Q1, Q2 | 2 | MMBT3904 NPN | SOT-23 | [C81464](https://www.lcsc.com/product-detail/C81464.html) | B=1 E=2 C=3 |
| USB1 | 1 | USB-C 16-pin | SMD | [C2765186](https://www.lcsc.com/product-detail/C2765186.html) | |
| SW1, SW2 | 2 | TS-1088 tact (RESET, BOOT) | SMD | [C720477](https://www.lcsc.com/product-detail/C720477.html) | |
| SW3, SW4 | 2 | MSK12C02 SPDT slide | SMD | [C431540](https://www.lcsc.com/product-detail/C431540.html) | IO 3V3/5V · UART/UPDI |
| H1 | 1 | 1×11 male header | THT | [C2840011](https://www.lcsc.com/product-detail/C2840011.html) | |
| J2 | 1 | 2×4 female header | THT | [C2897405](https://www.lcsc.com/product-detail/C2897405.html) | ESP-01 socket |
| LED1–4 | 4 | Red PWR, orange TX, yellow RX, green ACT | 0805 | C84256 · C84262 · C965814 · C84260 | |
| R1, R2 | 2 | 5.1k | 0805 | C27834 | USB-C CC |
| R3 | 1 | 1k | 0805 | C95781 | PWR LED |
| R4–R6 | 3 | 2.2k | 0805 | C17520 | LEDs |
| R7–R14 | 8 | 10k | 0805 | C84376 | base, pull-ups, IO15, RST |
| R15 | 1 | 4.7k | 0805 | C17673 | UPDI |
| C1, C5 | 2 | 10 µF 25 V | 0805 | C15850 | |
| C6, C8 | 2 | 22 µF 25 V | 0805 | C45783 | |
| C2–C4, C7, C9, C10 | 6 | 100 nF | 0805 | C49678 | |
| SJ1, SJ2 | 2 | solder jumper, bridged | PCB | — | auto-program enable |

**~43 parts, about $2.50 in parts per board** (low-quantity LCSC prices, without PCB and shipping).

---

## Schematic pages (EasyEDA)

The schematic is split into 4 EasyEDA pages. **Every pin with its footprint pin number, net and No-Connect flags** is in [`hardware/schematic-pages.md`](hardware/schematic-pages.md). The interactive tick-list is in [`docs/index.html`](docs/index.html#sch-check).

| Page | Contents | No-Connect flags |
|---|---|---|
| P1 · USB + Power | USB1, R1, R2, U3, F1, C1, D1, C5, U1, C6, C7, SW3, R3, LED1 | USB1.3 (SBU2), USB1.9 (SBU1) |
| P2 · USB-UART | U2, C2–C4, R4–R6, LED2–LED4 | U2.9 DCD#, U2.12 DSR#, U2.13 CTS#, U2.14 RI# |
| P3 · Auto-program + control | SJ1, SJ2, R7, R8, Q1, Q2, R9, C9, R10, R11, SW1, SW2, C10, R14, SW4, R15 | SW4.3 |
| P4 · Connectors | H1, J2, C8, R12, R13 | none |

Cross-check the finished schematic with **Design → Netlist** against [`hardware/netlist.csv`](hardware/netlist.csv).

---

## PCB placement

72 × 34 mm, 2 layers. Power runs left → right, the CH343G sits in the middle, target I/O is on the right edge, and the ESP-01 hangs off the bottom edge.
Starting coordinates for every footprint are in [`hardware/placement.csv`](hardware/placement.csv). The board map with tick boxes is in [`docs/index.html`](docs/index.html#placement).

- U3 within 3 mm of USB1. Keep D+/D− short and side by side over solid GND.
- C2/C3/C4 within 2 mm of U2 pins 16/4/15.
- SOT-223 tab: ≥ 1 cm² of copper + vias (ESP32 Wi-Fi peaks reach ~500 mA).
- SW1–SW4 on the top edge with big labels: `RESET` `BOOT` `IO 3V3|5V` `UART|UPDI`.
- Test pads: VBUS_F, +5V, +3V3, VIO, GND, TXD, RXD, DTR#, RTS#.

---

## Bring-up test plan
1. Before fitting U1/U2, check there's no short between VBUS / +5V / +3V3 and GND.
2. Rails: +5V ≈ 4.6–4.7 V, +3V3 = 3.30 V, and VIO follows SW3. PWR LED on.
3. The ACT LED comes on and a COM port appears.
4. TX↔RX loopback at 115200 and 2 Mbaud.
5. `esptool.py chip_id`: EN pulses low, then IO0 is held low as EN rises.
6. Flash an ESP32 DevKit, bare ESP-12F, ESP-01, Pro Mini 5 V (RST) and ATtiny1614 (UPDI).
7. Briefly short 5V to GND. The PTC trips and the PC port survives.

---

## Roadmap / feature ideas

These are ideas for V2.1 / V3. Nothing here is in the current design. Details in [`docs/feature-ideas.md`](docs/feature-ideas.md).

| Idea | Why |
|---|---|
| **ESP-Prog compatible 2×3 header** | Plug straight into boards that have Espressif's ESP-Prog programming header |
| **Current-limited target power switch** | Power-cycle the target with a button; a short trips a fast electronic limit before the PTC |
| **ESD array on header pins** | The header pins get touched and hot-plugged far more than USB |
| **5 V-IO warning LED** | Needs a DPDT slide switch (none in LCSC stock on 2026-11-12) |
| **CH342F dual UART** | Flash one target and watch a second device's log at the same time |
| **Tag-Connect / pogo pad standard** | Future ElectroIoT boards could be flashed with no header at all |
| **3D-printed case** | Protects the bottom of the board and the ESP-01 overhang |

---

## Repository layout
```
images/     animated SVG diagrams used in this README (CSS/SMIL, no JS)
docs/       index.html interactive design page + tick-lists; V1 review; feature ideas
hardware/   BOM_V2_LCSC.csv · netlist.csv · schematic-pages.md · placement.csv
tools/      gen_svgs.py (regenerates images/) · sch_parts.json (pin-level source data)
```

---

Licensed under **CERN-OHL-P-2.0** (see [LICENSE](LICENSE)).

Designed by **ElectroIoT**: [electroiot.in](https://electroiot.in) · [YouTube](https://www.youtube.com/@ElectroIoT-IN) · [Instagram](https://www.instagram.com/electroiot_in)
