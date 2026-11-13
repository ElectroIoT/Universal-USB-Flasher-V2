# PCBWay Shared Project post

**Title:** Universal USB Flasher V2.1 – ESP32 / ESP8266 / ESP-01 / Arduino / UPDI programmer (CH342F dual UART)

**Short description (≤ 200 characters):**
USB-C flasher for ESP32, ESP8266, ESP-01, Arduino and UPDI AVR. Dual UART, ESP-Prog port, 3.3/5 V logic, auto-program and current-limited target power.

**Category:** Tools / Programmer (or Development Board if Tools is not offered)

**Tags:** esp32, esp8266, esp-01, usb-uart, ch342f, programmer, updi, arduino, esp-prog

**Licence:** CERN-OHL-P-2.0

**Cover image:** `images/pcb-3d.png`

## Board options to pick when you upload the Gerber

| Option | Value |
|---|---|
| Layers | 2 |
| Size | 80 × 40 mm |
| Thickness | 1.6 mm |
| Material | FR-4 |
| Min track / spacing | 6 mil / 6 mil (design: 10 mil signals, 0.152 mm clearance) |
| Min hole | 0.3 mm |
| Solder mask | Blue (as in the renders; any colour works) |
| Silkscreen | White |
| Surface finish | HASL lead-free; ENIG is better for the 0.5 mm-pitch QFN (U2) |
| Copper | 1 oz |
| Castellated holes / gold fingers | No |

## Description (paste)

> **Status:** design finished (DRC 0 errors) but **not built or tested yet**. Photos and test results will follow after the first boards.

Universal USB Flasher V2.1 is a USB-C programmer and serial adapter that flashes ESP32 (all variants), ESP8266 / ESP-12F, plug-in ESP-01 modules, Arduino / ATmega boards and UPDI AVR chips (ATtiny 0/1/2-series, AVR-DA/DB/DD) from one board.

**Main parts:** WCH CH342F dual USB-UART (two COM ports), SGM2212 3.3 V LDO, two TPS2553 current-limited power switches, USBLC6 ESD arrays, MMBT3904 auto-program transistors.

**Features**
- Two UARTs: flash a target on UART1 (H1 / J3 / J4 / J2) and watch a second device on UART2 (J5)
- 3.3 V / 5 V logic switch with a 5V IO warning LED
- Automatic EN / IO0 control for esptool, Arduino IDE and PlatformIO (remove the SJ1 / SJ2 caps to turn it off)
- ESP-Prog compatible 2×3 header at 1.27 mm (J3) and 2.54 mm (J4)
- ESP-01 socket with the pull-ups on the board
- UPDI mode switch for SerialUPDI programming
- Target power limited to about 0.6 A (3.3 V) and 0.5 A (5 V), POWER button and OVERLOAD LED
- ESD protection on USB and on every header signal, PTC fuse
- Pin names on the top silkscreen, full pinout on the bottom

**Pinout**
- H1: 1 3V3 · 2 5V · 3 GND · 4 TX · 5 RX/UPDI · 6 DTR · 7 RTS · 8 RST · 9 EN · 10 IO0 · 11 IO15 (TX/RX named from the flasher side)
- J3 / J4 (ESP-Prog): 1 EN · 2 VDD · 3 TXD · 4 GND · 5 RXD · 6 IO0
- J2 ESP-01: 1 GND · 2 TX · 3 IO2 · 4 EN · 5 IO0 · 6 RST · 7 RX · 8 3V3
- J5 UART2: 1 GND · 2 TX2 · 3 RX2 · 4 DTR2

**Assembly:** 66 parts, all with LCSC numbers (BOM and pick-and-place attached). U2 is a 0.5 mm-pitch QFN-24 (hot air or SMT service); the rest is 0805, SOT-23, SOT-23-6, SOD-123, SOT-223 and through-hole headers.

**Source and docs:** https://github.com/ElectroIoT/Universal-USB-Flasher-V2

## Attach

- Gerber zip, BOM CSV, pick-and-place CSV, schematic PDF (see [README.md](README.md) for how to export them)
- Cover: `images/pcb-3d.png`; gallery: `pcb-3d-top.png`, `pcb-3d-bottom.png`, `pcb-2d-top.png`, `pcb-2d-bottom.png`
