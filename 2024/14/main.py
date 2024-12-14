from argparse import ArgumentParser
from typing import Iterator
import os
import re

from utils import logger, parse_input, coordinates, i_to_b64_chr

LINE_REGEX = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')


class Robot:

    def __init__(self, id: int, pos: coordinates, vel: coordinates):
        self.id = id
        self.pos = pos
        self.vel = vel

    def __str__(self) -> str:
        return f"p={self.pos[1]},{self.pos[0]} v={self.vel[1]},{self.vel[0]}"


class RestroomRedoubt:

    def __init__(self, lines: Iterator[str], dimensions: coordinates, part: int = 1):
        self.part = part
        self.dimensions = dimensions

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

    def predict_pos(self, robot: Robot, seconds: int, component: int) -> int:
        return (robot.pos[component] + (robot.vel[component] * seconds)) % self.dimensions[component]

    def simulate(self, seconds: int) -> Iterator[coordinates]:
        """return list of coordinates containing robots"""

        for i, robot in enumerate(self.robots):
            predicted_pos = (self.predict_pos(robot, seconds, 0), self.predict_pos(robot, seconds, 1))
            yield predicted_pos

    def is_in_quadrant(self, quadrant: coordinates, pos: coordinates) -> bool:
        halves = (self.dimensions[0] // 2, self.dimensions[1] // 2)

        offset = (-1 * quadrant[0] * (halves[0] + 1), -1 * quadrant[1] * (halves[1] + 1))

        check = (pos[0] + offset[0], pos[1] + offset[1])

        if check[0] >= 0 and check[0] < halves[0] and check[1] >= 0 and check[1] < halves[1]:
            logger.debug(f"{pos=} is in {quadrant}")
            return True

        return False

    def print_cell_ids(self, y: int, x: int, positions: list[coordinates]) -> str:
        try:
            index = positions.index((y, x))
            return i_to_b64_chr(index)

        except ValueError:  # position not in list
            return '.'

    def print_bots_in_cell(self,
                           y: int,
                           x: int,
                           positions: list[coordinates],
                           quadrant: coordinates | None = None) -> str:
        if quadrant is None or self.is_in_quadrant(quadrant, (y, x)):
            return f"{positions.count((y, x)) or '.'}"
        else:
            return ''

    def print_line(self, y: int, positions: list[coordinates], quadrant: coordinates | None = None) -> str:
        return ''.join(self.print_bots_in_cell(y, x, positions, quadrant=quadrant) for x in range(self.dimensions[1]))

    def print_grid(self, new_positions: list[coordinates] | None = None, quadrant: coordinates | None = None) -> str:
        positions = new_positions or list(bot.pos for bot in self.robots)

        lines = list(self.print_line(y, positions, quadrant=quadrant) for y in range(self.dimensions[0]))

        return '\n'.join(line for line in lines if line)


QUADRANTS = [(0, 0), (0, 1), (1, 0), (1, 1)]


def sim_and_safe(robots: RestroomRedoubt, seconds: int) -> int:
    accumulator = 1

    logger.info("Before:")
    logger.info(robots.print_grid())

    new_positions = list(robots.simulate(seconds))

    logger.info("After:")
    logger.info(robots.print_grid(new_positions))

    for quad in QUADRANTS:
        in_quadrant = [robot for robot in new_positions if robots.is_in_quadrant(quad, robot)]
        quad_factor = len(in_quadrant)
        logger.info(f"for quad {quad}, factor is {quad_factor}")
        # logger.info(robots.print_grid(in_quadrant, quad))
        # logger.info("all_robots?")
        # logger.info(robots.print_grid(quadrant=quad))
        accumulator *= quad_factor

    # solve part 1

    return accumulator


def find_easter_egg(robots: RestroomRedoubt) -> int:
    # loop through until all bots are on their own square
    i = 0
    n_bots = len(robots.robots)
    while True:
        new_positions = list(robots.simulate(i))

        if len(set(new_positions)) == n_bots:
            grid_vis = robots.print_grid(new_positions)
            logger.info(grid_vis)
            if '1111111111111111111111111111111' in grid_vis:
                break

        if i % 100 == 0:
            logger.info(f"{i} iterations...")

        i += 1

    return i


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
        'dimensions': (103, 101)
    },
    ('input.txt', 2): {
        'seconds': 0,
        'dimensions': (103, 101)
    },
}

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    input_name = os.path.basename(argus.input_path)
    lines = parse_input(argus.input_path)
    params = PART_PARAMS[input_name, argus.part]
    robots = RestroomRedoubt(lines, params['dimensions'], part=argus.part)
    match argus.part:
        case -1:
            answer = robots.esrap_lines()
        case 1:
            answer = sim_and_safe(robots, params['seconds'])
        case 2:
            answer = find_easter_egg(robots)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
