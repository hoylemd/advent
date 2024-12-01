from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator
from collections import defaultdict


def parse_line(line: str) -> tuple:
    left, right = line.split()
    return int(left), int(right)


class Bilist:
    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.left_list = []
        self.right_list = []
        self.right_counts = defaultdict(int)

        for left, right in (parse_line(line) for line in lines):
            print(f"parsing out {left}, {right}")
            self.left_list.append(left)
            self.right_list.append(right)
            self.right_counts[right] += 1

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"


def sum_similarity(bilist: Bilist) -> int:
    return sum(bilist.right_counts[left] * left for left in bilist.left_list)


def sum_distances(bilist: Bilist) -> int:
    accumulator = 0

    for left, right in zip(sorted(bilist.left_list), sorted(bilist.right_list)):
        print(f"comparing {left}, {right}: {abs(right - left)}")
        accumulator += abs(right - left)

    return accumulator


arg_parser = ArgumentParser('python -m 2024.1.main', description="Advent of Code 2024 Day 1")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    bilist = Bilist(lines)
    if argus.part == 1:
        answer = sum_distances(bilist)
    else:
        answer = sum_similarity(bilist)

    logger.debug('')

    print(f"answer:\n{answer}")
