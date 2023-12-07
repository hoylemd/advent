from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator, Tuple
from collections import defaultdict
from functools import cmp_to_key


def parse_hand_line(line: str, part=1) -> Tuple[str, int]:
    h, b = line.split()
    if part > 1:
        h = h.replace('J', 'j')
    return h, int(b), part


# string lookups in dicts are actually quite a but faster than parsing the digit
CARD_VALUES = {c: int(c) for c in '23456789'} | {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
    'j': 1  # special joker value
}


class Hand:
    def __init__(self, hand_spec: str, bid: int, part=1):
        self.bid = bid
        self._hand_spec = hand_spec

        types = defaultdict(int)
        for card in hand_spec:
            types[card] += 1

        if part > 1 and 'j' in types and len(types) > 1:
            jokers = types['j']
            del types['j']
            best_type = sorted(types.items(), key=lambda x: (x[1], x[0]))[-1][0]
            types[best_type] += jokers

        type_counts = sorted(types.values())
        match len(type_counts):
            case 1:
                self.strength = 6  # 5 of a kind
            case 2:
                if type_counts[-1] == 4:
                    self.strength = 5  # 4 of a kind
                else:
                    self.strength = 4  # full house
            case 3:
                if type_counts[-1] == 3:
                    self.strength = 3  # 3 of a kind
                else:
                    self.strength = 2  # Two pair
            case 4:
                self.strength = 1  # One pair
            case _:
                self.strength = 0  # High card

    @property
    def card_values(self) -> Iterator[int]:
        for card in self._hand_spec:
            yield CARD_VALUES[card]

    def __str__(self) -> str:
        return f"{self._hand_spec}: {self.strength}, bid {self.bid}"


def compare_hands(left: Hand, right: Hand):
    if left.strength < right.strength:
        return -1
    elif left.strength > right.strength:
        return 1

    # same hand strength, compare individual cards
    for l_card, r_card in zip(left.card_values, right.card_values):
        if l_card < r_card:
            return -1
        elif l_card > r_card:
            return 1

    # they're the same hand wtf?
    logger.info("compared 2 identical hands? {left}, {right}")
    return 0


def sub_bids_times_rank(hands: list[Hand]) -> int:
    hands.sort(key=cmp_to_key(compare_hands))

    accumulator = 0

    logger.info("Sorted hands:")
    for i, hand in enumerate(hands):
        logger.info(hand)
        accumulator += (i + 1) * hand.bid

    return accumulator


arg_parser = ArgumentParser('python -m 2023.7.main', description="Advent of Code 2023 Day 7")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    hands = [Hand(*parse_hand_line(line, argus.part)) for line in parse_input(argus.input_path)]
    answer = sub_bids_times_rank(hands)

    logger.debug('')

    print(f"answer:\n{answer}")
