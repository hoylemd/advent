from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input, CharGrid, coordinates


class ReindeerMaze(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.start = (0, 0)
        self.end = (0, 0)

        super().__init__(lines)

    def parse_cell(self, y: int, x: int, c: str) -> str:
        if c == 'S':
            self.start = (y, x)

        if c == 'E':
            self.end = (y, x)

        return c


def answer2(maze: ReindeerMaze) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(maze: ReindeerMaze) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.16.main', description="Advent of Code 2024 Day 16")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    maze = ReindeerMaze(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = maze.esrap_lines()
        case 1:
            answer = answer1(maze)
        case 2:
            answer = answer2(maze)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
