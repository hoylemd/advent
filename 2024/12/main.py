from argparse import ArgumentParser
from typing import Iterator, Mapping
from collections import defaultdict

from utils import logger, parse_input, CharGrid, coordinates, INFINITY


class Region:

    def __init__(self, parent: 'GardenMap', id: int, first_y: int, first_x: int):
        self.parent = parent
        self.id = id
        self.crop = parent.get(first_y, first_x)
        self.y = first_y
        self.x = first_x
        self.height = 1
        self.width = 1
        self.points: set[coordinates] = set()
        self.edges: set[coordinates] = set()
        self.ext_corners: set[coordinates] = set()
        self.int_corners: set[coordinates] = set()
        self.adjacency = defaultdict(set)

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    def add_point(self, y: int, x: int):
        self.points.add((y, x))

        if y < self.y:
            self.height += self.y - y
            self.y = y

        if y > self.bottom:
            self.height += y - self.bottom

        if x < self.x:
            self.width += self.x - x

        if x > self.bottom:
            self.width += x - self.bottom

        self.parent.region_map[y][x] = self

    def __str__(self) -> str:
        return f"Region of {self.crop} from {self.y}, {self.x} to {self.y + self.height - 1}, {self.x + self.width - 1}"

    def __repr__(self) -> str:
        return f"{self}"

    def map_region(self):
        """starting at y,x, find all adjacent cells with the same crop, count permimeters"""
        checked: set[coordinates] = set()
        to_check: list[coordinates] = [(self.y, self.x)]

        while len(to_check):
            y, x = to_check.pop()
            if (y, x) in checked:
                continue

            next_cells = self.map_cell(y, x)
            logger.debug(f"Adding {y, x} to Region {self.id}({self.crop})")
            self.add_point(y, x)

            checked.add((y, x))
            to_check += next_cells

    def map_cell(self, y: int, x: int) -> list[coordinates]:
        """for a given cell get adjacent same-region cells & determine if this is an edge piece"""

        next_cells = []
        for ay, ax in self.parent.get_adjacent_coordinates(y, x):
            if self.parent.lines[ay][ax] != self.crop:
                continue

            if self.parent.region_map[ay][ax] is None:
                next_cells.append((ay, ax))

            self.adjacency[(y, x)].add((ay, ax))

        if len(next_cells) < 4:
            self.edges.add((y, x))

        return next_cells

    def count_perimeter(self) -> int:
        p = 0

        for edge in self.edges:
            p += 4 - len(self.adjacency[edge])

        return p

    def price(self) -> int:
        return len(self.points) * self.count_perimeter()

    def render_cell(self, y: int, x: int) -> str:
        assert self.crop is not None

        if self.parent.region_map[y][x] == self:
            return self.crop
        return '.'

    def render_line(self, y: int) -> str:
        return ''.join(self.render_cell(y, x) for x in range(self.x, self.right + 1))

    def render(self) -> str:
        return '\n'.join(self.render_line(y) for y in range(self.y, self.bottom + 1))


class GardenMap(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        super().__init__(lines)
        self.regions = []
        self.region_map: list[list[Region | None]] = [[None] * self.width for y in range(self.height)]

        self.map_regions()

    def map_regions(self):
        for y, line in enumerate(self.lines):
            for x, cell in enumerate(line):
                if self.region_map[y][x] is None:
                    new_region = Region(self, len(self.regions), y, x)
                    self.region_map[y][x] = new_region
                    self.regions.append(new_region)
                    new_region.map_region()


def answer2(garden: GardenMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def fence_prices(garden: GardenMap) -> int:
    accumulator = 0
    for region in garden.regions:
        accumulator += region.price()

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
            answer = fence_prices(garden)
        case 2:
            answer = answer2(garden)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
