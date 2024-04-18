from functools import partial
import operator
from os import path
from typing import Callable, TypeVar

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
ascii_to_utf = {
    "|": "│",
    "-": "─",
    "L": "└",
    "J": "┘",
    "7": "┐",
    "F": "┌",
}

pipe_to_neighbors = {
    "│": {(0, -1), (0, 1)},
    "─": {(-1, 0), (1, 0)},
    "└": {(1, 0), (0, -1)},
    "┘": {(-1, 0), (0, -1)},
    "┐": {(-1, 0), (0, 1)},
    "┌": {(1, 0), (0, 1)},
}

T = TypeVar("T", list, tuple)


def dot_op(op: Callable, a: T, b: T) -> T:
    if len(a) != len(b):
        raise Exception(f"{a} has different dimensions to {b}")
    result = list(a)
    for i, bi in enumerate(b):
        result[i] = op(a[i], bi)
    if isinstance(a, list):
        return result
    if isinstance(a, tuple):
        return tuple(result)


dot = {
    "+": partial(dot_op, operator.__add__),
    "-": partial(dot_op, operator.__sub__),
}


def parse_input(filename: str):
    return [
        "".join(ascii_to_utf.get(c, c) for c in line)
        for line in map(str.strip, open(path.abspath(filename)).readlines())
    ]


def get_pos(field, pt):
    x, y = pt
    if 0 <= x < len(field[0]) and 0 <= y < len(field):
        return field[y][x]
    return None


def start_of(field):
    pos = next(
        (x, y)
        for y in range(len(field))
        for x in range(len(field[0]))
        if field[y][x] == "S"
    )
    for c in pipe_to_neighbors.keys():
        if all(
            map(
                lambda neighbor: get_pos(field, neighbor) in pipe_to_neighbors
                and any(
                    map(
                        lambda nn: dot["+"](nn, neighbor) == pos,
                        pipe_to_neighbors[get_pos(field, neighbor)],
                    )
                ),
                map(lambda neighbor: dot["+"](neighbor, pos), pipe_to_neighbors[c]),
            )
        ):
            return pos, c
    raise Exception("Unable to find start")


def trace_pipe(field):
    start_pos, start_pipe = start_of(field)
    from_pos, to_pos = start_pos, next(
        dot["+"](neighbor, start_pos) for neighbor in pipe_to_neighbors[start_pipe]
    )
    visited = [start_pos]
    while to_pos != start_pos:
        visited.append(to_pos)
        from_pos, to_pos = to_pos, next(
            dot["+"](to_pos, neighbor)
            for neighbor in pipe_to_neighbors[get_pos(field, to_pos)]
            if dot["+"](to_pos, neighbor) != from_pos
        )
    return visited


def is_enclosed(field, pipe_vecs, ground):
    cur_pos, winding, cast_vec = ground, 0, (1, 0)
    while get_pos(field, cur_pos):
        cur_pos = dot["+"](cur_pos, cast_vec)
        if cur_pos in pipe_vecs:
            winding += pipe_vecs[cur_pos][1]
    return winding != 0


def find_enclosed(field, pipeline):
    closed_pipeline = [pipeline[-1]] + pipeline + [pipeline[0]]
    pipe_vecs = {
        pos: dot["-"](before_pos, after_pos)
        for before_pos, pos, after_pos in zip(
            closed_pipeline[0:-2], closed_pipeline[1:-1], closed_pipeline[2:]
        )
    }
    return len(
        [
            (x, y)
            for y in range(len(field))
            for x in range(len(field[0]))
            if (x, y) not in pipe_vecs and is_enclosed(field, pipe_vecs, (x, y))
        ]
    )


def main():
    example1_input = parse_input("example1.txt")
    print("Example 1 part 1:", (len(trace_pipe(example1_input)) + 1) // 2)
    example2_input = parse_input("example2.txt")
    print("Example 2 part 1:", (len(trace_pipe(example2_input)) + 1) // 2)
    puzzle_input = parse_input("input.txt")
    print("Part 1:", (len(trace_pipe(puzzle_input)) + 1) // 2)
    example3_input = parse_input("example3.txt")
    print(
        "Example 3 part 2:", find_enclosed(example3_input, trace_pipe(example3_input))
    )
    example4_input = parse_input("example4.txt")
    print(
        "Example 4 part 2:", find_enclosed(example4_input, trace_pipe(example4_input))
    )
    example5_input = parse_input("example5.txt")
    print(
        "Example 5 part 2:", find_enclosed(example5_input, trace_pipe(example5_input))
    )
    print("Part 2:", find_enclosed(puzzle_input, trace_pipe(puzzle_input)))


if __name__ == "__main__":
    main()
