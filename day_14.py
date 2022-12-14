from collections import defaultdict

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

raw = aoc_helper.fetch(14, 2022)


def parse_raw(raw):
    return list(raw.splitlines()).mapped(extract_ints).mapped(lambda i: i.chunked(2))


data = parse_raw(raw)


def place_grain(graph, bottom, left, right, p2=False):
    x, y = 500, 0
    while True:
        if graph[x, y + 1] == 0:
            y += 1
        elif graph[x - 1, y + 1] == 0:
            x -= 1
            y += 1
        elif graph[x + 1, y + 1] == 0:
            x += 1
            y += 1
        else:
            graph[x, y] = 2
            return False
        if y > bottom:
            if not p2:
                return True
            else:
                graph[x, y] = 2
                return False
        if not p2:
            if x < left or x > right:
                return True


def part_one(data):
    graph = defaultdict(int)
    for path in data:
        for (fx, fy), (tx, ty) in path.windowed(2):
            for y in irange(fy, ty):
                for x in irange(fx, tx):
                    graph[(x, y)] = 1
    left = min([x for x, y in graph])
    right = max([x for x, y in graph])
    bottom = max([y for x, y in graph])
    while not place_grain(graph, bottom, left, right):
        pass
    return list(graph.values()).count(2)


aoc_helper.lazy_test(day=14, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    graph = defaultdict(int)
    for path in data:
        for (fx, fy), (tx, ty) in path.windowed(2):
            for y in irange(fy, ty):
                for x in irange(fx, tx):
                    graph[(x, y)] = 1
    left = min([x for x, y in graph])
    right = max([x for x, y in graph])
    bottom = max([y for x, y in graph])
    while graph[500, 0] == 0:
        place_grain(graph, bottom, left, right, p2=True)
    return list(graph.values()).count(2)


aoc_helper.lazy_test(day=14, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=14, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=14, year=2022, solution=part_two, data=data)
