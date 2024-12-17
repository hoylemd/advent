from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input

class ChronospatialComputer:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.registers = [0, 0, 0] # A, B, C
        self.i_ptr = 0

        self.program = self.parse_lines(lines)

    @property
    def reg_a(self):
        return self.registers[0]

    @reg_a.setter
    def reg_a(self, value):
        self.registers[0] = value

    @property
    def reg_b(self):
        return self.registers[1]

    @reg_b.setter
    def reg_b(self, value):
        self.registers[1] = value

    @property
    def reg_c(self):
        return self.registers[2]

    @reg_c.setter
    def reg_c(self, value):
        self.registers[2] = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_lines(self, lines: Iterator[str]) -> list[int]:
        for y, line in enumerate(lines):
            if line == '':
                continue
            content = line.split(': ')[1]
            if y < 3:
                self.registers[y] = int(content)
            if y == 4:
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

    def adv(self, operand: int):
        """opcode 0, division"""

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
