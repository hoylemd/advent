import os
from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input, CharGrid, coordinates


class Maze(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.start: coordinates = (-1, -1)
        self.end: coordinates = (-1, -1)

        super().__init__(lines)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_cell(self, y: int, x: int, c: str) -> str:
        if c == 'S':
            self.start = (y, x)

        if c == 'E':
            self.end = (y, x)

        return super().parse_cell(y, x, c)


type cheat = tuple[coordinates, coordinates]


def possible_cheats(maze: Maze, path: list[coordinates]) -> list[cheat]:
    """Find every pair of points a, b in path such that:

    - index(b) - index(a) > 1 (they aren't already adjacent)
    - taxicab_distance(b, a) == 2 (they're only 2 tiles apart)
    - the tile between them is a wall
    """
    pass


def cheat_savings(original_path: list[coordinates], the_cheat: cheat) -> int:
    """Count the # of tiles between the points in the cheat, add 1 (to accommodate for the hacked wall)"""
    pass


def answer2(maze: Maze, **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def count_cheats(maze: Maze, min_save: int = 1) -> int:
    original_path, branches = maze.shortest_path(maze.start, maze.end)

    good_cheats = {}

    for c in possible_cheats(maze, original_path):
        savings = cheat_savings(original_path, c)

        if savings > min_save:
            good_cheats[c] = savings

    return len(good_cheats)


INPUT_PARAMS = {
    ('test.txt'): {},
    ('input.txt'): {
        'min_save': 99
    }
}

arg_parser = ArgumentParser('python -m 2024.20.main', description="Advent of Code 2024 Day 20")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    params = INPUT_PARAMS[os.path.basename(argus.input_path)]
    lines = parse_input(argus.input_path)
    maze = Maze(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = maze.esrap_lines()
        case 1:
            answer = count_cheats(maze, **params)
        case 2:
            answer = answer2(maze, **params)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
