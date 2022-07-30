import os

import requests as requests

bad_rssi_limit = -30
url = 'https://hooks.slack.com/services/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'


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def wifi_strength():
    x = os.popen(
        "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I").read()

    # Parsing response
    split_responses = x.splitlines()
    result = {}

    for response in split_responses:
        key_value = response.split(":")
        result[key_value[0].strip()] = key_value[1].strip()

    if "AirPort" in result and result["AirPort"] == 'Off':
        raise Exception("WiFi is turned off")

    if "state" in result and result["state"] == 'init':
        raise Exception("WiFi not connected")

    if "state" in result and result["state"] == "running" and "agrCtlRSSI" in result:
        return int(result["agrCtlRSSI"])

    raise Exception("Not able to find signal strength")


def notify_bad_connection(rssi):
    payload = {
        'text': 'WiFi signal strength has gone in *unreliable* region. *RSSI*: {}'.format(rssi)
    }
    res = requests.post(url, json=payload)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        strength = wifi_strength()
        if strength < bad_rssi_limit:
            notify_bad_connection(strength)

    except Exception as error:
        print(error)
