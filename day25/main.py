from collections import deque
from itertools import combinations
import math
from os import path

def parse_input(filename: str):
    result = {}
    for line in open(path.abspath(filename)):
        src, rest = line.strip().split(": ")
        for dest in rest.split(" "):
            result.setdefault(src, set()).add(dest)
            result.setdefault(dest, set()).add(src)
    return result

def connected_components(graph):
    graph_copy = {src: dests.copy() for src, dests in graph.items()}
    components = []
    while len(graph_copy):
        src, *srcs = graph_copy.keys()
        component = {src} | graph_copy[src]
        for s in srcs:
            group = {s} | graph_copy[s]
            if len(group & component):
                component |= group
                del graph_copy[s]
        components.append(component)
        del graph_copy[src]
    # print(components)
    return components

def calc_disconnect_factor(graph):
    dc_cands = set()
    for src, dests in graph.items():
        for dest in dests:
            if len((dests - {dest}) & (graph[dest] - {src})) == 0:
                dc_cands.add(tuple(sorted([src, dest])))
    print("calc_disconnect_factor", len(dc_cands))
    for dcs in combinations(dc_cands, 3):
        graph_copy = {src: dests.copy() for src, dests in graph.items()}
        for dc in dcs:
            graph_copy[dc[0]].remove(dc[1])
            graph_copy[dc[1]].remove(dc[0])
        cc = list(connected_components(graph_copy))
        if len(cc) == 2:
            # print("dcs", dcs)
            return math.prod(map(len, cc))
    raise Exception("Can not find disconnection factor")

def main():
    example1_input = parse_input("example1.txt")
    print("Example 1 Part 1:", calc_disconnect_factor(example1_input))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", calc_disconnect_factor(puzzle_input))

if __name__ == "__main__":
    main()
