import math
from os import path
import re


def parse_input(filename: str):
    return list(map(str.strip, open(path.abspath(filename)).readlines()))


def neighbor_symbols(schematic, r, span):
    start, end = span
    check_intervals = [
        [r, max(start - 1, 0), start - 1],
        [r, end, min(end, len(schematic[r]) - 1)],
        [r - 1, max(start - 1, 0), min(end, len(schematic[r]) - 1)],
        [r + 1, max(start - 1, 0), min(end, len(schematic[r]) - 1)],
    ]
    symbols = []
    for r, start, end in check_intervals:
        if end < start or r < 0 or len(schematic) <= r:
            continue
        for i in range(start, end + 1):
            if re.match(r"(?![.0-9]).", schematic[r][i]):
                symbols.append(((r, i), schematic[r][i]))
    return symbols


def find_part_numbers(schematic):
    result = []
    for r, row in enumerate(schematic):
        for match in re.finditer(r"[0-9]+", row):
            if neighbor_symbols(schematic, r, match.span()):
                result.append(int(match.group()))
    return result


def find_gear_ratios(schematic):
    gear_to_part = {}
    for r, row in enumerate(schematic):
        for match in re.finditer(r"[0-9]+", row):
            for pos, sym in neighbor_symbols(schematic, r, match.span()):
                if sym == "*":
                    gear_to_part.setdefault(pos, []).append(int(match.group()))
    return {
        gear: math.prod(parts)
        for gear, parts in gear_to_part.items()
        if len(parts) == 2
    }


if __name__ == "__main__":
    example_input = parse_input("example.txt")
    print("Example Part 1:", sum(find_part_numbers(example_input)))
    print("Example Part 2:", sum(find_gear_ratios(example_input).values()))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", sum(find_part_numbers(puzzle_input)))
    print("Part 2:", sum(find_gear_ratios(puzzle_input).values()))
