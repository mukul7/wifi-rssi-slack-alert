import os
import pickle

import requests as requests
import rumps as rumps
from setinterval import SetInterval

CONFIGURATION = os.path.join('config', 'configuration')


# def resource_path(relative):
#     if hasattr(sys, "_MEIPASS"):
#         return os.path.join(sys._MEIPASS, relative)
#     return os.path.join(relative)


def update_configuration(key, value):
    try:
        with open(CONFIGURATION, 'rb') as config_file:
            config_dictionary = pickle.load(config_file)
    except Exception:
        config_dictionary = {}
    config_dictionary[key] = value
    with open(CONFIGURATION, 'wb') as config_dictionary_file:
        pickle.dump(config_dictionary, config_dictionary_file)


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


class RSSIApp(object):
    def __init__(self):
        self.config = {
            "app_name": "Wifi RSSI Slack Alert",
            "set_url": "Set Slack Webhook Url",
            "rssi_limit": "Set RSSI Threshold"
        }
        self.alert_conf = pickle.load(open(CONFIGURATION, 'rb'))
        self.app = rumps.App(self.config["app_name"])
        self.preference_button = rumps.MenuItem(title=self.config["set_url"], callback=self.open_webhook_setter)
        self.limit_button = rumps.MenuItem(title=self.config["rssi_limit"], callback=self.open_rssi_limit_setter)
        self.last_status = None
        self.app.menu = [self.limit_button, self.preference_button]
        SetInterval(0.5, self.start_checking)

    def open_webhook_setter(self, sender):
        win = rumps.Window(title='Wifi RSSI Slack Alert',
                           message="Add the webhook of channel in which you want to send alerts",
                           default_text=self.alert_conf['url'], cancel=True)
        response = win.run()
        if response.clicked == 1:
            self.alert_conf['url'] = response.text.strip()
            update_configuration('url', response.text.strip())

    def open_rssi_limit_setter(self, sender):
        win = rumps.Window(title='Send Alert when RSSI drops below', message='The app will send a alert on slack if '
                                                                             'the rssi drops below the given. This '
                                                                             'should always be within range of 0 to '
                                                                             '-1',
                           default_text=self.alert_conf['bad_rssi_limit'],
                           cancel=True)
        response = win.run()
        if response.clicked == 1:
            res = int(response.text.strip())
            if 0 >= res >= -100:
                self.alert_conf['bad_rssi_limit'] = res
                update_configuration('bad_rssi_limit', res)

    def notify_bad_connection(self, rssi):
        payload = {
            'text': 'WiFi signal strength is in *unreliable* region. *RSSI*: {}'.format(rssi) + ' 👎'
        }

        requests.post(self.alert_conf['url'], json=payload)
        print("sent bad notification")

    def notify_good_connection(self, rssi):
        payload = {
            'text': 'WiFi signal strength is in *reliable* region. *RSSI*: {}'.format(rssi) + ' 👍'
        }
        requests.post(self.alert_conf['url'], json=payload)
        print("sent good notification")

    def start_checking(self):
        try:
            strength = wifi_strength()
            self.app.title = str(strength)
            if strength < self.alert_conf['bad_rssi_limit'] and (self.last_status is True or self.last_status is None):
                self.last_status = False
                self.notify_bad_connection(strength)
            elif strength >= self.alert_conf['bad_rssi_limit'] and (
                    self.last_status is False or self.last_status is None):
                self.last_status = True
                self.notify_good_connection(strength)
        except Exception as error:
            self.app.title = '🏴‍☠️'
            print(error)

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = RSSIApp()
    app.run()
