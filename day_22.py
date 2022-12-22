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

raw = aoc_helper.fetch(22, 2022)
import re


def parse_raw(raw):
    map, path = raw.split("\n\n")
    max_len = max(len(i) for i in map.splitlines())
    return Grid.from_string(
        "\n".join(f"{row:{max_len}}" for row in map.splitlines()),
        lambda i: " .#".index(i) - 1,
    ), list(re.findall(r"(\d+)(.)?", path)).mapped(lambda i: (int(i[0]), i[1]))


data = parse_raw(raw)


def part_one(data):
    grid: Grid[int]
    grid, path = data
    y = 0
    x = grid[0].index(0)
    facing = (1, 0)
    for (distance, direction) in path:
        for _ in range(distance):
            next_pos = (
                (x + facing[0]) % len(grid[0]),
                (y + facing[1]) % len(grid.data),
            )
            if grid[next_pos[1]][next_pos[0]] == -1:
                next_pos = (
                    (
                        facing[0]
                        * grid[y][:: facing[0] or 1]
                        .enumerated()
                        .filtered(lambda i: i[1] != -1)
                        .find()[0]
                        - (1 if facing[0] == -1 else 0)
                    )
                    if facing[0]
                    else x,
                    (
                        facing[1]
                        * list(row[x] for row in grid.data)[:: facing[1] or 1]
                        .enumerated()
                        .filtered(lambda i: i[1] != -1)
                        .find()[0]
                        - (1 if facing[1] == -1 else 0)
                    )
                    if facing[1]
                    else y,
                )
            if grid[next_pos[1]][next_pos[0]] == 1:
                break
            x, y = next_pos
        if direction == "L":
            facing = (facing[1], -facing[0])
        elif direction == "R":
            facing = (-facing[1], facing[0])
    return 1000 * (y + 1) + 4 * (x + 1) + facing_to_direction(facing)


aoc_helper.lazy_test(
    day=22,
    year=2022,
    parse=parse_raw,
    solution=part_one,
    test_data=(
        """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""",
        6032,
    ),
)


def facing_to_direction(facing):
    return [(1, 0), (0, 1), (-1, 0), (0, -1)].index(facing)


def part_two(
    data,
    cube_size=50,
    face_connections=[
        [(1, (1, 0)), (2, (0, 1)), (3, (1, 0)), (4, (1, 0))],
        [(4, (-1, 0)), (2, (-1, 0)), (0, (-1, 0)), (5, (0, -1))],
        [(1, (0, -1)), (4, (0, 1)), (3, (0, 1)), (0, (0, -1))],
        [(4, (1, 0)), (5, (0, 1)), (0, (1, 0)), (2, (1, 0))],
        [(1, (-1, 0)), (5, (-1, 0)), (3, (-1, 0)), (2, (0, -1))],
        [(4, (0, -1)), (1, (0, 1)), (0, (0, 1)), (3, (0, -1))],
    ],
):
    grid: Grid[int]
    grid, path = data
    display_grid = grid.deepcopy()
    y = 0
    x = grid[0].index(0)
    facing = (1, 0)
    face_no = -1
    faces = [
        [-1 if col == -1 else (face_no := face_no + 1) for col in row[::cube_size]]
        for row in grid[::cube_size]
    ]
    positions = [(0, 0) for _ in range(6)]
    # face_connections = [[(0, (0, 0)) for _ in range(4)] for _ in range(6)]

    for _y, row in enumerate(faces):
        for _x, face in enumerate(row):
            if face == -1:
                continue
            positions[face] = (_x * cube_size, _y * cube_size)
    #         if faces[_y][(_x + 1) % len(row)] != -1:
    #             face_connections[face][0] = faces[_y][(_x + 1) % len(row)], (1, 0)
    #             face_connections[faces[_y][(_x + 1) % len(row)]][2] = face, (-1, 0)
    #         if faces[(_y + 1) % len(faces)][_x] != -1:
    #             face_connections[face][1] = faces[(_y + 1) % len(faces)][_x], (0, 1)
    #             face_connections[faces[(_y + 1) % len(faces)][_x]][3] = face, (0, -1)
    #         if faces[_y][(_x - 1) % len(row)] != -1:
    #             face_connections[face][2] = faces[_y][(_x - 1) % len(row)], (-1, 0)
    #             face_connections[faces[_y][(_x - 1) % len(row)]][2] = face, (1, 0)
    #         if faces[(_y - 1) % len(faces)][_x] != -1:
    #             face_connections[face][3] = faces[(_y - 1) % len(faces)][_x], (0, -1)
    #             face_connections[faces[(_y - 1) % len(faces)][_x]][1] = face, (0, 1)
    # while any((0, (0, 0)) in row for row in face_connections):
    #     for _y, row in enumerate(faces):
    #         for _x, face in enumerate(row):
    #             if face == -1:
    #                 continue
    #             if (0, (0, 0)) in face_connections[face]:
    #                 if face_connections[face][0] != (0, (0, 0)):
    #                     # try connecting down then right
    #                     if face_connections[face][1] != (0, (0, 0)):
    #                         connection, direction = face_connections[face][1]
    #                         face_connections[face][0] = connection, (

    #                         )
    #                     elif
    # for row in face_connections:
    #     print(row)

    for (distance, direction) in path:
        for _ in range(distance):
            next_pos = (
                (x + facing[0]),
                (y + facing[1]),
            )
            next_direction = facing
            if (
                next_pos[1] >= len(grid.data)
                or next_pos[0] >= len(grid[next_pos[1]])
                or grid[next_pos[1]][next_pos[0]] == -1
            ):
                # print(len(faces), next_pos[1] // cube_size)
                # print(len(faces[next_pos[1] // cube_size]), next_pos[0] // cube_size)
                cur_face = faces[y // cube_size][x // cube_size]
                next_face, next_direction = face_connections[cur_face][
                    facing_to_direction(facing)
                ]
                # print(face_connections[cur_face])
                # print(cur_face, next_face)
                position_in_face = (next_pos[0] % cube_size, next_pos[1] % cube_size)
                if next_direction == (facing[1], -facing[0]):
                    position_in_face = (
                        position_in_face[1],
                        (cube_size - 1) - position_in_face[0],
                    )
                elif next_direction == (-facing[1], facing[0]):
                    position_in_face = (
                        (cube_size - 1) - position_in_face[1],
                        position_in_face[0],
                    )
                elif next_direction == (-facing[0], -facing[1]):
                    position_in_face = (
                        (cube_size - 1) - position_in_face[0],
                        (cube_size - 1) - position_in_face[1],
                    )
                face_pos = positions[next_face]
                next_pos = (
                    face_pos[0] + position_in_face[0],
                    face_pos[1] + position_in_face[1],
                )
            if grid[next_pos[1]][next_pos[0]] == 1:
                break
            # print(x, y, next_pos, facing)
            x, y = next_pos
            facing = next_direction
            display_grid[y][x] = 2 + facing_to_direction(facing)
        if direction == "L":
            facing = (facing[1], -facing[0])
        elif direction == "R":
            facing = (-facing[1], facing[0])
        # print(x, y, facing)
        display_grid[y][x] = 2 + facing_to_direction(facing)
    # for row in display_grid:
    #     print("".join(" .#>v<^"[col + 1] for col in row))
    return 1000 * (y + 1) + 4 * (x + 1) + facing_to_direction(facing)


aoc_helper.lazy_test(
    day=22,
    year=2022,
    parse=parse_raw,
    solution=lambda i: part_two(
        i,
        4,
        [
            [(5, (-1, 0)), (3, (0, 1)), (2, (0, 1)), (1, (0, 1))],
            [(2, (1, 0)), (4, (0, -1)), (5, (0, -1)), (0, (0, 1))],
            [(3, (1, 0)), (5, (1, 0)), (2, (-1, 0)), (0, (1, 0))],
            [(5, (0, 1)), (4, (0, 1)), (3, (-1, 0)), (0, (0, -1))],
            [(5, (1, 0)), (1, (0, -1)), (2, (0, -1)), (3, (0, -1))],
            [(0, (-1, 0)), (1, (1, 0)), (4, (-1, 0)), (3, (-1, 0))],
        ],
    ),
    test_data=(
        """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""",
        5031,
    ),
)

aoc_helper.lazy_submit(day=22, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=22, year=2022, solution=part_two, data=data)
