import config
from dth import DTH
import machine
import pycom
import rgb
import time
import ubidots

pycom.heartbeat(False)

ubidots.setup()
print('Connected to WiFi')
rgb.blink(0x00ff00, 3)

d = DTH(machine.Pin(config.DHT_PIN, mode=machine.Pin.OPEN_DRAIN), 1)
light = machine.Pin(config.LIGHT_PIN, mode=machine.Pin.IN)
adc = machine.ADC(bits=10)
read_light_value = adc.channel(attn=machine.ADC.ATTN_11DB, pin=config.LIGHT_PIN)
soil_moisture_power = machine.Pin(config.SOIL_MOISTURE_POWER_PIN,
                                  mode=machine.Pin.OUT,
                                  pull=machine.Pin.PULL_DOWN)
read_soil_moisture_value = adc.channel(attn=machine.ADC.ATTN_11DB,
                                       pin=config.SOIL_MOISTURE_READ_PIN)

while True:
    result = d.read()

    while not result.is_valid():
        time.sleep(1)
        result = d.read()

    soil_moisture_power.value(1)
    time.sleep(0.1)
    soil_moisture_percentage = read_soil_moisture_value()*100/1024
    soil_moisture_power.value(0)
    light_percentage = read_light_value()*100/1024

    data = {
        'temperature': {'value': result.temperature},
        'humidity': {'value': result.humidity},
        'light': {'value': light_percentage},
        'soil_moisture': {'value': soil_moisture_percentage}
    }

    ubidots.send(data)
    rgb.blink(0x0000ff, 1)

    time.sleep(config.DELAY)
