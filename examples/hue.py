# -----------------------------------------------------------
# Turn Philipps Hue lamps on/off when phone enters/leaves
# bluetooth reach
#
# (C) 2022 Robin Seidel, Munich, Germany
# Released under MIT License
# Email: robin.seidel@tum.de
# -----------------------------------------------------------

from phue import Bridge

from pyfindphone import PhoneFinder

BRIDGE_IP = "192.168.1.2"
BRIDGE_USER = "BRIDGEUSERNAME"
PHONE_MAC = "PHONEMACADDRESS"


def toggle_lights(success, mac, name):
    lights = bridge.lights
    for light in lights:
        light.on = success


def main():
    bridge = Bridge(BRIDGE_IP, username=BRIDGE_USER)
    PhoneFinder(PHONE_MAC, toggle_lights, interval=30, on_change=True).start()


if __name__ == "__main__":
    main()
