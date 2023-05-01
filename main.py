import json
import random
import clipboard
import keyboard
import mouse
import pyautogui
import time
import re
import requests

PRICE_TRESHOLD = 70

def read_positions(filename):
    """Read inventory coordinates where:
        0 - resonator;
        1 - fossil;
        2-5 - second colon of jewewls;
        6-46 - inventory cooordinates"""

    with open(filename, "r") as positions:
        return [list(map(int, line.split(","))) for line in positions.read().splitlines()]

def fill_resonators():
    for i in range(4):
        go_to_resonator()
        mouse.click("left")
        keyboard.press("shift")
        for j in range(1, 11):
            mouse.move(positions[6+j+10*i][0], positions[6+j+10*i][1], duration=0.015)
            time.sleep(0.05)
            mouse.click()
        keyboard.release("shift")
        time.sleep(0.05)


def fill_fossils():
    for i in range(2):
        go_to_fossil()
        mouse.click("left")
        keyboard.press("shift")
        for j in range(1, 21):
            mouse.move(positions[6+j+20*i][0], positions[6+j+20*i][1], duration=0.015)
            time.sleep(0.05)
            mouse.click()
        keyboard.release("shift")
        time.sleep(0.05)

def go_to_resonator():
    mouse.move(positions[0][0], positions[0][1], duration=0.09)
    time.sleep(0.2)

def go_to_fossil():
    mouse.move(positions[1][0], positions[1][1], duration=0.09)
    time.sleep(0.2)

def check_jewel():
    time.sleep(0.2)
    keyboard.send("ctrl+c")
    #time.sleep(0.5)
    time.sleep(0.2)
    if len(re.findall("1 Added Passive Skill is*", clipboard.paste())) == 3:
        passives = format_jewel()
        if check_price(passives):
            print("Good Price")
            clipboard.copy('0')
            return True
        else:
            print("Low Price")
        time.sleep(0.2)
    return False

def craft_jewel(amount):
    current_fossil = 0
    current_jewel = 0
    while True:
        if current_fossil == 40:
            current_fossil = 0
            time.sleep(3)
            fill_resonators()
            fill_fossils()
        if current_jewel == amount:
            break
        mouse.move(positions[current_fossil + 7][0] + random.randint(-8, 8), positions[current_fossil + 7][1] + random.randint(-8, 8), duration=0.015)
        time.sleep(0.05)
        mouse.click("right")

        mouse.move(positions[current_jewel + 2][0] + random.randint(-8, 8), positions[current_jewel + 2][1] + random.randint(-8, 8), duration=0.015)
        time.sleep(0.05)
        mouse.click("left")
        time.sleep(0.01)

        #time.sleep(3)
        current_fossil += 1
        if check_jewel() is True:
            current_jewel += 1
            #break
            continue

def check_price(passives=None):
    url = "https://www.pathofexile.com/api/trade/search/Crucible"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'POESESSID': '9533aa1d4d979bf05b44d210763f702a'
    }
    qr = {
        "query": {
            "status": {
                "option": "online"
            },
            "stats": [{
                "type": "and",
                "filters": [passives[0], passives[1], passives[2]]
                #"filters": [{"id":"explicit.stat_1616734644"}, {"id":"explicit.stat_1603621602"}, {"id":"explicit.stat_729163974"}]
            }]
        },
        "sort": {
            "price": "asc"
    }
}
    req = requests.post(url, json=qr, headers=headers)
    conts = json.loads(req.content)
    #req = requests.post(url1)
    url2 = "https://www.pathofexile.com/api/trade/fetch/"
    amount_to_check = 5
    if len(conts["result"]) < 5:
        amount_to_check = len(conts["result"])
    url2 += ",".join(conts["result"][:amount_to_check]) +"?query=" + conts["id"]
    req2 = requests.get(url2, headers=headers)
    items = json.loads(req2.content)
    items_to_check = []
    for i in range(amount_to_check):
        items_to_check.append(items["result"][i]["listing"]["price"]['amount'])
        if items["result"][i]["listing"]["price"]['currency'] == "divine":
            items_to_check[i] *= 220
    print("price:", sum(items_to_check) / amount_to_check)
    if (sum(items_to_check) / amount_to_check) > PRICE_TRESHOLD:
        print((sum(items_to_check) / amount_to_check))
        return True
    return False


def format_jewel():
    """returns: list of ids of passives"""
    passives = [a.split("\n")[:3][0].strip() for a in re.split("1 Added Passive Skill is*", clipboard.paste())[1:]]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'POESESSID': '9533aa1d4d979bf05b44d210763f702a'
    }
    url = "https://www.pathofexile.com/api/trade/data/stats"
    data = json.loads(requests.get(url, headers=headers).content)["result"][1]["entries"]
    passives_ids = []
    for i in range(3):
        passives_ids.append(next(item for item in data if item["text"] == f"1 Added Passive Skill is {passives[i]}"))
    for i in range(3):
        del passives_ids[i]["text"]
        del passives_ids[i]["type"]
    return passives_ids

if __name__ == "__main__":
    #setpos()
    positions = read_positions("pos.txt")
    amount_to_craft = 4
    time.sleep(2)
    fill_resonators()
    fill_fossils()
    craft_jewel(amount_to_craft)


