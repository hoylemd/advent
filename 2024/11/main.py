from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


def parse_line(line: str) -> Iterator[int]:
    for num in line.split():
        yield int(num)


class StoneArray:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.stones = list(self.parse_lines(lines))
        self.memory: dict[tuple[int, int], int] = {}

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_lines(self, lines: Iterator[str]) -> Iterator[int]:
        for line in lines:
            for num in parse_line(line):
                yield num

    def esrap_lines(self) -> str:
        return ' '.join(f"{stone}" for stone in self.stones)

    def blink(self, stone: int) -> list[int]:
        if stone == 0:
            return [1]
        elif len(stone_str := f"{stone}") % 2 == 0:
            l, r = stone_str[:len(stone_str) // 2], stone_str[len(stone_str) // 2:]
            return [int(l), int(r)]

        return [stone * 2024]

    def blink_all(self) -> list[int]:
        new_stones = []
        for stone in self.stones:
            new_stones += self.blink(stone)

        return new_stones

    def count_stones(self, stone: int, n: int) -> int:
        if n < 1:
            return 1

        if count := self.memory.get((stone, n)):
            return count

        next_stones = self.blink(stone)

        count = sum(self.count_stones(next_stone, n-1) for next_stone in next_stones)

        self.memory[stone, n] = count

        return count


def blink_quietly(stone_array: StoneArray, blinks: int) -> int:
    accumulator = 0

    for stone in stone_array.stones:
        accumulator += stone_array.count_stones(stone, blinks)

    return accumulator


def blink_verbosely(stone_array: StoneArray, blinks: int) -> int:
    logger.info(f"Initial arrangement:")
    logger.info(stone_array.esrap_lines() + '\n')

    for i in range(blinks):
        stone_array.stones = stone_array.blink_all()
        logger.info(f"After {i + 1} blinks")
        logger.info(stone_array.esrap_lines() + '\n')

    return len(stone_array.stones)


arg_parser = ArgumentParser('python -m 2024.11.main', description="Advent of Code 2024 Day 11")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    stone_array = StoneArray(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = stone_array.esrap_lines()
        case -2:
            answer = blink_verbosely(stone_array, 6)
        case 1:
            answer = blink_quietly(stone_array, 25)
        case 2:
            answer = blink_quietly(stone_array, 75)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
