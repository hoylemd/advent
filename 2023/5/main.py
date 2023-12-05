from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


def answer_second_part(almanac: Iterator[str]) -> int:
    accumulator = 0

    for line in almanac:
        pass

    return accumulator


def find_lowest_location(almanac: Iterator[str]) -> int:
    accumulator = 0

    for line in almanac:
        pass

    return accumulator


arg_parser = ArgumentParser('python -m 2023.5.main', description="Advent of Code 2023 Day 5")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    almanac = parse_input(argus.input_path)
    if argus.part == 1:
        answer = find_lowest_location(almanac)
    else:
        answer = answer_second_part(almanac)

    logger.debug('')

    print(f"answer:\n{answer}")
