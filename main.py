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


if __name__ == "__main__":
    b = Bridge("192.168.0.11")
    lights_object = b.get_light_objects()
    luke_room = get_hue_lights_from_file(b, "light_names.txt")
    hue_flash_lights(luke_room, 10)

# TODO
#   Sort out light exclusivity
