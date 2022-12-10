import random
from itertools import count
from os import listdir
from sys import argv

from PIL import Image
from tqdm import tqdm

x = 1
with open(argv[1], "w") as f:
    for file in tqdm(sorted(listdir("frames"))):
        instructions = []
        img = Image.open(f"frames/{file}").convert("1")
        data: list[int] = list(img.getdata())
        frame_cycles = 0
        frame_length = img.width * img.height
        # Always blank for at least 1 cycle. If frame_length is 1 less than a power
        # of 2, this code will crash :( (but it's not worth fixing)
        frame_total: int = next(2**i for i in count() if 2**i > frame_length)
        frame_blank = frame_total - frame_length
        n_addx, n_noop = divmod(frame_blank, 2)
        n_addx_steal = random.randrange(n_addx // 2)
        n_addx -= n_addx_steal
        n_noop += 2 * n_addx_steal
        for i in range(n_addx - 1):
            dx = random.randint(-img.width * 2, img.width * 2)
            x += dx
            instructions.append(f"addx {dx}\n")
        for i in range(n_noop):
            instructions.append("noop\n")
        random.shuffle(instructions)
        f.write("".join(instructions))
        for i in range(0, frame_length, 2):
            match data[i : i + 2]:
                case (False, False):
                    if abs((i % img.width) + 0.5 - x) <= 1.5 or random.random() < 0.6:
                        targets = [
                            *range(-img.width, i - 1),
                            *range(i + 2, img.width * 2),
                        ]
                        new_pos = random.choice(targets)
                        f.write(f"addx {new_pos-x}\n")
                        x = new_pos
                    else:
                        f.write("noop\n")
                        f.write("noop\n")
                case (False, True):
                    new_pos = (i % img.width) + 2
                    f.write(f"addx {new_pos-x}\n")
                    x = new_pos
                case (True, False):
                    new_pos = (i % img.width) - 1
                    f.write(f"addx {new_pos-x}\n")
                    x = new_pos
                case (True, True):
                    new_pos = random.randint((i % img.width), (i % img.width) + 1)
                    f.write(f"addx {new_pos-x}\n")
                    x = new_pos
