from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator, Mapping


class LinenLayout:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.towels, self.designs = self.parse_lines(lines)

        self.sorted_towels = sorted(self.towels, key = lambda t: -1* len(t))
        self.towels_by_width = {}
        self.towels_by_width = self.towel_width_map()
        self.impossible_patterns = []

    def towel_width_map(self) -> Mapping[int, list[str]]:
        last_width = None
        reversed_towels = list(reversed(self.sorted_towels))
        width_map = {}
        for i, towel in enumerate(reversed_towels):
            if last_width is None:
                last_width = len(towel)

            if len(towel) > last_width:
                width_map[last_width] = list(reversed(reversed_towels[:i]))
                last_width = len(towel)

        return width_map


    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> str:
        return line

    def parse_lines(self, lines: Iterator[str]) -> tuple[list[str],list[str]]:
        towels = []
        designs = []
        for y, line in enumerate(lines):
            if y == 0:
                towels = line.split(', ')
                continue
            if not line:
                continue
            designs.append(line)

        return towels, designs


    def esrap_lines(self) -> str:
        return '\n'.join([
            ', '.join(self.towels),
            ''
        ] + self.designs)

    def validate_design(self, design: str) -> bool:
        pass

    def slow_validate_design(self, design: str) -> bool:
        if len(design) == 0:
            return True

        #logger.info(f"Validating design {design}")
        for towel in self.towels:
            if design.startswith(towel):
                #logger.info(f"Can start with {towel}")
                if self.validate_design(design[len(towel):]):
                    #logger.info(f"{design} is valid!")
                    return True

        #logger.info(f"{design} is impossible")
        return False


def answer2(towels: LinenLayout) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def count_valid_designs(towels: LinenLayout) -> int:
    accumulator = 0
    for i, design in enumerate(towels.designs):
        logger.info(f"Validating {design} {i}/{len(towels.designs)}")
        if towels.validate_design(design):
            logger.info("  valid")
            accumulator += 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.19.main', description="Advent of Code 2024 Day 19")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    towels = LinenLayout(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = towels.esrap_lines()
        case 1:
            answer = count_valid_designs(towels)
        case 2:
            answer = answer2(towels)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
