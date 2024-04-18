import sys
from operator import itemgetter
from typing import Iterable, List, Optional, Tuple, TypedDict


class Pattern(TypedDict):
    rows: List[str]
    cols: List[str]


def find_reflection(
    rows: List[str], exclude: Optional[int] = None, num_smudges: int = 0
) -> int:
    for i in range(1, len(rows)):
        if i == exclude:
            continue
        top = rows[0:i][::-1]
        bottom = rows[i:]
        num_rows_reflected = min(map(len, (top, bottom)))
        num_diff = sum(
            0 if top_cell == bottom_cell else 1
            for top_cell, bottom_cell in zip(
                (c for line in top[0:num_rows_reflected] for c in line),
                (c for line in bottom[0:num_rows_reflected] for c in line),
            )
        )
        if num_diff == num_smudges:
            return i
    return 0


def summarize_reflection(input: Iterable[Pattern], fix_smudge: bool):
    result = 0
    for pattern in input:
        row_reflection = find_reflection(
            list(pattern["rows"]),
            find_reflection(list(pattern["rows"])) if fix_smudge else None,
            1 if fix_smudge else 0,
        )
        col_reflection = find_reflection(
            list(pattern["cols"]),
            find_reflection(list(pattern["cols"])) if fix_smudge else None,
            1 if fix_smudge else 0,
        )
        result += 100 * row_reflection + col_reflection
    return result


def parse_input(raw_input: Iterable[str]) -> Iterable[Pattern]:
    patterns = [[]]
    for raw_line in raw_input:
        line = raw_line.strip()
        if line:
            patterns[-1].append(line)
        elif len(patterns[-1]):
            patterns.append([])
    result = []
    for pattern in patterns:
        rows = pattern
        cols = [[" "] * len(rows) for _ in range(len(rows[0]))]
        for y in range(len(pattern)):
            for x in range(len(pattern[y])):
                cols[x][y] = pattern[y][x]
        result.append(Pattern(rows=rows, cols=["".join(c) for c in cols]))
    return result


if __name__ == "__main__":
    fix_smudge = len(sys.argv) > 1 and sys.argv[1] == "2"
    print(summarize_reflection(parse_input(sys.stdin), fix_smudge=fix_smudge))
