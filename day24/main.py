import math
import sys

from fractions import Fraction
from functools import partial
from typing import Callable, Iterable, List, Tuple, TypeVar
import operator

import numpy as np


def parse_input(data):
    result = []
    for line in "".join(data).strip().splitlines():
        ps, vs = line.split("@")
        result.append(
            (
                tuple(int(p.strip()) for p in ps.split(",")),
                tuple(int(v.strip()) for v in vs.split(",")),
            )
        )
    return result


def count_xy_intersections(hailstones, minmax):
    intersections = 0
    # Convert hailstones to line segments in test area
    # px + a * vx = minx, px + b * vx = maxx
    # py + c * vy = miny, py + d * vy = maxy
    min_t, max_t = 0, 0
    for (px, py, _), (vx, vy, _) in hailstones:
        a = (minmax[0] - px) / vx if vx else 0
        b = (minmax[1] - px) / vx if vx else 0
        c = (minmax[0] - py) / vy if vy else 0
        d = (minmax[1] - py) / vy if vy else 0
        abcd = list(filter(lambda t: 0 <= t, [a, b, c, d]))
        if abcd:
            min_t = min(min_t, math.floor(min(abcd)))
            max_t = max(max_t, math.ceil(max(abcd)))
    segments = [
        (
            (px + min_t * vx, py + min_t * vy),
            (px + max_t * vx, py + max_t * vy),
            (vx, vy),
        )
        for (px, py, _), (vx, vy, _) in hailstones
    ]
    pairs = ((a, b) for a in segments for b in segments if a != b)
    for ((x1, y1), (x2, y2), (avx, avy)), ((x3, y3), (x4, y4), (bvx, bvy)) in pairs:
        if avx * bvy == bvx * avy:  # lines are parallel
            continue
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t_numer = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        u_numer = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)
        if 0 <= t_numer <= denom and 0 <= u_numer <= denom:  # lines intersect
            t = t_numer / denom
            ix, iy = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
            if minmax[0] <= ix <= minmax[1] and minmax[0] <= iy <= minmax[1]:
                intersections += 1
    return intersections


def to_real(v: int | float | Fraction) -> int | float:
    if isinstance(v, Fraction):
        return v.numerator if v.denominator == 1 else float(v)
    else:
        return v


Coord3d = Tuple[int | float, int | float, int | float]

# ri, vi, rj, vj are the positions and velocities of the i-th and j-th hailstones
# r0, v0 are the position and velocity of the rock
# ti is the time of collision for the i-th hailstone
# ri + vi * ti = r0 + v0 * tn (must hold for each hailstone)
# (vi - v0) * ti = r0 - ri (rearrange terms)
# (vi - v0) X (ri - r0) = 0 (apply cross product of (vi - v0) to both sides)
# (vi X ri) - (vi X r0) - (v0 X ri) + (v0 X r0) = 0 (distribute product over addition)
# (vi X ri) - (vi X r0) - (v0 X ri) - (vj X rj) + (vj X r0) + (v0 X rj) = 0 (take difference with itself but using j as the count)
# (r0 X vi) - (r0 X vj) + (v0 X rj) - (v0 X ri) - (vj X rj) + (vi X ri) = 0 (rearrange terms)
# r0 X (vi - vj) + v0 X (rj - ri) = (vj X rj) - (vi X ri) (factor terms and collect unknowns on LHS)

T = TypeVar("T", list, tuple)


def dot_operate(op: Callable, a: T, b: T) -> T:
    if len(a) != len(b):
        raise Exception(f"{a} has different dimensions to {b}")
    result = list(a)
    for i, bi in enumerate(b):
        result[i] = op(a[i], bi)
    if isinstance(a, list):
        return result
    if isinstance(a, tuple):
        return tuple(result)


dot = {
    "+": partial(dot_operate, operator.__add__),
    "-": partial(dot_operate, operator.__sub__),
}


def cross(a: Coord3d, b: Coord3d) -> Coord3d:
    return (
        (a[1] * b[2] - a[2] * b[1]),
        (a[2] * b[0] - a[0] * b[2]),
        (a[0] * b[1] - a[1] * b[0]),
    )


def get_mat_coeff(
    hailstones: List[Tuple[Coord3d, Coord3d]], r: Coord3d, v: Coord3d, i: int, j: int
) -> Coord3d:
    return dot["+"](
        cross(r, dot["-"](hailstones[i][1], hailstones[j][1])),
        cross(v, dot["-"](hailstones[j][0], hailstones[i][0])),
    )


def get_rhs(hailstones: List[Tuple[Coord3d, Coord3d]], i: int, j: int) -> Coord3d:
    return dot["-"](
        cross(hailstones[j][1], hailstones[j][0]),
        cross(hailstones[i][1], hailstones[i][0]),
    )


def get_eq_strip(
    hailstones: List[Tuple[Coord3d, Coord3d]], i: int, j: int
) -> Tuple[Tuple[Iterable[int | float]], Coord3d]:
    a = get_mat_coeff(hailstones, (1, 0, 0), (0, 0, 0), i, j)
    b = get_mat_coeff(hailstones, (0, 1, 0), (0, 0, 0), i, j)
    c = get_mat_coeff(hailstones, (0, 0, 1), (0, 0, 0), i, j)
    d = get_mat_coeff(hailstones, (0, 0, 0), (1, 0, 0), i, j)
    e = get_mat_coeff(hailstones, (0, 0, 0), (0, 1, 0), i, j)
    f = get_mat_coeff(hailstones, (0, 0, 0), (0, 0, 1), i, j)
    return tuple(map(tuple, zip(a, b, c, d, e, f))), get_rhs(hailstones, i, j)


def get_eq(hailstones: List[Tuple[Coord3d, Coord3d]], i: int, j: int, k: int):
    a, b = get_eq_strip(hailstones, i, j)
    c, d = get_eq_strip(hailstones, j, k)
    return a + c, b + d


def find_one_shot(
    hailstones: List[Tuple[Coord3d, Coord3d]]
) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    for i in range(len(hailstones) - 2):
        a, y = get_eq(hailstones, i, i + 1, i + 2)
        if np.linalg.det(np.array(a)) != 0:
            x = list(map(int, np.round(np.linalg.solve(np.array(a), np.array(y)))))
            # print(f"Solved with hailstones {list(range(i, 3))}")
            return (x[0], x[1], x[2]), (x[3], x[4], x[5])
        else:
            pass
            # print(f"Cannot solve with hailstones {list(range(i, 3))}")
    raise Exception("Cannot find solution")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        hailstones = parse_input(sys.stdin)
        r, _ = find_one_shot(hailstones)
        print(sum(r))
    else:
        hailstones = parse_input(sys.stdin)
        minmax = (7, 27) if len(hailstones) == 5 else (200000000000000, 400000000000000)
        print(count_xy_intersections(hailstones, minmax))
