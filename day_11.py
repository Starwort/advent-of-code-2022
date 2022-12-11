import math

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

raw = aoc_helper.fetch(11, 2022)


def parse_one(raw):
    _, starting, op, test, true, false = raw.splitlines()
    return {
        "items": extract_ints(starting),
        "op": op.removeprefix("  Operation: "),
        "test": extract_ints(test)[0],
        "true": extract_ints(true)[0],
        "false": extract_ints(false)[0],
    }


def parse_raw(raw):
    return list(raw.split("\n\n")).mapped(parse_one)


data = parse_raw(raw)


def part_one(data):
    data = data.deepcopy()
    inspected = [0 for _ in data]
    for _ in range(20):
        for i, monkey in enumerate(data):
            for old in monkey["items"]:
                inspected[i] += 1
                new = 0
                _locals = {"old": old}
                exec(monkey["op"], {}, _locals)
                new = _locals["new"]
                new = new // 3
                if new % monkey["test"] == 0:
                    data[monkey["true"]]["items"].append(new)
                else:
                    data[monkey["false"]]["items"].append(new)
            monkey["items"].clear()
    return math.prod(sorted(inspected)[-2:])


aoc_helper.lazy_test(day=11, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    data = data.deepcopy()
    inspected = [0 for _ in data]
    loop_factor = math.prod(monkey["test"] for monkey in data)
    for _ in range(10000):
        for i, monkey in enumerate(data):
            for old in monkey["items"]:
                inspected[i] += 1
                new = 0
                _locals = {"old": old}
                exec(monkey["op"], {}, _locals)
                new = _locals["new"]
                new = (
                    new
                ) % loop_factor  # shrink the number without affecting the tests
                if new % monkey["test"] == 0:
                    data[monkey["true"]]["items"].append(new)
                else:
                    data[monkey["false"]]["items"].append(new)
            monkey["items"].clear()
    return math.prod(sorted(inspected)[-2:])


aoc_helper.lazy_test(day=11, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=11, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=11, year=2022, solution=part_two, data=data)
