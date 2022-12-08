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

raw = aoc_helper.fetch(4, 2022)


def parse_raw():
    return (
        list(raw.splitlines())
        .mapped(lambda i: i.split(","))
        .mapped_each(lambda i: list(map(int, i.split("-"))))
    )


data = parse_raw()


def part_one(data):
    count = 0
    for a, b in data:
        if a[0] >= b[0] and a[1] <= b[1]:
            count += 1
        elif b[0] >= a[0] and b[1] <= a[1]:
            count += 1
    return count


def part_two(data):
    count = 0
    for a, b in data:
        if b[0] <= a[0] <= b[1]:
            count += 1
        elif a[0] <= b[0] <= a[1]:
            count += 1
    return count


aoc_helper.lazy_submit(day=4, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=4, year=2022, solution=part_two, data=data)
