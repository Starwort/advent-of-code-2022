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

raw = aoc_helper.fetch(16, 2022)


def parse_raw(raw):
    def parse_line(line):
        parts = line.split()
        return (
            parts[1],
            extract_ints(line)[0],
            list(parts[9:]).mapped(lambda i: i.strip(",")),
        )

    data = list(raw.splitlines()).mapped(parse_line)
    data.sort(key=lambda i: i[1] == 0)
    return {
        i: (
            rate,
            connections.mapped(
                lambda i: data.enumerated().find(lambda k: k[1][0] == i)[0]
            ),
        )
        for i, (valve, rate, connections) in data.enumerated()
    }, data.enumerated().find(lambda i: i[1][0] == "AA")[0]


data = parse_raw(raw)


def pathfind(a, b, data):
    pos = a
    queue = PrioQueue([(0, a)])
    visited = set()
    for cost, pos in queue:
        if pos == b:
            return cost
        if pos in visited:
            continue
        visited.add(pos)
        rate, connections = data[pos]
        for connection in connections:
            queue.push((cost + 1, connection))
    return -1


def part_one(data):
    data, pos = data
    pairwise_distances = {(a, b): pathfind(a, b, data) for a in data for b in data}
    n_nonzero = next(i for i, (r, c) in data.items() if r == 0)
    dp_table = [
        [[-float("inf") for _ in range(1 << n_nonzero)] for _ in range(n_nonzero)]
        for _ in range(31)
    ]
    for i, (rate, connections) in data.items():
        if rate:
            dist = pairwise_distances[(pos, i)]
            dp_table[dist + 1][i][1 << i] = 0
    answer = 0
    for i in range(1, 31):
        print(i)
        for j in range(1 << n_nonzero):
            for k in range(n_nonzero):
                flow = sum(data[i][0] for i in range(n_nonzero) if j & (1 << i))
                if_stay = dp_table[i - 1][k][j] + flow
                if if_stay > dp_table[i][k][j]:
                    dp_table[i][k][j] = if_stay
                answer = max(answer, if_stay)
                if not ((1 << k) & j):
                    continue
                for l in range(n_nonzero):
                    if (1 << l) & j:
                        continue
                    dist = pairwise_distances[(k, l)]
                    if i + dist > 29:
                        continue
                    if_go = dp_table[i][k][j] + flow * (dist + 1)
                    if if_go > dp_table[i + dist + 1][l][j | (1 << l)]:
                        dp_table[i + dist + 1][l][j | (1 << l)] = if_go
    return answer


aoc_helper.lazy_test(
    day=16,
    year=2022,
    parse=parse_raw,
    solution=part_one,
    test_data=(
        """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""",
        1651,
    ),
)


def part_two(data):
    data, pos = data
    pairwise_distances = {(a, b): pathfind(a, b, data) for a in data for b in data}
    n_nonzero = next(i for i, (r, c) in data.items() if r == 0)
    dp_table = [
        [[-float("inf") for _ in range(1 << n_nonzero)] for _ in range(n_nonzero)]
        for _ in range(31)
    ]
    for i, (rate, connections) in data.items():
        if rate:
            dist = pairwise_distances[(pos, i)]
            dp_table[dist + 1][i][1 << i] = 0
    for i in range(1, 27):
        print(i)
        for j in range(1 << n_nonzero):
            for k in range(n_nonzero):
                flow = sum(data[i][0] for i in range(n_nonzero) if j & (1 << i))
                if_stay = dp_table[i - 1][k][j] + flow
                if if_stay > dp_table[i][k][j]:
                    dp_table[i][k][j] = if_stay
                if not ((1 << k) & j):
                    continue
                for l in range(n_nonzero):
                    if (1 << l) & j:
                        continue
                    dist = pairwise_distances[(k, l)]
                    if i + dist > 29:
                        continue
                    if_go = dp_table[i][k][j] + flow * (dist + 1)
                    if if_go > dp_table[i + dist + 1][l][j | (1 << l)]:
                        dp_table[i + dist + 1][l][j | (1 << l)] = if_go
    answer = 0
    for i in range(1 << n_nonzero):
        for j in range(1 << n_nonzero):
            if (i & j) != j:  # (i, j) where (j, i) is already computed
                continue
            a = b = -float("inf")
            for k in range(n_nonzero):
                a = max(a, dp_table[26][k][j])
            for k in range(n_nonzero):
                b = max(b, dp_table[26][k][i & ~j])
            answer = max(answer, a + b)
    return answer


# aoc_helper.lazy_test(day=16, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=16, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=16, year=2022, solution=part_two, data=data)
