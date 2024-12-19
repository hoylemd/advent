from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


class LinenLayout:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.towels, self.designs = self.parse_lines(lines)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> str:
        return line

    def parse_lines(self, lines: Iterator[str]) -> tuple[list[str],list[str]]:
        towels = []
        designs = []
        for y, line in enumerate(lines):
            if y == 0:
                towels = line.split(', ')
                continue
            if not line:
                continue
            designs.append(line)

        return towels, designs


    def esrap_lines(self) -> str:
        return '\n'.join([
            ', '.join(self.towels),
            ''
        ] + self.designs)

def answer2(towels: LinenLayout) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(towels: LinenLayout) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.19.main', description="Advent of Code 2024 Day 19")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    towels = LinenLayout(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = towels.esrap_lines()
        case 1:
            answer = answer1(towels)
        case 2:
            answer = answer2(towels)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
