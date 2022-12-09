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

raw = aoc_helper.fetch(8, 2022)


def parse_raw(raw):
    return Grid.from_string(raw)


data = parse_raw(raw)


def part_one(data: Grid[int]):
    visible = list(list(False for _ in row) for row in data)
    for y, row in enumerate(data.data):
        for x, height in enumerate(row):
            if (
                not row[:x]
                or row[:x].max() < height
                or not row[x + 1 :]
                or row[x + 1 :].max() < height
            ):
                visible[y][x] = True
    for x, row in enumerate(data.transpose().data):
        for y, height in enumerate(row):
            if (
                not row[:x]
                or row[:x].max() < height
                or not row[x + 1 :]
                or row[x + 1 :].max() < height
            ):
                visible[y][x] = True
    return visible.mapped(sum).sum()


aoc_helper.lazy_test(day=8, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    scores = list(list(1 for _ in row) for row in data)
    for y, row in enumerate(data.data):
        for x, height in enumerate(row):
            count = 0
            for x_ in range(x - 1, -1, -1):
                count += 1
                if data[y][x_] >= data[y][x]:
                    break
            scores[y][x] *= count
            count = 0
            for x_ in range(x + 1, len(data[0])):
                count += 1
                if data[y][x_] >= data[y][x]:
                    break
            scores[y][x] *= count
    for x in range(len(data.data[0])):
        for y in range(len(data.data)):
            count = 0
            for y_ in range(y - 1, -1, -1):
                count += 1
                if data[y_][x] >= data[y][x]:
                    break
            scores[y][x] *= count
            count = 0
            for y_ in range(y + 1, len(data.data)):
                count += 1
                if data[y_][x] >= data[y][x]:
                    break
            scores[y][x] *= count
    return scores.mapped(max).max()


aoc_helper.lazy_test(day=8, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=8, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=8, year=2022, solution=part_two, data=data)
