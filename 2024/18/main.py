from argparse import ArgumentParser
from typing import Iterator, Iterable
import os
import itertools

from utils import logger, parse_input, CharGrid, coordinates, INFINITY, DIRECTION_MAP

class RamRun(CharGrid):

    def __init__(self, lines: Iterator[str], height: int, width: int, blocks_dropped: int, part: int = 1):
        self.part = part
        self.blocks_dropped = blocks_dropped

        self.blocks = [line for line in self.parse_lines(lines)]

        def init_cell(y: int, x: int) -> str:
            if (y, x) in (self.blocks[:blocks_dropped]):
                return '#'
            return '.'

        self.lines = self.init_grid(height, width, value_fact=init_cell)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> coordinates:
        xs, ys = line.split(',')
        return int(ys), int(xs)

    def parse_lines(self, lines: Iterator[str]) -> Iterator[coordinates]:
        for y, line in enumerate(lines):
            yield self.parse_line(y, line)

    def esrap_block(self, y: int, block_coords: coordinates) -> str:
        return f"{block_coords[1]},{block_coords[0]}"

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_block(y, e) for y, e in enumerate(self.blocks)
        )

    def print_grid(self, *args, **kwargs) -> str:
        return super().esrap_lines(*args, **kwargs)

    def print_grid_with_path(self, path: Iterable[coordinates], start: coordinates = (0, 0)):
        path_notes = {start: 'S', **{pc: 'O' for pc in path}}
        return self.print_grid(annotations = path_notes)


def find_cutoff(ram: RamRun) -> tuple[int,int]:
    path_list, _= ram.shortest_path((0, 0), (ram.height - 1, ram.width - 1))
    path = set(path_list)

    while ram.blocks_dropped < len(ram.blocks):
        y, x = ram.blocks[ram.blocks_dropped]
        ram.lines[y][x] = '#'
        ram.blocks_dropped += 1

        if (y, x) in path:
            try:
                path_list, _ = ram.shortest_path((0, 0), (ram.height - 1, ram.width - 1))
            except ValueError as exc:
                return y, x

            path = set(path_list)

    raise Exception('Path never gets cut off?')


def min_steps_to_exit(ram: RamRun) -> int:
    path, _= ram.shortest_path((0, 0), (ram.height -1, ram.width -1))

    ram.print_grid_with_path(path)
    # solve part 1

    return len(path)

PART_PARAMS = {
    'test.txt': {
        'width': 7,
        'height': 7,
        'blocks_dropped': 12
    },
    'input.txt': {
        'width': 71,
        'height': 71,
        'blocks_dropped': 1024
    }
}

arg_parser = ArgumentParser('python -m 2024.18.main', description="Advent of Code 2024 Day 18")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    dimensions = PART_PARAMS[os.path.basename(argus.input_path)]
    lines = parse_input(argus.input_path)
    ram = RamRun(lines, **dimensions, part=argus.part)
    match argus.part:
        case -1:
            answer = ram.esrap_lines()
        case 1:
            answer = min_steps_to_exit(ram)
        case 2:
            y, x = find_cutoff(ram)
            answer = f"{x},{y}"

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
