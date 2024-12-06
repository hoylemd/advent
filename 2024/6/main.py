from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


class LabMap:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.guard_position = (0, 0)  # placeholder
        self.width = 0

        self.lines = [self.parse_line(i, line) for i, line in enumerate(lines)]
        self.height = len(self.lines)

    def parse_line(self, y: int, line: str) -> str:
        if self.width == 0:
            self.width = len(line)

        # maybe chart the obstacles?
        try:
            self.guard_position = (y, line.index('^'))
        except ValueError:
            # shes not here
            pass

        return line

    def find_obstacle(self, pos: tuple[int, int], direction: tuple[int, int]) -> int:
        """returns distance to obstacle (i.e. # of tiles between start and obstacle)"""
        tiles = 0

        while True:
            y, x = radar_ping(pos, direction, tiles)
            logger.debug(f"{tiles} steps, {direction} from {pos}, looking at ({y}, {x})")

            if self.is_out_of_bounds((y, x)):
                logger.debug(f"out of bounds at ({y}, {x})")
                # OOB, we're leaving
                return tiles

            content = self.lines[y][x]

            if content == '#':
                logger.debug(f"obstacle found at ({y}, {x})")
                # Obstacle found!
                return tiles

            # Maybe X in the tile?
            tiles += 1

    def is_out_of_bounds(self, pos: tuple[int, int]) -> bool:
        return pos[0] < 0 or pos[1] < 0 or pos[0] >= self.height or pos[1] >= self.width

    def is_on_edge(self, pos: tuple[int, int]) -> bool:
        return pos[0] == 0 or pos[1] == 0 or pos[0] == self.height - 1 or pos[1] == self.width - 1

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"


DIRECTIONS = [
    (-1, 0),  # North
    (0, 1),  # East
    (1, 0),  # South
    (0, -1),  # West
]


def radar_ping(from_pos: tuple[int, int], direction: tuple[int, int], distance: int = 0) -> tuple[int, int]:
    return (from_pos[0] + direction[0] * (distance + 1), from_pos[1] + direction[1] * (distance + 1))


def count_visited(lab_map: LabMap) -> int:
    guard_position = lab_map.guard_position
    seen = set([guard_position])
    turns = 0

    # solve part 1
    while True:
        direction = DIRECTIONS[turns % 4]
        logger.info(f"{guard_position=}, {turns=}, positions={len(seen)}")
        crossed = lab_map.find_obstacle(guard_position, direction)
        logger.info(f"{crossed=}")

        for i in range(crossed):
            guard_position = radar_ping(guard_position, direction)
            seen.add(guard_position)

        if lab_map.is_on_edge(guard_position):
            # shes a-leaving
            break

        turns += 1

    return len(seen)


def leads_to_loop(lab_map: LabMap, seen_obstacles: set[tuple[tuple[int, int], tuple[int, int]]],
                  guard_position: tuple[int, int], direction_index: int) -> bool:
    turns = 0
    direction = DIRECTIONS[direction_index % 4]
    p_crossed = lab_map.find_obstacle(guard_position, direction)
    p_obstacle = radar_ping(guard_position, direction, p_crossed)

    if (p_obstacle, direction) in seen_obstacles:
        logger.info(f"possible obstacle found! {guard_position} leads to {p_obstacle}, facing {direction}")
        return True
    return False


def count_loop_obstacles(lab_map: LabMap) -> int:
    """Count places in the path where an obstruction would send the guard back to a previous obstruction, facing the same direction"""
    guard_position = lab_map.guard_position
    seen_obstacles = set()
    potential_obstacles = set()
    turns = 0

    # solve part 2
    while True:
        direction = DIRECTIONS[turns % 4]
        next_direction = DIRECTIONS[(turns + 1) % 4]
        logger.info(f"{guard_position=}, {turns=}, obstacles={len(seen_obstacles)}")
        crossed = lab_map.find_obstacle(guard_position, direction)
        logger.info(f"{crossed=}")

        for i in range(crossed):
            next_position = radar_ping(guard_position, direction)

            if leads_to_loop(lab_map, seen_obstacles, guard_position, turns + 1):
                potential_obstacles.add(next_position)

            guard_position = next_position

        new_obstacle = (  # position, direction
            radar_ping(guard_position, direction), direction)

        seen_obstacles.add(new_obstacle)

        if lab_map.is_on_edge(guard_position):
            # shes a-leaving
            break

        turns += 1

    return len(potential_obstacles)


arg_parser = ArgumentParser('python -m 2024.6.main', description="Advent of Code 2024 Day 6")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    lab_map = LabMap(lines, part=argus.part)
    if argus.part == 1:
        answer = count_visited(lab_map)
    else:
        answer = count_loop_obstacles(lab_map)

    logger.debug('')

    print(f"answer:\n{answer}")
