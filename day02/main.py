import math
from os import path

red, green, blue = "red", "green", "blue"


def parse_input(filename: str):
    result = []
    with open(path.abspath(filename)) as file:
        for line in map(str.strip, file.readlines()):
            result.append(
                [
                    {
                        cubes.split(" ")[1]: int(cubes.split(" ")[0])
                        for cubes in revealed.split(", ")
                    }
                    for revealed in line.split(": ")[1].split("; ")
                ]
            )
    return result


def possible_games(games, total):
    return [
        i + 1
        if all(count <= total[color] for aset in sets for color, count in aset.items())
        else 0
        for i, sets in enumerate(games)
    ]


def power_of(games):
    result = []
    for game in games:
        color_to_maxcount = {}
        for aset in game:
            for color, count in aset.items():
                color_to_maxcount[color] = int(
                    max(count, color_to_maxcount.get(color, 0))
                )
        result.append(math.prod(color_to_maxcount.values()))
    return result


if __name__ == "__main__":
    total = {
        red: 12,
        green: 13,
        blue: 14,
    }
    example_input = parse_input("example.txt")
    print("Example Part 1:", sum(possible_games(example_input, total)))
    print("Example Part 2:", sum(power_of(example_input)))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", sum(possible_games(puzzle_input, total)))
    print("Part 2:", sum(power_of(puzzle_input)))
