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
    ...


data = parse_raw(raw)


def part_one(data):
    ...


aoc_helper.lazy_test(day=12, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    ...


aoc_helper.lazy_test(day=12, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=12, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=12, year=2022, solution=part_two, data=data)
