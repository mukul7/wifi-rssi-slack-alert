# wifi-rssi-slack-alert
Notifies to slack when RSSI goes below certain limit. 
In telecommunications, received signal strength indicator (RSSI) is a measurement of the power present in a received radio signal.

## Running the application
Either you can simply download the .app file from the dist folder. double click on the app and you are good to go.
or you can build your own app by running the following command

```
pip install py2app rumps
git clone git@github.com:mukul7/wifi-rssi-slack-alert.git
cd wifi-rssi-slack-alert
python3 setup.py py2app
```

or you can also run the app from cli without building by simply running the following commands

```
pip install rumps
git clone git@github.com:mukul7/wifi-rssi-slack-alert.git
cd wifi-rssi-slack-alert
python3 main.py
```

## Using the app
Once you have started the app by following one of the methods mentioned above the app will constantly check the RSSI value and display in Menu Bar
If the rssi goes below the threshold value it sends a notification to configured channel on slack.

The default value of threshold is -67 you can change this by clicking the app icon in menu bar. Similarly you can configure the incoming webhook url for slack channel

## Understanding RSSI Value

| RSSI (Strength)  | Rating | Comments | Required for |
| ------------- | ------------- | ------------- | ------------- |
| -30 dBm  | Amazing | Max achievable signal strength. the client can only be a few feet from the AP to achieve this. Not typical or desirable in the real world. | N/A |
| -67 dBm  | Very Good | Minimum signal strength for applications that require very reliable, timely delivery of data packets. | VoIP/VoWiFi, streaming video |
| -70 dBm | Okay | Minimum signal strength for reliable packet delivery. | Email, web |
| -80 dBm | Not Good | Minimum signal strength for basic connectivity. Packet delivery may be unreliable. | N/A |
| -90 dBm | Unusable | Approaching or drowning in the noise floor. Any functionality is highly unlikely. | N/A |
