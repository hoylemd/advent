import os
from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input


def devector(number: int) -> tuple[int, int]:
    return abs(number), -1 if number < 0 else 1


class Dial:
    position: int

    def __init__(
        self,
        lines: Iterator[str],
        start_position: int = 50,
        max_num: int = 100,
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
        dir, mag_s = line[0], line[1:]

        self.cmd_width = max(self.cmd_width, len(mag_s))

        mag = int(mag_s)

        return -1 * mag if dir == 'L' else mag

    def parse_lines(self, lines: Iterator[str]) -> Iterator:
        self.cmd_width = 0
        for y, line in enumerate(lines):
            yield self.parse_line(y, line)

        self.cmd_width += 1

    def esrap_line(self, y: int, command: int) -> str:
        if command < 0:
            return f"L{command * -1}"
        else:
            return f"R{command}"

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, e) for y, e in enumerate(self.commands)
        )

    def pad_cmd(self, command: int) -> str:
        return f"{self.esrap_line(0, command)}".ljust(self.cmd_width)

    def next_pos(self, command: int) -> int:
        return (self.position + command) % (self.max)

    def reset(self):
        self.position = self.start_position

    def out_of_bounds(self, number: int) -> bool:
        return number < 0 or number > self.max

    def how_many_zero_clicks(self, command) -> int:
        mag, dir = devector(command)

        full_circles = mag // self.max
        remaining = command - (full_circles * self.max * dir)
        dest = self.position + remaining

        zero_clicks = full_circles + (1 if (self.position != 0 and self.out_of_bounds(dest)) else 0)
        zero_clicks += 1 if (dest) % self.max == 0 else 0

        return zero_clicks

    def count_zeros(self, count_clicks: bool = False, max_steps: int = 0) -> int:
        zeroes = 0

        logger.info(f"The dial starts by pointing at {self.position}")
        for idx, command in enumerate(self.commands):
            if max_steps and idx > max_steps:
                break

            prev_token = f"{self.position}".ljust(2)
            clicks_suffix = "."
            next_pos = self.next_pos(command)
            new_clicks = 0
            if (count_clicks):
                new_clicks += self.how_many_zero_clicks(command)
            else:
                if next_pos == 0:
                    new_clicks += 1

            self.position = next_pos
            zeroes += new_clicks

            position_token = f"{self.position}".ljust(2)
            if self.position == 0:
                position_token = "0*"

            command_token = f"{command}".ljust(self.cmd_width)
            clicks_suffix = f", ({new_clicks} new clicks = {zeroes})" if new_clicks else ""
            logger.info(
                f"{prev_token} + {command_token} -> {position_token}{clicks_suffix}"
            )

        return zeroes


def answer2(dial: Dial, **_: dict) -> int:
    return dial.count_zeros(True)


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

    params = INPUT_PARAMS.get(os.path.basename(argus.input_path), {})
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
