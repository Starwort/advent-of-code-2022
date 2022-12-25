import itertools
import math

import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    SparseGrid,
    decode_text,
    extract_ints,
    extract_iranges,
    extract_ranges,
    extract_uints,
    frange,
    irange,
    iter,
    list,
    map,
    range,
    tail_call,
)

raw = aoc_helper.fetch(25, 2022)


def parse_raw(raw: str):
    return list(raw.translate(str.maketrans("210-=", "43210")).splitlines()).mapped(
        lambda i: sum((int(dig) - 2) * 5**val for val, dig in enumerate(i[::-1]))
    )


data = parse_raw(raw)


def parse(result):
    return sum(
        (int(dig) - 2) * 5**val
        for val, dig in enumerate(
            result.translate(str.maketrans("210-=", "43210"))[::-1]
        )
    )


def unparse(n):
    if n == 0:
        return ""
    match n % 5:
        case 0:
            return unparse(n // 5) + "0"
        case 1:
            return unparse(n // 5) + "1"
        case 2:
            return unparse(n // 5) + "2"
        case 3:
            return unparse((n + 2) // 5) + "="
        case 4:
            return unparse((n + 1) // 5) + "-"


def part_one(data):
    target = sum(data)
    # digits = int(math.log2(target) / math.log2(5))
    # for comb in itertools.product("210-=", repeat=digits + 1):
    #     if comb[0] != 1:
    #         continue
    #     result = "".join(comb)
    #     if parse(result) == target:
    #         return result
    return unparse(target)
    # print(target, result, parse(result))


aoc_helper.lazy_test(day=25, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    ...


# aoc_helper.lazy_test(day=25, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=25, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=25, year=2022, solution=part_two, data=data)
