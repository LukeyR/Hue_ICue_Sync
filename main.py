import threading
import time
from phue import Bridge
from cuesdk import CueSdk



def get_hue_lights_from_file(bridge, dir):
    """Retrieves lights to control from file

    Will read file "light_names.txt" in specified directory.
    Add lights to control as a line of text in this file.
    Comments must start with a '#' and ech light must have its own line.

    Args:
        bridge: A 'Bridge' class
        dir: Directory of file to read

    returns:
        List containing phue.light objects
    """
    lights_as_object = bridge.get_light_objects()
    lights_names = []
    with open(dir, 'r') as f:
        for line in f:
            if line[0] == "#":
                continue
            else:
                lights_names.append(str.rstrip(line))
    to_return = []
    for light in lights_as_object:
        if light.name in lights_names:
            to_return.append(light)
    return to_return


def get_available_leds():
    leds = list()
    device_count = sdk.get_device_count()
    for device_index in range(device_count):
        led_positions = sdk.get_led_positions_by_device_index(device_index)
        leds.append(led_positions)
    return leds


def hue_flash_lights(lights, run_time):
    """Will flash Hue lights, on/off, for a specified time

    Leave run_time as 0 for indefinite loop

    Args:
        lights: List of light objects
        run_time: Time, in seconds, to flash lights for
    """
    start = time.time()
    while True:
        if time.time() - run_time >= start and run_time > 0:
            break
        for light in lights:
            light.on = not light.on
            if light.on:
                light.brightness = 254
        time.sleep(0.8)

def set_all_devices_colour(colour):
    "Colour is a tuple of type (int, int, int) where: 0 <= int <= 265"
    allLEDs = get_available_leds()
    for deviceID in range(len(allLEDs)):
        device = allLEDs[deviceID]
        for led in device:
            device[led] = colour
        sdk.set_led_colors_buffer_by_device_index(deviceID, device)
    sdk.set_led_colors_flush_buffer()
    time.sleep(1/100)


def cue_rainbow_cycle(iterations):
    "30 is not arbitrary, its the number of loops needed to complete one RGB cycle"
    inc = 17
    r = 255
    g = 0
    b = 0
    for i in range(30 * iterations):
        print("colour (%s,%s,%s)" % (r, g, b))
        set_all_devices_colour((r, g, b))
        if r == 255:
            if b > 0:
                b -= inc
                continue
            elif g < 255:
                g += inc
                continue
        if g == 255:
            if r > 0:
                r -= inc
                continue
            elif b < 255:
                b += inc
                continue
        if b == 255:
            if g > 0:
                g -= inc
                continue
            elif r < 255:
                r += inc
                continue
    print("colour (%s,%s,%s)" % (r, g, b))
    set_all_devices_colour((r, g, b))


if __name__ == "__main__":
    # Set-Up Hues
    # b = Bridge("192.168.0.11")
    # lights_object = b.get_light_objects()
    # luke_room = get_hue_lights_from_file(b, "light_names.txt")

    # hue_flash_lights(luke_room, 10)

    # Set-Up CUE
    sdk = CueSdk()
    connected = sdk.connect()
    if not connected:
        err = sdk.get_last_error()
        print("Handshake failed: %s" % err)

    cue_rainbow_cycle(6)




# TODO
#   Threads
#   Speed adjustment
