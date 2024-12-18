from argparse import ArgumentParser
from typing import Iterator
import os

from utils import logger, parse_input, CharGrid, coordinates

class RamRun(CharGrid):

    def __init__(self, lines: Iterator[str], height: int, width: int, part: int = 1):
        self.part = part

        self.lines = self.init_grid(height, width)

        self.blocks = [line for line in self.parse_lines(lines)]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> coordinates:
        xs, ys = line.split(',')
        return int(ys), int(xs)

    def parse_lines(self, lines: Iterator[str]) -> Iterator[coordinates]:
        for y, line in enumerate(lines):
            yield self.parse_line(y, line)

    def esrap_line(self, y: int, block_coords: coordinates) -> str:
        return f"{block_coords[1]},{block_coords[0]}"

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, e) for y, e in enumerate(self.blocks)
        )

def answer2(ram: RamRun) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(ram: RamRun) -> int:
    accumulator = 0

    # solve part 1

    return accumulator

PART_PARAMS = {
    ('test.txt', 1): {
        'width': 6,
        'height': 6
    }
}

arg_parser = ArgumentParser('python -m 2024.18.main', description="Advent of Code 2024 Day 18")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    dimensions = PART_PARAMS[os.path.basename(argus.input_path), abs(argus.part)]
    lines = parse_input(argus.input_path)
    ram = RamRun(lines, **dimensions, part=argus.part)
    match argus.part:
        case -1:
            answer = ram.esrap_lines()
        case 1:
            answer = answer1(ram)
        case 2:
            answer = answer2(ram)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
