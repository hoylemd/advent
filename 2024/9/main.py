from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input, i_to_b64_chr


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
        self.files: int = 0
        self.disk: list[int | None] = []

        self.raw_map = self.parse(raw_map)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse(self, raw_map: str) -> str:
        pointer = 0
        for i, (file, free) in enumerate(parse_blocks(raw_map)):

            self.disk += [i] * file

            if free is not None:
                self.disk += [None] * free

        self.files = i

        return raw_map

    def esrap(self) -> str:
        # TODO: reimplement
        return ''

    def print_blocks(self) -> str:
        return ''.join(f"{'.' if b is None else i_to_b64_chr(b)}" for b in self.disk)

    def compact(self):
        left = 0
        right = len(self.disk) - 1

        logger.debug(self.print_blocks())
        while left < right:
            logger.info(f"{left=}, {right=}, {len(self.disk)}")
            if self.disk[left] is not None:
                left += 1
                continue

            if self.disk[right] is None:
                right -= 1
                continue

            self.disk[left] = self.disk[right]
            self.disk[right] = None

            logger.debug(self.print_blocks())

    def checksum(self) -> int:
        return sum(i * file for i, file in enumerate(self.disk) if file is not None)


def answer2(disk_map: DiskMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def compact_and_checksum(disk_map: DiskMap) -> int:
    accumulator = 0

    # solve part 1
    disk_map.compact()
    logger.debug(disk_map.print_blocks())

    return disk_map.checksum()


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
            answer = compact_and_checksum(disk_map)
        case 2:
            answer = answer2(disk_map)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
