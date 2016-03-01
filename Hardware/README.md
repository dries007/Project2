Hardware
========

Datasheets
----------

- [RTC DS3231](DS3231.pdf)
- [DAC pcm5102a](pcm5102a.pdf)
- [LCD ILI9341](ILI9341.pdf)
- [3.3V regulator MCP1703](22049f.pdf)
- [Audio Amplifier TPA2016D2RTJR](slos524d-122167.pdf)
- [I²C Levelshifter BSS138](AN10441.pdf)
- [Rotary Encoder ECN11E](ECN11.pdf)
- [NOR gates](74HC_HCT4002-839393.pdf)

Eigenschappen
-------------

- SMD Weerstanden: 1206
- SMD Condensatoren: 0805
- Rotary encoder: EC11
- 3.3V regulator MCP1703: SOT-23
- I²C Levelshifter BSS138: SOT-23
- DAC pcm5102a: TSSOP-20
- Audio Amplifier: 20QFN
- Speakers: Ø50mm x ↔19mm
- Power jack: 3.5mm x 1.35mm
- Supercap: ↔5mm
- RTC DS3231: SOP-16
- Buzzer: Ø12mm x ↕ 10mm

### SMD Elco
F    | V  | FP
-----|----|-----
1µ   | 50 | 4x5
2µ2  | 50 | 4x5
4µ7  | 50 | 4x5
10µ  | 16 | 4x5
10µ  | 25 | 4x5
22µ  | 16 | 4x5
22µ  | 25 | 4x5
47µ  | 10 | 5x5
47µ  | 16 | 5x5
100µ | 10 | 6x5
100µ | 16 | 6x5
220µ | 10 | 6x5
220µ | 16 | 6x7

Spanningen
----------

### 5.0 V
- Pi (Voeding)
- SuperCap voor RTC (Diode & Weerstand -> 4.3 V )
- RTC

### 3.3 V
- Pi (Bussen & GPIO)
- DAC
- LCD

Bussen
------
### I²S
- Pi (Master) Pin 18, 35 & 40
- DAC

### I²C
- Pi (Master) Pin 2 & 3
- RTC (Time keeping)
- Amplifier (Volume control)

### SPI
- Pi (Master) SPI0 Pin 19, 21, 23, 24 & 26
- LCD

