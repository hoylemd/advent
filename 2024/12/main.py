from argparse import ArgumentParser
from typing import Iterator, Mapping
from collections import defaultdict

from utils import logger, parse_input, CharGrid, coordinates, INFINITY, DIAGONAL_DIRECTIONS


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
        self.adjacency: defaultdict[coordinates, set[coordinates]] = defaultdict(set)

    @property
    def right(self):
        return self.x + (self.width - 1)

    @property
    def bottom(self):
        return self.y + (self.height - 1)

    def add_point(self, y: int, x: int):
        self.points.add((y, x))

        if y < self.y:
            self.height += self.y - y
            self.y = y

        if y > self.bottom:
            self.height = y - self.y

        if x < self.x:
            self.width += self.x - x
            self.x = x

        if x > self.right:
            self.width = x - self.x

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

    def count_internal_corners(self, y: int, x: int) -> int:
        corners = 0

        for dy, dx in self.parent.get_diagonal_coordinates(y, x):
            if self.parent.region_map[dy][dx] is self:
                continue

            if (self.parent.region_map[y][dx] is self and self.parent.region_map[dy][x] is self):
                corners += 1

        return corners

    def check_corners(self, y: int, x: int) -> int:
        external = 0
        adj = list(self.adjacency[y, x])

        if len(adj) == 0:
            return 4
        elif len(adj) == 1:
            return 2
        elif len(adj) == 2:
            # if opposing corners, no corner
            dy1, dx1 = y - adj[0][0], x - adj[0][1]
            dy2, dx2 = y - adj[1][0], x - adj[1][1]

            dy, dx = dy1 + dy2, dx1 + dx2

            # straight segment: 0, corner: 1
            external = 0 if (dy, dx) == (0, 0) else 1

        return self.count_internal_corners(y, x) + external

    def count_corners(self) -> int:
        corners = 0
        for y, x in self.points:
            yx_corners = self.check_corners(y, x)
            if yx_corners:
                logger.info(f"{y, x} has {yx_corners} corners")
            corners += yx_corners

        return corners

    def price(self) -> int:
        return len(self.points) * (self.count_perimeter() if self.parent.part == 1 else self.count_corners())

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


def fence_prices(garden: GardenMap) -> int:
    accumulator = 0
    for region in garden.regions:
        logger.info(region)
        logger.info(region.render())
        price = region.price()
        logger.info(f"price: {price}")

        accumulator += price
        logger.info('')

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
        case _:
            answer = fence_prices(garden)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
