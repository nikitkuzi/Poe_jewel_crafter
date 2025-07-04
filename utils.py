import re
import random

import keyboard
import mouse
import time
import json
import clipboard
import pyperclip
from json.decoder import JSONDecodeError


class CoordsGenerator:
    supported_coords = {"inventory": "_get_inventory_coords"}

    def __init__(self, target_to_chage: str, json_file: json = None):
        if target_to_chage not in self.supported_coords:
            print("Not Supported coord space")
        else:
            self.target = target_to_chage
            self.file = json_file

    def get_coords(self) -> dict[str, list[int, int]]:
        method = getattr(self, self.supported_coords[self.target])
        return method()

    def _get_inventory_coords(self) -> dict[str, list[int, int]]:
        x_coord_middle = 1725
        y_coord_middle = 818
        shift = 70
        new_coords = {}
        for i in range(12):
            for j in range(5):
                new_coords[f"pos{i * 5 + j}"] = [x_coord_middle + shift * i, y_coord_middle + shift * j]
        return new_coords


def get_coords_by_clicking() -> list[tuple[int, int]]:
    coords = []
    while True:
        mouse.wait(button="left", target_types="down")
        print(mouse.get_position())
        coords.append(mouse.get_position())
        if keyboard.is_pressed("space"):
            break
    return coords


def change_coords(target_to_change: str) -> None:
    try:
        with open("pos_for_clicker.json", 'r+') as file:
            pos_for_clicker = json.load(file)
            new_coords = CoordsGenerator(target_to_change).get_coords()
            pos_for_clicker[target_to_change] = new_coords
            file.seek(0)
            json.dump(pos_for_clicker, file, indent=4)
            file.truncate()
    except FileNotFoundError:
        print("File not found")
    except JSONDecodeError:
        print("File is empty")
    else:
        print(f"Updated coords of {target_to_change} successfully")


change_coords("inventory")
