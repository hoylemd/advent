from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator, Tuple


def parse_line(line: str):
    start_index = None
    cells = []
    for x, c in enumerate(line):
        if c == 'S':
            start_index = x
        cells.append(c)
    return cells, start_index


DIRECTIONS = {
    'N': (-1, 0),
    'E': (0, 1),
    'W': (0, -1),
    'S': (1, 0),
}

PIPES = {
    '|': ('N', 'S'),
    '-': ('E', 'W'),
    'L': ('N', 'E'),
    'J': ('N', 'W'),
    '7': ('W', 'S'),
    'F': ('E', 'S'),
}


def figure_pipe_part(first_part_delta: Tuple[int, int], last_part_delta: Tuple[int, int]) -> str:
    deltas = set([first_part_delta, last_part_delta])
    for pipe, dirs in PIPES.items():
        if deltas == set(DIRECTIONS[d] for d in dirs):
            return pipe

    raise ValueError('cant be done?')


class NoPathError(Exception):
    pass


class PipeGrid:

    def __init__(self, map: Iterator[str], part: int = 1):
        self.part = part

        self.rows = []
        for y, line in enumerate(map):
            row, start_x = parse_line(line)
            if start_x is not None:
                self.start = (y, start_x)
            self.rows.append(row)

        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.loop_coords = {}

    def row_strings(self):
        return (''.join(row) for row in self.rows)

    def grid_string(self):
        return "\n".join(self.row_strings())

    def connecting_coords(self, y: int, x: int) -> list[Tuple[int, int]]:
        pipe_at = self.rows[y][x]
        try:
            directions = PIPES[pipe_at]
        except KeyError as exc:
            raise NoPathError(f'No pipe at ({y}, {x}): {pipe_at}') from exc

        results = []
        for dy, dx in (DIRECTIONS[direction] for direction in directions):
            coords = (y + dy, x + dx)
            if self.valid_coords(*coords):
                results.append(coords)

        return results

    def valid_coords(self, y: int, x: int) -> bool:
        if y < 0 or y >= self.height:
            return False

        if x < 0 or x >= self.width:
            return False

        return True

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def loop_distance_from(self, direction: str) -> int:
        """Raise NoPathError if this way is not a loop"""
        y, x = self.start
        ny, nx = y + DIRECTIONS[direction][0], x + DIRECTIONS[direction][1]
        steps = 1
        self.loop_coords = {(y, x): self.rows[y][x]}
        first_loop_part = None

        while (ny, nx) != self.start:
            connections = self.connecting_coords(ny, nx)
            self.loop_coords[(ny, nx)] = self.rows[ny][nx]
            if first_loop_part is None:
                first_loop_part = (ny, nx)

            if connections[0] == (y, x):
                y, x = ny, nx
                ny, nx = connections[1]
            elif connections[1] == (y, x):
                y, x = ny, nx
                ny, nx = connections[0]
            else:
                raise NoPathError('Current corrdinates are not connected to next pipe? hwat')
            steps += 1

        start_part = figure_pipe_part(
            (first_loop_part[0] - ny, first_loop_part[1] - nx),  # type: ignore
            (y - ny, x - nx))  # type: ignore
        self.loop_coords[(self.start[0], self.start[1])] = start_part

        return steps


def loop_enclosed_area(grid: PipeGrid) -> int:
    accumulator = 0

    # find the loop
    farthest_pipe_distance(grid)

    # solve part 2
    for y, row in enumerate(grid.rows):
        mode = 0
        vis_row = []
        h_seg_start = None

        cross_corners = [set(['F', 'J']), set(['L', '7'])]
        for x, cell in enumerate(row):
            loop_pipe = grid.loop_coords.get((y, x))
            if loop_pipe is None:
                if mode:
                    vis_row.append('#')
                    accumulator += 1
                else:
                    vis_row.append('.')
            else:
                vis_row.append(loop_pipe)
                if loop_pipe == '|':
                    mode = (mode + 1) % 2
                elif loop_pipe == '-':
                    pass  # horizontal pipe, doesn't mean anything
                else:
                    if h_seg_start is None:
                        h_seg_start = loop_pipe
                    else:
                        if set([h_seg_start, loop_pipe]) in cross_corners:
                            mode = (mode + 1) % 2
                        h_seg_start = None

        logger.info(''.join(vis_row))

    return accumulator


def farthest_pipe_distance(grid: PipeGrid) -> int:
    loop_length = 0
    for direction in DIRECTIONS:
        try:
            loop_length = grid.loop_distance_from(direction)
            break
        except NoPathError as exc:
            logger.info(f'Could not find a loop starting {direction}: {exc}')
            continue

    return loop_length // 2


arg_parser = ArgumentParser('python -m 2023.10.main', description="Advent of Code 2023 Day 10")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    map = parse_input(argus.input_path)
    grid = PipeGrid(map)
    if argus.part == 1:
        answer = farthest_pipe_distance(grid)
    else:
        answer = loop_enclosed_area(grid)

    logger.debug('')

    print(f"answer:\n{answer}")
