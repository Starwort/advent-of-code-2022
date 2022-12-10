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

raw = aoc_helper.fetch(10, 2022)


def parse_raw(raw):
    return list(raw.splitlines()).mapped(extract_ints)


data = parse_raw(raw)

test = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def part_one(data):
    cycles = 0
    X = 1
    total = 0
    for i in data:
        if i:
            cycles += 2
            if cycles in [20, 21, 60, 61, 100, 101, 140, 141, 180, 181, 220, 221]:
                print(total, cycles, X, X * (cycles // 2) * 2)
                total += X * (cycles // 2) * 2
            X += i[0]
        else:
            cycles += 1
            if cycles in [20, 60, 100, 140, 180, 220]:
                print(total, cycles, X, X * cycles)
                total += X * cycles
    return total


# aoc_helper.lazy_test(day=10, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    output = Grid(list(list(False for _ in range(40)) for _ in range(6)))
    cycles = 0
    X = 1
    for i in data:
        if i:
            y, x = divmod(cycles, 40)
            if abs(x - X) <= 1:
                output[y][x] = True
            cycles += 1
            y, x = divmod(cycles, 40)
            if abs(x - X) <= 1:
                output[y][x] = True
            cycles += 1
            X += i[0]
        else:
            y, x = divmod(cycles, 40)
            if abs(x - X) <= 1:
                output[y][x] = True
            cycles += 1
    print(output)


# part_two(parse_raw(test))
# aoc_helper.lazy_test(day=10, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=10, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=10, year=2022, solution=part_two, data=data)
