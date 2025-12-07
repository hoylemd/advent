import os
from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input


class Map:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.rows = [line for line in self.parse_lines(lines)]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> list[str]:
        return [cell for cell in line]

    def parse_lines(self, lines: Iterator[str]) -> Iterator[list[str]]:
        for y, line in enumerate(lines):
            yield self.parse_line(y, line)

    def esrap_line(self, y: int, row: list[str]) -> str:
        return f"{''.join(row)}"

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, e) for y, e in enumerate(self.rows)
        )


def answer2(map: Map, **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(map: Map, **_: dict) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


INPUT_PARAMS = {
    ('test.txt'): {
    },
    ('test2.txt'): {
    },
    ('input.txt'): {
    }
}


arg_parser = ArgumentParser('python -m 2025.4.main', description="Advent of Code 2025 Day 4")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    params = INPUT_PARAMS[os.path.basename(argus.input_path)]
    lines = parse_input(argus.input_path)
    map = Map(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = map.esrap_lines()
        case 1:
            answer = answer1(map, **params)
        case 2:
            answer = answer2(map, **params)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
