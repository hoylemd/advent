from argparse import ArgumentParser
from typing import Iterator
import os
import itertools

from utils import logger, parse_input, CharGrid, coordinates, INFINITY, DIRECTION_MAP

class RamRun(CharGrid):

    def __init__(self, lines: Iterator[str], height: int, width: int, block_limit: slice, part: int = 1):
        self.part = part

        self.blocks = [line for line in self.parse_lines(lines)]

        def init_cell(y: int, x: int) -> str:
            if (y, x) in (self.blocks[block_limit]):
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

    def djikstra(self, start: coordinates, end: coordinates | None = None) -> list[list[int]]:
        """Hello djikstra my old friend
        if end is provided, will stop when it finds an optimal route there
        """
        y, x = start
        unvisited = set(itertools.product(range(self.height), range(self.width)))
        nav_map = self.init_nav_map()
        nav_map[y][x] = 0

        def pop_shortest_unvisited() -> tuple[coordinates, int]:
            sy, sx = -1, -1
            shortest = INFINITY

            for uy, ux in unvisited:
                dist = nav_map[uy][ux]
                if dist < shortest:
                    sy, sx = uy, ux
                    shortest = dist

            if (sy, sx) == (-1, -1):
                # no more reachable nodes
                raise StopIteration

            unvisited.remove((sy, sx))

            return (sy, sx), shortest

        def is_open_and_unvisited(y: int, x: int) -> bool:
            return self.lines[y][x] != '#' and (y, x) in unvisited

        while(len(unvisited)):
            try:
                (y, x), distance = pop_shortest_unvisited()
            except StopIteration:
                break

            if distance == INFINITY:
                raise ValueError("Shortest unvisited node is unreachable - that's impossible!")

            if end is not None and (y, x) == end:
                break

            for cy, cx in self.get_adjacent_coordinates(y, x, test=is_open_and_unvisited):
                cost_from_here = distance + 1

                if cost_from_here < nav_map[cy][cx]:
                    nav_map[cy][cx] = cost_from_here

        return nav_map

    def shortest_path(
        self, start: coordinates, end: coordinates, branch: coordinates | None = None
    ) -> tuple[list[coordinates],list[coordinates]]:
        nav_map = self.djikstra(start, end)
        path: list[coordinates] = []
        branches: list[coordinates] = []

        y, x = end

        def is_not_in_path_branch_or_unreachable(y: int, x: int) -> bool:
            return not(
                (branch is not None and (y, x) == branch)
                or (y, x) in path or nav_map[y][x] == INFINITY
            )

        while (y, x) != start:
            path.append((y, x))

            next_steps = sorted([
                (nav_map[cy][cx], cy, cx)
                for cy, cx in self.get_adjacent_coordinates(y, x, test=is_not_in_path_branch_or_unreachable)
            ], key=lambda ns: -1 * ns[0])

            nd, y, x = next_steps.pop()
            # it 2nd shortest next step has same dist, add it to branches
            if next_steps and next_steps[-1][0] == nd:
                branches.append((y, x))

        assert (y, x) == start
        assert nav_map[y][x] == 0

        path.reverse()
        return path, branches


def answer2(ram: RamRun) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def min_steps_to_exit(ram: RamRun) -> int:
    accumulator = 0

    path, _= ram.shortest_path((0, 0), (ram.height -1, ram.width -1))

    path_notes = {(0, 0): 'S', **{pc: 'O' for pc in path}}
    logger.info(ram.print_grid(annotations=path_notes))
    # solve part 1

    return len(path)

PART_PARAMS = {
    ('test.txt', 1): {
        'width': 7,
        'height': 7,
        'block_limit': slice(None, 12)
    },
    ('input.txt', 1): {
        'width': 71,
        'height': 71,
        'block_limit': slice(None, 1024)
    }
}

arg_parser = ArgumentParser('python -m 2024.18.main', description="Advent of Code 2024 Day 18")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    dimensions = PART_PARAMS[os.path.basename(argus.input_path), abs(argus.part)]
    lines = parse_input(argus.input_path)
    ram = RamRun(lines, **dimensions, part=argus.part)
    match argus.part:
        case -1:
            answer = ram.esrap_lines()
        case 1:
            answer = min_steps_to_exit(ram)
        case 2:
            answer = answer2(ram)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
