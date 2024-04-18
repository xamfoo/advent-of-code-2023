from pprint import pprint
from dataclasses import dataclass, field
from functools import reduce
import math
import operator
from operator import itemgetter
from os import path
import re
from typing import Callable, Dict, Iterable, List, Optional, Tuple, TypeVar, Set


def dot(*p, op):
    return tuple(reduce(op, s) for s in zip(*p))


def dotsum(*p):
    return dot(*p, op=operator.__add__)


def dotmod(*p):
    return dot(*p, op=operator.__mod__)


ConfigItem = Tuple[str, List[str]]
Config = List[ConfigItem]


def parse_input(filename: str) -> Config:
    return [
        (m, d)
        for m, _, *d in (
            line.replace(",", "").split() for line in open(path.abspath(filename))
        )
    ]


Pulse = Tuple[str, bool, str]


@dataclass
class PulseModule:
    name: str
    dispatch: Callable[[str, bool, List[str]], None]
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)

    def send(self, _: Optional[Pulse] = None):
        pass


@dataclass
class Button(PulseModule):
    def send(self, _: Optional[Pulse] = None):
        self.dispatch(self.name, False, self.outputs)


@dataclass
class Broadcaster(PulseModule):
    def send(self, pulse: Optional[Pulse] = None):
        if pulse is not None:
            self.dispatch(self.name, pulse[1], self.outputs)


@dataclass
class FlipFlop(PulseModule):
    state: bool = False

    def send(self, pulse: Optional[Pulse] = None):
        if pulse and pulse[1] is False:
            self.state = not self.state
            self.dispatch(self.name, self.state, self.outputs)


@dataclass
class Conjunction(PulseModule):
    state: Dict[str, bool] = field(default_factory=dict)

    def send(self, pulse: Optional[Pulse] = None):
        # if self.name == "con":
        #     print("con", self.state, pulse, self.outputs)
        if pulse is None:
            return
        if pulse[1]:
            self.state[pulse[0]] = pulse[1]
        else:
            if pulse[0] in self.state:
                del self.state[pulse[0]]
        self.dispatch(self.name, len(self.state) != len(self.inputs), self.outputs)


class Store:
    pulses: List[Pulse]
    sent_count: int = 0
    name_to_mod: Dict[str, PulseModule]
    name_to_src: Dict[str, List[str]]
    name_to_src_conj: Dict[str, Set[str]]

    def __init__(self, config: Config):
        self.pulses = []
        self.name_to_mod = {}
        self.name_to_src: Dict[str, List[str]] = {}
        for typedsrc, dests in config:
            for name in dests:
                self.name_to_src.setdefault(name, []).append(typedsrc.lstrip("%&"))
        for typedsrc, dests in config:
            if typedsrc == "broadcaster":
                self.name_to_mod[typedsrc] = Broadcaster(
                    name=typedsrc, dispatch=self.dispatch, outputs=dests
                )
            elif typedsrc.startswith("%"):
                self.name_to_mod[typedsrc[1:]] = FlipFlop(
                    name=typedsrc[1:], dispatch=self.dispatch, outputs=dests,
                )
            elif typedsrc.startswith("&"):
                self.name_to_mod[typedsrc[1:]] = Conjunction(
                    name=typedsrc[1:],
                    dispatch=self.dispatch,
                    inputs=self.name_to_src[typedsrc[1:]],
                    outputs=dests,
                )
            else:
                raise NotImplementedError(f"Unknown module type {typedsrc}")
        self.name_to_src_conj = {name: {sc for src in srcs for sc in self.find_src_conj(src)} for name, srcs in self.name_to_src.items()}

    def dispatch(self, src: str, pulse: bool, dests: List[str]):
        for dest in dests:
            self.pulses.append((src, pulse, dest))

    def wait(self):
        while len(self.pulses) > self.sent_count:
            pulse = self.pulses[self.sent_count]
            if pulse[2] in self.name_to_mod:
                self.name_to_mod[pulse[2]].send(pulse)
            self.sent_count += 1
        pulses, self.pulses, self.sent_count = self.pulses, [], 0
        return pulses, {
            name: mod.state
            for name, mod in self.name_to_mod.items()
            if isinstance(mod, (FlipFlop, Conjunction))
        }

    def find_src_conj(self, dest: str):
        srcs = self.name_to_src.get(dest, []).copy()
        src_conjs = set()
        while srcs:
            src = srcs.pop()
            if src == "broadcaster":
                continue
            elif src not in self.name_to_mod or isinstance(self.name_to_mod[src], Conjunction):
                src_conjs.add(src)
            else:
                srcs.extend(self.name_to_src[src])
        return src_conjs


def stringify_pulses(pulses: List[Pulse]):
    result = []
    for pulse in pulses:
        pulsetype = "-high" if pulse[1] else "-low"
        result.append(f"{pulse[0]} {pulsetype}-> {pulse[2]}")
    return "\n".join(result)


def sum_pulses(pulses: List[Pulse]):
    return sum(1 for _, pulsetype, _ in pulses if not pulsetype), sum(
        1 for _, pulsetype, _ in pulses if pulsetype
    )


def check_config(config: Config, times: int = 1000):
    store = Store(config)
    button = Button(name="button", dispatch=store.dispatch, outputs=["broadcaster"])
    tpulses: List[List[Pulse]] = []
    for _ in range(times):
        button.send()
        pulses, _ = store.wait()
        tpulses.append(pulses)
    return dotsum(*(sum_pulses(pulses) for pulses in tpulses))


# class Predictor:
#     def __init__(self, config: List[Tuple[str, List[str]]]):
#         self.store = Store(config)
#         name_to_predictor = {"broadcaster": lambda _: False}
#         for dest in self.store.name_to_mod["broadcaster"].outputs:
#             mod = self.store.name_to_mod[dest]
#             if isinstance(mod, FlipFlop):


# def broadcaster_predictor(self, ):
#     self.store.name_to_mod["broadcaster"].outputs


def watch_module(adj_ls: List[Tuple[str, List[str]]]):
    # src_dests, src_to_type = parse_src_types(adj_ls)
    # src_to_dests, dest_to_srcs = dict(src_dests), dict(invert_adj_ls(src_dests))
    store = Store(adj_ls)
    button = Button(name="button", dispatch=store.dispatch, outputs=["broadcaster"])
    # tpulses: List[List[Pulse]] = []
    name_to_src_conj = {name: src_conj.copy() for name, src_conj in store.name_to_src_conj.items() if src_conj}
    name_to_first_low: Dict[str, int] = {}
    btn_presses = 0
    while name_to_src_conj:
        button.send()
        btn_presses += 1
        pulses, _ = store.wait()
        for src, pulse, dest in pulses:
            # Low pulse sent
            if not pulse and src not in name_to_first_low and src in name_to_src_conj:
                name_to_first_low[src] = btn_presses
                del name_to_src_conj[src]
                print(name_to_src_conj.keys())
                for output in filter(lambda output: output in name_to_src_conj, store.name_to_mod[src].outputs):
                    print("output", output, name_to_src_conj[output])
                    if all(map(lambda src_conj: src_conj in name_to_first_low, name_to_src_conj[output])):
                        name_to_first_low[output] = math.lcm(*map(lambda src_conj: name_to_first_low[src_conj], name_to_src_conj[output]))
                        del name_to_src_conj[output]
                        print(name_to_src_conj.keys())
    return name_to_first_low

    #     # for cm in conj_mods:
    #     # tpulses.append(pulses)
    # # button = Button(name="button", dispatch=store.dispatch, outputs=["broadcaster"])
    # to_find_deps = [mod_name]
    # deps = []
    # depset = set()
    # while to_find_deps:
    #     dep = to_find_deps.pop()
    #     if dep in depset:
    #         continue
    #     deps.append(dep)
    #     depset.add(dep)
    #     for src in dest_to_srcs.get(deps[-1], []):
    #         to_find_deps.append(src)
    # print([(d, src_to_type.get(d)) for d in deps])
    # return None
    # last_pulses: List[List[Pulse]]
    # tpulses:
    # i = 0
    # while True:
    #     i += 1
    #     button.send()
    #     pulses, state = store.wait()
    #     for pulse in pulses:
    #         if pulse[0] == mod_name:
    #     # for pulse in pulses:
    #     #     state.get()
    #     yield pulses
    #     tpulses.append(pulses)
    # return dotsum(*(sum_pulses(pulses) for pulses in tpulses))

TNode = TypeVar("TNode")

def invert_adj_ls(adj_ls: Iterable[Tuple[TNode, Iterable[TNode]]]) -> List[Tuple[TNode, Set[TNode]]]:
    return list(reduce(
        lambda acc, v: acc.setdefault(v[0], set()).update(v[1]) or acc,
        ((d, {src}) for src, dests in adj_ls for d in dests),
        {},
    ).items())


def parse_src_types(
    adj_ls: Iterable[Tuple[str, Iterable[str]]]
) -> Tuple[List[Tuple[str, List[str]]], Dict[str, str]]:
    src_dests: List[Tuple[str, List[str]]] = []
    src_to_type: Dict[str, str] = {}
    for typedsrc, dests in adj_ls:
        match = re.fullmatch(r"^([%&]?)(.+)", typedsrc)
        if not match:
            raise RuntimeError(f"Unable to parse node: {typedsrc}")
        srctype, src = match.groups()
        src_dests.append((src, list(dests)))
        src_to_type[src] = srctype
    return src_dests, src_to_type


def main():
    example1_input = parse_input("example1.txt")
    example2_input = parse_input("example2.txt")
    print("Example 1 part 1:", math.prod(check_config(example1_input)))
    print("Example 1 part 2:", math.prod(check_config(example2_input)))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", math.prod(check_config(puzzle_input)))
    # print(topo_sort(split_mod_states(*parse_src_types(example1_input))))
    print(watch_module(puzzle_input))
    # print("Example 1 part 1:", list(filter(lambda ab: ab[0] != ab[1], (zip(check_config(example1_input, 1), check_config(example1_input, 2))))))
    # print("Example 2 part 1:", list(filter(lambda ab: ab[0] != ab[1], (zip(check_config(example2_input, 1), check_config(example2_input, 4))))))


if __name__ == "__main__":
    main()
