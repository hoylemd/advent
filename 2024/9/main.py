from argparse import ArgumentParser
from typing import Iterator
import itertools

from utils import logger, parse_input


def parse_blocks(raw_map: str) -> Iterator[tuple[int, int | None]]:  # file blocks, free blocks
    normed_map = raw_map
    if len(normed_map) % 2:
        normed_map += 'X'

    for i in range(0, len(normed_map), 2):
        file, free = normed_map[i:i + 2]
        yield int(file), int(free) if free != 'X' else None


class DiskMap:

    def __init__(self, raw_map: str, part: int = 1):
        self.part = part
        self.files = []
        self.free = []

        self.raw_map = self.parse(raw_map)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse(self, raw_map: str) -> str:
        for file, free in parse_blocks(raw_map):
            self.files.append(file)
            if free is not None:
                self.free.append(free)

        return raw_map

    def esrap(self) -> str:
        return ''.join(
            f"{file}{free if free is not None else ''}" for file, free in itertools.zip_longest(self.files, self.free))


def answer2(disk_map: DiskMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(disk_map: DiskMap) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.9.main', description="Advent of Code 2024 Day 9")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    raw_map = list(parse_input(argus.input_path))[0]
    disk_map = DiskMap(raw_map, part=argus.part)
    match argus.part:
        case -1:
            answer = disk_map.esrap()
        case 1:
            answer = answer1(disk_map)
        case 2:
            answer = answer2(disk_map)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
