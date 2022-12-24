import math

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

raw = aoc_helper.fetch(24, 2022)


def parse_raw(raw):
    return Grid.from_string(
        raw, lambda i: [0 for _ in range(1) if i in "^v<>"] + [".#^v<>".index(i)]
    )


data = parse_raw(raw)


def blizzard_step(map):
    next_map = Grid[list[int]](
        map.data.mapped(lambda i: i.mapped(lambda i: [j for j in i if j < 2]))
    )
    for _y, row in map.data.enumerated():
        for _x, cell in row.enumerated():
            for thing in cell:
                if thing < 2:
                    continue
                if thing == 2:
                    if _y == 1:
                        next_map[-2][_x].append(2)
                    else:
                        next_map[_y - 1][_x].append(2)
                if thing == 3:
                    if _y == len(map.data) - 2:
                        next_map[1][_x].append(3)
                    else:
                        next_map[_y + 1][_x].append(3)
                if thing == 4:
                    if _x == 1:
                        next_map[_y][-2].append(4)
                    else:
                        next_map[_y][_x - 1].append(4)
                if thing == 5:
                    if _x == len(map[0]) - 2:
                        next_map[_y][1].append(5)
                    else:
                        next_map[_y][_x + 1].append(5)
    return next_map


def pathfind(start, end, data):
    map = Grid(data.data.deepcopy())
    x, y = start
    tx, ty = end
    minute_maps = [map]
    states = PrioQueue([(abs(y - ty) + abs(x - tx), (x, y), 0, [])])
    seen = set()
    repeat = math.lcm(len(map[0]) - 2, len(map.data) - 2)
    # from tqdm import tqdm

    # state_count = tqdm()
    # progress = tqdm()
    for _, (x, y), minute, path in states:
        # state_count.update(len(states._data) - state_count.n)
        map = minute_maps[minute]
        if (x, y, minute % repeat) in seen:
            continue
        if minute + 1 == len(minute_maps):
            # progress.update(minute + 1 - progress.n)
            next_map = blizzard_step(map)
            minute_maps.append(next_map)
        else:
            next_map = minute_maps[minute + 1]
        if (x, y) == (tx, ty):
            print(path)
            return minute, map
        seen.add((x, y, minute % repeat))

        if next_map[y][x] == [0]:
            states.push(
                (
                    minute + 1 + abs(y - ty) + abs(x - tx),
                    (x, y),
                    minute + 1,
                    [*path, (x, y)],
                )
            )
        for (x, y), cell in next_map.orthogonal_neighbours(x, y):
            if cell == [0]:
                states.push(
                    (
                        minute + 1 + abs(y - ty) + abs(x - tx),
                        (x, y),
                        minute + 1,
                        [*path, (x, y)],
                    )
                )
    return 0, map


def part_one(data: Grid[list[int]]):
    map = Grid(data.data.deepcopy())
    y = 0
    x = map[0].index([0])
    tx, ty = map[-1].index([0]), len(map.data) - 1
    return pathfind((x, y), (tx, ty), map)[0]


aoc_helper.lazy_test(
    day=24,
    year=2022,
    parse=parse_raw,
    solution=part_one,
    test_data=(
        """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""",
        18,
    ),
)


def part_two(data: Grid[list[int]]):
    map = Grid(data.data.deepcopy())
    y = 0
    x = map[0].index([0])
    tx, ty = map[-1].index([0]), len(map.data) - 1
    repeat = math.lcm(len(map[0]) - 2, len(map.data) - 2)
    first, map = pathfind((x, y), (tx, ty), map)
    print(first)
    second, map = pathfind((tx, ty), (x, y), map)
    print(second)
    third, _ = pathfind((x, y), (tx, ty), map)
    print(third)
    return first + second + third


aoc_helper.lazy_test(
    day=24,
    year=2022,
    parse=parse_raw,
    solution=part_two,
    test_data=(
        """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""",
        54,
    ),
)

aoc_helper.lazy_submit(day=24, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=24, year=2022, solution=part_two, data=data)
