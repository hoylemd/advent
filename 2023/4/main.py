from argparse import ArgumentParser
from utils import logger, parse_input
from collections import deque


def parse_card(card):
    _, numbers = card.split(': ')
    winning, have = numbers.split(' | ')
    return [int(w) for w in winning.split()], [int(h) for h in have.split()]


def find_matches(winning, have):
    logger.debug(f"w: {winning}, h: {have}")
    return set(winning).intersection(set(have))


def score_card(winning, have):
    matches = find_matches(winning, have)
    score = 2 ** (len(matches) - 1) if matches else 0

    logger.info(f"matches: {matches}, score: {score}")

    return score


def score_cards(cards):
    return sum(score_card(*parse_card(card)) for card in cards)


def tribble_cards(cards):
    accumulator = 0
    bonus_cards = deque()
    card_num = 0
    for matches in (len(find_matches(*parse_card(card))) for card in cards):
        card_num += 1
        try:
            bonuses = bonus_cards.popleft()
        except IndexError:
            bonuses = 0
        logger.info(f"Card {card_num}: has {bonuses} bonus cards and {matches} matches.")

        copies = 1 + bonuses
        accumulator += copies
        logger.info(f"{accumulator} cards so far")

        # add bonuses from this card
        for i in range(matches):
            try:
                bonus_cards[i] += copies
            except IndexError:
                bonus_cards.append(copies)

    return accumulator


arg_parser = ArgumentParser('python -m 2023.4.main', description="Advent of Code 2023 Day 4")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    cards = parse_input(argus.input_path)

    if argus.part == 1:
        answer = score_cards(cards)
    else:
        answer = tribble_cards(cards)

    print(f"answer:\n{answer}")
