https://github.com/francescopace/espectre

Motion detection system based on Wi-Fi spectre analysis (CSI), with native Home Assistant integration via ESPHome.

What you need: A ~€10 ESP32 device (S3 and C6 recommended, other variants supported)

Setup

Download
https://github.com/francescopace/espectre/releases/download/2.5.1/espectre-2.5.1-esp32.bin

Flash Firmware Directly at 0x10000 Using Flashing Tools

Connect To ESPECTRE Wifi 
Enter Wifi Router SSID And Password
Create Yaml
For Eg espectre.yaml

Connect To Same Wifi as Espectre

Install esphome if you haven't already

pip install esphome

Run

esphome --dashboard logs espectre.yaml --device OTA

OR 

esphome logs espectre.yaml --device ESP32-IP


For An Interactive Web Page

