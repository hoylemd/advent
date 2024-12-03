from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator
import re

MULT_PATTERN = r'(mul)\((\d{1,3}),(\d{1,3})\)'
DO_PATTERN = r'(do)\(\)'
DONT_PATTERN = r"(don\'t)\(\)"

KEYWORD_PATTERN = fr'({MULT_PATTERN}|{DO_PATTERN}|{DONT_PATTERN})'


def parse_mult(command: re.Match) -> tuple[int, int]:
    return (int(command[2]), int(command[3]))


def parse_command(command: re.Match) -> tuple:
    match command[0][:3]:
        case 'mul':
            return 'MUL', int(command[3]), int(command[4])
        case 'do(':
            return 'ON',
        case 'don':
            return 'OFF',

    raise ValueError(f"Unrecognized command: {command[0]}")


class Memory:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.commands = []
        patt = re.compile(KEYWORD_PATTERN)

        source = ''.join(lines)

        for command in patt.finditer(source):
            self.commands.append(parse_command(command))

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def compute(self):
        accumulator = 0
        condition = True
        for command in self.commands:
            match command[0]:
                case 'MUL':
                    if condition:
                        accumulator += command[1] * command[2]
                case 'ON':
                    condition = True
                case 'OFF':
                    if self.part > 1:
                        condition = False

        return accumulator


arg_parser = ArgumentParser('python -m 2024.3.main', description="Advent of Code 2024 Day 3")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    memory = Memory(lines, part=argus.part)
    answer = memory.compute()

    logger.debug('')

    print(f"answer:\n{answer}")
