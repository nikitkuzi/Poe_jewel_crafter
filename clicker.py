import re
import random

import keyboard
import mouse
import time
import json
import clipboard
import pyperclip


def get_coords():
    while True:
        mouse.wait(button="left", target_types="down")
        print(mouse.get_position())
        if keyboard.is_pressed("space"):
            return


def take(coords):
    dx, dy = random.randint(-8, 8), random.randint(-8, 8)
    mouse.move(coords[0] + dx, coords[1] + dy)
    time.sleep(0.015)
    mouse.right_click()
    time.sleep(0.015)


def use(coords):
    dx, dy = random.randint(-8, 8), random.randint(-8, 8)
    mouse.move(coords[0] + dx, coords[1] + dy)
    time.sleep(0.015)
    mouse.click()
    time.sleep(0.015)


def loop_click(currency, item):
    take(currency)
    use(item)


def check_click_with_regex(item, regex):
    dx, dy = random.randint(-8, 8), random.randint(-8, 8)
    mouse.move(item[0] + dx, item[1] + dy)
    time.sleep(0.1)
    keyboard.send("ctrl+alt+c")
    time.sleep(0.02)
    clip = pyperclip.paste()

    with open("log.txt", 'a', encoding="utf-8") as f:
        f.write(clip)

    for reg in regex:
        if reg in clip:
            return True
    return False




def check_min_amont(args):
    mn = 99999999
    # reg = '(Stack Size: )\d,?\d*\/\d.?\d+'
    reg = '(Stack Size: )\d,?\d*\/\d+'
    for item in args:
        mouse.move(item[0], item[1])
        time.sleep(0.11)
        keyboard.send("ctrl+c")
        time.sleep(0.11)
        size = re.search(reg, clipboard.paste()).group(0)
        # Stack Size: 2,301/20
        amount = int(size.split(":")[1].split('/')[0].replace(',', ''))
        mn = min(mn, int(amount))
        pyperclip.copy(" ")
    return mn


def run_currency_spam(currency: list[str], tab: str, regex: list[str], check: bool = True,
                      pos_for_clicker: dict = None) -> None:
    """
    Perform a currency spam on an item in a tab.
    """
    i = 0
    currency_converted = [pos_for_clicker[tab][current] for current in currency]
    item_pos = pos_for_clicker[tab]['item']
    mn = check_min_amont(currency_converted)
    if check:
        while i < mn:
            if keyboard.is_pressed("space"):
                break
            for cur in currency_converted:
                loop_click(cur, item_pos)
                if check_click_with_regex(item_pos, regex):
                    return
            i += 1
    else:
        while i < mn:
            if keyboard.is_pressed("space"):
                break
            for cur in currency_converted:
                loop_click(cur, item_pos)
            i += 1


def run_inventory_spam(currency: list[str], tab: str, items: list[list[str, str]], regex: list[str],
                       check: bool = True):
    """
    Performs currency spam in the inventory from selected tab at selected positions
    """
    item = 0
    i = 0
    currency_converted = [pos_for_clicker[tab][current] for current in currency]
    mn = check_min_amont(currency_converted)
    if check:
        while i < mn and item < len(items):
            if keyboard.is_pressed("space"):
                break
            for cur in currency_converted:
                loop_click(cur, items[item])
                if check_click_with_regex(items[item], regex):
                    item += 1
                    i += 1
                    time.sleep(1)
                    break
            i += 1
    else:
        while i < mn:
            if keyboard.is_pressed("space"):
                break
            for cur in currency_converted:
                loop_click(cur, items[item])
                item = (item + 1) % len(items)
            i += 1


if __name__ == '__main__':
    with open("pos_for_clicker.json") as f:
        pos_for_clicker = json.load(f)
    with open("regex_to_find.txt") as f:
        regex = f.read().split('\n')

    # pos_needed = ['pos0', 'pos2', 'pos10', 'pos12', 'pos20', 'pos22', 'pos30', 'pos32', 'pos40', 'pos42', 'pos50', 'pos52']
    # pos_needed = ['pos0', 'pos5', 'pos10', 'pos15', 'pos20', 'pos25', 'pos30', 'pos35', 'pos40', 'pos45', 'pos50', 'pos55']
    # pos_needed = ['pos0', 'pos10', 'pos20', 'pos30', 'pos40', "pos50"]
    # pos_needed = ['pos0', 'pos5', 'pos10']
    # pos_needed = ['pos0','pos10','pos20','pos30','pos40','pos50']
    # pos_needed = ['pos0', 'pos2', 'pos10']
    pos_needed = ['pos0', 'pos5']
    items_in_inventory = [pos_for_clicker['inventory'][pos] for pos in pos_needed]
    time.sleep(2)
    print("start")

    # run_currency_spam(["chance", "scour"], item_in_currency, regex, check=False, pos_for_clicker=pos_for_clicker)
    run_currency_spam(["alt", "aug"], "currency tab", regex, check=True, pos_for_clicker=pos_for_clicker)
    # run_currency_spam(["Hatred"], "essence tab", regex, check=True, pos_for_clicker=pos_for_clicker)
    # run_inventory_spam(["alt", "aug"], "currency tab", items_in_inventory, regex, check=True)
