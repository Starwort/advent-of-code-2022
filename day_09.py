import collections

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

raw = aoc_helper.fetch(9, 2022)

VECTOR = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def parse_raw(raw: str):
    return (
        list(raw.splitlines())
        .mapped(lambda i: i.split())
        .mapped(lambda i: (VECTOR[i[0]], int(i[1])))
    )


data = parse_raw(raw)


def move_towards(dest, src):
    dx, dy = dest
    sx, sy = src
    if dx > sx:
        sx += 1
    elif dx < sx:
        sx -= 1
    if dy > sy:
        sy += 1
    elif dy < sy:
        sy -= 1
    return sx, sy


def part_one(data):
    visited = collections.defaultdict(bool)
    head = (0, 0)
    tail = (0, 0)
    for direction, distance in data:
        for _ in range(distance):
            head = (head[0] + direction[0], head[1] + direction[1])
            if list(zip(head, tail)).mapped(lambda i: abs(i[0] - i[1])).max() > 1:
                tail = move_towards(head, tail)
            visited[tail] = True
    return len(visited)


aoc_helper.lazy_test(day=9, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    visited = collections.defaultdict(bool)
    head = (0, 0)
    tails = [(0, 0)] * 9
    for direction, distance in data:
        for _ in range(distance):
            head = (head[0] + direction[0], head[1] + direction[1])
            for i, (prev, next) in list([head, *tails]).windowed(2).enumerated():
                if list(zip(prev, next)).mapped(lambda i: abs(i[0] - i[1])).max() > 1:
                    tails[i] = move_towards(prev, next)
            visited[tails[-1]] = True
    return len(visited)


aoc_helper.lazy_test(day=9, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=9, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=9, year=2022, solution=part_two, data=data)
