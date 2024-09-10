import time
import network
import urequests

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
