from collections import defaultdict

import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    SparseGrid,
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

raw = aoc_helper.fetch(14, 2022)


def parse_raw(raw):
    return list(raw.splitlines()).mapped(extract_ints).mapped(lambda i: i.chunked(2))


data = parse_raw(raw)


def place_grain(graph, bottom, left, right, p2=False):
    x, y = 500, 0
    while True:
        if graph[x, y + 1] == 0:
            y += 1
        elif graph[x - 1, y + 1] == 0:
            x -= 1
            y += 1
        elif graph[x + 1, y + 1] == 0:
            x += 1
            y += 1
        else:
            graph[x, y] = 2
            return False
        if y > bottom:
            if not p2:
                return True
            else:
                graph[x, y] = 2
                return False
        if not p2:
            if x < left or x > right:
                return True


def part_one(data):
    return list(get_part_one_graph(data).values()).count(2)


def get_part_one_graph(data):
    graph = SparseGrid(int)
    for path in data:
        graph.draw_lines(path, 1)
    left, _, right, bottom = graph.bounds([0])
    while not place_grain(graph, bottom, left, right):
        pass
    return graph


aoc_helper.lazy_test(day=14, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    return list(get_part_two_graph(data).values()).count(2)


def get_part_two_graph(data) -> SparseGrid[int]:
    graph = SparseGrid(int)
    for path in data:
        graph.draw_lines(path, 1)
    left, _, right, bottom = graph.bounds([0])
    while graph[500, 0] == 0:
        place_grain(graph, bottom, left, right, p2=True)
    return graph


def create_text_graphs(data):
    p1_graph = get_part_one_graph(data)
    p2_graph = get_part_two_graph(data)
    p1_graph[500, 0]
    p2_graph[500, 0]
    import sys
    from io import StringIO

    old_stdout = sys.stdout
    sys.stdout = p1_out = StringIO()
    p1_graph.pretty_print(lambda i: " █⣿"[i], [0])
    sys.stdout = p2_out = StringIO()
    p2_graph.pretty_print(lambda i: " █⣿"[i], [0])
    sys.stdout = old_stdout
    with open("14p1.txt", "w") as f:
        f.write(p1_out.getvalue())
    with open("14p2.txt", "w") as f:
        f.write(p2_out.getvalue())


aoc_helper.lazy_test(day=14, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=14, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=14, year=2022, solution=part_two, data=data)
