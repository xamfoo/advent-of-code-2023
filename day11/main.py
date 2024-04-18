import sys
from typing import Iterable, Set, Tuple

GALAXY = "#"


def expand_galaxies(galaxies: Set[Tuple[int, int]], expansion_factor: int = 1):
    occupied_n = tuple(set([g[dimension] for g in galaxies]) for dimension in range(2))
    max_n = tuple(max(occupied_n[dimension]) for dimension in range(2))
    offsets = ([0], [0])
    for dimension in range(2):
        for n in range(1, max_n[dimension] + 1):
            offsets[dimension].append(
                offsets[dimension][n - 1]
                + (0 if n in occupied_n[dimension] else expansion_factor - 1)
            )
    return [(x + offsets[0][x], y + offsets[1][y]) for x, y in galaxies]


def distance(a: Tuple[int, int], b: Tuple[int, int]):
    return sum(abs(a[dimension] - b[dimension]) for dimension in range(len(a)))


def list_pairs(list_len):
    return set((i, j) for i in range(list_len) for j in range(list_len) if i < j)


def parse_input(input: Iterable[str]) -> Set[Tuple[int, int]]:
    lines = list(filter(bool, [it.strip() for it in input]))
    galaxies = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == GALAXY:
                galaxies.add((x, y))
    return galaxies


def main():
    expansion_factor = int(1e6) if len(sys.argv) > 1 and sys.argv[1] == "2" else 2
    expanded_galaxies = expand_galaxies(
        parse_input(sys.stdin), expansion_factor=expansion_factor
    )
    pairs = list_pairs(len(expanded_galaxies))
    print(sum([distance(expanded_galaxies[i], expanded_galaxies[j]) for i, j in pairs]))


if __name__ == "__main__":
    main()
