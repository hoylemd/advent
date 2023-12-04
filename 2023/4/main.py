from argparse import ArgumentParser
from utils import logger, parse_input


def score_cards(cards):
    pass


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
