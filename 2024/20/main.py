import os
from argparse import ArgumentParser
from typing import Iterator
from collections import defaultdict

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

    def get_path(self) -> list[coordinates]:
        assert self.start != (-1, -1)
        assert self.end != (-1, -1)

        prev = (-1, -1)

        def is_not_prev_and_is_open(y: int, x: int) -> bool:
            return not ((y, x) == prev or self.lines[y][x] == '#')

        path = []
        y, x = self.start

        while (y, x) != self.end:
            path.append((y, x))

            adj = list(self.get_adjacent_coordinates(y, x, test=is_not_prev_and_is_open))
            assert len(adj) == 1  # should only be one next step option

            prev = (y, x)
            y, x = adj[0]

        return path


type cheat = tuple[coordinates, coordinates]


def taxicab(a: coordinates, b: coordinates) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def possible_cheats(maze: Maze, path: list[coordinates]) -> Iterator[tuple[cheat, int]]:
    """Find every pair of points a, b in path such that:

    - index(b) - index(a) > 1 (they aren't already adjacent)
    - taxicab_distance(b, a) == 2 (they're only 2 tiles apart)
    - the tile between them is a wall
    """
    for i, (y, x) in enumerate(path):
        for j, (ny, nx) in enumerate(path[i:]):
            if taxicab((y, x), (ny, nx)) == 2:
                logger.info(f"possible cheat between {y, x} and {ny, nx}")
                mid_y = y + ((ny - y) // 2)
                mid_x = x + ((nx - x) // 2)
                if maze.lines[mid_y][mid_x] == '#':
                    logger.info(f"adding cheat: {mid_y, mid_x}, {ny, nx}: ({j + 2})")
                    yield (((mid_y, mid_x), (ny, nx)), (j + 2))


def answer2(maze: Maze, **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def count_cheats(maze: Maze, min_save: int = 1) -> int:
    original_path = maze.get_path()

    # return len(original_path)
    good_cheats = {}
    cheats_by_saves = defaultdict(list)

    for cheat, savings in possible_cheats(maze, original_path):
        if savings > min_save:
            cheats_by_saves[savings].append(cheat)
            good_cheats[cheat] = savings

    for save, cheats in cheats_by_saves.items():
        logger.info(f"There are {len(cheats)} cheats thate save {save} picoseconds")

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
