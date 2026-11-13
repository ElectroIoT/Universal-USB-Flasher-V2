# Universal USB Flasher V2.1 - pinout and PCB notes

Board 80 x 40 mm, 2 layers, 1 oz. All of this is also printed on the PCB silkscreen
(short labels next to the pins on top, full table on the bottom).

## H1 - main header 1x11, 2.54 mm (right edge, pin 1 at top)

| Pin | Label | Net | Notes |
|---|---|---|---|
| 1 | 3V3 | +3V3_T | switched 3.3 V, 0.6 A limit (U4) |
| 2 | 5V | +5V_T | switched 5 V, 0.5 A limit (U5) |
| 3 | GND | GND | |
| 4 | TX | TXD | flasher TX out -> target RX |
| 5 | RX | RXD | flasher RX in <- target TX; also UPDI when SW4 = UPDI |
| 6 | DTR | DTR_N | |
| 7 | RTS | RTS_N | |
| 8 | RST | RST | Arduino auto-reset (100 nF from DTR, 10k pull-up to VIO) |
| 9 | EN | EN | ESP auto-program (Q1) |
| 10 | IO0 | IO0 | ESP auto-program (Q2) |
| 11 | IO15 | IO15 | 10k pull-down (ESP32 strap) |

## J3 (1.27 mm box) and J4 (2.54 mm) - ESP-Prog PROG header

Same pin order as Espressif ESP-Prog; names are target-side.

| Pin | Name | Pin | Name |
|---|---|---|---|
| 1 | EN | 2 | VDD (3V3) |
| 3 | TXD (target TX -> flasher RX) | 4 | GND |
| 5 | RXD (target RX <- flasher TX) | 6 | IO0 |

## J2 - ESP-01 socket 2x4 female

| Pin | ESP-01 | Pin | ESP-01 |
|---|---|---|---|
| 1 | GND | 2 | TX |
| 3 | GPIO2 (10k up) | 4 | EN / CH_PD |
| 5 | GPIO0 | 6 | RST (10k up) |
| 7 | RX | 8 | VCC 3V3 |

## J5 - UART2 1x4 (second CH342F channel)

| 1 GND | 2 TX2 | 3 RX2 | 4 DTR2 |
|---|---|---|---|

## Switches, jumpers, LEDs

| Part | Silk | Function |
|---|---|---|
| SW5 | POWER | hold = target power off (TPWR_EN low) |
| SW1 | RESET | EN to GND |
| SW2 | BOOT | IO0 to GND |
| SW3 | SW3 5V / 3V3 | target I/O voltage (VIO) |
| SW4 | SW4 UART / UPDI | UPDI joins TX to RX through 4.7k |
| SJ1 + SJ2 | AUTO-PROG (cap = ON) | fit both caps for ESP auto-program |
| LED1 | PWR | target 3V3 on |
| LED6 | OVLD | U4/U5 overload (FAULT) |
| LED2 / LED3 / LED4 | TX / RX / RX2 | activity |
| LED5 | 5V IO | warning: I/O is at 5 V |

## Routing (done 2026-11-13, EasyEDA autorouter + checks)

| Nets | Width |
|---|---|
| VBUS, +5V, +3V3, +3V3_T, +5V_T | 0.5 - 0.6 mm (rule "power") |
| VBUS_F | 0.5 mm (0.25 mm only at the U2 pins) |
| signals, VIO, GND | 0.254 mm |
| GND | plus copper pour on top and bottom |
| vias | 0.3 mm drill / 0.6 mm pad |

DRC: 0 errors (clearance 0.152 mm, all nets connected).
