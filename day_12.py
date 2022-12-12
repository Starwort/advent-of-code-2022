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


def part_one(data):
    grid, pos, target = data
    return grid.pathfind(pos, target, lambda i, j: j - i <= 1, lambda i, j: 1)


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
