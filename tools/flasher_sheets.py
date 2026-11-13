"""Universal USB Flasher V2.1 - the 8 schematic sheets drawn as simplified SVG (planning drawings).
Sheet names, references and net names match the EasyEDA project and tools/design.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schem_lib import *   # noqa: F401,F403

C_T = "#e11d48"      # switched target rails +3V3_T / +5V_T
C_VIO = "#db2777"
C_DATA = "#16a34a"   # TXD / RXD / TX2 / RX2 / UPDI
C_CTL = "#2563eb"    # DTR / RTS / EN / IO0 / RST / TPWR_EN
C_FLT = "#7c3aed"    # FAULT_N, LED nodes
MUTE = "var(--mute)"


def lab_end(p, name, color, dx=10, anchor="start"):
    """Short wire from a pin end and a net label."""
    x, y = p
    x2 = x + dx
    return line([(x, y), (x2, y)], color) + label(x2 + (4 if dx >= 0 else -4), y + 4, name, color, anchor if dx >= 0 else "end")


def to_gnd(p, dx=14):
    x, y = p
    return line([(x, y), (x + dx, y)], C_GND) + gnd(x + dx, y)


# ------------------------------------------------------------------ sheet 1: Power
def sheet1():
    o = []
    y = 70
    o.append(label(20, y + 4, "VBUS", C_5V) + line([(62, y), (90, y)], C_5V) + res(90, y, "F1", "PTC 500 mA", True, 80, C_5V))
    o.append(line([(170, y), (300, y)], C_5V) + dot(210, y, C_5V) + label(176, y - 12, "VBUS_F", C_5V))
    o.append(cap(210, y, "C1", "10 uF", False, 60) + gnd(210, y + 60))
    o.append(line([(210, y), (210, y - 34), (300, y - 34)], C_5V) + label(306, y - 30, "VBUS_F -> U2 VDD5 + VBUS (sheet 4)", C_5V))
    o.append(diode(300, y, "D1", "1N5819HW  A -> K", True, 70, C_5V))
    o.append(line([(370, y), (520, y)], C_5V) + dot(420, y, C_5V) + label(380, y - 12, "+5V", C_5V))
    o.append(cap(420, y, "C5", "10 uF", False, 60) + gnd(420, y + 60))
    u1, p = ic(520, y - 46, 170, 110, "U1", "SGM2212-3.3 (SOT-223)", ["3 VIN"], ["2/4 VOUT"], C_3V3, bottom=["1 GND"], y0=46, step=24)
    o.append(u1 + line([(500, y), p["3 VIN"]], C_5V) + gnd(*p["1 GND"]))
    vo = p["2/4 VOUT"]
    o.append(line([vo, (vo[0] + 200, vo[1])], C_3V3) + dot(vo[0] + 50, vo[1], C_3V3) + dot(vo[0] + 110, vo[1], C_3V3)
             + cap(vo[0] + 50, vo[1], "C6", "22 uF", False, 60) + gnd(vo[0] + 50, vo[1] + 60)
             + cap(vo[0] + 110, vo[1], "C7", "100 nF", False, 60) + gnd(vo[0] + 110, vo[1] + 60)
             + label(vo[0] + 150, vo[1] - 8, "+3V3", C_3V3) + text(vo[0] + 150, vo[1] + 18, "to sheets 2, 6, 7", 11, "start", MUTE))
    # Q3 5V-IO warning
    Y = 300
    o.append(text(20, Y - 86, "5V-IO warning LED: lights only when VIO is about 5 V (SW3 on 5V)", 12, "start", MUTE, "700"))
    o.append(rail(60, Y - 20, "+3V3", C_3V3) + line([(60, Y - 20), (60, Y)], C_3V3) + line([(60, Y), (90, Y)], C_3V3) + res(90, Y, "R16", "4.7k", True, 70, C_3V3))
    q, qp = bjt(160, Y, "Q3", "MMBT3906 (PNP)", pnp=True)
    o.append(q)
    e_ = qp["E"]; c_ = qp["C"]
    o.append(line([e_, (e_[0], e_[1] + 20)], C_VIO) + label(e_[0] + 6, e_[1] + 34, "VIO (emitter, arrow)", C_VIO))
    o.append(line([c_, (c_[0], c_[1] - 10), (260, c_[1] - 10)], C_FLT) + res(260, c_[1] - 10, "R17", "1k", True, 70, C_FLT))
    o.append(line([(330, c_[1] - 10), (360, c_[1] - 10)], C_FLT) + text(345, c_[1] - 22, "LED5_A", 10, "middle", C_FLT))
    o.append(led(360, c_[1] - 10, "LED5", "red 5V IO  (A top, K bottom)", 50, "#dc2626") + gnd(360, c_[1] + 40))
    # C8
    o.append(text(560, Y - 86, "C8: ESP-01 bulk capacitor (place next to J2)", 12, "start", MUTE, "700"))
    o.append(label(560, Y - 16, "+3V3_T", C_T) + line([(620, Y - 20), (640, Y - 20)], C_T) + cap(640, Y - 20, "C8", "22 uF", False, 60) + gnd(640, Y + 40))
    o.append(text(20, Y + 120, "D1: anode (triangle) on VBUS_F, cathode (bar) on +5V. C5 goes from +5V to GND, never across D1.", 12, "start", MUTE))
    return svg(960, Y + 140, "".join(o))


# ------------------------------------------------------------------ sheet 2: Target power
def _switch(o, x, y, ref, vin, vout, ril, rref, cin, cout, vin_col, out_col):
    u, p = ic(x, y, 180, 120, ref, "TPS2553 (SOT-23-6)", ["1 IN", "2 GND", "3 EN"], ["6 OUT", "5 ILIM", "4 /FAULT"], out_col, y0=34, step=30)
    o.append(u)
    a = p["1 IN"]
    o.append(line([a, (a[0] - 110, a[1])], vin_col) + dot(a[0] - 80, a[1], vin_col) + label(a[0] - 114, a[1] + 4, vin, vin_col, "end")
             + cap(a[0] - 80, a[1], cin, "100 nF", False, 46) + gnd(a[0] - 80, a[1] + 46))
    o.append(to_gnd(p["2 GND"], -14))
    o.append(lab_end(p["3 EN"], "TPWR_EN", C_CTL, -16))
    q = p["6 OUT"]
    o.append(line([q, (q[0] + 230, q[1])], out_col) + dot(q[0] + 120, q[1], out_col) + label(q[0] + 234, q[1] + 4, vout, out_col)
             + cap(q[0] + 120, q[1], cout, "10 uF", False, 46) + gnd(q[0] + 120, q[1] + 46))
    il = p["5 ILIM"]
    o.append(line([il, (il[0] + 50, il[1])], INK) + res(il[0] + 50, il[1], rref, ril, False, 50) + gnd(il[0] + 50, il[1] + 50))
    f = p["4 /FAULT"]
    o.append(line([f, (f[0] + 14, f[1]), (f[0] + 14, f[1] + 30)], C_FLT) + label(f[0] + 14, f[1] + 46, "FAULT_N", C_FLT, "middle"))
    return p


def sheet2():
    o = []
    p4 = _switch(o, 200, 40, "U4", "+3V3", "+3V3_T", "43k", "R18", "C11", "C12", C_3V3, C_T)
    # PWR LED on +3V3_T
    x = p4["6 OUT"][0] + 180
    o.append(dot(x, p4["6 OUT"][1], C_T) + res(x, p4["6 OUT"][1], "R3", "1k", False, 50, C_T) + led(x, p4["6 OUT"][1] + 50, "LED1", "green PWR  A top", 46, "#16a34a") + gnd(x, p4["6 OUT"][1] + 96))
    _switch(o, 200, 270, "U5", "+5V", "+5V_T", "51k", "R19", "C13", "C14", C_5V, C_T)
    # enable / power-cycle
    X, Y = 760, 60
    o.append(text(X - 20, Y - 30, "Enable + POWER-CYCLE", 12, "start", MUTE, "700"))
    o.append(rail(X, Y, "+3V3", C_3V3) + res(X, Y, "R20", "100k", False, 60, C_3V3) + dot(X, Y + 60, C_CTL)
             + line([(X, Y + 60), (X - 40, Y + 60)], C_CTL) + label(X - 44, Y + 64, "TPWR_EN", C_CTL, "end")
             + sw(X, Y + 60, "SW5 POWER", 50) + gnd(X, Y + 110))
    o.append(text(X - 20, Y + 150, "TPWR_EN goes to U4 pin 3 AND U5 pin 3.", 11, "start", MUTE))
    # overload LED
    Y2 = 300
    o.append(text(X - 20, Y2 - 30, "OVERLOAD LED", 12, "start", MUTE, "700"))
    o.append(rail(X, Y2, "+5V", C_5V) + res(X, Y2, "R21", "1k", False, 50, C_5V) + led(X, Y2 + 50, "LED6", "red  A top, K bottom", 46, "#dc2626")
             + line([(X, Y2 + 96), (X, Y2 + 110)], C_FLT) + label(X + 6, Y2 + 124, "FAULT_N", C_FLT))
    o.append(text(X - 20, Y2 + 150, "FAULT_N comes from U4 pin 4 AND U5 pin 4.", 11, "start", MUTE))
    return svg(1000, 470, "".join(o))


# ------------------------------------------------------------------ sheet 3: USB + ESD
def sheet3():
    o = []
    j, p = ic(20, 30, 190, 400, "USB1", "USB-C 16P (C2765186)", [],
              ["VBUS  A4B9,B4A9", "CC1  A5", "CC2  B5", "DP  A6,B6", "DN  A7,B7", "SBU  A8,B8", "GND  A1B12,B1A12", "SHELL  EH 13,14"], C_USB, y0=54, step=44)
    o.append(j)
    o.append(lab_end(p["VBUS  A4B9,B4A9"], "VBUS", C_5V, 40))
    for nm, rf in (("CC1  A5", "R1"), ("CC2  B5", "R2")):
        c = p[nm]
        o.append(line([c, (c[0] + 20, c[1])], C_USB) + res(c[0] + 20, c[1], rf, "5.1k", True, 70, C_USB) + gnd(c[0] + 90, c[1]))
    o.append(nc(p["SBU  A8,B8"][0] + 4, p["SBU  A8,B8"][1]) + text(p["SBU  A8,B8"][0] + 16, p["SBU  A8,B8"][1] + 4, "No-Connect", 10.5, "start", MUTE))
    o.append(to_gnd(p["GND  A1B12,B1A12"]) + to_gnd(p["SHELL  EH 13,14"]))
    dp, dn = p["DP  A6,B6"], p["DN  A7,B7"]
    u3, q = ic(330, dp[1] - 40, 160, 110, "U3", "USBLC6-2SC6", ["1 I/O1", "3 I/O2"], ["6 I/O1", "4 I/O2"], C_USB, top=["5 VBUS"], bottom=["2 GND"], y0=40, step=36)
    o.append(u3)
    o.append(line([dp, q["1 I/O1"]], C_USB) + line([dn, (dn[0] + 60, dn[1]), (dn[0] + 60, q["3 I/O2"][1]), q["3 I/O2"]], C_USB))
    o.append(lab_end(q["6 I/O1"], "USB_DP", C_USB, 20) + lab_end(q["4 I/O2"], "USB_DM", C_USB, 20))
    o.append(line([q["5 VBUS"], (q["5 VBUS"][0], q["5 VBUS"][1] - 10)], C_5V) + label(q["5 VBUS"][0] + 6, q["5 VBUS"][1] - 12, "VBUS", C_5V) + gnd(*q["2 GND"]))
    o.append(text(330, dn[1] + 100, "USB_DP / USB_DM continue to U2 pins 3 / 4 (sheet 4).", 11, "start", MUTE))
    for k, (ref, nets) in enumerate((("U6", ["TXD", "RXD", "RTS_N", "DTR_N"]), ("U7", ["EN", "IO0", "RX2", "TX2"]))):
        x, y = 700, 40 + k * 200
        u, r = ic(x, y, 160, 120, ref, "USBLC6-4SC6 (header ESD)", ["1 I/O1", "3 I/O2"], ["6 I/O4", "4 I/O3"], C_DATA, top=["5 VBUS"], bottom=["2 GND"], y0=44, step=40)
        o.append(u)
        col = C_DATA if ref == "U6" else C_CTL
        o.append(lab_end(r["1 I/O1"], nets[0], C_DATA if nets[0] in ("TXD", "RXD", "TX2", "RX2") else C_CTL, -14)
                 + lab_end(r["3 I/O2"], nets[1], C_DATA if nets[1] in ("TXD", "RXD", "TX2", "RX2") else C_CTL, -14)
                 + lab_end(r["6 I/O4"], nets[2], C_DATA if nets[2] in ("TXD", "RXD", "TX2", "RX2") else C_CTL, 14)
                 + lab_end(r["4 I/O3"], nets[3], C_DATA if nets[3] in ("TXD", "RXD", "TX2", "RX2") else C_CTL, 14))
        o.append(line([r["5 VBUS"], (r["5 VBUS"][0], r["5 VBUS"][1] - 8)], C_5V) + label(r["5 VBUS"][0] + 6, r["5 VBUS"][1] - 10, "+5V", C_5V) + gnd(*r["2 GND"]))
    o.append(text(330, 470, "U6/U7: their pin numbers are hidden in your symbol - left-middle = 2 GND, right-middle = 5 (+5V).", 11, "start", MUTE))
    return svg(1000, 490, "".join(o))


# ------------------------------------------------------------------ sheet 4: USB-UART
def sheet4():
    o = []
    L = [("1 RI0#", None), ("2 GND", "GND"), ("3 UD+", "USB_DP"), ("4 UD-", "USB_DM"), ("5 VIO", "VIO"), ("6 V3", "V3"),
         ("7 VDD5", "VBUS_F"), ("8 VBUS", "VBUS_F"), ("9 RST#", None), ("10 CTS1#", None), ("11 RTS1#", None), ("12 RXD1", "RX2")]
    R = [("13 TXD1", "TX2"), ("14 DSR1#", None), ("15 DTR1#", "DTR2_N"), ("16 DCD1#", None), ("17 RI1#", None), ("18 CTS0#", None),
         ("19 RTS0#", "RTS_N"), ("20 RXD0", "RXD"), ("21 TXD0", "TXD"), ("22 DSR0#", None), ("23 DTR0#", "DTR_N"), ("24 DCD0#", None), ("25 EP", "GND")]
    u, p = ic(330, 30, 230, 420, "U2  (rename U8 -> U2)", "CH342F dual UART, QFN-24", [a for a, _ in L], [a for a, _ in R], "#14b8a6", y0=50, step=28)
    o.append(u)
    col = {"USB_DP": C_USB, "USB_DM": C_USB, "VIO": C_VIO, "V3": C_GND, "VBUS_F": C_5V, "RX2": C_DATA, "TX2": C_DATA, "RXD": C_DATA, "TXD": C_DATA,
           "DTR2_N": C_CTL, "RTS_N": C_CTL, "DTR_N": C_CTL}
    for side, lst in ((-1, L), (1, R)):
        for nm, net in lst:
            pt = p[nm]
            if net is None:
                o.append(nc(pt[0] + 6 * side, pt[1]))
            elif net == "GND":
                o.append(line([pt, (pt[0] + 14 * side, pt[1])], C_GND) + gnd(pt[0] + 14 * side, pt[1]))
            else:
                o.append(lab_end(pt, net, col[net], 16 * side))
    # decoupling
    X = 60
    for i, (ref, net, c) in enumerate((("C2", "VBUS_F", C_5V), ("C3", "V3", C_GND), ("C4", "VIO", C_VIO))):
        x = X + i * 85
        o.append(label(x - 20, 64, net, c) + line([(x, 72), (x, 84)], c) + cap(x, 84, ref, "100 nF", False, 50) + gnd(x, 134))
    o.append(text(40, 168, "C2 pin 7, C3 pin 6, C4 pin 5", 11, "start", MUTE))
    # LEDs
    X2 = 720
    o.append(text(X2 - 30, 60, "Activity LEDs (VIO -> R -> LED A, K on the data line)", 12, "start", MUTE, "700"))
    for i, (r, l, c, net) in enumerate((("R4", "LED2", "#f97316", "TXD"), ("R5", "LED3", "#eab308", "RXD"), ("R6", "LED4", "#3b82f6", "RX2"))):
        x = X2 + i * 95
        o.append(rail(x, 110, "VIO", C_VIO) + res(x, 110, r, "2.2k", False, 50, C_VIO) + led(x, 160, l, ("orange", "yellow", "blue")[i], 46, c)
                 + line([(x, 206), (x, 222)], C_DATA) + label(x, 236, net, C_DATA, "middle"))
    o.append(text(X2 - 30, 270, "Bar (K) side faces the data line; the LED blinks when the line goes low.", 11, "start", MUTE))
    o.append(text(40, 470, "Red X = No-Connect flag (10 pins). DTR0# / DTR1#: no pull-down resistor (it would switch them to RS485 mode).", 11, "start", MUTE))
    return svg(1040, 490, "".join(o))


# ------------------------------------------------------------------ sheet 5: Auto-program
def sheet5():
    o = []
    o.append(label(20, 84, "DTR_N", C_CTL) + line([(70, 80), (90, 80)], C_CTL) + hdr2(90, 80, "SJ1", "2-pin hdr + cap", 70, C_CTL))
    o.append(label(20, 284, "RTS_N", C_CTL) + line([(70, 280), (90, 280)], C_CTL) + hdr2(90, 280, "SJ2", "2-pin hdr + cap", 70, C_CTL))
    o.append(line([(160, 80), (260, 80)], C_CTL) + dot(200, 80, C_CTL) + label(170, 70, "DTR_AP", C_CTL))
    o.append(line([(160, 280), (260, 280)], C_CTL) + dot(230, 280, C_CTL) + label(170, 300, "RTS_AP", C_CTL))
    o.append(res(260, 80, "R7", "10k", True, 70) + res(260, 280, "R8", "10k", True, 70))
    q1, p1 = bjt(330, 80, "Q1", "MMBT3904 (EN)")
    q2, p2 = bjt(330, 280, "Q2", "MMBT3904 (IO0)")
    o.append(q1 + q2)
    o.append(line([p1["C"], (p1["C"][0], 30), (480, 30)], "#ca8a04") + label(486, 34, "EN", "#ca8a04"))
    o.append(line([p2["C"], (p2["C"][0], 230), (480, 230)], "#ca8a04") + label(486, 234, "IO0", "#ca8a04"))
    # Q1 emitter -> RTS_AP, Q2 emitter -> DTR_AP (crossed)
    o.append(line([p1["E"], (p1["E"][0], 160), (230, 160), (230, 280)], C_CTL))
    o.append(line([p2["E"], (p2["E"][0], 340), (200, 340), (200, 80)], C_CTL))
    o.append(text(560, 70, "DTR#  RTS#  ->  EN    IO0", 12, "start", INK, "700", True))
    for i, row in enumerate(("1     1         high  high   run", "1     0         LOW   high   reset", "0     1         high  LOW    boot", "0     0         high  high   (monitor)")):
        o.append(text(560, 92 + i * 18, row, 12, "start", INK, "400", True))
    o.append(text(560, 190, "Q1: base via R7 from DTR_AP, emitter RTS_AP, collector EN.", 11, "start", MUTE))
    o.append(text(560, 208, "Q2: base via R8 from RTS_AP, emitter DTR_AP, collector IO0.", 11, "start", MUTE))
    o.append(text(560, 226, "Cap on SJ1 and SJ2 = auto-program ON.", 11, "start", MUTE))
    return svg(960, 380, "".join(o))


# ------------------------------------------------------------------ sheet 6: Target I/O
def sheet6():
    o = []
    items = [("R9", "10k", "+3V3_T", "EN", C_T), ("R10", "10k", "+3V3_T", "IO0", C_T), ("R12", "10k", "+3V3_T", "ESP01_RST", C_T),
             ("R13", "10k", "+3V3_T", "ESP01_IO2", C_T), ("R14", "10k", "VIO", "RST", C_VIO)]
    for i, (r, v, top, bot, c) in enumerate(items):
        x = 60 + i * 130
        o.append(rail(x, 60, top, c) + res(x, 60, r, v, False, 60, c) + line([(x, 120), (x, 140)], C_CTL) + label(x, 156, bot, C_CTL, "middle"))
    o.append(text(40, 190, "Pull-ups: four 10k from +3V3_T (switched), R14 from VIO.", 11, "start", MUTE))
    Y = 260
    o.append(label(30, Y + 4, "EN", C_CTL) + line([(56, Y), (90, Y)], C_CTL) + dot(90, Y, C_CTL) + cap(90, Y, "C9", "100 nF", False, 50) + gnd(90, Y + 50))
    o.append(label(200, Y + 4, "IO15", C_CTL) + line([(240, Y), (260, Y)], C_CTL) + res(260, Y, "R11", "10k", False, 50) + gnd(260, Y + 50))
    o.append(label(360, Y + 4, "DTR_N", C_CTL) + line([(410, Y), (430, Y)], C_CTL) + cap(430, Y, "C10", "100 nF", True, 60) + line([(490, Y), (510, Y)], C_CTL) + label(514, Y + 4, "RST", C_CTL))
    o.append(label(600, Y + 4, "UPDI_R", C_DATA) + line([(656, Y), (676, Y)], C_DATA) + res(676, Y, "R15", "4.7k", True, 70, C_DATA) + line([(746, Y), (766, Y)], C_DATA) + label(770, Y + 4, "RXD", C_DATA))
    o.append(text(40, Y + 100, "C10 + R14 = Arduino auto-reset on RST. R15 links TX to RX when SW4 is on UPDI (UPDI_R = SW4 common).", 11, "start", MUTE))
    return svg(900, Y + 120, "".join(o))


# ------------------------------------------------------------------ sheet 7: switches
def sheet7():
    o = []
    for i, (ref, net, txt) in enumerate((("SW1", "EN", "RESET"), ("SW2", "IO0", "BOOT"))):
        x = 60 + i * 160
        o.append(label(x, 44, net, C_CTL, "middle") + line([(x, 50), (x, 60)], C_CTL) + sw(x, 60, f"{ref} {txt}", 50) + gnd(x, 110))
    s3, p3 = spdt(420, 90, "SW3", "IO voltage")
    o.append(s3 + lab_end(p3["2"], "VIO", C_VIO, -20) + lab_end(p3["1"], "+3V3", C_3V3, 16) + lab_end(p3["3"], "+5V", C_5V, 16))
    s4, p4 = spdt(680, 90, "SW4", "UART | UPDI")
    o.append(s4 + lab_end(p4["2"], "UPDI_R", C_DATA, -20) + lab_end(p4["1"], "TXD", C_DATA, 16) + nc(p4["3"][0] + 8, p4["3"][1]))
    o.append(text(400, 170, "Pin 4 (metal tab) of SW3 and SW4 -> GND.  SW4 pin 3 = No-Connect flag.", 11, "start", MUTE))
    return svg(900, 190, "".join(o))


# ------------------------------------------------------------------ sheet 8: connectors
def sheet8():
    o = []
    h1n = [("1 3V3", "+3V3_T", C_T), ("2 5V", "+5V_T", C_T), ("3 GND", "GND", C_GND), ("4 TX", "TXD", C_DATA), ("5 RX/UPDI", "RXD", C_DATA), ("6 DTR", "DTR_N", C_CTL),
           ("7 RTS", "RTS_N", C_CTL), ("8 RST", "RST", C_CTL), ("9 EN", "EN", C_CTL), ("10 IO0", "IO0", C_CTL), ("11 IO15", "IO15", C_CTL)]
    u, p = ic(160, 30, 130, 350, "H1", "1x11 header", [a for a, _, _ in h1n], [], "#64748b", y0=46, step=28)
    o.append(u)
    for a, n, c in h1n:
        o.append(to_gnd(p[a], -14) if n == "GND" else lab_end(p[a], n, c, -16))
    j2l = [("1 GND", "GND"), ("3 GPIO2", "ESP01_IO2"), ("5 GPIO0", "IO0"), ("7 RXD", "TXD")]
    j2r = [("2 TXD", "RXD"), ("4 CH_PD", "EN"), ("6 RST", "ESP01_RST"), ("8 VCC", "+3V3_T")]
    u, p = ic(460, 30, 150, 150, "J2", "ESP-01 socket 2x4", [a for a, _ in j2l], [a for a, _ in j2r], "#64748b", y0=46, step=28)
    o.append(u)
    cc = lambda n: C_GND if n == "GND" else C_T if n.startswith("+3V3") else C_DATA if n in ("TXD", "RXD") else C_CTL
    for a, n in j2l:
        o.append(to_gnd(p[a], -14) if n == "GND" else lab_end(p[a], n, cc(n), -16))
    for a, n in j2r:
        o.append(lab_end(p[a], n, cc(n), 16))
    o.append(text(460, 200, "ESP TXD -> flasher RXD, ESP RXD <- flasher TXD.", 11, "start", MUTE))
    pr = [("1 ESP_EN", "EN"), ("3 ESP_TXD", "RXD"), ("5 ESP_RXD", "TXD")]
    pr2 = [("2 VDD", "+3V3_T"), ("4 GND", "GND"), ("6 ESP_IO0", "IO0")]
    for k, (ref, sub) in enumerate((("J3", "ESP-Prog 2x3 1.27 mm"), ("J4", "PROG 2x3 2.54 mm"))):
        x, y = 460 + k * 300, 250
        u, p = ic(x, y, 150, 120, ref, sub, [a for a, _ in pr], [a for a, _ in pr2], "#64748b", y0=46, step=28)
        o.append(u)
        for a, n in pr:
            o.append(lab_end(p[a], n, cc(n), -16))
        for a, n in pr2:
            o.append(to_gnd(p[a]) if n == "GND" else lab_end(p[a], n, cc(n), 16))
    j5 = [("1 GND", "GND"), ("2 TX2", "TX2"), ("3 RX2", "RX2"), ("4 DTR2", "DTR2_N")]
    u, p = ic(820, 30, 120, 150, "J5", "UART2 1x4", [], [a for a, _ in j5], "#64748b", y0=46, step=28)
    o.append(u)
    for a, n in j5:
        o.append(to_gnd(p[a]) if n == "GND" else lab_end(p[a], n, C_DATA if n in ("TX2", "RX2") else C_CTL, 16))
    return svg(1060, 400, "".join(o))


SHEETS = {"P1": sheet1, "P2": sheet2, "P3": sheet3, "P4": sheet4, "P5": sheet5, "P6": sheet6, "P7": sheet7, "P8": sheet8}
