import config
import machine
from network import WLAN
import urequests as requests

def setup():
    wlan = WLAN(mode=WLAN.STA)
    wlan.antenna(WLAN.INT_ANT)
    wlan.connect(config.WIFI_SSID, auth=(WLAN.WPA2, config.WIFI_PASSWORD), timeout=5000)

    while not wlan.isconnected():
        machine.idle()

def send(data):
    try:
        url = 'https://industrial.api.ubidots.com/api/v1.6/devices/' + config.DEVICE_NAME
        headers = {'X-Auth-Token': config.UBIDOTS_TOKEN, 'Content-Type': 'application/json'}
        if data is not None:
            post_request = requests.post(url=url, headers=headers, json=data)
            return post_request.json()
    except:
        pass
