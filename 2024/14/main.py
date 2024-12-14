from argparse import ArgumentParser
from typing import Iterator
import os
import re

from utils import logger, parse_input, coordinates

LINE_REGEX = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')


class Robot:

    def __init__(self, id: int, pos: coordinates, vel: coordinates):
        self.id = id
        self.pos = pos
        self.vel = vel

    def __str__(self) -> str:
        return f"p={self.pos[1]},{self.pos[0]} v={self.vel[1]},{self.vel[0]}"


class RestroomRedoubt:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.robots = [bot for bot in self.parse_lines(lines)]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, line: str) -> tuple[coordinates, coordinates]:
        result = LINE_REGEX.match(line)

        if result is None:
            raise ValueError(f"robot could not be parsed from '{line}'")

        return ((int(result.group(2)), int(result.group(1))), (int(result.group(4)), int(result.group(3))))

    def parse_lines(self, lines: Iterator[str]) -> Iterator[Robot]:
        for y, line in enumerate(lines):
            pos, vel = self.parse_line(line)
            yield Robot(y, *self.parse_line(line))

    def esrap_line(self, y: int, robot: Robot) -> str:
        return f"{robot}"

    def esrap_lines(self) -> str:
        return '\n'.join(self.esrap_line(y, e) for y, e in enumerate(self.robots))


def sim_and_safe(robots: RestroomRedoubt, second: int, dimensions: coordinates) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.13.main', description="Advent of Code 2024 Day 13")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

PART_PARAMS = {
    ('test.txt', 1): {
        'seconds': 100,
        'dimensions': (7, 11)
    },
    ('input.txt', 1): {
        'seconds': 100,
        'dimensions': (103, 107)
    }
}

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    input_name = os.path.basename(argus.input_path)
    lines = parse_input(argus.input_path)
    robots = RestroomRedoubt(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = robots.esrap_lines()
        case _:
            answer = sim_and_safe(robots, **PART_PARAMS[input_name, argus.part])

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
