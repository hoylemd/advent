from argparse import ArgumentParser
from typing import Iterator
import itertools

from utils import logger, parse_input, i_to_b64_chr

type block = tuple[int, int, int | None] # offset, length, content


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
        self.blocks: list[block] = []
        self.files: int = 0

        self.raw_map = self.parse(raw_map)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse(self, raw_map: str) -> str:
        pointer = 0
        for i, (file, free) in enumerate(parse_blocks(raw_map)):

            self.blocks.append((pointer, file, i))
            pointer += file

            if free is not None:
                self.blocks.append((pointer, free, None))

        self.files = i

        return raw_map

    def esrap(self) -> str:
        return ''.join(
            f"{length}" for _, length, _ in self.blocks
        )

    def print_blocks(self) -> str:
        return ''.join(
            f"{(i_to_b64_chr(content) if content is not None else '.') * length}"
            for _, length, content in self.blocks
        )


    """
    def print_disk_state(self, from_index: int = 0, to_index: int | None = None, delimiter: str = '') -> str:
        return delimiter.join(
            f"{str(i % 10) * file}{'.' * free or 0}" for i, (file, free) in enumerate(zip(self.files, self.free)))
    """


def answer2(disk_map: DiskMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def frag_and_checksum(disk_map: DiskMap) -> int:
    accumulator = 0

    # solve part 1

    logger.info(disk_map.print_blocks())

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
            answer = frag_and_checksum(disk_map)
        case 2:
            answer = answer2(disk_map)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
