import os
from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input


def parse_range(range: str) -> tuple[int, int]:
    parts = range.split('-')
    return (int(parts[0]), int(parts[1]))


def parse_ranges(line, part=1):
    range_specs = line.split(',')
    return (parse_range(spec) for spec in range_specs)


def esrap_range(range: tuple[int, int]) -> str:
    return f"{range[0]}-{range[1]}"


def esrap_ranges(ranges):
    return ','.join(esrap_range(range) for range in ranges)


class Thing:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.elements = [line for line in self.parse_lines(lines)]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> str:
        return line

    def parse_lines(self, lines: Iterator[str]) -> Iterator:
        for y, line in enumerate(lines):
            yield self.parse_line(y, line)

    def esrap_line(self, y: int, element: str) -> str:
        return f"{element}"

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, e) for y, e in enumerate(self.elements)
        )


def answer2(ranges: Iterator[tuple[int, int]], **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(ranges: Iterator[tuple[int, int]], **_: dict) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


INPUT_PARAMS = {
    ('test.txt'): {
    },
    ('input.txt'): {
    }
}


arg_parser = ArgumentParser('python -m 2025.2.main', description="Advent of Code 2025 Day 2")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    params = INPUT_PARAMS[os.path.basename(argus.input_path)]
    lines = parse_input(argus.input_path)
    ranges = parse_ranges([line for line in lines][0], part=argus.part)
    match argus.part:
        case -1:
            answer = esrap_ranges(ranges)
        case 1:
            answer = answer1(ranges, **params)
        case 2:
            answer = answer2(ranges, **params)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
