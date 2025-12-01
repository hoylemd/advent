import os
from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input


class Dial:
    position: int

    def __init__(
        self,
        lines: Iterator[str],
        start_position: int = 50,
        max_num: int = 99,
        part: int = 1
    ):
        self.part = part
        self.start_position = start_position
        self.max = max_num

        self.commands = [line for line in self.parse_lines(lines)]

        self.reset()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> int:
        dir, mag = line[0], int(line[1:])

        return -1 * mag if dir == 'L' else mag

    def parse_lines(self, lines: Iterator[str]) -> Iterator:
        for y, line in enumerate(lines):
            yield self.parse_line(y, line)

    def esrap_line(self, y: int, command: int) -> str:
        if command < 0:
            return f"L{command * -1}"
        else:
            return f"R{command}"

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, e) for y, e in enumerate(self.commands)
        )

    def next_pos(self, command: int) -> int:
        return (self.position + command) % (self.max + 1)

    def reset(self):
        self.position = self.start_position

    def count_zeros(self):
        zeroes = 0

        logger.info(f"The dial starts by pointing at {self.position}")
        for command in self.commands:
            self.position = self.next_pos(command)

            if self.position == 0:
                zeroes += 1
                position_token = f"**{dial.position}**"
            else:
                position_token = f"{dial.position}"

            logger.info(f"The dial is rotated {dial.esrap_line(0, command)} to point at {position_token}")

        return zeroes


def answer2(dial: Dial, **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(dial: Dial, **_: dict) -> int:
    return dial.count_zeros()


INPUT_PARAMS = {
    ('test.txt'): {
    },
    ('input.txt'): {
    }
}


arg_parser = ArgumentParser('python -m 2025.1.main', description="Advent of Code 2025 Day 1")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    params = INPUT_PARAMS[os.path.basename(argus.input_path)]
    lines = parse_input(argus.input_path)
    dial = Dial(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = dial.esrap_lines()
        case 1:
            answer = answer1(dial, **params)
        case 2:
            answer = answer2(dial, **params)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
