from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator, Mapping
from collections import defaultdict
from functools import cached_property

type coord = tuple[int, int]


def parse_line(line: str) -> Iterator[tuple[int, str]]:
    for x, c in enumerate(line):
        if c == '.':
            continue
        yield (x, c)


class AntennaMap:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.height = 0
        self.width = 0

        self.antennas = self.parse_lines(lines)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_lines(self, lines: Iterator[str]) -> Mapping[str, list[coord]]:
        antennas = defaultdict(list)
        for y, line in enumerate(lines):
            if not self.width:
                self.width = len(line)
            self.height += 1

            for x, c in parse_line(line):
                antennas[c].append((y, x))

        return antennas

    @cached_property
    def reverse_map(self) -> Mapping[coord, str]:
        rev_map = {}
        for c, coords in self.antennas.items():
            for coord in coords:
                rev_map[coord] = c

        return rev_map

    def esrap_line(self, y: int) -> str:
        return ''.join(
            self.reverse_map.get((y, x), '.') for x in range(self.width)
        )

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y) for y in range(self.height)
        )


def answer2(antenna_map: AntennaMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(antenna_map: AntennaMap) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.8.main', description="Advent of Code 2024 Day 8")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    antenna_map = AntennaMap(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = antenna_map.esrap_lines()
        case 1:
            answer = answer1(antenna_map)
        case 2:
            answer = answer2(antenna_map)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
