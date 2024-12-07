from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input


def parse_line(line: str) -> tuple[int, list[int]]:
    test_value, operands_s = line.split(': ')
    operands = [int(o) for o in operands_s.split(' ')]
    return int(test_value), operands


def esrap_line(test_value: int, operands: list[int]) -> str:
    return f"{test_value}: {' '.join(str(o) for o in operands)}"


class Calibrator:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.equations = [parse_line(line) for line in lines]

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def esrap(self) -> str:
        return '\n'.join(esrap_line(*e) for e in self.equations)


def answer2(calibrator: Calibrator) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def sum_valid(calibrator: Calibrator) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.7.main', description="Advent of Code 2024 Day 7")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    calibrator = Calibrator(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = calibrator.esrap()
        case 1:
            answer = sum_valid(calibrator)
        case 2:
            answer = answer2(calibrator)

    logger.debug('')

    print(answer)
