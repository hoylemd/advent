import os
from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input


class BatteryArray:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.banks = [line for line in self.parse_lines(lines)]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> list[int]:
        return [int(battery) for battery in line]

    def parse_lines(self, lines: Iterator[str]) -> Iterator:
        for y, line in enumerate(lines):
            yield self.parse_line(y, line)

    def esrap_line(self, y: int, bank: list[int]) -> str:
        return ''.join(f"{battery}" for battery in bank)

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, e) for y, e in enumerate(self.banks)
        )


def max_joltage(bank: list[int], num_batteries: int = 2) -> int:
    buffer = []
    joltage_map = [[] for _ in range(10)]
    width = len(bank)

    for index, battery in enumerate(bank):
        joltage_map[battery].append(index)

    max_i = width - num_batteries
    min_i = 0
    for b in range(num_batteries):
        for v in range(9, 0, -1):
            for i in joltage_map[v]:
                if i <= max_i and i >= min_i:
                    min_i = i + 1
                    buffer.append(v)
                    break
            if len(buffer) > b:
                break
        max_i += 1
        logger.debug(f"{b}: {buffer}")

    sequence = ''.join(f"{b}" for b in buffer)
    return int(sequence)


def answer2(battery_array: BatteryArray, **_: dict) -> int:
    accumulator = 0

    for bank in battery_array.banks:
        joltage = max_joltage(bank, 12)
        logger.info(f"In {battery_array.esrap_line(0, bank)}, {joltage=}")
        accumulator += joltage

    return accumulator

    # solve part 2

    return accumulator


def answer1(battery_array: BatteryArray, **_: dict) -> int:
    accumulator = 0

    for bank in battery_array.banks:
        joltage = max_joltage(bank)
        logger.info(f"In {battery_array.esrap_line(0, bank)}, {joltage=}")
        accumulator += joltage

    return accumulator


INPUT_PARAMS = {
    ('test.txt'): {
    },
    ('test2.txt'): {
    },
    ('input.txt'): {
    }
}


arg_parser = ArgumentParser('python -m 2025.3.main', description="Advent of Code 2025 Day 3")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    params = INPUT_PARAMS[os.path.basename(argus.input_path)]
    lines = parse_input(argus.input_path)
    battery_array = BatteryArray(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = battery_array.esrap_lines()
        case 1:
            answer = answer1(battery_array, **params)
        case 2:
            answer = answer2(battery_array, **params)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
