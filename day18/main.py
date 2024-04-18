import re
import sys

from operator import itemgetter
from typing import Dict, Iterable, List, Tuple

dir_vectors: Dict[str, Tuple[int, int]] = {
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
    "U": (0, -1),
}
ordered_dir_vectors = list(dir_vectors.keys())


def add_vector(a: Tuple[int, int], b: Tuple[int, int]):
    return (a[0] + b[0], a[1] + b[1])


def multiply_vector(a: Tuple[int, int], b: Tuple[int, int]):
    return (a[0] * b[0], a[1] * b[1])


def parse_input(input: Iterable[str]) -> List[Tuple[str, int, str, int]]:
    result = []
    for line in (line.strip() for line in input):
        if line:
            match = re.match(r"([A-Z]) ([0-9]+) \(#(.....)(.)\)", line)
            if not match:
                raise Exception(f"No match for {line}")
            result.append(
                (
                    match[1],
                    int(match[2]),
                    ordered_dir_vectors[int(match[4])],
                    int(match[3], base=16),
                )
            )
    return result


# Shoelace polygon area
def area(p: List[Tuple[int, int]]):
    return 0.5 * abs(
        sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in zip(p, p[1:] + [p[0]]))
    )


def dig(plan: List[Tuple[str, int]], start_pos: Tuple[int, int]) -> int:
    points = [start_pos]
    curr_pos = start_pos
    for cmd in plan:
        d, t = cmd
        curr_pos = add_vector(curr_pos, multiply_vector(dir_vectors[d], (t, t)))
        points.append(curr_pos)
    # Adjust with Pick's theorem (+1 due to a full rotation)
    return int(area(points) + sum(cmd[1] for cmd in plan) / 2 + 1)


def print_points(points: Iterable[Tuple[int, int]]):
    max_point = (max(map(itemgetter(0), points)), max(map(itemgetter(1), points)))
    grid = [["."] * (max_point[0] + 1) for _ in range(max_point[1] + 1)]
    for x, y in points:
        grid[y][x] = "#"
    print("\n".join("".join(row) for row in grid))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        print(dig([(cmd[2], cmd[3]) for cmd in parse_input(sys.stdin)], (0, 0)))
    else:
        print(dig([(cmd[0], cmd[1]) for cmd in parse_input(sys.stdin)], (0, 0)))
