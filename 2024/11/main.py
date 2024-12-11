from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


def parse_line(line: str) -> Iterator[int]:
    for num in line.split():
        yield int(num)


class StoneArray:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.stones = list(self.parse_lines(lines))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_lines(self, lines: Iterator[str]) -> Iterator[int]:
        for line in lines:
            for num in parse_line(line):
                yield num

    def esrap_lines(self) -> str:
        return ' '.join(f"{stone}" for stone in self.stones)

def answer2(stone_array: StoneArray) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(stone_array: StoneArray) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.11.main', description="Advent of Code 2024 Day 11")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    stone_array = StoneArray(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = stone_array.esrap_lines()
        case 1:
            answer = answer1(stone_array)
        case 2:
            answer = answer2(stone_array)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
