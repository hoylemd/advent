from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


class Report:

    def __init__(self, levels: list):
        self.levels = levels
        self.direction = None

    def is_safe(self) -> bool:
        prev = self.levels[0]

        for level in self.levels[1:]:
            delta = level - prev
            if self.direction is None:
                self.direction = 1 if delta > 0 else -1

            normalized_delta = delta * self.direction
            if normalized_delta < 1 or normalized_delta > 3:
                return False

            prev = level

        return True


def parse_line(line: str):
    return Report([int(l) for l in line.split()])


class Reports:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.reports = (parse_line(line) for line in lines)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"


def solve_part_2(reports: Reports) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def solve_part_1(reports: Reports) -> int:
    return sum(1 for report in reports.reports if report.is_safe())


arg_parser = ArgumentParser('python -m {{year}}.{{day}}.main', description="Advent of Code {{ year }} Day {{ day }}")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    reports = Reports(lines)
    if argus.part == 1:
        answer = solve_part_1(reports)
    else:
        answer = solve_part_2(reports)

    logger.debug('')

    print(f"answer:\n{answer}")
