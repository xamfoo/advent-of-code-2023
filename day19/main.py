import math
import re
import sys

from typing import Dict, Iterable, Literal, List, Optional, Tuple

Sign = Literal[1] | Literal[-1]
Rule = str | Tuple[str, Sign, int, str]
Workflows = Dict[str, List[Rule]]
Part = Dict[str, int]
Intervals = Dict[str, Tuple[int, int]]


def parse_rule(input: str) -> Rule:
    if ":" in input:
        rest, workflow = input.split(":")
        sign: Sign = -1 if "<" in rest else 1
        attr, score = re.split(r"[<>]", rest)
        return (attr, sign, int(score), workflow)
    else:
        return input


def parse_input(input: Iterable[str]) -> Tuple[Workflows, List[Part]]:
    workflows: Workflows = {}
    parts: List[Part] = []
    lines = [l.strip() for l in input]
    separator_idx = lines.index("")
    for l in lines[0:separator_idx]:
        name, rest = l.replace("}", "").split("{")
        workflows[name] = list(map(parse_rule, rest.split(",")))
    for l in lines[separator_idx + 1 :]:
        part: Part = {}
        for kv in re.sub(r"[{}]", "", l).split(","):
            k, v = kv.split("=")
            part[k] = int(v)
        parts.append(part)
    return (workflows, parts)


def filter_intervals(
    workflows: Workflows,
    jobs: List[Tuple[str, Intervals]],
) -> List[Intervals]:
    accepted: List[Intervals] = []
    while len(jobs):
        curr_workflow, intervals = jobs.pop()
        if curr_workflow == "A":
            accepted.append(intervals)
            continue
        elif curr_workflow == "R":
            continue
        rules = workflows[curr_workflow]
        curr_intervals = intervals.copy()
        for rule in rules:
            if isinstance(rule, str):
                jobs.append((rule, intervals))
                break
            else:
                attr, sign, rating, target_workflow = rule
                target_interval = (1, rating - 1) if sign < 0 else (rating + 1, 4000)
                interval_intersection = intersect(curr_intervals[attr], target_interval)
                if interval_intersection:
                    jobs.append(
                        (
                            target_workflow,
                            {**curr_intervals, attr: interval_intersection},
                        )
                    )
                    for interval_diff in (
                        difference(curr_intervals[attr], interval_intersection) or []
                    ):
                        jobs.append(
                            (curr_workflow, {**curr_intervals, attr: interval_diff})
                        )
                    break
    return accepted


def intersect(a: Tuple[int, int], b: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    return None if a[1] < b[0] or b[1] < a[0] else tuple(sorted(a + b)[1:3])


def difference(
    a: Tuple[int, int], b: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    result = [
        min_max
        for min_max in [(a[0], b[0] - 1), (b[1] + 1, a[1])]
        if min_max[0] <= min_max[1]
    ]
    return result if len(result) else None


def sum_interval_ratings(intervals_list: List[Intervals]):
    return sum(
        sum(sum(range(minr, maxr + 1)) for minr, maxr in intervals.values())
        for intervals in intervals_list
    )


def sum_combinations(intervals_list: List[Intervals]):
    return sum(
        math.prod(maxr - minr + 1 for minr, maxr in intervals.values())
        for intervals in intervals_list
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        workflows, parts = parse_input(sys.stdin)
        intervals = filter_intervals(
            workflows, [("in", dict((k, (1, 4000)) for k in ["x", "m", "a", "s"]))]
        )
        print(sum_combinations(intervals))
    else:
        workflows, parts = parse_input(sys.stdin)
        accepted = filter_intervals(
            workflows,
            [("in", dict((k, (v, v)) for k, v in part.items())) for part in parts],
        )
        print(sum_interval_ratings(accepted))
