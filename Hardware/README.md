Hardware
========

Datasheets
----------

- [RTC DS3231](DS3231.pdf)
- [DAC pcm5102a](pcm5102a.pdf)
- [LCD ILI9341](ILI9341.pdf)
- [3.3V regulator](22049f.pdf)
- [I²C Amplifier](slos524d-122167.pdf)
- [I²C Levelshifter met BSS138](AN10441.pdf)

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

