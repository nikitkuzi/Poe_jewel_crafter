import keyboard
import mouse
import time


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


if __name__ == '__main__':
    with open("pos_for_clicker.txt") as f:
        print(f.readline())
        print(f.readline())
        print(f.readline())
        exit(0)
        alt = [int(a) for a in f.readline()[1:-2].split(",")]
        item = [int(a) for a in f.readline()[1:-2].split(",")]
        aug = [int(a) for a in f.readline()[1:-1].split(",")]
        print(alt, item, aug)
    # while True:
    time.sleep(4)
    # while True:
    # take(alt)
    # use(item)
    # take(aug)
    # use(item)
    i = 0
    mouse.on_click(loop_click, (alt, aug, item))
    while i < 10:
        time.sleep(0.5)
        i += 1
