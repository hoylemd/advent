import os
import logging
import fileinput

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
logger.addHandler(ch)


def parse_input():
    return (line.strip() for line in fileinput.input())


def render_line(line, shader=str):
    return ''.join(shader(c) for c in line)


def render_lines(lines, shader=str):
    return (render_line(line, shader) for line in lines)


def render_grid(grid, shader=str):
    return '\n'.join(render_lines(grid, shader))


def num_width(number):
    width = 1
    if number < 0:
        width += 1

    val = abs(number)
    while val := int(val / 10):
        width += 1

    return width


DIR_MAP = {
    'L': (-1, 0),
    'U': (0, 1),
    'R': (1, 0),
    'D': (0, -1),
    '<': (-1, 0),
    '^': (0, 1),
    '>': (1, 0),
    'V': (0, -1)
}


def decomp_direction(dir):
    return DIR_MAP[dir]


def reduce_vector(x, y):
    if x > 1:
        x = 1
    elif x < -1:
        x = -1

    if y > 1:
        y = 1
    elif y < -1:
        y = -1

    return (x, y)


def vector(start, dest):
    return dest[0] - start[0], dest[1] - start[1]


class Point():
    """A 2-dimensional coordinate

    :param int x: x coordinate
    :param int y: y coordinate

    Alternatively, pass in one of L,U,R,D,<,^,>,V for a unit vector in that direction

    x and y coordinates can be accessed via the `x` and `y` attributes, or by item
    indexes 0 and 1 respectively.  Behaves like a 2-tuple coordinate as much as possible
    """
    def __init__(self, x, y=None):
        if isinstance(x, str) and x in DIR_MAP:  # handle directions
            x, y = DIR_MAP[x]

        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y

    def __iter__(self):
        return iter((self.x, self.y))

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repr__(self):
        return f"<Point object({self.x},{self.y})>"

    def vector_to(self, *args):
        """Given another point (or x,y coordinates), determine the vector to that point

        usage:
        point.vector_to(x, y)
        point.vector_to(other_point)
        """
        return Point(*vector(self, args))

    def unit(self):
        """Reduce this point to a unit vector"""
        return Point(*reduce_vector(*self))
