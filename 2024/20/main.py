import os
from argparse import ArgumentParser
from typing import Iterator
from collections import defaultdict

from utils import logger, parse_input, CharGrid, coordinates


type path = list[coordinates]
type cheat = tuple[coordinates, coordinates]


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

    def get_path(self) -> path:
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

    def print_cheat(self, path: path, cheat: cheat) -> str:
        annotations = {c: str(i) for i, c in enumerate(cheat)}
        skip_start = path.index(cheat[0])
        skip_end = path.index(cheat[1])

        for skipped_step in path[skip_start + 1: skip_end]:
            annotations[skipped_step] = 'X'

        return self.print_grid(annotations=annotations)


def taxicab(a: coordinates, b: coordinates) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def possible_cheats(maze: Maze, path: path, max_cheat: int = 2) -> Iterator[tuple[cheat, int]]:
    """Find every pair of points a, b in path such that:

    - index(b) - index(a) > 1 (they aren't already adjacent)
    - taxicab_distance(b, a) == 2 (they're only 2 tiles apart)
    - the tile between them is a wall
    """
    for i, (y, x) in enumerate(path):
        for j, (ny, nx) in enumerate(path[i:]):
            cheat_dist = taxicab((y, x), (ny, nx))
            if cheat_dist <= max_cheat and cheat_dist < j:
                # logger.info(f"possible cheat between {y, x} and {ny, nx}")
                savings = j - cheat_dist
                # logger.info(f"adding cheat: {y, x}, -> {ny, nx}: ({savings})")
                yield (((y, x), (ny, nx)), (savings))


def count_cheats(maze: Maze, min_save: int = 1, cheat_time: int = 2) -> int:
    original_path = maze.get_path() + [maze.end]

    # return len(original_path)
    good_cheats = {}
    cheats_by_saves = defaultdict(list)

    for cheat, savings in possible_cheats(maze, original_path, cheat_time):
        if savings > min_save:
            # logger.info(maze.print_cheat(original_path, cheat))
            # logger.info(f"cheat {cheat} saves {savings} picoseconds")
            cheats_by_saves[savings].append(cheat)
            good_cheats[cheat] = savings

    for save, cheats in sorted(cheats_by_saves.items(), key=lambda x: x[0]):
        logger.info(f"There are {len(cheats)} cheats thate save {save} picoseconds")

    return len(good_cheats)


INPUT_PARAMS = {
    ('test.txt', 1): {},
    ('input.txt', 1): {
        'min_save': 99
    },
    ('test.txt', 2): {
        'min_save': 49,
        'cheat_time': 20,
    },
    ('input.txt', 2): {
        'min_save': 99,
        'cheat_time': 20
    }
}

arg_parser = ArgumentParser('python -m 2024.20.main', description="Advent of Code 2024 Day 20")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    maze = Maze(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = maze.esrap_lines()
        case _:
            params = INPUT_PARAMS[os.path.basename(argus.input_path), argus.part]
            answer = count_cheats(maze, **params)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
