# Imports #
from adafruit_magtag.magtag import MagTag
import displayio
import terminalio
import socketpool
import adafruit_requests
import wifi
import ssl
import time
import alarm
import board
from secrets import secrets
from adafruit_io.adafruit_io import IO_HTTP



magtag = MagTag()

## Set the light sensor pin
light_pin = board.LIGHT

## Set the threshold for deep sleep (e.g. if light level is below this value, go to sleep)
light_threshold = 360
while True:
        # Read and print the light level
    light_level = magtag.peripherals.light
    print("Light level:", light_level)
        #Read and print the Battery voltage
    battery_level = magtag.peripherals.battery
    battery_level = round(battery_level, 2)
    battery_percent = (battery_level - 3.3) / (4.2-3.3) * 100
    battery_percent = round(battery_percent)
    print (f"Battery Voltage:{battery_level}")
        # Check if the light level is below the threshold
    if light_level < light_threshold:
        ## Set background sleeping picture
        #magtag.set_background("/bmps/sleeping.bmp")
        ##Refresh display
        #magtag.display.refresh()
        print("Going to sleep...")
        time.sleep(2)
        print("sleeping for 1 hour")
        #Set deep sleep for 60 seconds * 60
        PAUSE = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 60 * 60)
        alarm.exit_and_deep_sleep_until_alarms(PAUSE)

    else:
        # Set Background, comment out if no background is required
        # For Fahreheit change the file name to "/bmps/temperature_background_F.bmp"
        magtag.set_background("/bmps/temperature_background.bmp")
        #magtag.set_background("/bmps/temperature_background_F.bmp")
        #magtag.set_background("/bmps/temperature_background_blank.bmp")

        # Connect to Wi-Fi #
        # Make sure to put wifi credentials in secrets.py
        print("[!] Connecting to network: %s..." % secrets["ssid"])
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        print("[+] Connected to network: %s!" % secrets["ssid"])
        pool = socketpool.SocketPool(wifi.radio)

        # Connect to Adafruit IO using HTTP requests #
        # Put adafruit.io username and key in secrets.py
        print("[!] Connecting to Adafruit IO...")
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        io = IO_HTTP(secrets["aio_username"], secrets["aio_key"], requests)
        print("[+] Connected to Adafruit IO...")

        # Connect to feed
        # Put correct feed name here
        temperature_feed = None
        try:
            temperature_feed = io.get_feed('temperature')
            print("[+] Subscribed to 'temperature' feed!")

        except Exception as err:
            print(f"Error getting feed, {err}")

        while True:
           # temperature = ""

            temperature = (io.receive_data("temperature")["value"])
            if isinstance(temperature, str):
                temperature = float(temperature)
                rounded_temp = round(temperature, 1)


            print(temperature)

            magtag.add_text(
                text_font="/fonts/OpenSans-Semibold-75.bdf",
                text_position=(
                    (magtag.graphics.display.height // 2) - 1,
                    (magtag.graphics.display.width // 2) - 75,
                ),
                text_anchor_point=(0.1, 0.5), # center the text on x & y
                text_scale = 1, # Scale size of text

            )
            magtag.add_text(
            text_font="/fonts/Arial-Italic-12.bdf",
            text_position=(magtag.graphics.display.width // 1.2, 10),
            text_anchor_point=(0.1, 0.5),  # left justify this line
        )
            # This will print feed value and battery percent
            message = f"{rounded_temp}"
            message2 = f"{battery_percent}%"
            magtag.set_text(message, 0)
            magtag.set_text(message2, 1)

            # put the MagTag to sleep for 30 minutes
            time.sleep(2)
            print("sleeping for 30 minutes")
            PAUSE = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 60 * 30)
            alarm.exit_and_deep_sleep_until_alarms(PAUSE)
