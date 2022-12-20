from argparse import ArgumentParser
from utils import logger, parse_input, Point, Grid
import re


def parse_sensor(line):
    sx, sy, bx, by = re.findall(r'-?\d+', line)

    return Point(int(sx), int(sy)), Point(int(bx), int(by))


def merge_ranges(first, second):
    return (min(first[0], second[0]), max(first[1], second[1]))


def simplify_ranges(ranges):
    new_ranges = []

    ranges.sort()
    current = None
    for rng in ranges:
        if current is None:
            current = rng
            continue

        logger.debug(f"Comparing {current} vs {rng}")
        if current[0] <= rng[1] or current[0] <= rng[0] and current[1] >= rng[1]:
            current = merge_ranges(current, rng)
            logger.debug(f"  - merged: {current}")
        else:
            logger.debug(f"pushed {current}, next is {rng}")
            new_ranges.append(current)
            current = rng

    logger.debug(f"pushing final {current}")
    if current: new_ranges.append(current)

    return new_ranges


class Sensor:
    def __init__(self, line):
        self.pos, self.beacon = parse_sensor(line)
        self.range = self.pos.taxi_to(self.beacon)

    def __str__(self):
        return (
            f"Sensor at x={self.pos.x}, y={self.pos.y}: "
            f"closest beacon is at x={self.beacon.x}, y={self.beacon.y}"
        )

    def __repr__(self):
        return f"<Sensor ({self.pos}), range={self.range}>"


class Thing:
    def __init__(self, lines, part):
        self.part = part
        self.x_bounds = [0, 0]
        self.y_bounds = [0, 0]
        self.beacons = set()
        self.sensors = []
        self.parse(lines)

        self.grid = Grid.from_points([s.pos for s in self.sensors] + [b for b in self.beacons])
        if self.grid.width < 80:
            self.grid.init_grid('.')

            for x, y in self.beacons:
                self.grid.set(x, y, 'B')

            for sensor in self.sensors:
                self.grid.set(sensor.pos, 'S')
        else:
            logger.warning("Grid is too large to render, not visualizing")

    def __str__(self):
        return '\n'.join(str(sensor) for sensor in self.sensors)

    def parse(self, lines):
        for line in lines:
            sensor = Sensor(line)
            self.sensors.append(sensor)
            self.beacons.add(sensor.beacon)

    def answer(self, target_y):
        ranges = []
        for sensor in self.sensors:
            dist = abs(target_y - sensor.pos.y)
            logger.debug(f"{repr(sensor)}: {dist} from y={target_y}")
            if dist > sensor.range:
                logger.debug(f"  No overlap.")
                continue

            overlap = sensor.range - dist

            clear_range = (sensor.pos.x - overlap, sensor.pos.x + overlap)
            ranges.append(clear_range)
            logger.debug(f"  {overlap} of overlap, so range: {clear_range} added")

        ranges = simplify_ranges(ranges)

        logger.debug('\nRanges:')
        for r in ranges:
            logger.debug(f"  {r}")

        return sum(u - l for l, u in ranges)


arg_parser = ArgumentParser('python -m 15.main 15', description="Triangulate Distress Beacons")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

arg_parser.add_argument('target_y', type=int, help="Which line to count beaconless tiles on")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    thing = Thing(parse_input(argus.input_path), argus.part)

    logger.info(thing)
    logger.debug('')
    logger.debug(repr(thing.grid))
    if thing.grid.ready:
        logger.info(thing.grid)

    print(f"answer:\n{thing.answer(argus.target_y)}")
