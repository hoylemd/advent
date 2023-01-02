from argparse import ArgumentParser
from utils import parse_input_line, Point, decomp_direction


COMPASS = [decomp_direction(d) for d in 'NESW']


class CityWalk:
    def __init__(self, script, part):
        self.part = part
        self.commands = self.parse(script)
        self.position = Point(0, 0)
        self.heading = 0  # refer to COMPASS for how this gets decoded
        self.visited = set()

        self.visited.add(self.position)

    def parse(self, script):
        for spec in script.split(', '):
            yield spec[0], int(spec[1:])

    def turn(self, direction):
        delta = -1 if direction == 'L' else 1
        self.heading = (self.heading + delta) % len(COMPASS)
        return Point(*COMPASS[self.heading])

    def EB_HQ_distance(self):
        for dir, dist in self.commands:
            vector = self.turn(dir)
            for i in range(dist):
                self.position += vector
                if self.part == 2 and self.position in self.visited:
                    return self.position.taxi_to(0, 0)
                self.visited.add(self.position)

        return self.position.taxi_to(0, 0)


arg_parser = ArgumentParser('python -m 2016.1.main', description="Advent of Code 2016 Day 1")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    input_path = argus.input_path
    if 'test' in input_path:
        input_path = f"{input_path[:-4]}{argus.part}{input_path[-4:]}"

    thing = CityWalk(parse_input_line(input_path), argus.part)

    answer = thing.EB_HQ_distance()

    print(f"answer:\n{answer}")
