from collections import deque
from operator import itemgetter
from os import path
from typing import Deque, List


def parse_input(filename: str):
    return [
        deque(map(int, line.split()))
        for line in filter(str.strip, open(path.abspath(filename)).readlines())
    ]


def extrapolate(history: Deque[int]):
    sequences: List[Deque[int]] = [history]
    while any(map(bool, sequences[-1])):
        sequences.append(
            deque(
                sequences[-1][i] - sequences[-1][i - 1]
                for i in range(1, len(sequences[-1]))
            )
        )
    for i in range(2, len(sequences) + 1):
        sequences[-i].append(sequences[-i][-1] + sequences[-i + 1][-1])
        sequences[-i].appendleft(sequences[-i][0] - sequences[-i + 1][0])
    return sequences[0][0], sequences[0][-1]


def extrapolate_sum(histories: List[Deque[int]]):
    extrapolated = [extrapolate(history) for history in histories]
    return sum(map(itemgetter(0), extrapolated)), sum(map(itemgetter(1), extrapolated))


def main():
    example_input = parse_input("example.txt")
    example_output = extrapolate_sum(example_input)
    print("Example part 1:", example_output[1])
    print("Example part 2:", example_output[0])
    puzzle_input = parse_input("input.txt")
    puzzle_output = extrapolate_sum(puzzle_input)
    print("Part 1:", puzzle_output[1])
    print("Part 2:", puzzle_output[0])


if __name__ == "__main__":
    main()
