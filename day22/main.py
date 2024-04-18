import sys

from operator import itemgetter
from typing import Dict, Iterable, List, Tuple, Set

Point2d = Tuple[int, int]
Point3d = Tuple[int, int, int]
Brick = Tuple[Point3d, Point3d]
MinMax = Tuple[Point2d, Point2d, Point2d]
BelowAbove = Dict[Brick, Tuple[Set[Brick], Set[Brick]]]

def parse_input(lines: Iterable[str]) -> List[Brick]:
    result = []
    for line in filter(len, (line.strip() for line in lines)):
        a, b = (map(int, p.split(",")) for p in line.split("~"))
        result.append(tuple((x, y, z) for x, y, z in [a, b]))
    return result

def cubes_of(brick: Brick) -> List[Point3d]:
    min_max = [(min(map(itemgetter(dim), brick)), max(map(itemgetter(dim), brick)) + 1) for dim in range(3)]
    return [(x, y, z)for z in range(*min_max[2]) for y in range(*min_max[1]) for x in range(*min_max[0])]

def minmax_of(brick: Brick) -> MinMax:
    return tuple((min(map(itemgetter(dim), brick)), max(map(itemgetter(dim), brick)) + 1) for dim in range(3))

def z_move(brick: Brick, steps: int) -> Brick:
    return tuple((x, y, z + steps) for x, y, z in brick)

def intersect_minmax(a: MinMax, b: MinMax) -> bool:
    (axmin, axmax), (aymin, aymax), (azmin, azmax) = a
    (bxmin, bxmax), (bymin, bymax), (bzmin, bzmax) = b
    return (
        axmin < bxmax and
        axmax > bxmin and
        aymin < bymax and
        aymax > bymin and
        azmin < bzmax and
        azmax > bzmin
    );

def settle(bricks: List[Brick]) -> BelowAbove:
    moving = sorted(bricks, key=lambda brick: min(map(itemgetter(2), brick)), reverse=True)
    stopped: Dict[Brick, MinMax] = {}
    belowabove: BelowAbove = {}
    while moving:
        brick = moving.pop()
        next_brick = z_move(brick, -1)
        next_minmax = minmax_of(next_brick)
        _, _, (nextzmin, _) = next_minmax
        if nextzmin < 1:
            stopped[brick] = minmax_of(brick)
            belowabove[brick] = (set(), set())
            continue
        intersected = set(sbrick for sbrick, sminmax in stopped.items() if intersect_minmax(sminmax, next_minmax))
        if intersected:
            for ibrick in intersected:
                belowabove[ibrick][1].add(brick)
            belowabove[brick] = (intersected, set())
            stopped[brick] = minmax_of(brick)
            continue
        moving.append(next_brick)
    return belowabove

def distintegratable(belowabove: BelowAbove) -> Set[Brick]:
    critical_bricks = set(next(iter(below)) for _, (below, _) in belowabove.items() if len(below) == 1)
    return set(belowabove.keys()) - critical_bricks

def chain_reaction(belowabove: BelowAbove, brick: Brick) -> Set[Brick]:
    cbelowabove = belowabove.copy()
    jobs = [brick]
    falling = set()
    while jobs:
        removed = jobs.pop()
        _, above_removed = cbelowabove[removed]
        for supported_brick in above_removed:
            cbelowabove[supported_brick] = (set(filter(lambda it: it != removed, cbelowabove[supported_brick][0])), cbelowabove[supported_brick][1])
            below_supported, _ = cbelowabove[supported_brick]
            if not below_supported:
                falling.add(supported_brick)
                jobs.append(supported_brick)
    return falling
    
def chainable(bricks: List[Brick]) -> int:
    belowabove = settle(bricks)
    return sum(len(chain_reaction(belowabove, brick)) for brick in set(belowabove.keys()) - distintegratable(belowabove))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        bricks = parse_input(sys.stdin)
        print("chain", chainable(bricks))
    else:
        bricks = parse_input(sys.stdin)
        belowabove = settle(bricks)
        print("disintegratable", len(distintegratable(belowabove)))
