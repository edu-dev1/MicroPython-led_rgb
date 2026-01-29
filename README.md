# MicroPython-led_rgb
Led RGB.
A simple library for LED RGB.

## Features
-Easy to use.
-Compatible with ESP32 and Raspberry.

## Example of usage
```python
from led_rgb import LedRGB
from time import sleep
my_ledrgb = LedRGB(R=1, G=2, B=3, common_anode:bool=True)

my_ledrgb.red()
sleep(1)
my_ledrgb.green()
sleep(1)
my_ledrgb.blue()
sleep(1)

my_ledrgb.ser_color(r=255, g=255, b=0)#yellow
sleep(1)
