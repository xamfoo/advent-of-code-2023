import sys

from typing import Dict, FrozenSet, List, Set, Tuple

Point2d = Tuple[int, int]
start = (1, 0)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parse_input(lines) -> List[List[str]]:
    return list(map(list, filter(len, (line.strip() for line in lines))))


def vecadd(a: Point2d, b: Point2d) -> Point2d:
    return (a[0] + b[0], a[1] + b[1])

def vecsub(a: Point2d, b: Point2d) -> Point2d:
    return (a[0] - b[0], a[1] - b[1])


slopes = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}


def io_of(grid, pt) -> Tuple[Set[Point2d], Set[Point2d]]:
    tile = grid[pt[1]][pt[0]]
    valid_neighbors = set(
        (x, y)
        for x, y in (
            vecadd(pt, (dx, dy)) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        )
        if 0 <= x < len(grid[0])
        and 0 <= y < len(grid)
        and grid[y][x] != "#"
        and (x, y) != start
    )
    incoming = set(
        (x, y)
        for x, y in valid_neighbors
        if grid[y][x] == "."
        or (grid[y][x] in slopes and vecadd(slopes[grid[y][x]], (x, y)) == pt)
    )
    if tile == ".":
        return (incoming, valid_neighbors)
    elif tile in slopes:
        slope_dest = vecadd(pt, slopes[tile])
        return (incoming, set() if slope_dest == start else {slope_dest})
    else:
        raise Exception(f"Unknown tile {tile} at {pt}")


def find_longest_path(grid: List[List[str]]):
    end = (len(grid[-1]) - 2, len(grid) - 1)
    init_io_by_pt = {
        (x, y): io_of(grid, (x, y))
        for y in range(len(grid))
        for x in range(len(grid[0]))
        if grid[y][x] != "#"
    }
    jobs: List[
        Tuple[Point2d, FrozenSet[Point2d], Dict[Point2d, Tuple[Set[Point2d], Set[Point2d]]]]
    ] = [(start, frozenset({start}), init_io_by_pt)]
    rating_by_pt = {
        (x, y): 0 for y in range(len(grid)) for x in range(len(grid[0]))
    }
    path_lengths: Set[int] = set()
    max_path_length = 0
    job_count = 0
    while jobs:
        job_count += 1
        cur_pos, visited, io_by_pt = jobs.pop()
        # print("\r\033[{len(grid)}A" + "\n".join(["".join(f"{bcolors.BOLD}{bcolors.OKCYAN}O{bcolors.ENDC}" if (x, y) in visited else c for x, c in zip(range(len(row)), row)) for y, row in zip(range(len(grid)), grid)]), flush=True)
        print("\r", job_count, "jobs:", len(jobs), "visited:", len(visited), "paths:", len(path_lengths), "maxpath:", max_path_length, "   ", flush=True, end="")
        if cur_pos == end:
            path_lengths.add(len(visited) - 1)
            max_path_length = max(max_path_length, len(visited) - 1)
            for v in visited:
                rating_by_pt[v] += 1
            jobs.sort(key=lambda job: rating_by_pt[job[0]])
            continue
        _, cur_out = io_by_pt[cur_pos]
        cur_out = [out_pt for out_pt in cur_out if out_pt not in visited]
        if not cur_out:
            for v in visited:
                rating_by_pt[v] -= 1
            jobs.sort(key=lambda job: rating_by_pt[job[0]])
            continue
        for out_pt in cur_out:
            jobs.append(
                (
                    out_pt,
                    visited | {out_pt},
                    {
                        pt: (pin.copy() - {cur_pos} if cur_pos in pin else pin, pout.copy() - {out_pt} if out_pt in pout else pout)
                        for pt, (pin, pout) in io_by_pt.items()
                    },
                )
            )
        jobs.sort(key=lambda job: rating_by_pt[job[0]])
    print()
    return max_path_length


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        grid = parse_input(sys.stdin)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                grid[y][x] = "." if grid[y][x] in slopes else grid[y][x]
        print(find_longest_path(grid))
    else:
        grid = parse_input(sys.stdin)
        print(find_longest_path(grid))
