from argparse import ArgumentParser
from typing import Iterator
import itertools

from utils import logger, parse_input, CharGrid, coordinates, CARDINAL_DIRECTIONS, INFINITY, DIRECTION_MAP


class ReindeerMaze(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.start = (0, 0)
        self.end = (0, 0)

        super().__init__(lines)
        self.nav_map: list[list[tuple[int, coordinates]]] = self.add_layer((INFINITY, DIRECTION_MAP['E']))
        self.nav_map[self.start[0]][self.start[1]] = (0, DIRECTION_MAP['E'])
        self.unvisited = set(itertools.product(range(self.height), range(self.width)))

    def parse_cell(self, y: int, x: int, c: str) -> str:
        if c == 'S':
            self.start = (y, x)

        if c == 'E':
            self.end = (y, x)

        return c

    def pop_shortest_unvisited(self) -> tuple[coordinates, int, coordinates]:
        sy, sx = -1, -1
        shortest = INFINITY
        s_dir = DIRECTION_MAP['E']

        for uy, ux in self.unvisited:
            dist, dir = self.nav_map[uy][ux]
            if dist < shortest:
                sy, sx = uy, ux
                shortest = dist
                s_dir = dir

        if (sy, sx) == (-1, -1):
            # no more reachable nodes
            raise StopIteration

        self.unvisited.remove((sy, sx))

        return (sy, sx), shortest, s_dir


    def djikstra(self) -> int:
        """Hello djikstra my old friend"""
        y, x = -1, -1

        def is_open_and_unvisited(y: int, x: int) -> bool:
            return self.lines[y][x] != '#' and (y, x) in self.unvisited

        while(len(self.unvisited)): # technically should also check for all-infinity, but that wont happen
            try:
                (y, x), distance, (hy, hx) = self.pop_shortest_unvisited()
            except StopIteration:
                break
            #logger.info(f"At {y, x}, current distance is {distance}, heading {hy, hx}")

            if distance == INFINITY:
                # shortest unvisited is unreachable what
                breakpoint()

            if (y, x) == self.end and self.part == 1:
                return distance # shortest path found! (probably)

            for cy, cx in self.get_adjacent_coordinates(y, x, test=is_open_and_unvisited):
                cost_from_here = distance + 1
                if (cy, cx) != (y + hy, x + hx):
                    cost_from_here += 1000

                #logger.info(f"checking {cy, cx}: {cost_from_here}")

                if cost_from_here < self.nav_map[cy][cx][0]:
                    #logger.info(f"  shorter than {self.nav_map[cy][cx][0]}")
                    self.nav_map[cy][cx] = (cost_from_here, (cy - y, cx - x))


        return distance

    def count_best_paths(self) -> int:
        best_path_tiles = set()

        self.djikstra()

        def is_reachable(y: int, x: int) -> bool:
            return self.nav_map[y][x][0] < INFINITY

        def by_distance(coords) -> int:
            y, x = coords
            return self.nav_map[y][x][0]

        # backtrack from end?
        to_check = [self.end]


        while len(to_check):
            y, x = to_check.pop()

            best_path_tiles.add((y, x))
            logger.info(self.esrap_lines({tile: 'O' for tile in best_path_tiles}))

            if (y, x) == self.start:
                break

            candidates = sorted(
                self.get_adjacent_coordinates(y, x, test=is_reachable),
                key=by_distance
            )
            #if (y, x) == (7, 5):
            #    breakpoint()

            shortest = INFINITY
            for cy, cx in candidates:
                dist = self.nav_map[cy][cx][0]
                if dist < shortest:
                    shortest = dist
                if dist > shortest:
                    break

                to_check.append((cy, cx))


        return len(best_path_tiles)




def answer2(maze: ReindeerMaze) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


arg_parser = ArgumentParser('python -m 2024.16.main', description="Advent of Code 2024 Day 16")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    maze = ReindeerMaze(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = maze.esrap_lines()
        case 1:
            answer = maze.djikstra()
        case 2:
            answer = maze.count_best_paths()

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
