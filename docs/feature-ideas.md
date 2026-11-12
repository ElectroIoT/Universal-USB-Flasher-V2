# Feature ideas (not in the current design)

Ranked by value for effort. None of these are designed or part-checked yet. Look up LCSC stock before adopting one.

## Worth adding in V2.1

### 1. ESP-Prog compatible 2×3 header
Espressif's ESP-Prog uses a 2×3, 2.54 mm "PROG" header carrying VDD, EN, TXD, RXD, IO0 and GND. Many ESP boards (including your own future ones) can carry that 6-pin footprint, and then the flasher plugs in with one ribbon cable, with no loose jumper wires.
- Cost: one 2×3 header, plus the nets already exist.
- Check the exact ESP-Prog pin order in Espressif's ESP-Prog docs before drawing it.

### 2. Current-limited target power switch
Put a load switch with an adjustable current limit between +3V3/+5V and the header (for example a USB power-distribution switch IC), with a small button to power-cycle the target.
- Protects the LDO and the target much faster than the PTC.
- Lets you power-cycle a module without unplugging USB, which is handy for deep-sleep testing.

### 3. ESD protection on the header pins
The 11 header pins are touched and hot-plugged far more than the USB port. A 4- or 6-line TVS array on TX, RX, EN, IO0, DTR and RTS is cheap insurance.

## Worth considering

### 4. 5 V-IO warning LED
A red LED that lights only when SW3 is on 5 V. The clean way is a DPDT slide switch (second pole drives the LED). None was in LCSC stock on 2026-11-12, so check again later.

### 5. Dual UART (CH342F)
A second UART lets you flash one target while logging another device, for example a gateway and a node.

### 6. Standard pogo / Tag-Connect pads
Pick one pad pattern (Tag-Connect TC2030 or your own 6-pad pogo layout) for all future ElectroIoT boards. Then make a matching pogo cable for this flasher. Production boards then need no programming header at all.

### 7. Enclosure
A 3D-printed or acrylic sandwich case that protects the bottom side and gives the ESP-01 overhang something to rest on.

## Bigger, separate project

### 8. Stand-alone offline programmer
An ESP32-S3 with an SD card and a "Flash" button that writes a stored firmware image to targets with no PC. That's useful for small production runs, but it is its own project.
