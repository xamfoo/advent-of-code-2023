from dataclasses import dataclass, field
from functools import reduce
from heapq import heappush, heappop
import operator
from typing import Dict, List, Tuple

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_input(filename: str):
    return list(map(str.strip, open(filename)))


def dot(*p, op):
    return tuple(reduce(op, s) for s in zip(*p))


def dotsum(*p):
    return dot(*p, op=operator.__add__)


def dotmod(*p):
    return dot(*p, op=operator.__mod__)


@dataclass
class Frontier:
    """
    Priority queue implementation
    """

    heap: List[List[int | Tuple[Tuple[int, ...], int]]] = field(default_factory=list)
    nodes: Dict[
        Tuple[Tuple[int, ...], int], List[int | Tuple[Tuple[int, ...], int]]
    ] = field(default_factory=dict)
    removed = ((-1, -1), -1)

    def push(self, node: Tuple[Tuple[int, ...], int], cost: int):
        if node not in self.nodes:
            self.nodes[node] = [cost, node]
            heappush(self.heap, self.nodes[node])

    def pop(self) -> Tuple[int, Tuple[Tuple[int, ...], int]]:
        while True:
            item = heappop(self.heap)
            if isinstance(item[1], tuple) and item[1] != self.removed:
                del self.nodes[item[1]]
                if isinstance(item[0], int):
                    return (item[0], item[1])
                raise TypeError(f"Unknown heap item {item}")

    def update(self, node: Tuple[Tuple[int, ...], int], cost: int):
        if node not in self.nodes:
            raise KeyError(f"Key {node} does not exist")
        self.nodes[node][1] = self.removed
        self.nodes[node] = [cost, node]
        heappush(self.heap, self.nodes[node])

    def cost_of(self, node: Tuple[Tuple[int, ...], int]) -> int:
        if node not in self.nodes:
            raise KeyError(f"Key {node} does not exist")
        cost = self.nodes[node][0]
        if isinstance(cost, int):
            return cost
        raise TypeError(f"Expected cost as int but got {cost}")


def min_heat_loss(B, ultra=False):
    """
    procedure uniform_cost_search(start) is
        node ← start
        frontier ← priority queue containing node only
        expanded ← empty set
        do
            if frontier is empty then
                return failure
            node ← frontier.pop()
            if node is a goal state then
                return solution(node)
            expanded.add(node)
            for each of node's neighbors n do
                if n is not in expanded and not in frontier then
                    frontier.add(n)
                else if n is in frontier with higher cost
                    replace existing node with n
    """
    start, end, size = (0, 0), (len(B[0]) - 1, len(B) - 1), (len(B[0]), len(B))
    frontier, expanded, cr = Frontier(), set(), (4, 10) if ultra else (1, 3)
    frontier.push((start, -1), 0)

    def h_of(p: Tuple[int, ...]):
        return int(B[p[1]][p[0]])

    while frontier.heap:
        node_cost, node = frontier.pop()
        p, d = node
        if p == end:
            return node_cost
        expanded.add(node)
        for n, t in (
            ((dotsum(*([p] + t * [directions[td]])), td), t)
            for td in set(range(4))
            - (set() if d < 0 else {d, (d + 2) % len(directions)})
            for t in range(cr[0], cr[1] + 1)
        ):
            if n[0] == dotmod(n[0], size):
                nh = (
                    node_cost
                    + h_of(n[0])
                    + sum(
                        h_of(dotsum(*([p] + i * [directions[n[1]]])))
                        for i in range(1, t)
                    )
                )
                if n not in expanded and n not in frontier.nodes:
                    frontier.push(n, nh)
                elif n in frontier.nodes and frontier.cost_of(n) > nh:
                    frontier.update(n, nh)


def main():
    example1_input = parse_input("example1.txt")
    example2_input = parse_input("example2.txt")
    print("Example 1 part 1:", min_heat_loss(example1_input))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", min_heat_loss(puzzle_input))
    print("Example 1 part 2:", min_heat_loss(example1_input, ultra=True))
    print("Example 2 part 2:", min_heat_loss(example2_input, ultra=True))
    print("Part 2:", min_heat_loss(puzzle_input, ultra=True))


if __name__ == "__main__":
    main()
