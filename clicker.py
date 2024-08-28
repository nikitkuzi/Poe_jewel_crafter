import re

import keyboard
import mouse
import time
import json
import clipboard


def get_coords():
    print(mouse.get_position())
    # return mouse.get_position()


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


def loop_click(currency, item):
    take(currency)
    use(item)


def check_click_with_regex(item, regex):
    mouse.move(*item)
    keyboard.send("ctrl+alt+c")
    time.sleep(0.1)
    clip = clipboard.paste()
    with open("log.txt", 'a') as f:
        f.write(clip)
    for reg in regex:
        if reg in clip:
            return True
    return False


def check_min_amont(*args):
    mn = 99999999
    reg = '(Stack Size: )\d,?\d*\/\d.?\d+'
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


def run_alt_spam(alt, aug, item_in_currency, regex):
    i = 0
    mn = check_min_amont(alt, aug)
    while i < mn:
        if keyboard.is_pressed("space"):
            break
        loop_click(alt, item_in_currency)
        if check_click_with_regex(item_in_currency, regex):
            break
        loop_click(aug, item_in_currency)
        if check_click_with_regex(item_in_currency, regex):
            break
        i += 1


def run_helmet_spam(alt, aug, items, regex):
    item = 0
    i = 0
    mn = check_min_amont(alt, aug)
    while i < mn and item < len(items):
        if keyboard.is_pressed("space"):
            break
        loop_click(alt, items[item])
        if check_click_with_regex(items[item], regex):
            item += 1
            break
        loop_click(aug, items[item])
        if check_click_with_regex(items[item], regex):
            item += 1
            break
        i += 1


if __name__ == '__main__':
    with open("pos_for_clicker.json") as f:
        file = json.load(f)
    with open("regex_to_find.txt") as f:
        regex = f.read().split('\n')


    # x, y pairs
    alt = file['currency tab']['alt']
    aug = file['currency tab']['aug']
    item_in_currency = file['currency tab']['item']
    pos_needed = ['pos0', 'pos2', 'pos5', 'pos7', 'pos10', 'pos12', 'pos15', 'pos17', 'pos20', 'pos22', 'pos25', 'pos27']
    items_in_inventory = [file['inventory'][pos] for pos in pos_needed]
    print(items_in_inventory)

    time.sleep(4)
    print("start")
    # run_alt_spam(alt, aug, item_in_currency, regex)
    run_helmet_spam(alt, aug, items_in_inventory, regex)
