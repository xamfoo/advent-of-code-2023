import sys
from typing import Iterable, List, Tuple, Set

mirrors = {
    "|": lambda x, y: [(0, -1), (0, 1)] if x else [(x, y)],
    "-": lambda x, y: [(-1, 0), (1, 0)] if y else [(x, y)],
    # (1, 0) > (0, 1)
    # (0, 1) > (1, 0)
    # (-1, 0) > (0, -1)
    # (0, -1) >  (-1, 0)
    "\\": lambda x, y: [(y, x)],
    # (1, 0) > (0, -1)
    # (0, 1) > (-1, 0)
    # (-1, 0) > (0, 1)
    # (0, -1) >  (1, 0)
    "/": lambda x, y: [(-y, -x)],
}

ENERGIZED = "#"

cardinal_vectors = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def parse_input(input: Iterable[str]):
    return [list(line) for line in (line.strip() for line in input) if len(line)]


def sum_energized(grid: List[List[str]]):
    return sum(1 if cell == ENERGIZED else 0 for row in grid for cell in row)


def trace_light(
    grid: List[List[str]], light: Tuple[Tuple[int, int], Tuple[int, int]]
) -> List[List[str]]:
    result = [["." for _ in row] for row in grid]
    lights: List[Tuple[Tuple[int, int], Tuple[int, int]]] = [light]
    seen_lights: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set(lights)
    while len(lights):
        loc, og_vector = lights.pop()
        x, y = loc
        if y < 0 or y >= len(result) or x < 0 or x >= len(result[0]):
            continue
        result[y][x] = ENERGIZED
        cell = grid[y][x]
        for vector in mirrors[cell](*og_vector) if cell in mirrors else [og_vector]:
            next_light = (tuple(a + b for a, b in zip(loc, vector)), vector)
            if next_light not in seen_lights:
                seen_lights.add(next_light)
                lights.append(next_light)
    return result


if __name__ == "__main__":
    grid = parse_input(sys.stdin)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        num_rows = len(grid)
        num_cols = len(grid[0])
        border_cells = set(
            (x, y)
            for x in range(num_cols)
            for y in range(num_rows)
            if x in (0, num_cols - 1) or y in (0, num_rows - 1)
        )
        print(
            max(
                sum_energized(trace_light(grid, (cell, vector)))
                for vector in cardinal_vectors
                for cell in border_cells
            )
        )
    else:
        print(sum_energized(trace_light(grid, ((0, 0), (1, 0)))))
