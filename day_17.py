import itertools

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

raw = aoc_helper.fetch(17, 2022)


def parse_raw(raw):
    return raw


data = parse_raw(raw)


def part_one(data, n=2022):
    grid = Grid(list(list(False for _ in range(7)) for _ in range(5000)))
    dropped = 0
    x, y = (2, 3)
    shapes = [
        [[True, True, True, True]],
        [[False, True, False], [True, True, True], [False, True, False]],
        [[True, True, True], [False, False, True], [False, False, True]],
        [[True], [True], [True], [True]],
        [[True, True], [True, True]],
    ]
    max_y = 0
    for char in itertools.cycle(data):
        # if dropped == 0:
        #     print(x, y)
        # if dropped == 10:
        #     print(Grid(grid.data[:40][::-1]))
        if dropped == n:
            # print(Grid(grid.data[:length][::-1]))
            return max_y
        if char == ">":
            if x + len(shapes[dropped % len(shapes)][0]) < 7 and not any(
                grid[y + i][x + j + 1] and shapes[dropped % len(shapes)][i][j]
                for i in range(len(shapes[dropped % len(shapes)]))
                for j in range(len(shapes[dropped % len(shapes)][i]))
            ):
                x += 1
        else:
            if x > 0 and not any(
                grid[y + i][x + j - 1] and shapes[dropped % len(shapes)][i][j]
                for i in range(len(shapes[dropped % len(shapes)]))
                for j in range(len(shapes[dropped % len(shapes)][i]))
            ):
                x -= 1
        if y == 0 or any(
            grid[y + i - 1][x + j] and shapes[dropped % len(shapes)][i][j]
            for i in range(len(shapes[dropped % len(shapes)]))
            for j in range(len(shapes[dropped % len(shapes)][i]))
        ):
            for _y, row in enumerate(shapes[dropped % len(shapes)]):
                for _x, cell in enumerate(row):
                    if cell:
                        grid[y + _y][x + _x] = cell
                        max_y = max(max_y, y + _y + 1)
            dropped += 1
            x = 2
            y = 3 + max_y
        else:
            y -= 1


aoc_helper.lazy_test(day=17, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    grid = SparseGrid(bool)
    dropped = 0
    x, y = (2, 3)
    shapes = [
        [[True, True, True, True]],
        [[False, True, False], [True, True, True], [False, True, False]],
        [[True, True, True], [False, False, True], [False, False, True]],
        [[True], [True], [True], [True]],
        [[True, True], [True, True]],
    ]
    max_y = 0
    cycles = {}

    def state_to_key():
        look_down = [-float("inf") for _ in range(7)]
        for (x, y), cell in grid.items():
            if cell:
                look_down[x] = max(look_down[x], y)
        return (
            tuple(col - max(look_down) for col in look_down),
            dropped % len(shapes),
            c,
        )

    extra_rows = 0

    while dropped < 1000000000000:
        for c, char in enumerate(data):
            if char == ">":
                if x + len(shapes[dropped % len(shapes)][0]) < 7 and not any(
                    grid[x + j + 1, y + i] and shapes[dropped % len(shapes)][i][j]
                    for i in range(len(shapes[dropped % len(shapes)]))
                    for j in range(len(shapes[dropped % len(shapes)][i]))
                ):
                    x += 1
            else:
                if x > 0 and not any(
                    grid[x + j - 1, y + i] and shapes[dropped % len(shapes)][i][j]
                    for i in range(len(shapes[dropped % len(shapes)]))
                    for j in range(len(shapes[dropped % len(shapes)][i]))
                ):
                    x -= 1
            if y == 0 or any(
                grid[x + j, y + i - 1] and shapes[dropped % len(shapes)][i][j]
                for i in range(len(shapes[dropped % len(shapes)]))
                for j in range(len(shapes[dropped % len(shapes)][i]))
            ):
                for _y, row in enumerate(shapes[dropped % len(shapes)]):
                    for _x, cell in enumerate(row):
                        if cell:
                            grid[x + _x, y + _y] = cell
                            max_y = max(max_y, y + _y + 1)
                dropped += 1
                if state_to_key() in cycles:
                    print("found cycle")
                    old_dropped, old_max_y = cycles[state_to_key()]
                    d_dropped = dropped - old_dropped
                    d_max_y = max_y - old_max_y
                    # dropping another d_dropped pieces puts us in the same state
                    # with d_max_y more height
                    n_repeats = (1000000000000 - dropped) // d_dropped
                    dropped += n_repeats * d_dropped
                    extra_rows += n_repeats * d_max_y
                    cycles = {}
                if dropped >= 1000000000000:
                    break

                cycles[state_to_key()] = (dropped, max_y)
                x = 2
                y = 3 + max_y
            else:
                y -= 1
    return max_y + extra_rows


aoc_helper.lazy_test(day=17, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=17, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=17, year=2022, solution=part_two, data=data)
