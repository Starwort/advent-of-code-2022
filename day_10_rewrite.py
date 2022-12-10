import aoc_helper
from aoc_helper import Grid, list

from computer import Computer

raw = aoc_helper.fetch(10, 2022)


def parse_raw(raw):
    return Computer(raw)


data = parse_raw(raw)


def part_one(data):
    return sum(
        state.x * cycle
        for cycle, state in enumerate(data.run(), start=1)
        if cycle in [20, 60, 100, 140, 180, 220]
    )


aoc_helper.lazy_test(day=10, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    output = Grid[bool](list(list(False for _ in range(40)) for _ in range(6)))
    for cycle, state in enumerate(data.run()):
        y, x = divmod(cycle, 40)
        if abs(x - state.x) <= 1:
            output[y][x] = True
    return output.decode_as_text()


# part_two(parse_raw(test))
aoc_helper.lazy_test(day=10, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=10, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=10, year=2022, solution=part_two, data=data)
