from collections import Counter
from operator import itemgetter
from os import path


CARDS = list(map(str, range(2, 10))) + ["T", "J", "Q", "K", "A"]
CARD_TO_RANK = {c: i for i, c in enumerate(CARDS)}

JCARDS = ["J"] + list(map(str, range(2, 10))) + ["T", "Q", "K", "A"]
JCARD_TO_RANK = {c: i for i, c in enumerate(JCARDS)}


def type_strength(hand):
    card_to_num = {}
    for card in hand:
        card_to_num[card] = card_to_num.get(card, 0) + 1
    values = sorted(card_to_num.values(), reverse=True)
    if values == [5]:
        return 50
    elif values == [4, 1]:
        return 41
    elif values == [3, 2]:
        return 32
    elif values == [3, 1, 1]:
        return 31
    elif values == [2, 2, 1]:
        return 22
    elif values == [2, 1, 1, 1]:
        return 21
    elif values == [1, 1, 1, 1, 1]:
        return 11
    else:
        raise Exception(f"Unknown hand type {hand}")


def jtype_strength(hand):
    card_to_count = Counter(hand)
    max_card, _ = max(
        filter(lambda cc: cc[0] != "J", card_to_count.items()),
        default=("J", card_to_count.get("J")),
        key=itemgetter(1),
    )
    return type_strength(hand.replace("J", max_card))


def card_strength(hand):
    return sum(
        CARD_TO_RANK[card] * (len(CARDS) ** i) for i, card in enumerate(reversed(hand))
    )


def jcard_strength(hand):
    return sum(
        JCARD_TO_RANK[card] * (len(JCARDS) ** i)
        for i, card in enumerate(reversed(hand))
    )


def hand_strength(hand):
    return type_strength(hand) * (len(CARDS) ** 5) + card_strength(hand)


def jhand_strength(hand):
    return jtype_strength(hand) * (len(CARDS) ** 5) + jcard_strength(hand)


def parse_input(filename):
    results = []
    for line in map(str.strip, open(path.abspath(filename)).readlines()):
        hand, bid = line.split()
        results.append((hand, int(bid)))
    return results


def calc_winnings(hands):
    return sum(
        (i + 1) * hand[-1]
        for i, hand in enumerate(sorted(hands, key=lambda h: hand_strength(h[0])))
    )


def calc_jwinnings(hands):
    return sum(
        (i + 1) * hand[-1]
        for i, hand in enumerate(sorted(hands, key=lambda h: jhand_strength(h[0])))
    )


def main():
    example_input = parse_input("example.txt")
    print("Example part 1:", calc_winnings(example_input))
    print("Example part 2:", calc_jwinnings(example_input))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", calc_winnings(puzzle_input))
    print("Part 2:", calc_jwinnings(puzzle_input))


if __name__ == "__main__":
    main()
