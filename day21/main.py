import sys

from operator import itemgetter
from typing import Dict, List, Set, Tuple


def parse_input(lines):
    grid = list(filter(len, (l.strip() for l in lines)))
    garden_plots = []
    start = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pt = grid[y][x]
            if pt != "#":
                garden_plots.append((x, y))
            if pt == "S":
                if start:
                    raise Exception(
                        "Multiple start points (S) found: {start} and {(x, y)}"
                    )
                start = (x, y)
    if not start:
        raise Exception("No start point (S) found")
    return (start, garden_plots)


def neighbors_of(vertex):
    return [
        (vertex[0] + x, vertex[1] + y) for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]
    ]


def warp_grid(grid_size: Tuple[int, int]):
    def warp(pt: Tuple[int, int]) -> Tuple[int, int]:
        return (pt[0] % grid_size[0], pt[1] % grid_size[1])

    return warp


def find_grid_size(garden_plots):
    return (
        max(map(itemgetter(0), garden_plots)) + 1,
        max(map(itemgetter(1), garden_plots)) + 1,
    )


def reachable(
    garden_plots: List[Tuple[int, int]], start: Tuple[int, int], max_steps: int
):
    plots_set = set(garden_plots)
    last_reachable: Set[Tuple[int, int]] = {start}
    steps = 0
    reachable_by_step: Dict[int, Set[Tuple[int, int]]] = {}
    grid_size = find_grid_size(garden_plots)
    warp = warp_grid(grid_size)
    while steps < max_steps:
        next_reachable = set()
        for plot in last_reachable:
            for n in neighbors_of(plot):
                if warp(n) in plots_set:
                    next_reachable.add(n)
        last_reachable = next_reachable
        steps += 1
        reachable_by_step[steps] = last_reachable
        print(
            f"\rStep {steps} has {len(last_reachable)} reachable plots",
            flush=True,
            end="",
        )
    print()
    return reachable_by_step


def lagrange_interpolate(xys: List[Tuple[int, int]], steps: int) -> int:
    """

    The grid is a square of 131x131 tiles. S is in the exact center at (65, 65).
    The edge rows and columns are all open, and S has a straight path to all of them.
    It takes 65 steps to reach the first set of edges, then 131 more to reach every next set.
    When we reach the first edges, the points form a diamond.
    Then we run to the next edges, and to the ones after that, making the diamond grow.
    For each of those 3 runs, we will store the number of steps taken (x) and the number of open tiles at that step (y).
    3 pairs are enough to interpolate the growth function - y = f(x),
    so I went searching for an online Lagrange interpolation calculator,
    because that is all I can remember about numerical methods from college. :)
    I found this, and it helped: https://www.dcode.fr/lagrange-interpolating-polynomial
    It's a quadratic formula! (it's a square grid, and with every step we form a perfect diamond, so it makes sense)
    So we can just calculate the formula for X = 26501365, and we get the answer.
    """
    if len(xys) != 3:
        raise Exception("Should only pass 3 pairs of intergers.")
    result = 0.0
    for i in range(3):
        term = xys[i][1]
        for j in range(3):
            if j != i:
                term = term * (steps - xys[j][0]) / (xys[i][0] - xys[j][0])
        result += term
    return int(result)


if __name__ == "__main__":
    start, garden_plots = parse_input(sys.stdin)
    print("start", start)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        target_steps = 26501365
        grid_size = find_grid_size(garden_plots)
        max_steps = 2 * grid_size[0] + start[0]
        reachable_by_step = reachable(garden_plots, start, max_steps)
        print(
            f"Step {target_steps} has",
            lagrange_interpolate(
                [
                    (step, len(sreachable))
                    for step, sreachable in reachable_by_step.items()
                    if (step - start[0]) % grid_size[0] == 0
                ],
                target_steps,
            ),
            "reachable plots",
        )
    else:
        target_steps = 64
        reachable(garden_plots, start, target_steps)
