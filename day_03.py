import string

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

raw = aoc_helper.fetch(3, 2022)


def parse_raw():
    return list(raw.splitlines()).mapped_each(
        lambda i: (
            (ord(i) - ord("a"))
            if i in string.ascii_lowercase
            else (ord(i) - ord("A") + 26)
        )
        + 1
    )


data = parse_raw()


def process_sack(sack):
    first_half, second_half = sack[: len(sack) // 2], sack[len(sack) // 2 :]
    for i in first_half:
        if i in second_half:
            return i


def part_one():
    return data.mapped(process_sack).sum()


def part_two():
    groups = data.chunked(3)
    sum = 0
    for first, second, third in groups:
        for i in first:
            if i in second and i in third:
                sum += i
                break
    return sum


aoc_helper.lazy_submit(day=3, year=2022, solution=part_one)
aoc_helper.lazy_submit(day=3, year=2022, solution=part_two)
