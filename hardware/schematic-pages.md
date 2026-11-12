# EasyEDA schematic: page-by-page connection list

Generated from `tools/design.json` (V2.1 (design)). 66 parts · 219 pins · 43 nets.

For every part: place the symbol (by LCSC number), then wire each pin to the net shown. Pins marked **NC** get an EasyEDA **No-Connect flag**. GND, +3V3 and +5V use global power symbols. Every other net that appears on more than one page needs a net label with exactly the same name.

> Check before you trust a pin number: D1 and LED1–LED6 (which symbol pin is K), Q1/Q2/Q3 (SOT-23: 1=B, 2=E, 3=C), U2 (QFN-24 pin 0 = exposed pad), J2 (odd pins top row assumed). R/C/PTC pins are interchangeable.

An interactive version with tick boxes is in [docs/index.html](../docs/index.html#sch-check).

## Page 1 · USB + Power

_USB-C, ESD, fuse, LDO, IO switch, 5V-IO LED_

**Net labels on this page:** `USB_DM`, `USB_DP`, `VBUS_F`, `VIO`  
**No-Connect flags:** `USB1.3 (SBU2)`, `USB1.9 (SBU1)`

### USB1: USB-C 16P

Footprint `USB-C-SMD_TYPE-C-16PIN-2MD(073)` · LCSC C2765186

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | GND | `GND` | power symbol (40 pins) |
| ☐ | 2 | VBUS | `VBUS` | USB1.11, U3.5, F1.1 |
| ☐ | 3 | SBU2 | `NC` | **No-Connect flag** |
| ☐ | 4 | CC1 | `CC1` | R1.1 |
| ☐ | 5 | DN2 | `USB_DM` | USB1.7, U3.3, U3.4, U2.4 (P3) |
| ☐ | 6 | DP1 | `USB_DP` | USB1.8, U3.1, U3.6, U2.3 (P3) |
| ☐ | 7 | DN1 | `USB_DM` | USB1.5, U3.3, U3.4, U2.4 (P3) |
| ☐ | 8 | DP2 | `USB_DP` | USB1.6, U3.1, U3.6, U2.3 (P3) |
| ☐ | 9 | SBU1 | `NC` | **No-Connect flag** |
| ☐ | 10 | CC2 | `CC2` | R2.1 |
| ☐ | 11 | VBUS | `VBUS` | USB1.2, U3.5, F1.1 |
| ☐ | 12 | GND | `GND` | power symbol (40 pins) |
| ☐ | 13 | SHELL | `GND` | power symbol (40 pins) |
| ☐ | 14 | SHELL | `GND` | power symbol (40 pins) |

### R1: 5.1k

Footprint `R0805` · LCSC C27834

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `CC1` | USB1.4 |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### R2: 5.1k

Footprint `R0805` · LCSC C27834

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `CC2` | USB1.10 |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### U3: USBLC6-2SC6

Footprint `SOT-23-6` · LCSC C7519

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | I/O1 | `USB_DP` | USB1.6, USB1.8, U3.6, U2.3 (P3) |
| ☐ | 2 | GND | `GND` | power symbol (40 pins) |
| ☐ | 3 | I/O2 | `USB_DM` | USB1.5, USB1.7, U3.4, U2.4 (P3) |
| ☐ | 4 | I/O2 | `USB_DM` | USB1.5, USB1.7, U3.3, U2.4 (P3) |
| ☐ | 5 | VBUS | `VBUS` | USB1.2, USB1.11, F1.1 |
| ☐ | 6 | I/O1 | `USB_DP` | USB1.6, USB1.8, U3.1, U2.3 (P3) |

### F1: PTC 500 mA

Footprint `F1206` · LCSC C2680506

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VBUS` | USB1.2, USB1.11, U3.5 |
| ☐ | 2 | 2 | `VBUS_F` | C1.1, D1.2, U2.7 (P3), U2.8 (P3), C2.1 (P3) |

### C1: 10 µF

Footprint `C0805` · LCSC C15850

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VBUS_F` | F1.2, D1.2, U2.7 (P3), U2.8 (P3), C2.1 (P3) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### D1: 1N5819HW

Footprint `SOD-123` · LCSC C82544

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | K (band) | `+5V` | power symbol (9 pins) |
| ☐ | 2 | A | `VBUS_F` | F1.2, C1.1, U2.7 (P3), U2.8 (P3), C2.1 (P3) |

### C5: 10 µF

Footprint `C0805` · LCSC C15850

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+5V` | power symbol (9 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### U1: SGM2212-3.3

Footprint `SOT-223-3` · LCSC C3294699

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | GND | `GND` | power symbol (40 pins) |
| ☐ | 2 | VOUT | `+3V3` | power symbol (9 pins) |
| ☐ | 3 | VIN | `+5V` | power symbol (9 pins) |
| ☐ | 4 | VOUT (tab) | `+3V3` | power symbol (9 pins) |

### C6: 22 µF

Footprint `C0805` · LCSC C45783

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (9 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### C7: 100 nF

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (9 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### SW3: MSK12C02 (IO 3V3|5V)

Footprint `SW-SMD_MSK12C02` · LCSC C431540

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | throw A | `+3V3` | power symbol (9 pins) |
| ☐ | 2 | common | `VIO` | Q3.2, U2.5 (P3), C4.1 (P3), R4.1 (P3), R5.1 (P3), R6.1 (P3), R14.1 (P4) |
| ☐ | 3 | throw B | `+5V` | power symbol (9 pins) |

### Q3: MMBT3906 (5V-IO detect)

Footprint `SOT-23-3` · LCSC C53444

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | B | `Q3_B` | R16.2 |
| ☐ | 2 | E | `VIO` | SW3.2, U2.5 (P3), C4.1 (P3), R4.1 (P3), R5.1 (P3), R6.1 (P3), R14.1 (P4) |
| ☐ | 3 | C | `Q3_C` | R17.1 |

### R16: 4.7k (Q3 base)

Footprint `R0805` · LCSC C17673

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (9 pins) |
| ☐ | 2 | 2 | `Q3_B` | Q3.1 |

### R17: 1k (5V-IO LED)

Footprint `R0805` · LCSC C95781

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `Q3_C` | Q3.3 |
| ☐ | 2 | 2 | `LED5_A` | LED5.2 |

### LED5: Red (5V IO warning)

Footprint `LED0805` · LCSC C84256

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED5_A` | R17.2 |
| ☐ | 1 | K | `GND` | power symbol (40 pins) |

## Page 2 · Target power

_TPS2553 switches, power-cycle button, PWR + OVERLOAD LEDs_

**Net labels on this page:** `+3V3_T`, `+5V_T`  
**No-Connect flags:** none

### U4: TPS2553 (3V3 target switch)

Footprint `SOT-23-6` · LCSC C55266

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | IN | `+3V3` | power symbol (9 pins) |
| ☐ | 2 | GND | `GND` | power symbol (40 pins) |
| ☐ | 3 | EN | `TPWR_EN` | U5.3, R20.2, SW5.1 |
| ☐ | 4 | FAULT# | `FAULT_N` | U5.4, LED6.1 |
| ☐ | 5 | ILIM | `ILIM3` | R18.1 |
| ☐ | 6 | OUT | `+3V3_T` | C12.1, R3.1, R9.1 (P4), R10.1 (P4), H1.1 (P5), J2.8 (P5), C8.1 (P5), R12.1 (P5), R13.1 (P5), J3.2 (P5), J4.2 (P5) |

### R18: 43k 1% (≈0.61 A limit)

Footprint `R0805` · LCSC C17695

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `ILIM3` | U4.5 |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### C11: 100 nF (U4 IN)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (9 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### C12: 10 µF (+3V3_T)

Footprint `C0805` · LCSC C15850

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3_T` | U4.6, R3.1, R9.1 (P4), R10.1 (P4), H1.1 (P5), J2.8 (P5), C8.1 (P5), R12.1 (P5), R13.1 (P5), J3.2 (P5), J4.2 (P5) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### U5: TPS2553 (5V target switch)

Footprint `SOT-23-6` · LCSC C55266

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | IN | `+5V` | power symbol (9 pins) |
| ☐ | 2 | GND | `GND` | power symbol (40 pins) |
| ☐ | 3 | EN | `TPWR_EN` | U4.3, R20.2, SW5.1 |
| ☐ | 4 | FAULT# | `FAULT_N` | U4.4, LED6.1 |
| ☐ | 5 | ILIM | `ILIM5` | R19.1 |
| ☐ | 6 | OUT | `+5V_T` | C14.1, H1.2 (P5) |

### R19: 51k 1% (≈0.51 A limit)

Footprint `R0805` · LCSC C17737

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `ILIM5` | U5.5 |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### C13: 100 nF (U5 IN)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+5V` | power symbol (9 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### C14: 10 µF (+5V_T)

Footprint `C0805` · LCSC C15850

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+5V_T` | U5.6, H1.2 (P5) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### R20: 100k (EN pull-up)

Footprint `R0805` · LCSC C96346

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (9 pins) |
| ☐ | 2 | 2 | `TPWR_EN` | U4.3, U5.3, SW5.1 |

### SW5: POWER-CYCLE (hold = off)

Footprint `SW-SMD_L3.9-W3.0-P4.45` · LCSC C720477

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `TPWR_EN` | U4.3, U5.3, R20.2 |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### R21: 1k (OVERLOAD LED)

Footprint `R0805` · LCSC C95781

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+5V` | power symbol (9 pins) |
| ☐ | 2 | 2 | `LED6_A` | LED6.2 |

### LED6: Red (OVERLOAD)

Footprint `LED0805` · LCSC C84256

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED6_A` | R21.2 |
| ☐ | 1 | K | `FAULT_N` | U4.4, U5.4 |

### R3: 1k (PWR LED)

Footprint `R0805` · LCSC C95781

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3_T` | U4.6, C12.1, R9.1 (P4), R10.1 (P4), H1.1 (P5), J2.8 (P5), C8.1 (P5), R12.1 (P5), R13.1 (P5), J3.2 (P5), J4.2 (P5) |
| ☐ | 2 | 2 | `LED1_A` | LED1.2 |

### LED1: Green (target PWR)

Footprint `LED0805` · LCSC C84260

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED1_A` | R3.2 |
| ☐ | 1 | K | `GND` | power symbol (40 pins) |

## Page 3 · USB dual UART

_CH342F, decoupling, TX/RX/RX2 LEDs_

**Net labels on this page:** `DTR2_N`, `DTR_N`, `RTS_N`, `RX2`, `RXD`, `TX2`, `TXD`, `USB_DM`, `USB_DP`, `VBUS_F`, `VIO`  
**No-Connect flags:** `U2.1 (RI0#)`, `U2.9 (RST#)`, `U2.10 (CTS1#)`, `U2.11 (RTS1#)`, `U2.14 (DSR1#)`, `U2.16 (DCD1#)`, `U2.17 (RI1#)`, `U2.18 (CTS0#)`, `U2.22 (DSR0#)`, `U2.24 (DCD0#)`

### U2: CH342F dual UART

Footprint `QFN-24_L4.0-W4.0-P0.50` · LCSC C2841530

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 0 | EP (GND) | `GND` | power symbol (40 pins) |
| ☐ | 1 | RI0# | `NC` | **No-Connect flag** |
| ☐ | 2 | GND | `GND` | power symbol (40 pins) |
| ☐ | 3 | UD+ | `USB_DP` | USB1.6 (P1), USB1.8 (P1), U3.1 (P1), U3.6 (P1) |
| ☐ | 4 | UD- | `USB_DM` | USB1.5 (P1), USB1.7 (P1), U3.3 (P1), U3.4 (P1) |
| ☐ | 5 | VIO | `VIO` | SW3.2 (P1), Q3.2 (P1), C4.1, R4.1, R5.1, R6.1, R14.1 (P4) |
| ☐ | 6 | V3 | `V3` | C3.1 |
| ☐ | 7 | VDD5 | `VBUS_F` | F1.2 (P1), C1.1 (P1), D1.2 (P1), U2.8, C2.1 |
| ☐ | 8 | VBUS | `VBUS_F` | F1.2 (P1), C1.1 (P1), D1.2 (P1), U2.7, C2.1 |
| ☐ | 9 | RST# | `NC` | **No-Connect flag** |
| ☐ | 10 | CTS1# | `NC` | **No-Connect flag** |
| ☐ | 11 | RTS1# | `NC` | **No-Connect flag** |
| ☐ | 12 | RXD1 | `RX2` | LED4.1, J5.3 (P5), U7.6 (P5) |
| ☐ | 13 | TXD1 | `TX2` | J5.2 (P5), U7.4 (P5) |
| ☐ | 14 | DSR1# | `NC` | **No-Connect flag** |
| ☐ | 15 | DTR1# | `DTR2_N` | J5.4 (P5) |
| ☐ | 16 | DCD1# | `NC` | **No-Connect flag** |
| ☐ | 17 | RI1# | `NC` | **No-Connect flag** |
| ☐ | 18 | CTS0# | `NC` | **No-Connect flag** |
| ☐ | 19 | RTS0# | `RTS_N` | SJ2.1 (P4), H1.7 (P5), U6.6 (P5) |
| ☐ | 20 | RXD0 | `RXD` | LED3.1, R15.2 (P4), H1.5 (P5), J2.2 (P5), J3.3 (P5), J4.3 (P5), U6.3 (P5) |
| ☐ | 21 | TXD0 | `TXD` | LED2.1, SW4.1 (P4), H1.4 (P5), J2.7 (P5), J3.5 (P5), J4.5 (P5), U6.1 (P5) |
| ☐ | 22 | DSR0# | `NC` | **No-Connect flag** |
| ☐ | 23 | DTR0# | `DTR_N` | SJ1.1 (P4), C10.1 (P4), H1.6 (P5), U6.4 (P5) |
| ☐ | 24 | DCD0# | `NC` | **No-Connect flag** |

### C2: 100 nF (VDD5)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VBUS_F` | F1.2 (P1), C1.1 (P1), D1.2 (P1), U2.7, U2.8 |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### C3: 100 nF (V3)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `V3` | U2.6 |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### C4: 100 nF (VIO)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2 (P1), Q3.2 (P1), U2.5, R4.1, R5.1, R6.1, R14.1 (P4) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### R4: 2.2k

Footprint `R0805` · LCSC C17520

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2 (P1), Q3.2 (P1), U2.5, C4.1, R5.1, R6.1, R14.1 (P4) |
| ☐ | 2 | 2 | `LED2_A` | LED2.2 |

### LED2: Orange (TX)

Footprint `LED0805` · LCSC C84262

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED2_A` | R4.2 |
| ☐ | 1 | K | `TXD` | U2.21, SW4.1 (P4), H1.4 (P5), J2.7 (P5), J3.5 (P5), J4.5 (P5), U6.1 (P5) |

### R5: 2.2k

Footprint `R0805` · LCSC C17520

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2 (P1), Q3.2 (P1), U2.5, C4.1, R4.1, R6.1, R14.1 (P4) |
| ☐ | 2 | 2 | `LED3_A` | LED3.2 |

### LED3: Yellow (RX)

Footprint `LED0805` · LCSC C965814

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED3_A` | R5.2 |
| ☐ | 1 | K | `RXD` | U2.20, R15.2 (P4), H1.5 (P5), J2.2 (P5), J3.3 (P5), J4.3 (P5), U6.3 (P5) |

### R6: 2.2k

Footprint `R0805` · LCSC C17520

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2 (P1), Q3.2 (P1), U2.5, C4.1, R4.1, R5.1, R14.1 (P4) |
| ☐ | 2 | 2 | `LED4_A` | LED4.2 |

### LED4: Blue (UART2 RX)

Footprint `LED0805` · LCSC C965817

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED4_A` | R6.2 |
| ☐ | 1 | K | `RX2` | U2.12, J5.3 (P5), U7.6 (P5) |

## Page 4 · Auto-program + control

_Q1/Q2, SJ1/SJ2, pull-ups, buttons, UPDI, Arduino RST_

**Net labels on this page:** `+3V3_T`, `DTR_N`, `EN`, `IO0`, `IO15`, `RST`, `RTS_N`, `RXD`, `TXD`, `VIO`  
**No-Connect flags:** `SW4.3 (throw B (UART))`

### SJ1: Solder jumper (bridged)

Footprint `SolderJumper-2_Bridged` · LCSC -

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `DTR_N` | U2.23 (P3), C10.1, H1.6 (P5), U6.4 (P5) |
| ☐ | 2 | 2 | `DTR_AP` | R7.1, Q2.2 |

### SJ2: Solder jumper (bridged)

Footprint `SolderJumper-2_Bridged` · LCSC -

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `RTS_N` | U2.19 (P3), H1.7 (P5), U6.6 (P5) |
| ☐ | 2 | 2 | `RTS_AP` | R8.1, Q1.2 |

### R7: 10k

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `DTR_AP` | SJ1.2, Q2.2 |
| ☐ | 2 | 2 | `Q1_B` | Q1.1 |

### R8: 10k

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `RTS_AP` | SJ2.2, Q1.2 |
| ☐ | 2 | 2 | `Q2_B` | Q2.1 |

### Q1: MMBT3904 (EN)

Footprint `SOT-23-3` · LCSC C81464

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | B | `Q1_B` | R7.2 |
| ☐ | 2 | E | `RTS_AP` | SJ2.2, R8.1 |
| ☐ | 3 | C | `EN` | R9.2, C9.1, SW1.1, H1.9 (P5), J2.4 (P5), J3.1 (P5), J4.1 (P5), U7.1 (P5) |

### Q2: MMBT3904 (IO0)

Footprint `SOT-23-3` · LCSC C81464

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | B | `Q2_B` | R8.2 |
| ☐ | 2 | E | `DTR_AP` | SJ1.2, R7.1 |
| ☐ | 3 | C | `IO0` | R10.2, SW2.1, H1.10 (P5), J2.5 (P5), J3.6 (P5), J4.6 (P5), U7.3 (P5) |

### R9: 10k (EN pull-up)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R10.1, H1.1 (P5), J2.8 (P5), C8.1 (P5), R12.1 (P5), R13.1 (P5), J3.2 (P5), J4.2 (P5) |
| ☐ | 2 | 2 | `EN` | Q1.3, C9.1, SW1.1, H1.9 (P5), J2.4 (P5), J3.1 (P5), J4.1 (P5), U7.1 (P5) |

### C9: 100 nF (EN)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `EN` | Q1.3, R9.2, SW1.1, H1.9 (P5), J2.4 (P5), J3.1 (P5), J4.1 (P5), U7.1 (P5) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### R10: 10k (IO0 pull-up)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R9.1, H1.1 (P5), J2.8 (P5), C8.1 (P5), R12.1 (P5), R13.1 (P5), J3.2 (P5), J4.2 (P5) |
| ☐ | 2 | 2 | `IO0` | Q2.3, SW2.1, H1.10 (P5), J2.5 (P5), J3.6 (P5), J4.6 (P5), U7.3 (P5) |

### R11: 10k (IO15 pull-down)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `IO15` | H1.11 (P5) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### SW1: RESET

Footprint `SW-SMD_L3.9-W3.0-P4.45` · LCSC C720477

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `EN` | Q1.3, R9.2, C9.1, H1.9 (P5), J2.4 (P5), J3.1 (P5), J4.1 (P5), U7.1 (P5) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### SW2: BOOT

Footprint `SW-SMD_L3.9-W3.0-P4.45` · LCSC C720477

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `IO0` | Q2.3, R10.2, H1.10 (P5), J2.5 (P5), J3.6 (P5), J4.6 (P5), U7.3 (P5) |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### C10: 100 nF (Arduino reset)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `DTR_N` | U2.23 (P3), SJ1.1, H1.6 (P5), U6.4 (P5) |
| ☐ | 2 | 2 | `RST` | R14.2, H1.8 (P5) |

### R14: 10k (RST pull-up)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2 (P1), Q3.2 (P1), U2.5 (P3), C4.1 (P3), R4.1 (P3), R5.1 (P3), R6.1 (P3) |
| ☐ | 2 | 2 | `RST` | C10.2, H1.8 (P5) |

### SW4: MSK12C02 (UART|UPDI)

Footprint `SW-SMD_MSK12C02` · LCSC C431540

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | throw A (UPDI) | `TXD` | U2.21 (P3), LED2.1 (P3), H1.4 (P5), J2.7 (P5), J3.5 (P5), J4.5 (P5), U6.1 (P5) |
| ☐ | 2 | common | `UPDI_R` | R15.1 |
| ☐ | 3 | throw B (UART) | `NC` | **No-Connect flag** |

### R15: 4.7k (UPDI)

Footprint `R0805` · LCSC C17673

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `UPDI_R` | SW4.2 |
| ☐ | 2 | 2 | `RXD` | U2.20 (P3), LED3.1 (P3), H1.5 (P5), J2.2 (P5), J3.3 (P5), J4.3 (P5), U6.3 (P5) |

## Page 5 · Connectors + ESD

_H1, ESP-01, ESP-Prog 1.27/2.54, UART2, header ESD_

**Net labels on this page:** `+3V3_T`, `+5V_T`, `DTR2_N`, `DTR_N`, `EN`, `IO0`, `IO15`, `RST`, `RTS_N`, `RX2`, `RXD`, `TX2`, `TXD`  
**No-Connect flags:** none

### H1: 1x11 male header

Footprint `HDR-TH_11P-P2.54-V-M` · LCSC C2840011

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 3V3 | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R9.1 (P4), R10.1 (P4), J2.8, C8.1, R12.1, R13.1, J3.2, J4.2 |
| ☐ | 2 | 5V | `+5V_T` | U5.6 (P2), C14.1 (P2) |
| ☐ | 3 | GND | `GND` | power symbol (40 pins) |
| ☐ | 4 | TX | `TXD` | U2.21 (P3), LED2.1 (P3), SW4.1 (P4), J2.7, J3.5, J4.5, U6.1 |
| ☐ | 5 | RX/UPDI | `RXD` | U2.20 (P3), LED3.1 (P3), R15.2 (P4), J2.2, J3.3, J4.3, U6.3 |
| ☐ | 6 | DTR | `DTR_N` | U2.23 (P3), SJ1.1 (P4), C10.1 (P4), U6.4 |
| ☐ | 7 | RTS | `RTS_N` | U2.19 (P3), SJ2.1 (P4), U6.6 |
| ☐ | 8 | RST | `RST` | C10.2 (P4), R14.2 (P4) |
| ☐ | 9 | EN | `EN` | Q1.3 (P4), R9.2 (P4), C9.1 (P4), SW1.1 (P4), J2.4, J3.1, J4.1, U7.1 |
| ☐ | 10 | IO0 | `IO0` | Q2.3 (P4), R10.2 (P4), SW2.1 (P4), J2.5, J3.6, J4.6, U7.3 |
| ☐ | 11 | IO15 | `IO15` | R11.1 (P4) |

### J2: 2x4 female (ESP-01)

Footprint `HDR-TH_8P-P2.54-V-F-R2-C4` · LCSC C2897405

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | GND | `GND` | power symbol (40 pins) |
| ☐ | 2 | TXD (ESP out) | `RXD` | U2.20 (P3), LED3.1 (P3), R15.2 (P4), H1.5, J3.3, J4.3, U6.3 |
| ☐ | 3 | GPIO2 | `ESP01_IO2` | R13.2 |
| ☐ | 4 | CH_PD | `EN` | Q1.3 (P4), R9.2 (P4), C9.1 (P4), SW1.1 (P4), H1.9, J3.1, J4.1, U7.1 |
| ☐ | 5 | GPIO0 | `IO0` | Q2.3 (P4), R10.2 (P4), SW2.1 (P4), H1.10, J3.6, J4.6, U7.3 |
| ☐ | 6 | RST | `ESP01_RST` | R12.2 |
| ☐ | 7 | RXD (ESP in) | `TXD` | U2.21 (P3), LED2.1 (P3), SW4.1 (P4), H1.4, J3.5, J4.5, U6.1 |
| ☐ | 8 | VCC | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R9.1 (P4), R10.1 (P4), H1.1, C8.1, R12.1, R13.1, J3.2, J4.2 |

### C8: 22 µF (ESP-01 bulk)

Footprint `C0805` · LCSC C45783

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R9.1 (P4), R10.1 (P4), H1.1, J2.8, R12.1, R13.1, J3.2, J4.2 |
| ☐ | 2 | 2 | `GND` | power symbol (40 pins) |

### R12: 10k (ESP-01 RST)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R9.1 (P4), R10.1 (P4), H1.1, J2.8, C8.1, R13.1, J3.2, J4.2 |
| ☐ | 2 | 2 | `ESP01_RST` | J2.6 |

### R13: 10k (ESP-01 GPIO2)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R9.1 (P4), R10.1 (P4), H1.1, J2.8, C8.1, R12.1, J3.2, J4.2 |
| ☐ | 2 | 2 | `ESP01_IO2` | J2.3 |

### J3: ESP-Prog PROG 2x3 1.27 mm box header

Footprint `IDC-TH_6P-P1.27-2x3` · LCSC C42372545

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | ESP_EN | `EN` | Q1.3 (P4), R9.2 (P4), C9.1 (P4), SW1.1 (P4), H1.9, J2.4, J4.1, U7.1 |
| ☐ | 2 | VDD | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R9.1 (P4), R10.1 (P4), H1.1, J2.8, C8.1, R12.1, R13.1, J4.2 |
| ☐ | 3 | ESP_TXD | `RXD` | U2.20 (P3), LED3.1 (P3), R15.2 (P4), H1.5, J2.2, J4.3, U6.3 |
| ☐ | 4 | GND | `GND` | power symbol (40 pins) |
| ☐ | 5 | ESP_RXD | `TXD` | U2.21 (P3), LED2.1 (P3), SW4.1 (P4), H1.4, J2.7, J4.5, U6.1 |
| ☐ | 6 | ESP_IO0 | `IO0` | Q2.3 (P4), R10.2 (P4), SW2.1 (P4), H1.10, J2.5, J4.6, U7.3 |

### J4: PROG 2x3 2.54 mm (pogo / 2.54 cable)

Footprint `HDR-TH_6P-P2.54-V-M-R2-C3` · LCSC C56153599

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | ESP_EN | `EN` | Q1.3 (P4), R9.2 (P4), C9.1 (P4), SW1.1 (P4), H1.9, J2.4, J3.1, U7.1 |
| ☐ | 2 | VDD | `+3V3_T` | U4.6 (P2), C12.1 (P2), R3.1 (P2), R9.1 (P4), R10.1 (P4), H1.1, J2.8, C8.1, R12.1, R13.1, J3.2 |
| ☐ | 3 | ESP_TXD | `RXD` | U2.20 (P3), LED3.1 (P3), R15.2 (P4), H1.5, J2.2, J3.3, U6.3 |
| ☐ | 4 | GND | `GND` | power symbol (40 pins) |
| ☐ | 5 | ESP_RXD | `TXD` | U2.21 (P3), LED2.1 (P3), SW4.1 (P4), H1.4, J2.7, J3.5, U6.1 |
| ☐ | 6 | ESP_IO0 | `IO0` | Q2.3 (P4), R10.2 (P4), SW2.1 (P4), H1.10, J2.5, J3.6, U7.3 |

### J5: UART2 1x4 header

Footprint `HDR-TH_4P-P2.54-V-M` · LCSC C2691448

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | GND | `GND` | power symbol (40 pins) |
| ☐ | 2 | TX2 | `TX2` | U2.13 (P3), U7.4 |
| ☐ | 3 | RX2 | `RX2` | U2.12 (P3), LED4.1 (P3), U7.6 |
| ☐ | 4 | DTR2 | `DTR2_N` | U2.15 (P3) |

### U6: USBLC6-4SC6 (header ESD A)

Footprint `SOT-23-6` · LCSC C111212

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | I/O1 | `TXD` | U2.21 (P3), LED2.1 (P3), SW4.1 (P4), H1.4, J2.7, J3.5, J4.5 |
| ☐ | 2 | GND | `GND` | power symbol (40 pins) |
| ☐ | 3 | I/O2 | `RXD` | U2.20 (P3), LED3.1 (P3), R15.2 (P4), H1.5, J2.2, J3.3, J4.3 |
| ☐ | 4 | I/O3 | `DTR_N` | U2.23 (P3), SJ1.1 (P4), C10.1 (P4), H1.6 |
| ☐ | 5 | VBUS | `+5V` | power symbol (9 pins) |
| ☐ | 6 | I/O4 | `RTS_N` | U2.19 (P3), SJ2.1 (P4), H1.7 |

### U7: USBLC6-4SC6 (header ESD B)

Footprint `SOT-23-6` · LCSC C111212

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | I/O1 | `EN` | Q1.3 (P4), R9.2 (P4), C9.1 (P4), SW1.1 (P4), H1.9, J2.4, J3.1, J4.1 |
| ☐ | 2 | GND | `GND` | power symbol (40 pins) |
| ☐ | 3 | I/O2 | `IO0` | Q2.3 (P4), R10.2 (P4), SW2.1 (P4), H1.10, J2.5, J3.6, J4.6 |
| ☐ | 4 | I/O3 | `TX2` | U2.13 (P3), J5.2 |
| ☐ | 5 | VBUS | `+5V` | power symbol (9 pins) |
| ☐ | 6 | I/O4 | `RX2` | U2.12 (P3), LED4.1 (P3), J5.3 |
