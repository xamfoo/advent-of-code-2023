from os import path


def parse_input(filename: str):
    return [
        tuple(
            set(map(int, filter(len, numbers.split())))
            for numbers in line.split(": ")[1].split(" | ")
        )
        for line in map(str.strip, open(path.abspath(filename)).readlines())
    ]


def calc_points(cards):
    return [
        int(2 ** (len(win_numbers & my_numbers) - 1))
        for win_numbers, my_numbers in cards
    ]


# 1*C1
# Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
# 1*C1, 2*C2, 2*C3, 2*C4, 2*C5
# Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
# Your copy of card 2 also wins one copy each of cards 3 and 4.
# 1*C1, 2*C2, 4*C3, 4*C4, 2*C5
# Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
# 1*C1, 2*C2, 4*C3, 8*C4, 6*C5
# Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
# 1*C1, 2*C2, 4*C3, 8*C4, 14*C5
# Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
# Your one instance of card 6 (one original) has no matching numbers and wins no more cards.
# 1*C1, 2*C2, 4*C3, 8*C4, 14*C5, 1*C6
def card_wins(cards):
    card_copies = [1] * len(cards)
    for i in range(len(cards)):
        win_numbers, my_numbers = cards[i]
        matching_numbers = win_numbers & my_numbers
        for j in range(1, len(matching_numbers) + 1):
            card_copies[i + j] += card_copies[i]
    return card_copies


def main():
    example_input = parse_input("example.txt")
    print("Example part 1:", sum(calc_points(example_input)))
    print("Example part 2:", sum(card_wins(example_input)))
    puzzle_input = parse_input("input.txt")
    print("Part 1:", sum(calc_points(puzzle_input)))
    print("Part 2:", sum(card_wins(puzzle_input)))


if __name__ == "__main__":
    main()
