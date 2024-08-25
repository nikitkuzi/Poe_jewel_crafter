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
    time.sleep(0.05)
    mouse.right_click()
    time.sleep(0.05)


def use(coords):
    mouse.move(*coords)
    time.sleep(0.05)
    mouse.click()
    time.sleep(0.05)


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
    reg = '(Stack Size: )\d.?\d*\/\d.?\d+'
    for item in args:
        mouse.move(*item)
        time.sleep(0.1)
        keyboard.send("ctrl+c")
        time.sleep(0.1)
        size = re.search(reg, clipboard.paste()).group(0)
        # Stack Size: 2,301/20
        amount = int(size.split(":")[1].split('/')[0].replace(',', ''))
        mn = min(mn, int(amount))
    return mn


if __name__ == '__main__':
    with open("pos_for_clicker.json") as f:
        file = json.load(f)
    with open("regex_to_find.txt") as f:
        regex = f.read().split('\n')
    alt = file['currency tab']['alt']
    aug = file['currency tab']['aug']
    item = file['currency tab']['item']

    time.sleep(4)
    i = 0
    mn = check_min_amont(alt, aug)
    while i < mn and i < 10:
        loop_click(alt, aug, item)
        if check_click_with_regex(item, regex):
            break
        i += 1
