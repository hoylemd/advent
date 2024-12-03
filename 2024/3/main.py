from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator
import re

MULT_PATTERN = r'mul\((\d{1,3}),(\d{1,3})\)'


def parse_line(line: str):
    return [(int(match[1]), int(match[2])) for match in re.finditer(MULT_PATTERN, line)]


class Memory:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.commands = parse_line(''.join(lines))

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def compute(self):
        return sum([command[0] * command[1] for command in self.commands])


def answer2(memory: Memory) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def compute_muls(memory: Memory) -> int:
    return memory.compute()


arg_parser = ArgumentParser('python -m 2024.3.main', description="Advent of Code 2024 Day 3")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    memory = Memory(lines)
    if argus.part == 1:
        answer = compute_muls(memory)
    else:
        answer = answer2(memory)

    logger.debug('')

    print(f"answer:\n{answer}")
