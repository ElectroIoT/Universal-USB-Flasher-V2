# OSHWLab post

**Project name:** Universal USB Flasher V2.1 (CH342F dual UART)

**Summary (one line):**
One USB-C board to flash ESP32, ESP8266 / ESP-12F / ESP-01, Arduino and UPDI AVR chips, with a second UART, ESP-Prog port, 3.3/5 V logic and current-limited target power.

**Tags:** ESP32, ESP8266, ESP-01, USB-UART, CH342F, programmer, flasher, UPDI, Arduino, ESP-Prog, USB-C

**Licence:** CERN-OHL-P-2.0

**Cover image:** `images/pcb-3d.png`

---

## Description (paste as Markdown)

> **Status:** design finished (schematic + routed 2-layer PCB, DRC 0 errors). **Not built or tested yet.** Feedback welcome.

### What it is
Universal USB Flasher V2.1 is a USB-C programmer and serial adapter for the boards makers use every day. It flashes ESP32 (all variants), ESP8266 / ESP-12F, plug-in ESP-01 modules, Arduino / ATmega boards and the newer UPDI AVR chips (ATtiny 0/1/2-series, AVR-DA/DB/DD). A second UART lets you watch another device's log at the same time.

It is V2 of the CH340C [Universal USB To Serial Flasher](https://github.com/ElectroIoT/Universal-USB-To-Serial-Flasher).

### Features
- **WCH CH342F dual UART**: two COM ports from one USB-C cable, up to 3 Mbaud, native driver on Windows 10/11, macOS and Linux
- **3.3 V / 5 V logic switch** (SW3) with a red **5V IO** warning LED
- **ESP auto-program** (two-transistor EN / IO0 circuit): esptool, Arduino IDE and PlatformIO flash with no button presses. Remove the SJ1 / SJ2 jumper caps to turn it off
- **ESP-Prog compatible port**: J3 1.27 mm box header and J4 2.54 mm header in Espressif's PROG pin order
- **ESP-01 socket** (J2) with the GPIO2 / RST / CH_PD pull-ups on the board
- **UPDI mode** (SW4): TX → 4.7k → RX makes the RX pin a SerialUPDI programmer
- **Arduino auto-reset** pin (DTR through 100 nF)
- **Current-limited target power**: TPS2553 switches, about 0.6 A on 3.3 V and 0.5 A on 5 V, POWER button (hold = off) and OVERLOAD LED
- **ESD on every line**: USBLC6-2SC6 on USB, two USBLC6-4SC6 on the header signals, 500 mA PTC fuse and a Schottky back-feed diode
- 6 status LEDs: PWR, TX, RX, RX2, 5V IO, OVERLOAD
- Every connector pin labelled on the top silkscreen, full pinout on the bottom

### Connectors
| Connector | Pins |
|---|---|
| H1 1×11 2.54 mm | 1 3V3 · 2 5V · 3 GND · 4 TX · 5 RX/UPDI · 6 DTR · 7 RTS · 8 RST · 9 EN · 10 IO0 · 11 IO15 |
| J3 1.27 mm / J4 2.54 mm (ESP-Prog) | 1 EN · 2 VDD · 3 TXD · 4 GND · 5 RXD · 6 IO0 |
| J2 ESP-01 | 1 GND · 2 TX · 3 IO2 · 4 EN · 5 IO0 · 6 RST · 7 RX · 8 3V3 |
| J5 UART2 | 1 GND · 2 TX2 · 3 RX2 · 4 DTR2 |

H1 TX / RX are named from the flasher side: TX goes to the target's RX.

### Board
- 80 × 40 mm, 2 layers, 1.6 mm FR-4, 1 oz copper
- Power tracks 0.5–0.6 mm, signals 0.254 mm, vias 0.3 mm / 0.6 mm, GND pour on both sides
- All 66 parts have LCSC part numbers. Only U2 (CH342F, QFN-24, 0.5 mm pitch) needs hot air or SMT assembly; the rest is 0805, SOT-23, SOT-23-6, SOD-123, SOT-223 and through-hole headers

### Files and docs
Full design, BOM, pinout, build guide and bring-up test plan: https://github.com/ElectroIoT/Universal-USB-Flasher-V2

### Status
Design only: not built or tested yet. This page will get photos and test results after the first boards.
