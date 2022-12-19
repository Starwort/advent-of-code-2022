import math
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

raw = aoc_helper.fetch(19, 2022)


def parse_raw(raw):
    return extract_ints(raw).chunked(7)


data = parse_raw(raw)


# def part_one(data):
#     states = PrioQueue(
#         [
#             (
#                 int(0),
#                 int(0),
#                 int(0),
#                 int(0),
#                 int(1),
#                 int(0),
#                 int(0),
#                 int(0),
#                 int(0),
#                 data[0],
#             )
#         ]
#     )
#     states.next()
#     for blueprint in data:
#         states.push((0, 0, 0, 0, 1, 0, 0, 0, 0, blueprint))
#     max_geodes = (0, 0, data[0])
#     for (
#         geodes_opened,
#         obsidian,
#         ore,
#         clay,
#         ore_robots,
#         clay_robots,
#         obsidian_robots,
#         geode_robots,
#         minute,
#         blueprint,
#     ) in states:
#         (
#             ore_cost,
#             clay_cost,
#             obsidian_cost_ore,
#             obsidian_cost_clay,
#             geode_cost_ore,
#             geode_cost_obsidian,
#             _,
#         ) = blueprint
#         ore += ore_robots
#         clay += clay_robots
#         obsidian += obsidian_robots
#         geodes_opened += geode_robots
#         minute += 1
#         max_geodes = max(
#             (geodes_opened, minute, blueprint),
#             max_geodes,
#         )
#         if minute == 24:
#             continue
#         if ore >= ore_cost:
#             states.push(
#                 (
#                     geodes_opened,
#                     obsidian,
#                     ore - ore_cost,
#                     clay,
#                     ore_robots + 1,
#                     clay_robots,
#                     obsidian_robots,
#                     geode_robots,
#                     minute,
#                     blueprint,
#                 )
#             )
#         if ore >= clay_cost:
#             states.push(
#                 (
#                     geodes_opened,
#                     obsidian,
#                     ore - clay_cost,
#                     clay,
#                     ore_robots,
#                     clay_robots + 1,
#                     obsidian_robots,
#                     geode_robots,
#                     minute,
#                     blueprint,
#                 )
#             )
#         if ore >= obsidian_cost_ore and clay >= obsidian_cost_clay:
#             states.push(
#                 (
#                     geodes_opened,
#                     obsidian,
#                     ore - obsidian_cost_ore,
#                     clay - obsidian_cost_clay,
#                     ore_robots,
#                     clay_robots,
#                     obsidian_robots + 1,
#                     geode_robots,
#                     minute,
#                     blueprint,
#                 )
#             )
#         if ore >= geode_cost_ore and clay >= geode_cost_obsidian:
#             states.push(
#                 (
#                     geodes_opened,
#                     obsidian - geode_cost_obsidian,
#                     ore - geode_cost_ore,
#                     clay,
#                     ore_robots,
#                     clay_robots,
#                     obsidian_robots,
#                     geode_robots + 1,
#                     minute,
#                     blueprint,
#                 )
#             )
#     return max_geodes[0] * max_geodes[2][0]


# def part_one(data):
#     states = PrioQueue(
#         [
#             (
#                 int(0),
#                 int(0),
#                 int(0),
#                 int(0),
#                 int(1),
#                 int(0),
#                 int(0),
#                 int(0),
#                 int(0),
#                 data[0],
#             )
#         ]
#     )
#     states.next()
#     for blueprint in data:
#         states.push((0, 0, 0, 0, 1, 0, 0, 0, 0, blueprint))
#     total = 0
#     for state in states:
#         (
#             geodes_opened,
#             obsidian,
#             ore,
#             clay,
#             ore_robots,
#             clay_robots,
#             obsidian_robots,
#             geode_robots,
#             minute,
#             blueprint,
#         ) = state
#         (
#             _,
#             ore_cost,
#             clay_cost,
#             obsidian_cost_ore,
#             obsidian_cost_clay,
#             geode_cost_ore,
#             geode_cost_obsidian,
#         ) = blueprint
#         ore += ore_robots
#         clay += clay_robots
#         obsidian += obsidian_robots
#         geodes_opened += geode_robots
#         minute += 1
#         if minute == 24:
#             total += geodes_opened * blueprint[0]
#             continue
#         if ore >= geode_cost_ore and obsidian >= geode_cost_obsidian:
#             states.push(
#                 (
#                     geodes_opened,
#                     obsidian - geode_cost_obsidian,
#                     ore - geode_cost_ore,
#                     clay,
#                     ore_robots,
#                     clay_robots,
#                     obsidian_robots,
#                     geode_robots + 1,
#                     minute,
#                     blueprint,
#                 )
#             )
#             continue
#         if ore >= obsidian_cost_ore and clay >= obsidian_cost_clay:
#             states.push(
#                 (
#                     geodes_opened,
#                     obsidian,
#                     ore - obsidian_cost_ore,
#                     clay - obsidian_cost_clay,
#                     ore_robots,
#                     clay_robots,
#                     obsidian_robots + 1,
#                     geode_robots,
#                     minute,
#                     blueprint,
#                 )
#             )
#             if obsidian + obsidian_robots < geode_cost_obsidian:
#                 continue
#         if ore >= ore_cost:
#             states.push(
#                 (
#                     geodes_opened,
#                     obsidian,
#                     ore - ore_cost,
#                     clay,
#                     ore_robots + 1,
#                     clay_robots,
#                     obsidian_robots,
#                     geode_robots,
#                     minute,
#                     blueprint,
#                 )
#             )
#         if ore >= clay_cost:
#             states.push(
#                 (
#                     geodes_opened,
#                     obsidian,
#                     ore - clay_cost,
#                     clay,
#                     ore_robots,
#                     clay_robots + 1,
#                     obsidian_robots,
#                     geode_robots,
#                     minute,
#                     blueprint,
#                 )
#             )
#         states.push(
#             (
#                 geodes_opened,
#                 obsidian,
#                 ore,
#                 clay,
#                 ore_robots,
#                 clay_robots,
#                 obsidian_robots,
#                 geode_robots,
#                 minute,
#                 blueprint,
#             )
#         )
#     return total


def part_one(data):
    dp_table = defaultdict[
        tuple[int, int, int, int, int, int], tuple[int, int, int, int]
    ](lambda: (0, 0, 0, 0))
    for (blueprint_id, *_) in data:
        dp_table[1, 0, 0, 0, 0, blueprint_id]

    def insert(key, value):
        dp_table[key] = max(dp_table[key], value)

    results = defaultdict[int, int](int)

    for minute in range(24):
        for (ore_robot, clay_robot, obsidian_robot, geode_robot, _, blueprint_id), (
            geode,
            obsidian,
            ore,
            clay,
        ) in list(dp_table.items()).filtered(lambda i: i[0][4] == minute):
            ore += ore_robot
            clay += clay_robot
            obsidian += obsidian_robot
            geode += geode_robot
            (
                _,
                ore_cost,
                clay_cost,
                obsidian_cost_ore,
                obsidian_cost_clay,
                geode_cost_ore,
                geode_cost_obsidian,
            ) = data[blueprint_id - 1]
            if minute == 23:
                if geode > results[blueprint_id]:
                    results[blueprint_id] = geode
                continue
            if (
                ore - ore_robot >= geode_cost_ore
                and obsidian - obsidian_robot >= geode_cost_obsidian
            ):
                insert(
                    (
                        ore_robot,
                        clay_robot,
                        obsidian_robot,
                        geode_robot + 1,
                        minute + 1,
                        blueprint_id,
                    ),
                    (
                        geode,
                        obsidian - geode_cost_obsidian,
                        ore - geode_cost_ore,
                        clay,
                    ),
                )
                # continue

            insert(
                (
                    ore_robot,
                    clay_robot,
                    obsidian_robot,
                    geode_robot,
                    minute + 1,
                    blueprint_id,
                ),
                (geode, obsidian, ore, clay),
            )

            if ore - ore_robot >= ore_cost:
                insert(
                    (
                        ore_robot + 1,
                        clay_robot,
                        obsidian_robot,
                        geode_robot,
                        minute + 1,
                        blueprint_id,
                    ),
                    (geode, obsidian, ore - ore_cost, clay),
                )
            if ore - ore_robot >= clay_cost:
                insert(
                    (
                        ore_robot,
                        clay_robot + 1,
                        obsidian_robot,
                        geode_robot,
                        minute + 1,
                        blueprint_id,
                    ),
                    (geode, obsidian, ore - clay_cost, clay),
                )
            if (
                ore - ore_robot >= obsidian_cost_ore
                and clay - clay_robot >= obsidian_cost_clay
            ):
                insert(
                    (
                        ore_robot,
                        clay_robot,
                        obsidian_robot + 1,
                        geode_robot,
                        minute + 1,
                        blueprint_id,
                    ),
                    (
                        geode,
                        obsidian,
                        ore - obsidian_cost_ore,
                        clay - obsidian_cost_clay,
                    ),
                )
    return sum(blueprint_id * geode for blueprint_id, geode in results.items())


aoc_helper.lazy_test(day=19, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    dp_table = defaultdict[
        tuple[int, int, int, int, int, int], tuple[int, int, int, int]
    ](lambda: (0, 0, 0, 0))
    for (blueprint_id, *_) in data[:3]:
        dp_table[1, 0, 0, 0, 0, blueprint_id]

    def insert(key, value):
        dp_table[key] = max(dp_table[key], value)

    results = defaultdict[int, int](int)

    for minute in range(32):
        for (ore_robot, clay_robot, obsidian_robot, geode_robot, _, blueprint_id), (
            geode,
            obsidian,
            ore,
            clay,
        ) in list(dp_table.items()).filtered(lambda i: i[0][4] == minute):
            ore += ore_robot
            clay += clay_robot
            obsidian += obsidian_robot
            geode += geode_robot
            (
                _,
                ore_cost,
                clay_cost,
                obsidian_cost_ore,
                obsidian_cost_clay,
                geode_cost_ore,
                geode_cost_obsidian,
            ) = data[blueprint_id - 1]
            if minute == 31:
                if geode > results[blueprint_id]:
                    results[blueprint_id] = geode
                continue
            if (
                ore - ore_robot >= geode_cost_ore
                and obsidian - obsidian_robot >= geode_cost_obsidian
            ):
                insert(
                    (
                        ore_robot,
                        clay_robot,
                        obsidian_robot,
                        geode_robot + 1,
                        minute + 1,
                        blueprint_id,
                    ),
                    (
                        geode,
                        obsidian - geode_cost_obsidian,
                        ore - geode_cost_ore,
                        clay,
                    ),
                )
                # continue

            insert(
                (
                    ore_robot,
                    clay_robot,
                    obsidian_robot,
                    geode_robot,
                    minute + 1,
                    blueprint_id,
                ),
                (geode, obsidian, ore, clay),
            )

            if ore - ore_robot >= ore_cost:
                insert(
                    (
                        ore_robot + 1,
                        clay_robot,
                        obsidian_robot,
                        geode_robot,
                        minute + 1,
                        blueprint_id,
                    ),
                    (geode, obsidian, ore - ore_cost, clay),
                )
            if ore - ore_robot >= clay_cost:
                insert(
                    (
                        ore_robot,
                        clay_robot + 1,
                        obsidian_robot,
                        geode_robot,
                        minute + 1,
                        blueprint_id,
                    ),
                    (geode, obsidian, ore - clay_cost, clay),
                )
            if (
                ore - ore_robot >= obsidian_cost_ore
                and clay - clay_robot >= obsidian_cost_clay
            ):
                insert(
                    (
                        ore_robot,
                        clay_robot,
                        obsidian_robot + 1,
                        geode_robot,
                        minute + 1,
                        blueprint_id,
                    ),
                    (
                        geode,
                        obsidian,
                        ore - obsidian_cost_ore,
                        clay - obsidian_cost_clay,
                    ),
                )
    return math.prod(geode for geode in results.values())


aoc_helper.lazy_test(day=19, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=19, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=19, year=2022, solution=part_two, data=data)
