import math
from operator import itemgetter
from os import path


def parse_input(filename: str):
    directions, *rest = filter(
        len, map(str.strip, open(path.abspath(filename)).readlines())
    )
    nodes = {}
    for line in rest:
        name, lr = line.split(" = ")
        nodes[name] = lr.replace("(", "").replace(")", "").split(", ")
    return directions, nodes


def direction_idx(direction: str):
    return 0 if direction == "L" else 1


def navigate(nodes, src: str, dest, directions: str, start_dir: int = 0):
    i = start_dir
    last_visited = src
    while last_visited not in dest:
        if all(lr == last_visited for lr in nodes[last_visited]):
            raise Exception(f"Trapped in a loop in node {last_visited}")
        next_direction = direction_idx(directions[i % len(directions)])
        last_visited = nodes[last_visited][next_direction]
        i += 1
    return i, last_visited


def lcm(*values: int):
    result = values[0]
    for v in values[1:]:
        result = abs(result * v) // math.gcd(result, v)
    return result


def names_ending_with(names, suffix: str):
    return filter(lambda n: n.endswith(suffix), names)


def navigate_all(nodes, src, dest, directions: str) -> int:
    node_to_phase = {node: navigate(nodes, node, dest, directions) for node in src}
    return lcm(*map(itemgetter(0), node_to_phase.values()))


def main():
    example1_input = parse_input("example1.txt")
    print(
        "Example 1 part 1:",
        navigate(example1_input[1], "AAA", {"ZZZ"}, example1_input[0])[0],
    )
    example2_input = parse_input("example2.txt")
    print(
        "Example 2 part 1:",
        navigate(example2_input[1], "AAA", {"ZZZ"}, example2_input[0])[0],
    )
    puzzle_input = parse_input("input.txt")
    print("Part 1:", navigate(puzzle_input[1], "AAA", {"ZZZ"}, puzzle_input[0])[0])
    example3_input = parse_input("example3.txt")
    print(
        "Example 3 part 2:",
        navigate_all(
            example3_input[1],
            set(names_ending_with(example3_input[1].keys(), "A")),
            set(names_ending_with(example3_input[1].keys(), "Z")),
            example3_input[0],
        ),
    )
    print(
        "Part 2:",
        navigate_all(
            puzzle_input[1],
            set(names_ending_with(puzzle_input[1].keys(), "A")),
            set(names_ending_with(puzzle_input[1].keys(), "Z")),
            puzzle_input[0],
        ),
    )


if __name__ == "__main__":
    main()
