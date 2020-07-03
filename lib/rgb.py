import pycom
import time

def blink(color, times):
    for i in range(times):
        pycom.rgbled(color)
        time.sleep(0.3)
        pycom.rgbled(0x000000)
        time.sleep(0.2)
