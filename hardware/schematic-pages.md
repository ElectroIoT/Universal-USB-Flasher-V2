# EasyEDA schematic: page-by-page connection list

Draw the schematic as 4 pages. For every part: place the symbol (by LCSC number), then wire each pin to the net shown.
Pins marked **NC** get an EasyEDA **No-Connect flag**. GND, +3V3 and +5V use global power symbols; every other net that appears on more than one page needs a net label with exactly the same name.

> Check before you trust a pin number: D1 and LED1-LED4 (which symbol pin is K), Q1/Q2 (SOT-23: 1=B, 2=E, 3=C), J2 (odd pins top row assumed). R/C/PTC pins are interchangeable.

An interactive version with tick boxes is in [docs/index.html](../docs/index.html).

## Page 1 · USB + Power

_USB-C, ESD, fuse, LDO, IO switch, PWR LED_

**Net labels on this page:** `USB_DM`, `USB_DP`, `VBUS_F`, `VIO`  
**No-Connect flags:** `USB1.3 (SBU2)`, `USB1.9 (SBU1)`

### USB1: USB-C 16P

Footprint `USB-C-SMD_TYPE-C-16PIN-2MD(073)` · LCSC C2765186

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | GND | `GND` | power symbol (24 pins) |
| ☐ | 2 | VBUS | `VBUS` | USB1.11, U3.5, F1.1 |
| ☐ | 3 | SBU2 | `NC` | **No-Connect flag** |
| ☐ | 4 | CC1 | `CC1` | R1.1 |
| ☐ | 5 | DN2 | `USB_DM` | USB1.7, U3.3, U3.4, U2.6 |
| ☐ | 6 | DP1 | `USB_DP` | USB1.8, U3.1, U3.6, U2.5 |
| ☐ | 7 | DN1 | `USB_DM` | USB1.5, U3.3, U3.4, U2.6 |
| ☐ | 8 | DP2 | `USB_DP` | USB1.6, U3.1, U3.6, U2.5 |
| ☐ | 9 | SBU1 | `NC` | **No-Connect flag** |
| ☐ | 10 | CC2 | `CC2` | R2.1 |
| ☐ | 11 | VBUS | `VBUS` | USB1.2, U3.5, F1.1 |
| ☐ | 12 | GND | `GND` | power symbol (24 pins) |
| ☐ | 13 | SHELL | `GND` | power symbol (24 pins) |
| ☐ | 14 | SHELL | `GND` | power symbol (24 pins) |

### R1: 5.1k

Footprint `R0805` · LCSC C27834

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `CC1` | USB1.4 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### R2: 5.1k

Footprint `R0805` · LCSC C27834

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `CC2` | USB1.10 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### U3: USBLC6-2SC6

Footprint `SOT-23-6` · LCSC C7519

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | I/O1 | `USB_DP` | USB1.6, USB1.8, U3.6, U2.5 |
| ☐ | 2 | GND | `GND` | power symbol (24 pins) |
| ☐ | 3 | I/O2 | `USB_DM` | USB1.5, USB1.7, U3.4, U2.6 |
| ☐ | 4 | I/O2 | `USB_DM` | USB1.5, USB1.7, U3.3, U2.6 |
| ☐ | 5 | VBUS | `VBUS` | USB1.2, USB1.11, F1.1 |
| ☐ | 6 | I/O1 | `USB_DP` | USB1.6, USB1.8, U3.1, U2.5 |

### F1: PTC 500 mA

Footprint `F1206` · LCSC C2680506

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VBUS` | USB1.2, USB1.11, U3.5 |
| ☐ | 2 | 2 | `VBUS_F` | C1.1, D1.2, U2.7, U2.16, C2.1 |

### C1: 10 µF

Footprint `C0805` · LCSC C15850

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VBUS_F` | F1.2, D1.2, U2.7, U2.16, C2.1 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### D1: 1N5819HW

Footprint `SOD-123` · LCSC C82544

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | K (band) | `+5V` | power symbol (5 pins) |
| ☐ | 2 | A | `VBUS_F` | F1.2, C1.1, U2.7, U2.16, C2.1 |

### C5: 10 µF

Footprint `C0805` · LCSC C15850

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+5V` | power symbol (5 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### U1: SGM2212-3.3

Footprint `SOT-223-3` · LCSC C3294699

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | GND | `GND` | power symbol (24 pins) |
| ☐ | 2 | VOUT | `+3V3` | power symbol (13 pins) |
| ☐ | 3 | VIN | `+5V` | power symbol (5 pins) |
| ☐ | 4 | VOUT (tab) | `+3V3` | power symbol (13 pins) |

### C6: 22 µF

Footprint `C0805` · LCSC C45783

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### C7: 100 nF

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### SW3: MSK12C02 (IO 3V3|5V)

Footprint `SW-SMD_MSK12C02` · LCSC C431540

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | throw A | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | common | `VIO` | U2.15, C4.1, R4.1, R5.1, R6.1, R14.1 |
| ☐ | 3 | throw B | `+5V` | power symbol (5 pins) |

### R3: 1k

Footprint `R0805` · LCSC C95781

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 2 | `LED1_A` | LED1.2 |

### LED1: Red (PWR)

Footprint `LED0805` · LCSC C84256

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED1_A` | R3.2 |
| ☐ | 1 | K | `GND` | power symbol (24 pins) |

## Page 2 · USB-UART

_CH343G, decoupling, TX/RX/ACT LEDs_

**Net labels on this page:** `DTR_N`, `RTS_N`, `RXD`, `TXD`, `USB_DM`, `USB_DP`, `VBUS_F`, `VIO`  
**No-Connect flags:** `U2.9 (DCD#)`, `U2.12 (DSR#)`, `U2.13 (CTS#)`, `U2.14 (RI#)`

### U2: CH343G

Footprint `SOP-16` · LCSC C2844153

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | GND | `GND` | power symbol (24 pins) |
| ☐ | 2 | TXD | `TXD` | LED2.1, SW4.1, H1.4, J2.7 |
| ☐ | 3 | RXD | `RXD` | LED3.1, R15.2, H1.5, J2.2 |
| ☐ | 4 | V3 | `V3` | C3.1 |
| ☐ | 5 | UD+ | `USB_DP` | USB1.6, USB1.8, U3.1, U3.6 |
| ☐ | 6 | UD- | `USB_DM` | USB1.5, USB1.7, U3.3, U3.4 |
| ☐ | 7 | VBUS | `VBUS_F` | F1.2, C1.1, D1.2, U2.16, C2.1 |
| ☐ | 8 | ACT# | `ACT_N` | LED4.1 |
| ☐ | 9 | DCD# | `NC` | **No-Connect flag** |
| ☐ | 10 | TNOW/DTR# | `DTR_N` | SJ1.1, C10.1, H1.6 |
| ☐ | 11 | RTS# | `RTS_N` | SJ2.1, H1.7 |
| ☐ | 12 | DSR# | `NC` | **No-Connect flag** |
| ☐ | 13 | CTS# | `NC` | **No-Connect flag** |
| ☐ | 14 | RI# | `NC` | **No-Connect flag** |
| ☐ | 15 | VIO | `VIO` | SW3.2, C4.1, R4.1, R5.1, R6.1, R14.1 |
| ☐ | 16 | VDD5 | `VBUS_F` | F1.2, C1.1, D1.2, U2.7, C2.1 |

### C2: 100 nF (VDD5)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VBUS_F` | F1.2, C1.1, D1.2, U2.7, U2.16 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### C3: 100 nF (V3)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `V3` | U2.4 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### C4: 100 nF (VIO)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2, U2.15, R4.1, R5.1, R6.1, R14.1 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### R4: 2.2k

Footprint `R0805` · LCSC C17520

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2, U2.15, C4.1, R5.1, R6.1, R14.1 |
| ☐ | 2 | 2 | `LED2_A` | LED2.2 |

### LED2: Orange (TX)

Footprint `LED0805` · LCSC C84262

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED2_A` | R4.2 |
| ☐ | 1 | K | `TXD` | U2.2, SW4.1, H1.4, J2.7 |

### R5: 2.2k

Footprint `R0805` · LCSC C17520

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2, U2.15, C4.1, R4.1, R6.1, R14.1 |
| ☐ | 2 | 2 | `LED3_A` | LED3.2 |

### LED3: Yellow (RX)

Footprint `LED0805` · LCSC C965814

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED3_A` | R5.2 |
| ☐ | 1 | K | `RXD` | U2.3, R15.2, H1.5, J2.2 |

### R6: 2.2k

Footprint `R0805` · LCSC C17520

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2, U2.15, C4.1, R4.1, R5.1, R14.1 |
| ☐ | 2 | 2 | `LED4_A` | LED4.2 |

### LED4: Green (ACT)

Footprint `LED0805` · LCSC C84260

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 2 | A | `LED4_A` | R6.2 |
| ☐ | 1 | K | `ACT_N` | U2.8 |

## Page 3 · Auto-program + control

_Q1/Q2, SJ1/SJ2, pull-ups, buttons, UPDI, Arduino RST_

**Net labels on this page:** `DTR_N`, `EN`, `IO0`, `IO15`, `RST`, `RTS_N`, `RXD`, `TXD`, `VIO`  
**No-Connect flags:** `SW4.3 (throw B (UART))`

### SJ1: Solder jumper (bridged)

Footprint `SolderJumper-2_Bridged` · LCSC -

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `DTR_N` | U2.10, C10.1, H1.6 |
| ☐ | 2 | 2 | `DTR_AP` | R7.1, Q2.2 |

### SJ2: Solder jumper (bridged)

Footprint `SolderJumper-2_Bridged` · LCSC -

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `RTS_N` | U2.11, H1.7 |
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
| ☐ | 3 | C | `EN` | R9.2, C9.1, SW1.1, H1.9, J2.4 |

### Q2: MMBT3904 (IO0)

Footprint `SOT-23-3` · LCSC C81464

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | B | `Q2_B` | R8.2 |
| ☐ | 2 | E | `DTR_AP` | SJ1.2, R7.1 |
| ☐ | 3 | C | `IO0` | R10.2, SW2.1, H1.10, J2.5 |

### R9: 10k (EN pull-up)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 2 | `EN` | Q1.3, C9.1, SW1.1, H1.9, J2.4 |

### C9: 100 nF (EN)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `EN` | Q1.3, R9.2, SW1.1, H1.9, J2.4 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### R10: 10k (IO0 pull-up)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 2 | `IO0` | Q2.3, SW2.1, H1.10, J2.5 |

### R11: 10k (IO15 pull-down)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `IO15` | H1.11 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### SW1: RESET

Footprint `SW-SMD_L3.9-W3.0-P4.45` · LCSC C720477

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `EN` | Q1.3, R9.2, C9.1, H1.9, J2.4 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### SW2: BOOT

Footprint `SW-SMD_L3.9-W3.0-P4.45` · LCSC C720477

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `IO0` | Q2.3, R10.2, H1.10, J2.5 |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### C10: 100 nF (Arduino reset)

Footprint `C0805` · LCSC C49678

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `DTR_N` | U2.10, SJ1.1, H1.6 |
| ☐ | 2 | 2 | `RST` | R14.2, H1.8 |

### R14: 10k (RST pull-up)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `VIO` | SW3.2, U2.15, C4.1, R4.1, R5.1, R6.1 |
| ☐ | 2 | 2 | `RST` | C10.2, H1.8 |

### SW4: MSK12C02 (UART|UPDI)

Footprint `SW-SMD_MSK12C02` · LCSC C431540

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | throw A (UPDI) | `TXD` | U2.2, LED2.1, H1.4, J2.7 |
| ☐ | 2 | common | `UPDI_R` | R15.1 |
| ☐ | 3 | throw B (UART) | `NC` | **No-Connect flag** |

### R15: 4.7k (UPDI)

Footprint `R0805` · LCSC C17673

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `UPDI_R` | SW4.2 |
| ☐ | 2 | 2 | `RXD` | U2.3, LED3.1, H1.5, J2.2 |

## Page 4 · Connectors

_H1 header, J2 ESP-01 socket_

**Net labels on this page:** `DTR_N`, `EN`, `IO0`, `IO15`, `RST`, `RTS_N`, `RXD`, `TXD`  
**No-Connect flags:** none

### H1: 1x11 male header

Footprint `HDR-TH_11P-P2.54-V-M` · LCSC C2840011

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 3V3 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 5V | `+5V` | power symbol (5 pins) |
| ☐ | 3 | GND | `GND` | power symbol (24 pins) |
| ☐ | 4 | TX | `TXD` | U2.2, LED2.1, SW4.1, J2.7 |
| ☐ | 5 | RX/UPDI | `RXD` | U2.3, LED3.1, R15.2, J2.2 |
| ☐ | 6 | DTR | `DTR_N` | U2.10, SJ1.1, C10.1 |
| ☐ | 7 | RTS | `RTS_N` | U2.11, SJ2.1 |
| ☐ | 8 | RST | `RST` | C10.2, R14.2 |
| ☐ | 9 | EN | `EN` | Q1.3, R9.2, C9.1, SW1.1, J2.4 |
| ☐ | 10 | IO0 | `IO0` | Q2.3, R10.2, SW2.1, J2.5 |
| ☐ | 11 | IO15 | `IO15` | R11.1 |

### J2: 2x4 female (ESP-01)

Footprint `HDR-TH_8P-P2.54-V-F-R2-C4` · LCSC C2897405

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | GND | `GND` | power symbol (24 pins) |
| ☐ | 2 | TXD (ESP out) | `RXD` | U2.3, LED3.1, R15.2, H1.5 |
| ☐ | 3 | GPIO2 | `ESP01_IO2` | R13.2 |
| ☐ | 4 | CH_PD | `EN` | Q1.3, R9.2, C9.1, SW1.1, H1.9 |
| ☐ | 5 | GPIO0 | `IO0` | Q2.3, R10.2, SW2.1, H1.10 |
| ☐ | 6 | RST | `ESP01_RST` | R12.2 |
| ☐ | 7 | RXD (ESP in) | `TXD` | U2.2, LED2.1, SW4.1, H1.4 |
| ☐ | 8 | VCC | `+3V3` | power symbol (13 pins) |

### C8: 22 µF (ESP-01 bulk)

Footprint `C0805` · LCSC C45783

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 2 | `GND` | power symbol (24 pins) |

### R12: 10k (ESP-01 RST)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 2 | `ESP01_RST` | J2.6 |

### R13: 10k (ESP-01 GPIO2)

Footprint `R0805` · LCSC C84376

| ✓ | Pin | Name | Net | Also on this net |
|---|---|---|---|---|
| ☐ | 1 | 1 | `+3V3` | power symbol (13 pins) |
| ☐ | 2 | 2 | `ESP01_IO2` | J2.3 |
