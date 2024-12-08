from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input, coordinates, CharGrid


# TODO: refactor with CharGrid
class LabMap(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.guard_position = (0, 0)  # placeholder
        super().__init__(lines)

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

    def find_obstacle(self, pos: coordinates, direction: coordinates, temp_obstacle: coordinates = (-1, -1)) -> int:
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

            if content == '#' or (y, x) == temp_obstacle:
                logger.debug(f"obstacle found at ({y}, {x})")
                # Obstacle found!
                return tiles

            # Maybe X in the tile?
            tiles += 1


DIRECTIONS = [
    (-1, 0),  # North
    (0, 1),  # East
    (1, 0),  # South
    (0, -1),  # West
]


def radar_ping(from_pos: coordinates, direction: coordinates, distance: int = 0) -> coordinates:
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

        if lab_map.is_out_of_bounds(radar_ping(guard_position, direction)):
            # shes a-leaving
            break

        turns += 1

    return len(seen)


def leads_to_loop(lab_map: LabMap, seen_obstacles: set[tuple[coordinates, coordinates]], first_position: coordinates,
                  direction_index: int, temp_obstacle: coordinates) -> bool:
    turns = 0
    new_obstacles = set()
    guard_position = first_position

    first_direction = DIRECTIONS[(direction_index + turns) % 4]
    logger.info(f"checking for loop from {first_position}, {first_direction}")

    while True:
        direction = DIRECTIONS[(direction_index + turns) % 4]
        p_crossed = lab_map.find_obstacle(guard_position, direction, temp_obstacle=temp_obstacle)
        next_position = radar_ping(guard_position, direction, p_crossed - 1)
        p_obstacle = radar_ping(guard_position, direction, p_crossed)
        if lab_map.is_out_of_bounds(p_obstacle):
            logger.info(f"would (inner) exit after {turns} turns, so no loop here")
            return False
        new_obstacle = (p_obstacle, direction)

        logger.debug(f"next obstruction at {new_obstacle}")
        if new_obstacle in seen_obstacles or new_obstacle in new_obstacles:
            logger.info(f"after {turns} more steps...")
            logger.info(f"possible obstacle at found! {first_position} leads to {p_obstacle}, facing {direction}")
            return True

        new_obstacles.add(new_obstacle)
        guard_position = next_position
        turns += 1

    logger.info(f"would (outer) exit after {turns} turns, so no loop here")
    return False


def count_loop_obstacles(lab_map: LabMap) -> int:
    """Count places in the path where an obstruction would send the guard back to a previous obstruction,
    facing the same direction"""
    guard_position = lab_map.guard_position
    seen = set([guard_position])
    seen_obstacles: set[tuple[coordinates, coordinates]] = set()
    potential_obstacles = list()
    turns = 0

    # solve part 2
    while True:
        direction = DIRECTIONS[turns % 4]
        logger.info(f"{guard_position=}, {direction=}{turns=}, obstacles={len(seen_obstacles)}")
        crossed = lab_map.find_obstacle(guard_position, direction)
        logger.info(f"{crossed=}")

        for i in range(crossed):
            next_position = radar_ping(guard_position, direction)

            # if next_position == (77, 59):
            #    breakpoint()
            if next_position not in seen and leads_to_loop(lab_map, seen_obstacles | set([(next_position, direction)]),
                                                           guard_position, turns + 1, next_position):
                logger.info(f"adding obstacle at {next_position}")
                potential_obstacles.append(next_position)

            seen.add(guard_position)
            guard_position = next_position

        new_obstacle = (  # position, direction
            radar_ping(guard_position, direction), direction)

        seen_obstacles.add(new_obstacle)

        if lab_map.is_out_of_bounds(radar_ping(guard_position, direction)):
            # shes a-leaving
            break

        turns += 1

    # logger.info(f"{potential_obstacles=}")
    # between 1665 and 1880 (?)
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
