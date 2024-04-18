from os import path
import re
from typing import Dict, Tuple, List

DAMAGED = "#"
UNKNOWN = "?"
OPERATIONAL = "."

Blocks = Tuple[int, ...]
Record = Tuple[str, Blocks]


def split_row(row: str, sep: str = OPERATIONAL) -> List[str]:
    return list(filter(len, row.split(sep)))


def validate_record(record: Record):
    return tuple(map(len, split_row(record[0]))) == record[1]


def count_arrangements(record: Record, cache: Dict[Record, int] = {}) -> int:
    record_row, record_blocks = record
    record_row = record_row.strip(OPERATIONAL)
    record = (record_row, record_blocks)
    if record in cache:
        return cache[record]
    sep_match = re.search(r"[.?]", record_row)
    if sep_match and sep_match.group() == OPERATIONAL:
        row_left, row_right = record_row.split(OPERATIONAL, maxsplit=1)
        cache[record] = sum(
            count_arrangements((row_right.lstrip(OPERATIONAL), record_blocks[i:]))
            for i in range(1, len(record_blocks) + 1)
            if validate_record((row_left, record_blocks[0:i]))
        )
        return cache[record]
    if UNKNOWN in record_row:
        cache[record] = sum(
            map(
                lambda c: count_arrangements(
                    (
                        record[0].replace(UNKNOWN, c, 1).lstrip(OPERATIONAL),
                        record_blocks,
                    ),
                    cache,
                ),
                (OPERATIONAL, DAMAGED),
            )
        )
        return cache[record]
    return 1 if validate_record(record) else 0


def sum_arrangements(records: List[Record]) -> int:
    return sum(count_arrangements(record) for record in records)


def parse_input(filename, unfold: bool = False) -> List[Record]:
    lines = list(
        filter(bool, [it.strip() for it in open(path.abspath(filename)).readlines()])
    )
    result: List[Record] = []
    for line in lines:
        row, blocks = line.split(" ")
        unfold_factor = 5 if unfold else 1
        result.append(
            (
                "?".join([row] * unfold_factor),
                tuple(map(int, blocks.split(","))) * unfold_factor,
            )
        )
    return result


def main():
    example1_input = parse_input("example1.txt")
    print("Example 1 part 1:", sum_arrangements(example1_input))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", sum_arrangements(puzzle_input))
    print(
        "Example 1 part 2:", sum_arrangements(parse_input("example1.txt", unfold=True))
    )
    print("Part 2:", sum_arrangements(parse_input("input.txt", unfold=True)))


if __name__ == "__main__":
    main()
