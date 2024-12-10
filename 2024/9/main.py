from argparse import ArgumentParser
from typing import Iterator, Mapping

from collections import defaultdict

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
        self.files: list[tuple[int, int]] = []
        self.gaps: list[tuple[int, int]] = []
        self.disk: list[int | None] = []

        self.gaps_by_size = defaultdict(list)

        self.raw_map = self.parse(raw_map)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse(self, raw_map: str) -> str:
        pointer = 0
        for i, (file, free) in enumerate(parse_blocks(raw_map)):

            self.files.append((len(self.disk), file))
            self.disk += [i] * file

            if free is not None:
                self.gaps.append((len(self.disk), free))
                self.gaps_by_size[free] = self.gaps_by_size[free] + [len(self.gaps) - 1]
                self.disk += [None] * free

        return raw_map

    def esrap(self) -> str:
        # TODO: reimplement
        return ''

    def print_blocks(self) -> str:
        return ''.join(f"{'.' if b is None else i_to_b64_chr(b % 64)}" for b in self.disk)

    def compact(self):
        left = 0
        right = len(self.disk) - 1

        logger.debug(self.print_blocks())
        while left < right:
            #logger.info(f"{left=}, {right=}, {len(self.disk)}")
            if self.disk[left] is not None:
                left += 1
                continue

            if self.disk[right] is None:
                right -= 1
                continue

            self.disk[left] = self.disk[right]
            self.disk[right] = None

            #logger.debug(self.print_blocks())

    def find_gap(self, size: int, max_offset: int) -> int | None:
        for i, (gap_offset, gap_size) in enumerate(self.gaps):
            if gap_offset >= max_offset:
                break
            if gap_size < size:
                continue
            return i

        return None

    def move_file_into_gap(self, file_id: int, gap_index: int):
        file_offset, file_size = self.files[file_id]
        gap_offset, gap_size = self.gaps[gap_index]


        if file_size > gap_size:
            raise ValueError(f"Gap {gap_index}({gap_size}) is too small for file {file_id} ({file_size})")

        # logger.debug(f"Moving file {file_id}:{i_to_b64_chr(file_id % 64) * file_size} from {file_offset} to {gap_offset}")
        # move blocks on disk
        for i in range(file_size):
            self.disk[gap_offset + i] = file_id
            self.disk[file_offset + i] = None

        # update file index
        self.files[file_id] = (gap_offset, file_size)

        # update gap index
        self.gaps[gap_index] = (gap_offset + file_size, gap_size - file_size)

    def compact_with_defrag(self):
        for i in range(len(self.files) -1, -1, -1):
            file_offset, file_size = self.files[i]
            # logger.info(f"file {i}: at {file_offset}, {file_size} blocks")

            leftmost_gap = self.find_gap(file_size, file_offset)

            if leftmost_gap is None:
                continue

            self.move_file_into_gap(i, leftmost_gap)
            # logger.debug(self.print_blocks())


    def checksum(self) -> int:
        return sum(i * file for i, file in enumerate(self.disk) if file is not None)


arg_parser = ArgumentParser('python -m 2024.9.main', description="Advent of Code 2024 Day 9")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    raw_map = list(parse_input(argus.input_path))[0]
    disk_map = DiskMap(raw_map, part=argus.part)
    # logger.debug(disk_map.print_blocks())
    match argus.part:
        case -1:
            answer = disk_map.esrap()
        case 1:
            disk_map.compact()
        case 2:
            disk_map.compact_with_defrag()

    logger.debug('')

    print(disk_map.checksum())
