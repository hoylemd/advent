from os import environ
from utils import logger, parse_input, render_lines, num_width, vector


def parse_point(spec):
    x, y = spec.split(',')
    return (int(x), int(y))


def get_int_char(number, i):
    return str(number)[i]


class Thing:
    def __init__(self, lines, part):
        self.part = part
        self.rocks = []
        self.origin = (500, 0)
        self.x_bounds = (500, 500)
        self.y_bounds = (0, 0)
        self.grid = self.parse(lines)

    def header_line(self, i, margin=2):
        btwn_l_and_o = (self.origin[0] - self.x_bounds[0]) - 1
        btwn_o_and_r = (self.x_bounds[1] - self.origin[0]) - 1
        return (
            f"{' ' * margin} {get_int_char(self.x_bounds[0], i)}"
            f"{' ' * btwn_l_and_o}{get_int_char(self.origin[0], i)}"
            f"{' ' * btwn_o_and_r}{get_int_char(self.x_bounds[1], i)}"
        )

    def header_lines(self, margin=2):
        return [self.header_line(i, margin) for i in range(num_width(self.x_bounds[1]))]

    def __str__(self):
        lines = [line for line in render_lines(self.grid)]
        margin = num_width(len(lines) - 1)
        stamp = f"{{i:{margin}}} {{line}}"

        grid_lines = [stamp.format(i=i, line=line) for i, line in enumerate(lines)]

        return '\n'.join(self.header_lines(margin) + grid_lines)

    def set_cell(self, x, y, val):
        self.grid[y][x - self.x_bounds[0]] = val

    def get_cell(self, x, y):
        return self.grid[y][x - self.x_bounds[0]]

    def draw_rock(self, points):
        for i, src in enumerate(points):
            try:
                dest = points[i + 1]
            except IndexError:  # last point, we done
                self.set_cell(*src, '#')
                break

            sx, sy = src
            dx, dy = vector(src, dest)
            logger.debug(f"drawing rock segment {sx},{sy}: {dx},{dy}")

            # draw x
            for i in range(0, dx, -1 if dx < 0 else 1):
                self.set_cell(sx + i, sy, '#')

            # draw y
            for i in range(0, dy, -1 if dy < 0 else 1):
                self.set_cell(sx, sy + i, '#')

    def parse_rock(self, line):
        points = [parse_point(spec) for spec in line.split(' -> ')]

        # scan points for dimensions
        for x, y in points:
            if x < self.x_bounds[0]:
                self.x_bounds = (x, self.x_bounds[1])
            if x > self.x_bounds[1]:
                self.x_bounds = (self.x_bounds[0], x)
            if y < self.y_bounds[0]:
                self.y_bounds = (y, self.y_bounds[1])
            if y > self.y_bounds[1]:
                self.y_bounds = (self.y_bounds[0], y)

        return points

    def parse(self, lines):
        rocks = [self.parse_rock(line) for line in lines]

        # prep grid
        self.grid = [
            ['.'] * (self.x_bounds[1] - self.x_bounds[0] + 1)
            for _ in range(self.y_bounds[1] - self.y_bounds[0] + 1)
        ]

        # set sand source
        self.set_cell(*self.origin, val='+')

        # draw rocks
        for rock in rocks:
            self.draw_rock(rock)

        return self.grid

    def simulate_sand(self):
        """Sim a unit of sand falling

        :raises IndexError: if the sand will fall forever
        """
        step = (self.sand[0], self.sand[1] + 1)
        if self.get_cell(*step) == '.':
            self.sand = step
            return

        step = (step[0] - 1, step[1])
        if self.get_cell(*step) == '.':
            self.sand = step
            return

        step = (step[0] + 2, step[1])
        if self.get_cell(*step) == '.':
            self.sand = step
            return

        # if we get here, the sand can't fall, so save it
        self.set_cell(*self.sand, 'o')
        self.fallen += 1
        self.sand = self.origin

    def run_simulation(self):
        while True:
            self.simulate_sand()
            logger.info(self)
            logger.info('')

    def find_steady_state(self):
        self.fallen = 0
        self.sand = self.origin

        try:
            self.run_simulation()
        except IndexError:
            return self.fallen

    def answer(self, func, *args, **kwargs):
        return func()

    def for_part(self, part=1):
        return {
            1: [self.find_steady_state],
            2: []
        }[part]


if __name__ == '__main__':
    part = int(environ.get('ADVENT_PART', 1))
    thing = Thing(parse_input(), part)

    logger.info(thing)
    logger.info('')

    print(f"answer:\n{thing.answer(*thing.for_part(part))}")
