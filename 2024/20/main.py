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


def answer2(maze: Maze, **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def count_cheats(maze: Maze, min_save: int = 1) -> int:
    path, _ = maze.shortest_path(maze.start, maze.end)
    return len(path)


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
