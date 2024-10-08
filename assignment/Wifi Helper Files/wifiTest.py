import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Wireless Network', 'The Password')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print(wlan.ifconfig())