import re
import random

import keyboard
import mouse
import time
import json
import clipboard
import pyperclip


def get_coords():
    print(mouse.get_position())
    # return mouse.get_position()


def take(coords):
    dx, dy = random.randint(-10, 10), random.randint(-10, 10)
    mouse.move(coords[0] + dx, coords[1] + dy)
    time.sleep(0.015)
    mouse.right_click()
    time.sleep(0.015)


def use(coords):
    dx, dy = random.randint(-10, 10), random.randint(-10, 10)
    mouse.move(coords[0] + dx, coords[1] + dy)
    time.sleep(0.015)
    mouse.click()
    time.sleep(0.015)


def loop_click(currency, item):
    take(currency)
    use(item)


def check_click_with_regex(item, regex):
    dx, dy = random.randint(-10, 10), random.randint(-10, 10)
    mouse.move(item[0] + dx, item[1] + dy)
    time.sleep(0.1)
    keyboard.send("ctrl+alt+c")
    time.sleep(0.02)
    clip = pyperclip.paste()

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
        mouse.move(item[0], item[1])
        time.sleep(0.1)
        keyboard.send("ctrl+c")
        time.sleep(0.1)
        size = re.search(reg, clipboard.paste()).group(0)
        # Stack Size: 2,301/20
        amount = int(size.split(":")[1].split('/')[0].replace(',', ''))
        mn = min(mn, int(amount))
        pyperclip.copy(" ")
    return mn


def run_currency_spam(currency1, currency2, item_in_currency, regex, check=True):
    i = 0
    mn = check_min_amont(currency1, currency2)
    if check:
        while i < mn:
            if keyboard.is_pressed("space"):
                break
            loop_click(currency1, item_in_currency)
            if check_click_with_regex(item_in_currency, regex):
                break
            loop_click(currency2, item_in_currency)
            if check_click_with_regex(item_in_currency, regex):
                break
            i += 1
    else:
        while i < mn:
            if keyboard.is_pressed("space"):
                break
            loop_click(currency1, item_in_currency)
            loop_click(currency2, item_in_currency)
            i += 1


def run_inventory_spam(alt, aug, items, regex):
    item = 0
    i = 0
    mn = check_min_amont(alt, aug)
    while i < mn and item < len(items):
        if keyboard.is_pressed("space"):
            break
        loop_click(alt, items[item])
        if check_click_with_regex(items[item], regex):
            item += 1
            i += 1
            time.sleep(1)
            continue
        loop_click(aug, items[item])
        if check_click_with_regex(items[item], regex):
            item += 1
            i += 1
            time.sleep(1)
            continue
        i += 1


if __name__ == '__main__':
    with open("pos_for_clicker.json") as f:
        file = json.load(f)
    with open("regex_to_find.txt") as f:
        regex = f.read().split('\n')

    # x, y pairs
    alt = file['currency tab']['alt']
    aug = file['currency tab']['aug']
    chance = file['currency tab']['chance']
    scour = file['currency tab']['scour']

    item_in_currency = file['currency tab']['item']
    # pos_needed = ['pos0', 'pos2', 'pos10', 'pos12', 'pos20', 'pos22', 'pos30', 'pos32', 'pos40', 'pos42', 'pos50', 'pos52']
    # pos_needed = ['pos0', 'pos5', 'pos10', 'pos15', 'pos20', 'pos25', 'pos30', 'pos35', 'pos40', 'pos45', 'pos50', 'pos55']
    # pos_needed = ['pos0', 'pos5', 'pos10']
    # pos_needed = ['pos0','pos10','pos20','pos30','pos40','pos50']
    # pos_needed = ['pos0', 'pos2', 'pos10']
    pos_needed = ['pos0', 'pos2']
    items_in_inventory = [file['inventory'][pos] for pos in pos_needed]
    time.sleep(2)
    print("start")
    # run_currency_spam(alt, aug, item_in_currency, regex)
    run_currency_spam(chance, scour, item_in_currency, regex, check=False)
    # run_inventory_spam(alt, aug, items_in_inventory, regex)
