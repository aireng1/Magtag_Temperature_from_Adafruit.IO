# Magtag_Temperature_from_Adafruit.IO
The Magtag reads and displays the temperature being sent to Adafruit.IO from a pi zero W in another location
The Magtag connects to Adafruit.IO and reads the temperature feed. It then displays this on the eink display. It is set to check the temperature every 30 minutes. The battery voltage is displayed in the top right corner. 
If the light sensor detects low light it will stop the temperature update and sleep for an hour and then check light level again. 

Put the code.py file in the root directory of circuitpy.
Add a secrets.py file with you wifi SSID and password, your adafruit username and key.
Put the BMP's in the BMP folder
Put the fonts in the fonts folder. 
