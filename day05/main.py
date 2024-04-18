import sys

from collections import deque
from functools import partial
from operator import itemgetter
from typing import Dict, Iterable, Optional, List, Tuple


def parse_input(
    lines: Iterable[str],
) -> Tuple[List[int], Dict[str, str], Dict[str, List[Tuple[int, int, int]]]]:
    iterable = map(str.strip, lines)
    seeds = list(map(int, next(iterable).split(": ")[1].split(" ")))
    maps, name_maps = [], []
    for line in filter(len, iterable):
        if line.endswith("map:"):
            name_maps.append(tuple(line.split(" ")[0].split("-to-")))
            maps.append([])
        else:
            maps[-1].append(tuple(map(int, line.split(" "))))
    return (
        seeds,
        {src: dest for src, dest in name_maps},
        {src_name: data for data, (src_name, _) in zip(maps, name_maps)},
    )


def intersect_intervals(
    a: Tuple[int, int], b: Tuple[int, int]
) -> Optional[Tuple[int, int]]:
    return None if a[1] < b[0] or b[1] < a[0] else tuple(sorted(a + b)[1:3])


def subtract_intervals(a: Tuple[int, int], b: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [
        interval
        for interval in [(a[0], b[0] - 1), (b[1] + 1, a[1])]
        if interval[0] <= interval[1]
    ]


def range_to_interval(input_range: Tuple[int, int]) -> Tuple[int, int]:
    start, length = input_range
    return (start, start + length - 1)


def to_location(
    src_to_dest_name: Dict[str, str],
    src_to_ranges: Dict[str, List[Tuple[int, int, int]]],
    seed_range: Tuple[int, int],
) -> Tuple[int, int]:
    jobs: List[Tuple[str, Tuple[int, int]]] = [("seed", range_to_interval(seed_range))]
    minmax = tuple()
    while jobs:
        src_name, job_interval = jobs.pop()
        if src_name == "location":
            minmax = (min(job_interval + minmax), max(job_interval + minmax))
            continue
        dest_name = src_to_dest_name[src_name]
        unmapped_intervals = deque([job_interval])
        for dest, src, length in src_to_ranges[src_name]:
            target_interval = range_to_interval((src, length))
            for _ in range(len(unmapped_intervals)):
                unmapped_interval = unmapped_intervals.popleft()
                intersection = intersect_intervals(unmapped_interval, target_interval)
                if intersection:
                    jobs.append(
                        (
                            dest_name,
                            tuple(map(lambda x: dest - src + x, intersection)),
                        )
                    )
                    for diff in subtract_intervals(unmapped_interval, intersection):
                        unmapped_intervals.append(diff)
                else:
                    unmapped_intervals.append(unmapped_interval)
        for unmapped_interval in unmapped_intervals:
            jobs.append((dest_name, unmapped_interval))
    return minmax


def min_location(
    src_to_dest_name: Dict[str, str],
    src_to_ranges: Dict[str, List[Tuple[int, int, int]]],
    seed_ranges: List[Tuple[int, int]],
):
    return min(
        map(
            itemgetter(0),
            map(
                partial(to_location, src_to_dest_name, src_to_ranges),
                seed_ranges,
            ),
        )
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        seeds, src_to_dest_name, src_to_ranges = parse_input(sys.stdin)
        print(
            "Part 2:",
            min_location(
                src_to_dest_name, src_to_ranges, list(zip(seeds[::2], seeds[1::2]))
            ),
        )
    else:
        seeds, src_to_dest_name, src_to_ranges = parse_input(sys.stdin)
        print(
            "Part 1:",
            min_location(src_to_dest_name, src_to_ranges, [(s, 1) for s in seeds]),
        )
