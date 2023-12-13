from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator, Optional, Tuple, Any


def parse_line(line: str):
    return line.split()


class GalaxyMap:

    def __init__(self, lines: Iterator[str], expansion: int = 0):
        self.expansion = expansion
        self.galaxies = {}

        [self.parse_line(y, line) for y, line in enumerate(lines)]

        self.galaxy_list = [coords for coords in self.galaxies]

        self.static_rows, self.static_cols = [set(e) for e in zip(*self.galaxies.keys())]
        self.height = max(self.static_rows) + 1
        self.width = max(self.static_cols) + 1

        self.blank_rows = set(range(self.height)) - self.static_rows
        self.blank_cols = set(range(self.width)) - self.static_cols

        logger.info(f" blank rows: {self.blank_rows}, cols: {self.blank_cols}")

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def expanded_coordinates(self, y: int, x: int):
        downshift = self.expansion * len([r for r in self.blank_rows if r < y])
        rightshift = self.expansion * len([c for c in self.blank_cols if c < x])

        return (y + downshift, x + rightshift)

    def get_at_coords(self, y: int, x: int) -> str:
        return str(self.galaxies.get((y, x), '.'))

    def parse_line(self, y: int, line: str):
        for x, cell in enumerate(line):
            if cell == '#':
                coords = (y, x)
                self.galaxies[coords] = len(self.galaxies)

    def render_grid(self, expansion: Optional[int] = None):
        rows = []
        for y in range(self.height):
            rows.append(''.join(self.get_at_coords(y, x) for x in range(self.width)))
        return '\n'.join(rows)


def answer2(map: GalaxyMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def taxicab_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def gen_pairs(elements: Iterator[Any]) -> Iterator[Tuple[Any, Any]]:
    for i, element in enumerate(elements):
        for other in elements[i + 1:]:
            yield (element, other)


def sum_galaxy_separations(map: GalaxyMap) -> int:
    accumulator = 0

    for first, second in gen_pairs(map.galaxy_list):
        x1 = map.expanded_coordinates(*first)
        x2 = map.expanded_coordinates(*second)
        dist = taxicab_distance(x1, x2)
        logger.info(f"distance between {map.galaxies[first]}:{x1} and {map.galaxies[second]}:{x2} = {dist}")
        accumulator += dist

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2023.11.main', description="Advent of Code 2023 Day 11")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    map = GalaxyMap(lines, 1)
    logger.info(map.render_grid())
    if argus.part == 1:
        answer = sum_galaxy_separations(map)
    else:
        answer = answer2(map)

    logger.debug('')

    print(f"answer:\n{answer}")
