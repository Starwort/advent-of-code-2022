from collections import defaultdict

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

raw = aoc_helper.fetch(15, 2022)


def parse_raw(raw):
    return extract_ints(raw).chunked(4)


data = parse_raw(raw)


def part_one(data, target=2_000_000):
    not_beacons = SparseGrid(bool)
    for (sx, sy, bx, by) in data:
        manhattan = abs(sx - bx) + abs(sy - by)
        # if sy < 2000000 - manhattan or sy > 2000000 + manhattan:
        #     continue
        for x in range(sx - manhattan, sx + manhattan + 1):
            height = manhattan - abs(sx - x)
            if sy - height <= target <= sy + height and (x, target) != (bx, by):
                not_beacons[x, target] = True
            # for y in range(sy - height, sy + height + 1):
            #     if (x, y) == (bx, by):
            #         continue
            #     if y != 2000000:
            #         continue
            #     not_beacons[x, y] = True

    # if target == 10:
    #     not_beacons.pretty_print(lambda i: ".#"[i], [False])

    return sum(
        map(lambda i: i[1], filter(lambda i: i[0][1] == target, not_beacons.items()))
    )


test_data = parse_raw(
    """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
)

# aoc_helper.lazy_test(day=15, year=2022, parse=parse_raw, solution=part_one)


# def part_two(data):
#     maybe_beacons = SparseGrid(bool)
#     for (sx, sy, bx, by) in data:
#         manhattan = abs(sx - bx) + abs(sy - by)
#         maybe_beacons.draw_lines(
#             [
#                 (sx - manhattan, sy),
#                 (sx, sy - manhattan),
#                 (sx + manhattan, sy),
#                 (sx, sy + manhattan),
#                 (sx - manhattan, sy),
#             ],
#             True,
#         )
#     for (sx, sy, bx, by) in data:
#         manhattan = abs(sx - bx) + abs(sy - by)
#         for x in range(sx - manhattan, sx + manhattan + 1):
#             height = manhattan - abs(sx - x)
#             for y in range(sy - height, sy + height + 1):
#                 if (x, y) in maybe_beacons:
#                     maybe_beacons[x, y] = False
#     x, y = (
#         list(maybe_beacons.items())
#         .filtered(lambda i: 0 <= i[0][0] <= 4_000_000 and 0 <= i[0][1] <= 4_000_000)
#         .filtered(lambda i: i[1])
#         .find()[0]
#     )
#     return x * 4_000_000 + y


def part_two(data):
    # screw it I'm learning z3
    import z3

    x = z3.Int("x")
    y = z3.Int("y")
    s = z3.Solver()
    s.add(x >= 0, y >= 0, x <= 4_000_000, y <= 4_000_000)
    for (sx, sy, bx, by) in data:
        dist = abs(sx - bx) + abs(sy - by)
        s.add(z3.Abs(sx - x) + z3.Abs(sy - y) > dist)
    s.check()
    m = s.model()
    return m[x].as_long() * 4_000_000 + m[y].as_long()


# aoc_helper.lazy_test(day=15, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=15, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=15, year=2022, solution=part_two, data=data)
