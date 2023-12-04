from argparse import ArgumentParser
from utils import logger, parse_input


def parse_card(card):
    _, numbers = card.split(': ')
    winning, have = numbers.split(' | ')
    return [int(w) for w in winning.split()], [int(h) for h in have.split()]


def score_card(winning, have):
    logger.info(f"w: {winning}, h: {have}")
    matches = set(winning).intersection(set(have))
    score = 2 ** (len(matches) - 1) if matches else 0

    logger.info(f"matches: {matches}, score: {score}")

    return score


def score_cards(cards):
    return sum(score_card(*parse_card(card)) for card in cards)


arg_parser = ArgumentParser('python -m 2023.4.main', description="Advent of Code 2023 Day 4")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    cards = parse_input(argus.input_path)

    if argus.part == 1:
        answer = score_cards(cards)
    else:
        answer = None

    print(f"answer:\n{answer}")
