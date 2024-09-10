"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import requests

import time
import network
import urequests

# Define the API endpoint
baseEndpoint = 'https://privateapitest.onrender.com/putData/'
ssid = 'BU Guest (unencrypted)'


N: int = 3
sample_ms = 10.0
on_ms = 500


def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)



def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    print(t_good)

    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {}
    

    
    if not t_good:
        print("No score :(")
        
    else:
        data['minimum'] = min(t_good)
        data['maximum'] = max(t_good)
        data['average'] = sum(t_good) / len(t_good)
            
        print("data json is: ")
        print(data)
        
    url = baseEndpoint + "{:.1f}".format(data['minimum']) + "/" + "{:.1f}".format(data['maximum']) + "/" + "{:.1f}".format(data['average'])
    
    print(url)
    
    connect_and_get_data(ssid, url)
  

def connect_and_get_data(ssid: str, url: str, max_wait: int = 10) -> None:
    """
    Connect to the specified Wi-Fi network and make an HTTP GET request.

    :param ssid: The SSID of the Wi-Fi network to connect to.
    :param url: The URL to make the HTTP GET request to.
    :param max_wait: Maximum time (in seconds) to wait for the connection to establish.
    """
    # Initialize WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid)

    # Wait for connection or fail
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('Connected')
        status = wlan.ifconfig()
        print('IP = ' + status[0])

        # Make GET request
        try:
            r = urequests.get(url)
            print(f'Status code: {r.status_code}')
            # You can also print r.text or r.json() if needed
        except Exception as e:
            print(f'Request failed: {e}')
        finally:
            r.close()


    

if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files
    print("Welcome to the Light Game!")

    # Set Pin 10 to be the Start/Stop LED
    led = Pin(10, Pin.OUT)
    
    # Set Pin 16 to be the Button
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
