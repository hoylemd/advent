from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input

class ChronospatialComputer:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0
        self.i_ptr = 0

        self.program = self.parse_lines(lines)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_lines(self, lines: Iterator[str]) -> list[int]:
        for y, line in enumerate(lines):
            if line == '':
                continue
            content = line.split(': ')[1]
            match y:
                case 0:
                    self.reg_a = int(content)
                case 1:
                    self.reg_b = int(content)
                case 2:
                    self.reg_c = int(content)
                case 3:
                    pass
                case 4:
                    return [int(c) for c in content.split(',')]

        raise ValueError('Incomplete input?')

    def esrap_lines(self) -> str:
        return '\n'.join([
            f"Register A: {self.reg_a}",
            f"Register B: {self.reg_b}",
            f"Register C: {self.reg_c}",
            "",
            f"Program: {','.join(str(i) for i in self.program)}"
        ])

def answer2(computer: ChronospatialComputer) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(computer: ChronospatialComputer) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.17.main', description="Advent of Code 2024 Day 17")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    computer = ChronospatialComputer(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = computer.esrap_lines()
        case 1:
            answer = answer1(computer)
        case 2:
            answer = answer2(computer)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
