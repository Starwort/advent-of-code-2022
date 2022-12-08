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

raw = aoc_helper.fetch(6, 2022)


def parse_raw():
    return list(raw)


data = parse_raw()


def part_one(data: list[str]):
    return (
        raw.index("".join(data.windowed(4).filtered(lambda i: len(set(i)) == 4).find()))
        + 4
    )


def part_two(data: list[str]):
    return (
        raw.index(
            "".join(data.windowed(14).filtered(lambda i: len(set(i)) == 14).find())
        )
        + 14
    )


aoc_helper.lazy_submit(day=6, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=6, year=2022, solution=part_two, data=data)
