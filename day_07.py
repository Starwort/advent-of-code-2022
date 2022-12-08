import collections
import typing

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

raw = aoc_helper.fetch(7, 2022)


def get(filesystem, dir):
    cwd = filesystem
    for segment in dir.split("/")[1:]:
        if segment == "":
            return cwd
        if segment not in cwd:
            cwd[segment] = {}
        cwd = cwd[segment]
    return cwd


def cd(current, filesystem, to):
    if to == "..":
        return current.rsplit("/", 1)[0], get(filesystem, current.rsplit("/", 1)[0])
    elif to.startswith("/"):
        return to, get(filesystem, to)
    else:
        return current.removesuffix("/") + "/" + to, get(
            filesystem, current.removesuffix("/") + "/" + to
        )


Folder = dict[str, typing.Union[int, "Folder"]]


def parse_raw():
    filesystem = {}
    cwd = "/"
    dir = filesystem
    for line in raw.splitlines():
        if line.startswith("$"):
            _, command, *args = line.split(" ", 2)
            if command == "cd":
                cwd, dir = cd(cwd, filesystem, *args)
            else:
                continue
        else:
            type, name = line.split()
            if type == "dir":
                dir[name] = {}
            else:
                dir[name] = int(type)
    return filesystem


data = parse_raw()


def count_files(sums, my_name, filesystem):
    sum = 0
    for name, data in filesystem.items():
        if isinstance(data, dict):
            sum += count_files(sums, my_name + "/" + name, data)
        else:
            sum += data
    sums[my_name] = sum
    return sum


def part_one(data: Folder):
    sizes = {}
    count_files(sizes, "", data)
    return list(sizes.values()).filtered(lambda i: i <= 100000).sum()


def part_two(data: Folder):
    max_used = 70000000 - 30000000
    sizes = {}
    to_free = count_files(sizes, "", data) - max_used
    if to_free < 0:
        return 0
    return list(sizes.values()).filtered(lambda i: i >= to_free).min()


aoc_helper.lazy_submit(day=7, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=7, year=2022, solution=part_two, data=data)
