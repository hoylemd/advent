from argparse import ArgumentParser
import re

from utils import logger, parse_input, Grid, Point


op_map = {
    'turn on': (1, 1),
    'toggle': (None, 2),
    'turn off': (0, -1)
}


class LightGrid:
    def __init__(self, commands, part=1):
        self.part = part or 1
        self.grid = Grid((1000, 1000), value=0)
        logger.debug('grid ready')
        self.main_op = self.set_light if part == 1 else self.tune_light

        for command in commands:
            self.execute(*command, func=self.main_op)

    @classmethod
    def parse_line(cls, line, part=1):
        matches = re.match(r'(turn on|turn off|toggle) (\d+,\d+) through (\d+,\d+)', line)

        op = op_map[matches.group(1)][part - 1]
        tl = Point(*(int(p) for p in matches.group(2).split(',')))
        br = Point(*(int(p) for p in matches.group(3).split(',')))

        return op, tl, br

    @classmethod
    def parse(cls, lines, line_parser=None, part=1):
        line_parser = line_parser or cls.parse_line
        return cls(
            (line_parser(line, part=part) for line in lines),
            part=part)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def set_light(self, op, x: int, y: int):
        if op is None:
            op = 0 if self.grid[y][x] else 1
        self.grid[y][x] = op

    def tune_light(self, op, x: int, y: int):
        self.grid[y][x] = max(0, self.grid[y][x] + op)

    def execute(self, op: str, tl: Point, br: Point, func: callable):
        logger.debug(f"executing {op} {tl} {br}")

        def gen_coords():
            for y in range(tl.y, br.y + 1):
                for x in range(tl.x, br.x + 1):
                    yield x, y

        for x, y in gen_coords():
            func(op, x, y)

    def count_lights(self, part=1):
        return sum(sum(row) for row in self.grid)


arg_parser = ArgumentParser('python -m 2015.6.main', description="Advent of Code 2015 Day 6")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    grid = LightGrid.parse(parse_input(argus.input_path), part=argus.part)

    logger.info(str(grid))
    logger.debug('')

    answer = grid.count_lights(argus.part)
    print(f"answer:\n{answer}")
