from argparse import ArgumentParser
from typing import Iterator, Mapping, Callable, Any

from utils import logger, parse_input, CharGrid, coordinates, CARDINAL_DIRECTIONS


class TrailMap(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.heads: list[coordinates] = []
        self.tails: list[coordinates] = []

        # self.reached_tails = set()
        super().__init__(lines)

        # if it's a set of coodinates, # of tails reachable
        # if None, unvisited (or a tail)
        self.subroutes: list[list[set[tuple[coordinates]] | None]] = [[None] * self.width for y in range(self.height)]

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

    def print_subscore_at(self, y: int, x: int, annotations: Mapping[coordinates, str] = {}) -> str:
        subroute = self.subroutes[y][x]

        if annotation := annotations.get((y, x)):
            return annotation

        if subroute is None:
            return '.'

        return f"{len(subroute)}"

    def print_score_line(self, y: int, annotations: Mapping[coordinates, str] = {}) -> str:
        return ''.join(self.print_subscore_at(y, x, annotations=annotations) for x in range(self.width))

    def print_scores(self, annotations: Mapping[coordinates, str] = {}) -> str:
        return '\n'.join(self.print_score_line(y, annotations=annotations) for y in range(self.height))

    def score_trail(self, trailhead: coordinates) -> set[tuple[coordinates]]:
        y, x = trailhead

        elevation = self.lines[y][x]

        if elevation == 9:
            logger.debug(f"Found peak at {trailhead}")
            return set(((y, x),))

        if (subroute := self.subroutes[y][x]) is not None:
            return subroute

        # depth-first-search? or is this djikstra?
        next_nodes = list(self.cardinal_adjacent_cells(y, x, test=lambda v: v is not None and v - elevation == 1))

        subroutes = set()
        for next_node in next_nodes:
            for next_sub in self.score_trail(next_node):
                subroutes.add((y, x) + next_sub)
                # logger.debug(self.print_scores({trailhead: f"{elevation}"}))
                #subroutes.update(next_subs)

        self.subroutes[y][x] = subroutes

        return subroutes


def score_all_trailheads(trail_map: TrailMap) -> int:
    accumulator = 0
    for head in trail_map.heads:
        scores = trail_map.score_trail(head)
        # TODO: for some reason the actual trail head is missing from the end of the paths now?
        score = len(set([score[-2:] for score in scores]))

        logger.info(f"head at {head} has score {score}")
        accumulator += score

    return accumulator


def score_all_trailheads_by_quality(trail_map: TrailMap) -> int:
    accumulator = 0
    for head in trail_map.heads:
        subscores = trail_map.score_trail(head)
        score = len(subscores)
        logger.info(f"head at {head} has score {score}")
        accumulator += score

    return accumulator


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
            answer = score_all_trailheads(trail_map)
        case 2:
            answer = score_all_trailheads_by_quality(trail_map)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        logger.info(f"No answer available for part {argus.part}")
        print(-1)
