import time

from phue import Bridge
from cuesdk import CueSdk


def initialise_hue():
    b = Bridge("192.168.0.11")
    return b.get_light_objects()


lights_object = initialise_hue()
i = 0
for j in range(10):
    for light in lights_object:
        light.brightness = i
    print(i)
    i = (i + 25) % 255
    time.sleep(0.2)
