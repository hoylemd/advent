import os
from argparse import ArgumentParser
from typing import Iterator, Callable

from utils import logger, parse_input

type CellContent = str
type Shader = Callable[[int, int, CellContent], str]


def pass_through(x: int, y: int, value: CellContent) -> str:
    return value


DIRECTIONS = [
    (-1, 0),  # up/north
    (-1, 1),  # up-right/northeast
    (0, 1),  # right/east
    (1, 1),  # down-right/southeast
    (1, 0),  # down/south
    (1, -1),  # down-left/southwest
    (0, -1),  # left/west
    (-1, -1),  # up-left/northwest
]


class Map:
    """Assumes all lines have same length"""
    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.rows = [line for line in self.parse_lines(lines)]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> list[CellContent]:
        return [cell for cell in line]

    def parse_lines(self, lines: Iterator[str]) -> Iterator[list[CellContent]]:
        for y, line in enumerate(lines):
            yield self.parse_line(y, line)

    def esrap_line(self, y: int, row: list[CellContent]) -> str:
        return f"{''.join(row)}"

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, e) for y, e in enumerate(self.rows)
        )

    def cell(self, y: int, x: int) -> CellContent:
        return self.rows[y][x]

    def set_cell(self, y: int, x: int, value: CellContent):
        self.rows[y][x] = value

    def render_cell(self, y: int, x: int, value: CellContent, shader: Shader = pass_through, **kwargs) -> str:
        return shader(y, x, value, **kwargs)

    def render_row(self, y: int, row: list[str], row_delimiter: str = '', **kwargs) -> str:
        return row_delimiter.join(
            self.render_cell(y, x, value, **kwargs)
            for x, value in enumerate(row)
        )

    def render(self, line_delimiter: str = '\n', **kwargs) -> str:
        return line_delimiter.join(
            self.render_row(y, row, **kwargs)
            for y, row in enumerate(self.rows)
        )

    @property
    def min_y(self):
        return 0

    @property
    def min_x(self):
        return 0

    @property
    def max_y(self):
        return len(self.rows) - 1

    @property
    def max_x(self):
        return len(self.rows[0]) - 1

    def in_bounds(self, y: int, x: int) -> bool:
        return (
            (y >= self.min_y and y <= self.max_y) and
            (x >= self.min_x and x <= self.max_x)
        )


class RollMap(Map):
    def __init__(self, *args, **kwargs):
        self.rolls = set()
        self.accessible = set()

        return super().__init__(*args, **kwargs)

    def parse_cell(self, y: int, x: int, cell: str) -> CellContent:
        if cell == '@':
            self.rolls.add((y, x))

        return cell

    def parse_line(self, y: int, line: str) -> list[CellContent]:
        return [self.parse_cell(y, x, cell) for x, cell in enumerate(line)]

    def has_roll(self, y: int, x: int) -> bool:
        return (y, x) in self.rolls

    def render(self) -> str:
        def accessible_shader(y: int, x: int, value: CellContent) -> str:
            if (y, x) in self.accessible:
                return 'x'
            return value

        return super().render(shader=accessible_shader)

    def adjacent_cells(self, y: int, x: int) -> Iterator[tuple[int, int]]:
        assert self.in_bounds(y, x), f"Coordinates {(y, x)} are out of bounds"

        for dy, dx in DIRECTIONS:
            cy, cx = y + dy, x + dx
            if not self.in_bounds(cy, cx):
                continue
            yield (cy, cx)

    def adjacent_rolls(self, y: int, x: int) -> list[tuple[int, int]]:
        # return [(cy, cx) for cy, cx in self.adjacent_cells(y, x) if ((cy, cx) in self.rolls)]
        adj_rolls = []
        for cy, cx in self.adjacent_cells(y, x):
            if (cy, cx) in self.rolls:
                adj_rolls.append((cy, cx))
        return adj_rolls

    def count_adjacent_rolls(self, y: int, x: int) -> int:
        return len(self.adjacent_rolls(y, x))

    def find_accessible(self) -> set[tuple[int, int]]:
        return set(
            (y, x) for (y, x) in self.rolls
            if self.count_adjacent_rolls(y, x) < 4
        )


def answer2(map: RollMap, **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(map: RollMap, **_: dict) -> int:

    map.accessible = map.find_accessible()
    logger.debug(map.render())

    # solve part 1

    return len(map.accessible)


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
    map = RollMap(lines, part=argus.part)
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
