from setuptools import setup
OPTIONS = {
    'argv_emulation': True
}

setup(
    app=['main.py'],
    name='wifi_rssi_slack_alert',
    version='0.1',
    # packages=['rumps', 'requests'],
    url='https://github.com/mukul7/wifi-rssi-slack-alert',
    license='',
    author='mukulpahwa',
    author_email='mukulpahwa504@gmail.com',
    description='Notifies to slack when RSSI goes below certain limit.',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    data_files=['config']

)
