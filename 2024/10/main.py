from argparse import ArgumentParser
from typing import Iterator, Mapping, Callable, Any

from utils import logger, parse_input, CharGrid, coordinates, CARDINAL_DIRECTIONS


class TrailMap(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.heads: list[coordinates] = []
        self.tails: list[coordinates] = []

        self.reached_tails = set()
        super().__init__(lines)

    def parse_cell(self, y: int, x: int, c: str) -> int | None:
        i = None if c == '.' else int(c)

        if i == 0:
            self.heads.append((y, x))
        elif i == 9:
            self.tails.append((y, x))

        return i

    def parse_line(self, y: int, line: str) -> list[int | None]:
        return [self.parse_cell(y, x, c) for x, c in enumerate(line)]

    def get_cell(self, y: int, x: int) -> int:
        return self.lines[y][x]

    def esrap_cell(self, y: int, x: int) -> str:
        return f"{self.lines[y][x]}"

    def esrap_line(self, y: int, annotations: Mapping[coordinates, str] = {}) -> str:
        return ''.join(annotations.get((y, x), self.esrap_cell(y, x)) for x in range(self.width))

    def cardinal_adjacent_cells(self,
                                y: int,
                                x: int,
                                test: Callable[[Any], bool] = lambda v: v) -> Iterator[coordinates]:
        for dy, dx in CARDINAL_DIRECTIONS:
            target = (y + dy, x + dx)
            if self.is_in_bounds(target) and test(self.lines[target[0]][target[1]]):
                yield target

    def score_trail(self, trailhead: coordinates) -> int:
        elevation = self.get_cell(*trailhead)

        if elevation == 9:
            self.reached_tails.add(coordinates)
            return 1

        # depth-first-search?
        next_nodes = list(self.cardinal_adjacent_cells(*trailhead, test=lambda v: v is not None and v - elevation == 1))

        return sum(self.score_trail(next_node) for next_node in next_nodes)


def answer2(trail_map: TrailMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(trail_map: TrailMap) -> int:
    for head in trail_map.heads:
        trail_map.score_trail(head)

    # solve part 1

    return len(trail_map.reached_tails)


arg_parser = ArgumentParser('python -m 2024.10.main', description="Advent of Code 2024 Day 10")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    trail_map = TrailMap(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = trail_map.esrap_lines()
        case 1:
            answer = answer1(trail_map)
        case 2:
            answer = answer2(trail_map)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        logger.info(f"No answer available for part {argus.part}")
        print(-1)
