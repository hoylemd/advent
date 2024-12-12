from argparse import ArgumentParser
from typing import Iterator, Mapping
from collections import defaultdict

from utils import logger, parse_input, CharGrid, coordinates, INFINITY

type stripe = tuple[str, int, int] # crop, offset, length


class Region:
    def __init__(self, first_y: int, first_stripe: stripe):
        self.crop = first_stripe[0]
        """
        self.y = first_y
        self.x = first_stripe[1]
        self.height = 1
        self.width = first_stripe[2]
        """
        self.stripes = defaultdict(list[stripe])

        self._add_stripe(first_y, first_stripe)

    def _add_stripe(self, y: int, next_stripe: stripe):
        c, x, l = next_stripe

        if c != self.crop:
            raise ValueError('Cannot add stripe of different crop')

        """
        if (delta_y := y - self.y) < 0:
            self.y = y
            self.height += delta_y

        if (delta_x := x - self.x) < 0:
            self.x
        """
        current_row = self.stripes[y]
        current_row.append(next_stripe)

        self.stripes[y] = sorted(current_row, key=lambda s: s[1])

    def add_stripe(self, y: int, next_stripe: stripe):
        self._add_stripe(y, next_stripe)
        self.compute_bounds()

    def add_stripes(self, stripes: Mapping[int, list[stripe]]):
        for y, y_stripes in stripes.items():
            for s in y_stripes:
                self._add_stripe(y, s)

        self.compute_bounds()

    def compute_bounds(self):
        ys = sorted(self.stripes.keys())

        self.y = ys[0]
        self.height = len(ys)

        self.x = INFINITY
        right = 0
        for y in ys:
            for s in self.stripes[y]:
                s_right = s[1] + s[2]

                if self.x is None:
                    self.x = s[1]

                if s[1] < self.x:
                    # if new stripe offset is to the left
                    self.x = s[1]

                if s_right > right:
                    # if new right is to the right
                    right = s_right

        self.width = right - self.x


class GardenMap(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.rows = list(self.parse_lines(lines))

        self.regions = list(self.merge_regions())

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> Iterator[stripe]:
        current_crop = ''
        current_offset = 0

        for i, c in enumerate(line):
            if c != current_crop:
                # new stripe
                if current_crop:
                    yield (current_crop, current_offset, i - current_offset)

                current_offset = i
                current_crop = c

        yield (current_crop, current_offset, i - current_offset + 1)


    def parse_lines(self, lines: Iterator[str]) -> Iterator[list[stripe]]:
        for y, line in enumerate(lines):
            yield list(self.parse_line(y, line))

    def esrap_line(self, y: int, row: list[stripe]) -> str:
        return ''.join(f"{c * l}" for c, _, l in row)

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, r) for y, r in enumerate(self.rows)
        )

    def print_stripes(self) -> str:
        return '\n'.join(f"{row}" for row in self.rows)

    def merge_regions(self) -> Iterator[Region]
        pass


def answer2(garden: GardenMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(garden: GardenMap) -> int:
    accumulator = 0

    logger.info(garden.print_stripes())
    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.12.main', description="Advent of Code 2024 Day 12")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    garden = GardenMap(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = garden.esrap_lines()
        case 1:
            answer = answer1(garden)
        case 2:
            answer = answer2(garden)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
