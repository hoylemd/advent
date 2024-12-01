from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


def parse_line(line: str) -> tuple:
    first, second = line.split()
    return int(first), int(second)


class Bilist:
    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.first_list = []
        self.second_list = []

        for first, second in (parse_line(line) for line in lines):
            print(f"parsing out {first}, {second}")
            self.first_list.append(first)
            self.second_list.append(second)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"


def answer2(bilist: Bilist) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(bilist: Bilist) -> int:
    accumulator = 0

    for first, second in zip(sorted(bilist.first_list), sorted(bilist.second_list)):
        print(f"comparing {first}, {second}: {abs(second - first)}")
        accumulator += abs(second - first)

    return accumulator


arg_parser = ArgumentParser('python -m 2024.1.main', description="Advent of Code 2024 Day 1")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    bilist = Bilist(lines)
    if argus.part == 1:
        answer = answer1(bilist)
    else:
        answer = answer2(bilist)

    logger.debug('')

    print(f"answer:\n{answer}")
