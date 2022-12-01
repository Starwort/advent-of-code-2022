from collections import Counter

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

raw = aoc_helper.fetch(1, 2022)


def parse_raw():
    return list(raw.split("\n\n")).mapped(extract_ints)


data = parse_raw()


def part_one():
    return data.mapped(lambda l: l.sum()).max()


def part_two():
    return data.mapped(lambda l: l.sum()).sorted(reverse=True)[:3].sum()


aoc_helper.lazy_submit(day=1, year=2022, solution=part_one)
aoc_helper.lazy_submit(day=1, year=2022, solution=part_two)
