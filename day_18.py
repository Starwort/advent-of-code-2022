import collections
import itertools

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

raw = aoc_helper.fetch(18, 2022)


def parse_raw(raw):
    return extract_ints(raw).chunked(3)


data = parse_raw(raw)


def part_one(data):
    tiles = collections.defaultdict(bool)
    for pos in data:
        tiles[pos] = True
    count = 0
    for x, y, z in data:
        for dx, dy, dz in [
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ]:
            if not tiles[x + dx, y + dy, z + dz]:
                count += 1
    return count


aoc_helper.lazy_test(
    day=18,
    year=2022,
    parse=parse_raw,
    solution=part_one,
    test_data=(
        """2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5""",
        64,
    ),
)


def part_two(data):
    tiles = collections.defaultdict(bool)
    for pos in data:
        tiles[pos] = True
    count = 0
    for x, y, z in data:
        for dx, dy, dz in [
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ]:
            if not tiles[x + dx, y + dy, z + dz]:
                count += 1
    top = min(x for x, y, z in data)
    bottom = max(x for x, y, z in data)
    left = min(y for x, y, z in data)
    right = max(y for x, y, z in data)
    front = min(z for x, y, z in data)
    back = max(z for x, y, z in data)

    def is_interior_surface(tiles, x, y, z):
        to_visit = collections.deque([(x, y, z)])
        visited = set()
        while to_visit:
            x, y, z = to_visit.popleft()
            if (x, y, z) in visited:
                continue
            visited.add((x, y, z))
            if x < top or x > bottom or y < left or y > right or z < front or z > back:
                return False
            for dx, dy, dz in [
                (-1, 0, 0),
                (1, 0, 0),
                (0, -1, 0),
                (0, 1, 0),
                (0, 0, -1),
                (0, 0, 1),
            ]:
                if (x + dx, y + dy, z + dz) not in visited and not tiles[
                    x + dx, y + dy, z + dz
                ]:
                    to_visit.append((x + dx, y + dy, z + dz))
        return True

    for (x, y, z), tile in list(tiles.items()):
        if not tile:
            neighbours = sum(
                tiles[x + dx, y + dy, z + dz]
                for dx, dy, dz in [
                    (-1, 0, 0),
                    (1, 0, 0),
                    (0, -1, 0),
                    (0, 1, 0),
                    (0, 0, -1),
                    (0, 0, 1),
                ]
            )
            interior = is_interior_surface(tiles, x, y, z)
            # print(x, y, z, neighbours, interior)
            if interior:
                count -= neighbours
    return count


aoc_helper.lazy_test(
    day=18,
    year=2022,
    parse=parse_raw,
    solution=part_two,
    test_data=(
        """2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5""",
        58,
    ),
)

aoc_helper.lazy_submit(day=18, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=18, year=2022, solution=part_two, data=data)
