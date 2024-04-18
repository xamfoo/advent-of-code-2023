import math
import operator
from os import path


def parse_input(filename: str):
    times, distances = [
        map(int, line.split()[1:])
        for line in map(str.strip, open(path.abspath(filename)).readlines())
    ]
    return list(zip(times, distances))


# a, v is acceleration and velocity
# t, t_btn are race duration and button press time
# d, d_rec is distance travelled and record distance
# a = 1
# v = a*t_btn
# d = v*(t - t_btn)
# d = t_btn*(t - t_btn) (substitute v and a = 1)
# d_rec + 1 = (t * t_btn) - t_btn^2 (min button press time to beat record)
# t_btn^2 - t * t_btn  + (d_rec + 1) = 0 (arrange to quadratic equation)
# a = 1, b = -t, c = (d_rec + 1), t_btn = (-b (+-)(b^2 - 4ac)^0.5) / 2a


def calc_btn_press_ms(races):
    results = []
    for t, d_rec in races:
        b = -t
        c = d_rec + 1
        min_t_btn, max_t_btn = sorted(
            [
                op(-b, (b**2 - 4 * c) ** 0.5) / 2
                for op in (operator.__add__, operator.__sub__)
            ]
        )
        results.append((math.ceil(min_t_btn), math.floor(max_t_btn)))
    return results


def error_margin(t_btn):
    return t_btn[1] + 1 - t_btn[0]


def fix_kerning(races):
    return [tuple(map(int, ("".join(str(td[i]) for td in races) for i in range(2))))]


def main():
    example_input = parse_input("example.txt")
    print("Example part 1:", math.prod(map(error_margin, calc_btn_press_ms(example_input))))
    print("Example part 2:", error_margin(calc_btn_press_ms(fix_kerning(example_input))[0]))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", math.prod(map(error_margin, calc_btn_press_ms(puzzle_input))))
    print("Part 2:", error_margin(calc_btn_press_ms(fix_kerning(puzzle_input))[0]))


if __name__ == "__main__":
    main()
