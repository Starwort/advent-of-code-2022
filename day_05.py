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

raw = aoc_helper.fetch(5, 2022)


def parse_raw():
    crates, moves = raw.split("\n\n")
    _crates = crates.splitlines()[:-1]
    n_crates = (len(_crates[0]) + 1) // 4
    crates = list(list() for _ in range(n_crates))
    for i in range(n_crates):
        for line in _crates[::-1]:
            if line[i * 4 + 1] == " ":
                break
            crates[i].append(line[i * 4 + 1])
    return crates, extract_ints(moves).chunked(3)


data = parse_raw()


def part_one(data):
    crates, moves = data
    crates = crates.deepcopy()
    for (n, from_, to) in moves:
        for _ in range(n):
            crates[to - 1].append(crates[from_ - 1].pop())
    return "".join(stack[-1] for stack in crates)


def part_two(data):
    crates, moves = data
    crates = crates.deepcopy()
    for (n, from_, to) in moves:
        to_move = [crates[from_ - 1].pop() for _ in range(n)]
        crates[to - 1].extend(to_move[::-1])
    return "".join(stack[-1] for stack in crates)


aoc_helper.lazy_submit(day=5, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=5, year=2022, solution=part_two, data=data)
