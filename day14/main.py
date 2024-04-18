import sys
from typing import Dict, List, Tuple, TypedDict

CUBE = "#"
ROUND = "O"
SPACE = "."
NORTH = "N"
SOUTH = "S"
WEST = "W"
EAST = "E"
tilt_config = {
    NORTH: ("cols", "ljust"),
    SOUTH: ("cols", "rjust"),
    WEST: ("rows", "ljust"),
    EAST: ("rows", "rjust"),
}


class Grid(TypedDict):
    rows: Tuple[str]
    cols: Tuple[str]


def transpose(rows: Tuple[str]) -> Tuple[str]:
    cols = [[""] * len(rows) for _ in range(len(rows[0]))]
    for y in range(len(rows)):
        for x in range(len(rows[y])):
            cols[x][y] = rows[y][x]
    return tuple("".join(c) for c in cols)


def tilt(input: Grid, config: Tuple[str, str]) -> Grid:
    cols_or_rows = tuple(
        CUBE.join(
            [
                getattr((space.count(ROUND) * ROUND), config[1])(len(space), ".")
                for space in line.split(CUBE)
            ]
        )
        for line in input[config[0]]
    )
    if config[0] == "rows":
        return Grid(rows=cols_or_rows, cols=transpose(cols_or_rows))
    else:
        return Grid(cols=cols_or_rows, rows=transpose(cols_or_rows))


def tilt_cycle(input: Grid):
    spin_order = [NORTH, WEST, SOUTH, EAST]
    result = input
    for d in spin_order:
        # print("\n".join(result["rows"]), "\n")
        # print("Tilt", d)
        result = tilt(result, tilt_config[d])
    # print("\n".join(result["rows"]), "\n")
    return result


def calc_load(input: Grid):
    return sum(
        sum(len(line) - i for i in range(len(line)) if line[i] == ROUND)
        for line in input["cols"]
    )


def floyd(f, x0) -> Tuple[int, int]:
    """Floyd's cycle detection algorithm."""
    # Main phase of algorithm: finding a repetition x_i = x_2i.
    # The hare moves twice as quickly as the tortoise and
    # the distance between them increases by 1 at each step.
    # Eventually they will both be inside the cycle and then,
    # at some point, the distance between them will be
    # divisible by the period λ.
    tortoise = f(x0)  # f(x0) is the element/node next to x0.
    hare = f(f(x0))
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(f(hare))

    # At this point the tortoise position, ν, which is also equal
    # to the distance between hare and tortoise, is divisible by
    # the period λ. So hare moving in cycle one step at a time,
    # and tortoise (reset to x0) moving towards the cycle, will
    # intersect at the beginning of the cycle. Because the
    # distance between them is constant at 2ν, a multiple of λ,
    # they will agree as soon as the tortoise reaches index μ.

    # Find the position μ of first repetition.
    mu = 0
    tortoise = x0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)  # Hare and tortoise move at same speed
        mu += 1

    # Find the length of the shortest cycle starting from x_μ
    # The hare moves one step at a time while tortoise is still.
    # lam is incremented until λ is found.
    lam = 1
    hare = f(tortoise)
    while tortoise != hare:
        hare = f(hare)
        lam += 1

    return lam, mu


def spin_cycle(initial_dish: Grid) -> Grid:
    total_spins = 1000000000
    period, mu = floyd(tilt_cycle, initial_dish)
    result = initial_dish
    for _ in range(((total_spins - mu) % period) + mu):
        result = tilt_cycle(result)
    return result


def parse_input(raw_input):
    rows = tuple(filter(len, (line.strip() for line in raw_input)))
    return Grid(rows=rows, cols=transpose(rows))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        print(calc_load(spin_cycle(parse_input(sys.stdin))))
    else:
        print(calc_load(tilt(parse_input(sys.stdin), tilt_config["N"])))


if __name__ == "__main__":
    main()
