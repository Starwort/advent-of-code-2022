import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    decode_text,
    extract_ints,
    frange,
    irange,
    iter,
    list,
    map,
    range,
    tail_call,
)

raw = aoc_helper.fetch(12, 2022)


def parse_raw(raw):
    return (
        Grid.from_string(
            raw,
            classify=lambda i: (ord("az"["SE".index(i)]) - ord("a"))
            if i in "SE"
            else (ord(i) - ord("a")),
        ),
        next(
            next((x, y) for x, i in enumerate(row) if i == "S")
            for y, row in enumerate(raw.splitlines())
            if "S" in row
        ),
        next(
            next((x, y) for x, i in enumerate(row) if i == "E")
            for y, row in enumerate(raw.splitlines())
            if "E" in row
        ),
    )


data = parse_raw(raw)


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def log(val):
    # print(val)
    return val


def part_one(data):
    grid, pos, target = data
    visited = set()
    options = PrioQueue([(0, dist(pos, target), pos, [pos])])
    for weight, _, (x, y), prevs in options:
        # print(weight, _, x, y)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) == target:
            # print(prevs)
            return weight
        node_value = grid[y][x]
        if x > 0 and (log(grid[y][x - 1] - node_value)) <= 1:
            options.push(
                (weight + 1, dist((x - 1, y), target), (x - 1, y), prevs + [(x - 1, y)])
            )
        if x < len(grid.data[0]) - 1 and (log(grid[y][x + 1] - node_value)) <= 1:
            options.push(
                (weight + 1, dist((x + 1, y), target), (x + 1, y), prevs + [(x + 1, y)])
            )
        if y > 0 and (log(grid[y - 1][x] - node_value)) <= 1:
            options.push(
                (weight + 1, dist((x, y - 1), target), (x, y - 1), prevs + [(x, y - 1)])
            )
        if y < len(grid.data) - 1 and (log(grid[y + 1][x] - node_value)) <= 1:
            options.push(
                (weight + 1, dist((x, y + 1), target), (x, y + 1), prevs + [(x, y + 1)])
            )
        # print(options._data)


raw_t = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
data_t = parse_raw(raw_t)

aoc_helper.lazy_test(day=12, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    grid, _, target = data
    return min(
        val if (val := part_one((grid, (x, y), target))) else 99999
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if cell == 0
    )


aoc_helper.lazy_test(day=12, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=12, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=12, year=2022, solution=part_two, data=data)
