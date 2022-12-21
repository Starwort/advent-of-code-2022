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

raw = aoc_helper.fetch(21, 2022)


def parse_raw(raw: str):
    return dict(i.replace("/", "//").split(": ") for i in raw.splitlines())


data = parse_raw(raw)


def part_one(data: dict[str, str]):
    values = {key: int(val) for key, val in data.items() if val.isnumeric()}
    while set(data) - set(values):
        for key, val in data.items():
            if key in values:
                continue
            try:
                values[key] = eval(val, values)
            except NameError:
                continue
    return values["root"]


aoc_helper.lazy_test(day=21, year=2022, parse=parse_raw, solution=part_one)


def part_two(data):
    import z3

    variables = {name: z3.Int(name) for name in data}
    solver = z3.Solver()
    for key, val in data.items():
        if key == "humn":
            continue
        if key == "root":
            left, _, right = val.split()
            solver.add(variables[left] == variables[right])
        solver.add(variables[key] == eval(val.replace("//", "/"), variables))
    solver.add(variables["humn"] != 3453748220117)
    solver.check()
    model = solver.model()
    variables.pop("__builtins__")  # wtf
    # print(model[variables["humn"]])
    # assert part_one({**data, "humn": str(model[variables["humn"]])}) == eval(
    #     data["root"], {key: model[val] for key, val in variables.items()}
    # )
    return model[variables["humn"]]


aoc_helper.lazy_test(day=21, year=2022, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=21, year=2022, solution=part_one, data=data)
aoc_helper.lazy_submit(day=21, year=2022, solution=part_two, data=data)
