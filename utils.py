"""General-purpose helper modules"""
import os
import logging

# region === logging ===
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
logger.addHandler(ch)
# endregion


# region === File IO ===
def _read_file(path):
    """Just emit lines from a file path

    :param str path: Path to the file to read from
    :yields str: Lines from the file (WITH trailing newline)
    """
    with open(path) as fp:
        for line in fp.readlines():
            yield line


def parse_input(path=None):
    """Parse file input into stripped lines.

    If path is provided, will use regular python file reading.
    Otherwise, uses the fileinput library.
    Note: if fileinput is used, it will consume *all* command line arguments as file paths!
    If you need command line arguments, provide a file path.

    :param str path: Path to the file to read from. Optional, will use fileinput if omitted.
    :yields str: Stripped lines from the file/input
    """
    if path:
        genny = _read_file(path)
    else:
        import fileinput
        genny = fileinput.input()

    return (line.strip() for line in genny)


def parse_input_line(path: str = None):
    """Parse file input into a single string

    See _parse_input_ above, this just joins the lines together and returns them

    :param str path: Path to the file to read from. Optional, will use fileinput if omitted.
    :return str: The entire contents of the file, without newlines
    """
    return ''.join(line for line in parse_input(path))
# endregion


# region === Misc ===
def noop(*args, **kwargs):
    """Single-argument noop, just returns the arg

    Just for when you need an operation but don't actually need to do anything

    :param list args: positional arguments to be returned
    :param list kwargs: keyword args to be returned
    :returns list, dict: The arguments passed in
    """
    return args, kwargs
# endregion


# region === Grid rendering ===
def render_line(line, shader=str):
    """Render all elements of an array together into a string.

    Used primarily for rendering grid lines.
    Provide a `shader` callable to mutate the elements before rendering them.

    :param list line: The array of elements to render together
    :param callable shader: Callable to mutate elements before rendering them together, optional

    :returns str: The rendered line
    """
    return ''.join(shader(c) for c in line)


def render_lines(lines, shader=str):
    """Pluralizer for render_line.

    see render_line for details

    :param list lines: The array of arrays to be rendered
    :param callable shader: Callable to mutate elements before rendering them together, optional

    :yields str: The rendered lines
    """
    return (render_line(line, shader) for line in lines)


def render_grid(grid, shader=str):
    """Render a 2-dimensional array into a single multiline string.

    see render_line for details

    :param list grid: The array of arrays to be rendered
    :param callable shader: Callable to mutate elements before rendering them together, optional

    :returns str: The rendered grid
    """
    return '\n'.join(render_lines(grid, shader))
# endregion


# region === Number rendering ===
def num_width(number):
    """Given a number, compute it's width in characters when rendered.

    :param int,float number: The number to measure
    :returns int: The width of the number in characters
    """
    return len(str(number))


def get_int_char(number, i, width=None):
    """Given a number, sample the ith character of it when rendered, with optional padding.

    :param int,float number: The number to render and sample.
    :param int i: the index of the rendered string to sample.
    :param int width: pad the string to this width before sampling.
        Optional, no padding if omitted.

    :returns str: The sampled character.
    """
    if width is None:
        rendered = str(number)
    else:
        rendered = f"{{:0{width}}}".format(number)
    return rendered[i]


def seconds_to_string(secs: int):
    """Convert an integer number of seconds into a HH:MM:SS, MM:SS, or SSs string

    :param int secs: Sconds to convert
    :return str: The number of seconds in human-readable format
    """
    if secs <= 60:
        return f"{secs}s"

    mins = secs // 60
    secs = secs - mins * 60

    if mins <= 60:
        return f"{mins}:{secs:02}"

    hrs = mins // 60
    mins = mins - hrs * 60

    return f"{hrs}:{mins:02}:{secs:02}"
# endregion


# region === Point helpers ===
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
    """Decompose a direction character into it's component unit vector tuple.

    :param str dir: The direction to decompose
    :returns (int, int): The unit vector of the specified direction."""
    return DIR_MAP[dir.upper()]


def reduce_vector(x, y):
    """Reduce a vector into a unit vector.

    :param int x: x-component to be reduced
    :param int y: y-component to be reduced

    :returns (int, int): The unit vector reduced from the input components.
    """
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
    """Calculate the vector between 2 xy coordinate pairs

    :param (int, int) start: The initial coordinates
    :param (int, int) dest: The destination coordinates

    :returns (int, int): Vector from `start` to `dest`
    """
    return dest[0] - start[0], dest[1] - start[1]
# endregion


# region === Cartesian plane stuff ===
class _Pair:
    """Represents a generic 2-tuple, meant as an abstract class for Point or Range"""

    def __init__(self, first, second):
        self._first = first
        self._second = second

    def __getitem__(self, key):
        if key == 0:
            return self._first
        if key == 1:
            return self._second

        raise IndexError

    def __iter__(self):
        return iter((self._first, self._second))

    def __str__(self):
        return f"{self._first},{self._second}"

    def __repr__(self):
        return f"<{self.__class__.__name__} object({self._first},{self._second})>"

    def __eq__(self, other):
        return (self._first, self._second) == other

    def __add__(self, other):
        o1, o2 = other
        return self.__class__(self.x + o1, self.y + o2)

    def __hash__(self):
        return hash((self._first, self._second))


class Range(_Pair):
    """Represent a range of values between a lower and upper bound (inclusive)

    behaves like a 2-tuple as much as possible

    :param int lower: Lower bound for the range
    :param int upper: Upper bound for the range
    """

    def __init__(self, lower, upper):
        """Constructor for a Range

        :param int lower: Lower bound for the range
        :param int upper: Upper bound for the range
        """
        super().__init__(lower, upper)

    @property
    def lower(self):
        return self._first

    @property
    def upper(self):
        return self._second

    @property
    def l(self):  # noqa E743
        return self.lower

    @property
    def u(self):
        return self.upper

    @property
    def right(self):
        return self.upper

    @property
    def r(self):
        return self.right

    def __contains__(self, key):
        try:
            return all(el in self for el in key)
        except TypeError:  # not iterable
            return key >= self.lower and key <= self.upper

    def constrain(self, n):
        """Given an integer, constrain it to the range

        :param int n: The integer to constrain
        :return int: The constrained integer
        """

        if n < self.lower:
            n = self.lower
        if n > self.upper:
            n = self.upper

        return n

    def is_disjoint_with(self, other_lower, other_upper):
        """Determine if another range is disjoint (not touching or overlapping) with this one

        to use with a Range, do `my_range.is_disjoint_with(*other_range)`

        :param int other_lower: lower-bound of the other range
        :param int other_upper: upper-bound of the other range
        :return bool: True if the ranges are disjoint, False if they touch or overlap
        """
        left = (self[0], self[1])
        right = (other_lower, other_upper)

        if left[0] > right[0]:
            left, right = right, left

        if right[0] - left[1] > 1:
            return True
        return False


class Point(_Pair):
    """A 2-dimensional coordinate

    :param int x: x coordinate
    :param int y: y coordinate

    Alternatively, pass in one of L,U,R,D,<,^,>,V for a unit vector in that direction

    x and y coordinates can be accessed via the `x` and `y` attributes, or by item
    indexes 0 and 1 respectively.  Behaves like a 2-tuple coordinate as much as possible

    To copy a Point object do: Point(*other_point)
    """

    def __init__(self, x, y=None):
        """Constructor for a Point object

        :param int|str x: x-component or direction string
        :param int y: y-component, omit for direction.
        """
        if isinstance(x, str) and x in DIR_MAP:  # handle directions
            x, y = DIR_MAP[x]

        super().__init__(x, y)

    @property
    def x(self):
        return self._first

    @property
    def y(self):
        return self._second

    def __repr__(self):
        return f"<{self.x},{self.y}>"

    def vector_to(self, *args):
        """Given another point (or x,y coordinates), determine the vector to that point

        usage:
        point.vector_to(x, y)
        point.vector_to(other_point)
        """
        if len(args) == 1 and isinstance(args[0], Point):
            x, y = args[0]
        else:
            x, y = args
        return Point(*vector(self, (x, y)))

    def taxi_to(self, *args):
        """Given another point (or x,y coodinates), determine taxicab distance to that point"""
        return sum(abs(comp) for comp in self.vector_to(*args))

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
        self.ready = False

        if value is not None:
            self.init_grid(value)

        self._header = None

    @classmethod
    def from_points(cls, points, origin=None):
        """Take in a bunch of points, compute appropriate origin/offset/dims and make a new Grid for it"""
        x_bounds = [0, 0]
        y_bounds = [0, 0]

        if origin is not None:  # if it's specified, include origin
            points.append(origin)

        for x, y in points:
            if x < x_bounds[0]:
                x_bounds[0] = x
            if x > x_bounds[1]:
                x_bounds[1] = x
            if y < y_bounds[0]:
                y_bounds[0] = y
            if y > y_bounds[1]:
                y_bounds[1] = y

        return Grid.from_bounds(x_bounds, y_bounds, origin)

    @classmethod
    def from_bounds(cls, x_bounds, y_bounds, origin=None):
        # if no origin, use top-left corner as origin, no offset
        if origin is None:
            # if 0,0 within bounds use that
            if x_bounds[0] <= 0 and x_bounds[1] >= 0 and y_bounds[0] <= 0 and y_bounds[1] >= 0:
                origin = Point(0, 0)
            else:
                origin = Point(x_bounds[0], y_bounds[0])

        offset = (origin.x - x_bounds[0], origin.y - y_bounds[0])
        dimensions = (x_bounds[1] + 1 - x_bounds[0], y_bounds[1] + 1 - y_bounds[0])

        # else, compute offset s.t. all points + origin included
        return Grid(dimensions, origin, offset)

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
        self._header = None
        self.values = [
            [value] * self.width
            for _ in range(self.height)
        ]
        self.ready = True

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
        right = f"{' ' * (self.x_bounds[1] - last_mark - 1)}{get_char(self.x_bounds[1])}"

        line = left + inner + right

        # add origin mark
        ox = self.origin.x - self.x_bounds[0]
        if self.origin.x not in marks and self.origin.x not in self.x_bounds:
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

        if self._header is None:
            self._header = self.header_lines(margin)

        return '\n'.join(self._header + grid_lines)

    def __repr__(self):
        return f"<Grid object(({self.width},{self.height}),origin:({self.origin}),offset:({self.offset})>"

    def __iter__(self):
        """iterator of rows, which can be iterated themselves"""
        return self.values
# endregion


INFINITY = 9_999_999_999


# region === Lists & bitmask ===

def list_from_mask(the_list: list, mask: int):
    """Given a list and bitmask, return a list of only the elements represented by the bitmask

    :param list the_list: The full list to filter
    :param int mask: Bitmask representing the elements of the list to pick.
        Note: the indexes o from left to right if the bitmask is rendered out in binary, so
        a bitmask of just 1 is only the first element, and a bitmask with only the first bit set
        will have only the last element

    :return list: The filtered list
    """
    return [item for i, item in enumerate(the_list) if mask & 2 ** i]


def mask_from_list(the_list: list, elements: list):
    """Given a list and a second list that is a subset of the first, produce a bitmask of the subset

    :param list the_list: The whole list to pick from
    :param list elements: The elements for which to produce a bitmask

    :return int: The bitmask representing _elements_ from _the_list_
    """
    mask = 0
    for i, item in enumerate(the_list):
        if the_list[i] in elements:
            mask |= 2 ** i

    return mask


def partition_elements_to_mask(the_list: list):
    """Generate pairs of bitmasks for every possible partition of _the_list_ into 2 lists

    A bitmask is an integer, which, when rendered out as a binary string, indicates which elements of _the_list_
    are represented by the bitmap. e.g. if I have a botmask of 13, that's renders to binary as 1101.
    So that means the first, third and 4th elements of _the_list_ are represented by that bitmask.
    Note it's 1, 3 and 4, NOT 1, 2 and 4.  This is because binary strings are written out most-significant
    to least significant

    :param list the_list: The full list for which to partition bitmasks
    :yield tuple[int, int]: Pairs of bitmasks representing a possible partition of _the_list_
    """
    full_mask = (1 << len(the_list)) - 1  # make a full bitmask for the array
    for i in range((full_mask + 1) // 2):
        yield i, full_mask ^ i


def letter_list(n):
    return [chr(ord('a') + i) for i in range(n)]


def rotate_list(obj: list, n: int):
    """Rotate a list by _n_, returns a new list

    :param list obj: The list to be rotated
    :param int n: Number of elements to rotate by
    :return list: The rotated list
    """
    return obj[n:] + obj[:n]


def find_cycle(seq: list[int]):
    """Given a list, find a repeating pattern in it, and where it begins

    :param list[int] seq: The sequence to search

    :return tuple[int, int]: index where the cycle starts, length of the cycle
    :raise IndexError: if a cycle could not be found.
    """
    # step one: find the cycle length via backtracking
    idx, length = 0, 0
    total_len = len(seq)

    while True:
        length += 1
        window_start = total_len - length
        window = seq[window_start:]
        if window == seq[window_start - length: window_start]:
            break
        if length > total_len / 2:
            raise IndexError('No repeating cycle found')

    # step two: find the first instance of the cycle in the sequence
    while True:
        if seq[idx:idx + length] == window:
            break
        idx += 1

    # step three: walk backwards and rotate to find the true start index
    for r in range(length):
        rot = r + 1
        n_win = rotate_list(window, -rot)
        n_idx = idx - rot
        if n_win != seq[n_idx:n_idx + length]:
            break

    return idx - r, length
# endregion
