from collections import Counter
from itertools import count

import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    SparseGrid,
    decode_text,
    extract_ints,
    extract_iranges,
    extract_ranges,
    extract_uints,
    frange,
    irange,
    iter,
    list,
    map,
    range,
    tail_call,
)

raw = aoc_helper.fetch(23, 2022)


def parse_raw(raw):
    data = SparseGrid(bool)
    for y, row in enumerate(raw.splitlines()):
        for x, char in enumerate(row):
            data[x, y] = char == "#"
    return data


data = parse_raw(raw)


def decide(data, x, y, turn):
    if not any(data[x + i, y + j] for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j):
        return x, y
    options = [
        (
            [data[x - 1, y - 1], data[x, y - 1], data[x + 1, y - 1]],
            x,
            y - 1,
        ),
        ([data[x - 1, y + 1], data[x, y + 1], data[x + 1, y + 1]], x, y + 1),
        ([data[x - 1, y - 1], data[x - 1, y], data[x - 1, y + 1]], x - 1, y),
        (
            [data[x + 1, y - 1], data[x + 1, y], data[x + 1, y + 1]],
            x + 1,
            y,
        ),
    ]
    # print(x, y)
    for option in options[turn - 4 :] + options[:turn]:
        # print(option)
        if not any(option[0]):
            return option[1], option[2]
    return x, y


def part_one(_data: SparseGrid[bool]):
    data = SparseGrid(bool)
    data.data.update(_data.data)
    for round in range(10):
        # print(f"Round {round}")
        # data.pretty_print(lambda I: ".#"[I], [False])
        elf_decisions = {
            (x, y): decide(data, x, y, round % 4)
            for (x, y), is_elf in list(data.items())
            if is_elf
        }
        chosen_per_square = Counter(elf_decisions.values())
        for (x, y), (new_x, new_y) in elf_decisions.items():
            if chosen_per_square[new_x, new_y] == 1:
                data[x, y] = False
                data[new_x, new_y] = True
    x, y, max_x, max_y = data.bounds([False])
    # data.pretty_print(lambda I: ".#"[I], [False])
    return (max_y - y + 1) * (max_x - x + 1) - sum(data.values())


aoc_helper.lazy_test(
    day=23,
    year=2022,
    parse=parse_raw,
    solution=part_one,
    test_data=(
        """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............""",
        110,
    ),
)


def part_two(_data):
    data = SparseGrid(bool)
    data.data.update(_data.data)
    for round in count(1):
        # print(f"Round {round}")
        # data.pretty_print(lambda I: ".#"[I], [False])
        elf_decisions = {
            (x, y): decide(data, x, y, round % 4)
            for (x, y), is_elf in list(data.items())
            if is_elf
        }
        if all(from_ == to for (from_, to) in elf_decisions.items()):
            return round
        chosen_per_square = Counter(elf_decisions.values())
        for (x, y), (new_x, new_y) in elf_decisions.items():
            if chosen_per_square[new_x, new_y] == 1:
                data[x, y] = False
                data[new_x, new_y] = True


# aoc_helper.lazy_test(day=23, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=23, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=23, year=2022, solution=part_two, data=data)
