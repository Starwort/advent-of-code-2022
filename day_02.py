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

raw = aoc_helper.fetch(2, 2022)

# raw = """A Y
# B X
# C Z"""


def parse_raw():
    return list(raw.splitlines()).mapped(str.split)


data = parse_raw()


def part_one(data):
    score = 0
    for move, resp in data:
        score += " XYZ".index(resp)
        score += 3 * ("ABC".index(move) == "XYZ".index(resp))
        score += 6 * ("CAB".index(move) == "XYZ".index(resp))
    return score


def part_two(data):
    score = 0
    for move, outcome in data:
        if outcome == "X":
            resp = "ZXY"["ABC".index(move)]
        if outcome == "Y":
            resp = "XYZ"["ABC".index(move)]
        if outcome == "Z":
            resp = "YZX"["ABC".index(move)]
        score += " XYZ".index(resp)
        score += 3 * ("ABC".index(move) == "XYZ".index(resp))
        score += 6 * ("CAB".index(move) == "XYZ".index(resp))
    return score


aoc_helper.lazy_submit(day=2, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=2, year=2022, solution=part_two, data=data)
