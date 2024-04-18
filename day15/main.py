import re
import sys
from operator import itemgetter
from typing import Dict, Iterable, List, Tuple


def parse_input(input: Iterable[str]):
    return [
        op
        for oplist in (
            line.split(",") for line in (line.strip() for line in input) if line
        )
        for op in oplist
    ]


def hash_str(input: str) -> int:
    hash_val = 0
    for ch in input:
        hash_val += ord(ch)
        hash_val *= 17
        hash_val %= 256
    return hash_val


def create_boxes() -> List[Dict[str, Tuple[int, int]]]:
    return [{} for _ in range(256)]


def hashmap_cmd(boxes: List[Dict[str, Tuple[int, int]]], cmd: str):
    new_boxes = [box.copy() for box in boxes]
    gid = 1000
    label, focal_len = (re.split(r"[-=]", cmd) + [""])[0:2]
    box_idx = hash_str(label)
    if "-" in cmd:
        if label in new_boxes[box_idx]:
            del new_boxes[box_idx][label]
    elif "=" in cmd:
        new_boxes[box_idx][label] = (gid, int(focal_len))
        gid += 1
    return new_boxes


def calc_focus_power(boxes: List[Dict[str, Tuple[int, int]]]):
    result = 0
    for box_idx, box in zip(range(len(boxes)), boxes):
        for slot_idx, focal_len in zip(
            range(len(box)), map(itemgetter(1), sorted(box.values(), key=itemgetter(0)))
        ):
            result += (1 + box_idx) * (1 + slot_idx) * focal_len
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        boxes = create_boxes()
        for cmd in parse_input(sys.stdin):
            boxes = hashmap_cmd(boxes, cmd)
        print(calc_focus_power(boxes))
    else:
        print(sum(hash_str(cmd) for cmd in parse_input(sys.stdin)))
