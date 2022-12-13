import builtins
import functools
from ast import literal_eval

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

raw = aoc_helper.fetch(13, 2022)


def parse_raw(raw):
    return list(raw.split("\n\n")).mapped(
        lambda i: list(i.split("\n")).mapped(literal_eval)
    )


data = parse_raw(raw)


def compare(a, b) -> int:
    match (isinstance(a, builtins.list), isinstance(b, builtins.list)):
        case (False, False):
            return a - b
        case (True, True):
            for (a_, b_) in zip(a, b):
                result = compare(a_, b_)
                if result != 0:
                    return result
            return len(a) - len(b)
        case (True, False):
            return compare(a, [b])
        case (False, True):
            return compare([a], b)
    assert False


def part_one(data: list[list[list[int]]]):
    return (
        data.mapped(lambda l: compare(*l) < 0)
        .enumerated(1)
        .filtered(lambda i: i[1])
        .mapped(lambda i: i[0])
        .sum()
    )


aoc_helper.lazy_test(day=13, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    packets = data.flat().deepcopy()
    packets.append([[2]])
    packets.append([[6]])
    packets.sort(key=functools.cmp_to_key(compare))
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


aoc_helper.lazy_test(day=13, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=13, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=13, year=2022, solution=part_two, data=data)
