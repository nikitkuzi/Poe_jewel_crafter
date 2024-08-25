import re

import keyboard
import mouse
import time
import json
import clipboard


def get_coords():
    time.sleep(4)
    return mouse.get_position()


def take(coords):
    mouse.move(*coords)
    time.sleep(0.1)
    mouse.right_click()
    time.sleep(0.1)


def use(coords):
    mouse.move(*coords)
    time.sleep(0.1)
    mouse.click()
    time.sleep(0.1)


def loop_click(alt, aug, item):
    take(alt)
    use(item)
    take(aug)
    use(item)


def check_click_with_regex(item, regex):
    mouse.move(*item)
    keyboard.send("ctrl+alt+c")
    time.sleep(0.1)
    clip = clipboard.paste()
    for reg in regex:
        if reg in clip:
            return True
    return False

def check_min_amont(*args):
    mn = 99999999
    reg = re.Pattern()
    for item in args:
        mouse.move(*item)
        keyboard.send("ctrl+c")



if __name__ == '__main__':
    with open("pos_for_clicker.json") as f:
        file = json.load(f)
    with open("regex_to_find.txt") as f:
        regex = f.read().split('\n')
    alt = file['currency tab']['alt']
    aug = file['currency tab']['aug']
    item = file['currency tab']['item']

    time.sleep(4)



