from argparse import ArgumentParser
from typing import Iterator
import re

from utils import logger, parse_input, coordinates

A_PATT = re.compile(r'Button A: X\+(\d+), Y\+(\d+)')
B_PATT = re.compile(r'Button B: X\+(\d+), Y\+(\d+)')
P_PATT = re.compile(r'Prize: X=(\d+), Y=(\d+)')

class ClawMachine:

    def __init__(self, lines: list[str], part: int = 1):
        self.part = part

        self.a, self.b, self.p = self.parse_lines(lines)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_lines(self, lines: list[str]) -> tuple[coordinates, coordinates, coordinates]:
        a_mat = A_PATT.match(lines[0])
        b_mat = B_PATT.match(lines[1])
        p_mat = P_PATT.match(lines[2])

        if a_mat is None or b_mat is None or p_mat is None:
            raise ValueError("Parsing error")

        return (int(a_mat[1]), int(a_mat[2])), (int(b_mat[1]), int(b_mat[2])), (int(p_mat[1]), int(p_mat[2]))


    def esrap_line(self, y: int, element: str) -> str:
        return f"{element}"

    def esrap_lines(self) -> str:
        return '\n'.join([
            f"Button A: X+{self.a[0]}, Y+{self.a[1]}",
            f"Button B: X+{self.b[0]}, Y+{self.b[1]}",
            f"Prize: X={self.a[0]}, Y={self.a[1]}",
        ])

    def calc_presses(self) -> tuple[int, int]:
        """cramer's rule yes of course i understand linear algebra and didnt cheat"""
        determinant = (self.a[1] * self.b[0] - self.a[0] * self.b[1])
        a_presses = (self.p[1] * self.b[0] - self.p[0] * self.b[1]) // determinant
        b_presses = (self.p[0] * self.a[1] - self.a[0]*self.p[1]) // determinant

        return (a_presses, b_presses)

def parse_machines(lines: list[str], part: int=1) -> Iterator[ClawMachine]:
    for i in range((len(lines) // 4) + 1):
        yield ClawMachine(lines[i*4:(i+1)*4])


def answer2(machines: Iterator[ClawMachine]) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def sum_cost(machines: Iterator[ClawMachine]) -> int:
    accumulator = 0

    for machine in machines:
        a_presses, b_presses = machine.calc_presses()
        logger.info(f"pressing A {a_presses} times and B {b_presses} times")
        test = (a_presses * machine.a[0] + b_presses * machine.b[0], a_presses * machine.a[1] + b_presses * machine.b[1])
        if test == machine.p:
            logger.info('  PRIZE GET')
            accumulator += a_presses*3 + b_presses
        else:
            logger.info('  RIGGED')

    return accumulator


arg_parser = ArgumentParser('python -m 2024.13.main', description="Advent of Code 2024 Day 13")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = list(parse_input(argus.input_path))
    machines = parse_machines(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = '\n\n'.join(machine.esrap_lines() for machine in machines)
        case 1:
            answer = sum_cost(machines)
        case 2:
            answer = answer2(machines)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
