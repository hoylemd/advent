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


def get_int_char(number, i, width=None):
    if width is None:
        rendered = str(number)
    else:
        rendered = f"{{:0{width}}}".format(number)
    return rendered[i]


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


class Grid:
    def __init__(self, dimensions=(0, 0), origin=(0, 0), offset=(0, 0), value=None, x_axis_spacing=5):
        """Construct the grid

        :param Point dimensions: the width and height of the grid. (0,0) by default
        :param Point origin: coordinates of the origin. Actual coordinate ranges are
            defined relative to this point. top-left corner (0,0) by default, see offset below
        :param Point offset: where the origin is in the grid
            top-left corner (0,0) by default
        :param any value: Value to pre-populate the grid with. Won't init_grid if None or omitted
        :param int x_axis_spacing: show x-axis label every x columns (first, last and origin always labelled)
        """
        self.dimensions = Point(*dimensions) if isinstance(dimensions, tuple) else dimensions
        self.origin = Point(*origin) if isinstance(origin, tuple) else origin
        self.offset = Point(*offset) if isinstance(offset, tuple) else offset

        self.values = []
        self.x_axis_spacing = x_axis_spacing

        if value is not None:
            self.init_grid(value)

    @property
    def width(self):
        return self.dimensions.x

    @property
    def height(self):
        return self.dimensions.y

    @property
    def x_bounds(self):
        lb = self.origin.x - self.offset.x
        return (lb, lb + self.width - 1)

    @property
    def y_bounds(self):
        lb = self.origin.y - self.offset.y
        return (lb, lb + self.height - 1)

    def init_grid(self, value=None):
        """actually create the values object"""
        self.values = [
            [value] * self.width
            for _ in range(self.height)
        ]

    def get(self, x, y=None):
        if y is None and isinstance(x, Point):
            x, y = x
        ax = x - self.x_bounds[0]
        ay = y - self.y_bounds[0]
        return self.values[ay][ax]

    def set(self, x, y, value=None):
        if value is None and isinstance(x, Point):  # unpack point if provided
            value = y
            x, y = x

        ax = x - self.x_bounds[0]
        ay = y - self.y_bounds[0]

        self.values[ay][ax] = value

    def all_values(self):
        """Depaged iterator to iterate over every cell in the grid"""
        for x, y in self.enumerate_coords():
            yield self.get(x, y)

    def all_items(self):
        """enumerate all coordinates and their values"""
        for x, y in self.enumerate_coords():
            yield (x, y, self.get(x, y))

    def enumerate_coords(self):
        """enumerate all coordinates in the grid"""
        for y in range(self.y_bounds[0], self.y_bounds[1] + 1):
            for x in range(self.x_bounds[0], self.x_bounds[1] + 1):
                yield x, y

    def header_line(self, i, margin, width):
        spacing = self.x_axis_spacing - 1

        def get_char(val):
            return get_int_char(val, i, width)

        # first column
        left = f"{get_char(self.x_bounds[0])}{' ' * (min(spacing, self.x_bounds[1] - self.x_bounds[0]) - 1)}"
        # inner parts
        marks = [m + self.x_bounds[0] for m in range(spacing, self.width, self.x_axis_spacing)]
        inner = (' ' * spacing).join(
            get_char(j) for j in marks
        )
        try:
            last_mark = marks[-1]
        except IndexError:
            last_mark = self.origin.x
        # last column
        breakpoint()
        right = f"{' ' * (self.x_bounds[1] - last_mark - 1)}{get_char(self.x_bounds[1])}"

        line = left + inner + right
        # add origin mark

        ox = self.origin.x - self.x_bounds[0]
        if ox not in marks and ox not in self.x_bounds:
            line = line[:ox] + get_char(self.origin.x) + line[ox + 1:]

        return f"{' ' * margin} {line}"

    def header_lines(self, margin=0):
        width = max(num_width(self.x_bounds[0]), num_width(self.x_bounds[1]))
        return [self.header_line(i, margin, width) for i in range(width)]

    def __str__(self):
        lines = [line for line in render_lines(self.values)]
        margin = max(num_width(self.y_bounds[0]), num_width(self.y_bounds[1]))
        stamp = f"{{n:0{margin}}} {{line}}"

        grid_lines = [stamp.format(n=i + self.y_bounds[0], line=line) for i, line in enumerate(lines)]

        return '\n'.join(self.header_lines(margin) + grid_lines)

    def __repr__(self):
        return f"<Grid object(({self.width},{self.height}),origin:({self.origin}),offset:({self.offset})>"

    def __iter__(self):
        """iterator of rows, which can be iterated themselves"""
        return self.values
