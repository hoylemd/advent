from argparse import ArgumentParser
from typing import Iterator, Mapping

from utils import logger, parse_input, CharGrid, coordinates


class TrailMap(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.heads: list[coordinates] = []
        self.tails: list[coordinates] = []
        super().__init__(lines)

    def parse_cell(self, y: int, x: int, c: str) -> int | None:
        i = None if c == '.' else int(c)

        if i == 0:
            self.heads.append((y, x))
        elif i == 9:
            self.tails.append((y, x))

        return i

    def parse_line(self, y: int, line: str) -> list[int | None]:
        return [self.parse_cell(y, x, c) for x, c in enumerate(line)]

    def esrap_cell(self, y: int, x: int) -> str:
        return f"{self.lines[y][x]}"

    def esrap_line(self, y: int, annotations: Mapping[coordinates, str] = {}) -> str:
        return ''.join(annotations.get((y, x), self.esrap_cell(y, x)) for x in range(self.width))


def answer2(trail_map: TrailMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(trail_map: TrailMap) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.10.main', description="Advent of Code 2024 Day 10")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    trail_map = TrailMap(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = trail_map.esrap_lines()
        case 1:
            answer = answer1(trail_map)
        case 2:
            answer = answer2(trail_map)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        logger.info(f"No answer available for part {argus.part}")
        print(-1)
