from argparse import ArgumentParser
from typing import Iterator, Mapping
from collections import defaultdict

from utils import logger, parse_input, CharGrid, coordinates, INFINITY

type stripe = tuple[str, int, int] # crop, offset, length


def stripes_overlap(first: stripe, second: stripe) -> bool:
    return calc_overlap(first, second) > 0

def calc_overlap(first: stripe, second: stripe) -> int:
    if first[1] > second[1]:
        first, second = second, first

    return first[1] + first[2] - second[1]




class Region:
    def __init__(self, first_y: int, first_stripe: stripe):
        self.crop = first_stripe[0]
        """
        self.y = first_y
        self.x = first_stripe[1]
        self.height = 1
        self.width = first_stripe[2]
        """
        self.stripes = defaultdict(list[stripe])

        self.add_stripe(first_y, first_stripe)

    def _add_stripe(self, y: int, next_stripe: stripe):
        c, x, l = next_stripe

        if c != self.crop:
            raise ValueError('Cannot add stripe of different crop')

        """
        if (delta_y := y - self.y) < 0:
            self.y = y
            self.height += delta_y

        if (delta_x := x - self.x) < 0:
            self.x
        """
        current_row = self.stripes[y]
        current_row.append(next_stripe)

        self.stripes[y] = sorted(current_row, key=lambda s: s[1])

    def add_stripe(self, y: int, next_stripe: stripe):
        self._add_stripe(y, next_stripe)
        self.compute_bounds()

    def add_stripes(self, stripes: Mapping[int, list[stripe]]):
        for y, y_stripes in stripes.items():
            for s in y_stripes:
                self._add_stripe(y, s)

        self.compute_bounds()

    def compute_bounds(self):
        ys = sorted(self.stripes.keys())

        self.y = ys[0]
        self.height = len(ys)

        self.x = INFINITY
        right = 0
        for y in ys:
            for s in self.stripes[y]:
                s_right = s[1] + s[2]

                if self.x is None:
                    self.x = s[1]

                if s[1] < self.x:
                    # if new stripe offset is to the left
                    self.x = s[1]

                if s_right > right:
                    # if new right is to the right
                    right = s_right

        self.width = right - self.x

    def can_merge(self, other_y: int, other: stripe) -> bool:
        if other[0] != self.crop:
            # wrong crop
            return False

        for b_stripe in self.stripes[other_y -1]:
            if stripes_overlap(b_stripe, other):
                return True

        return False

    def __str__(self) -> str:
        return f"Region of {self.crop} from {self.y}, {self.x} to {self.y + self.height - 1}, {self.x + self.width - 1}"

    def __repr__(self) -> str:
        return f"{self}"

    def render_row(self, y: int, full_width: int) -> str:
        buffer = ''
        return buffer


    def render(self, full_height: int, full_width: int) -> str:
        return '\n'.join(
            self.render_row(y, full_width)
            for y in range(full_height)
        )

    def price(self) -> int:
        area = 0
        perimeter = sum(s[2] for s in self.stripes[self.y]) # top edge
        prev_row = []

        for y, stripes in self.stripes.items():
            perimeter += 2 * len(stripes) # sides
            # top edge(s)
            for p_r_stripe in self.stripes[y - 1]:

        return area * perimeter




class GardenMap(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.rows = list(self.parse_lines(lines))

        self.regions = self.merge_regions()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_line(self, y: int, line: str) -> Iterator[stripe]:
        current_crop = ''
        current_offset = 0

        for i, c in enumerate(line):
            if c != current_crop:
                # new stripe
                if current_crop:
                    yield (current_crop, current_offset, i - current_offset)

                current_offset = i
                current_crop = c

        yield (current_crop, current_offset, i - current_offset + 1)


    def parse_lines(self, lines: Iterator[str]) -> Iterator[list[stripe]]:
        for y, line in enumerate(lines):
            yield list(self.parse_line(y, line))

    def esrap_line(self, y: int, row: list[stripe]) -> str:
        return ''.join(f"{c * l}" for c, _, l in row)

    def esrap_lines(self) -> str:
        return '\n'.join(
            self.esrap_line(y, r) for y, r in enumerate(self.rows)
        )

    def print_stripes(self) -> str:
        return '\n'.join(f"{row}" for row in self.rows)

    def merge_regions(self) -> list[Region]:
        all_regions: list[Region] = []
        prev_row_regions: list[Region] = []
        this_row_regions: list[Region] = []
        for y, row in enumerate(self.rows):
            for i, stripe in enumerate(row):
                this_region = None
                for region in prev_row_regions:

                    # if stripe[0] == 'V' and y == 5:
                    #     breakpoint()

                    if region.can_merge(y, stripe):
                        if this_region is None:
                            this_region = region
                            region.add_stripe(y, stripe)
                        else:
                            this_region.add_stripes(region.stripes)
                            all_regions.remove(region)

                if this_region is None:
                    this_region = Region(y, stripe)
                    all_regions.append(this_region)

                if this_region not in this_row_regions:
                    this_row_regions.append(this_region)

            prev_row_regions = this_row_regions
            this_row_regions = []

        return all_regions

def answer2(garden: GardenMap) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(garden: GardenMap) -> int:
    accumulator = 0

    logger.info(garden.print_stripes())
    breakpoint()
    # solve part 1

    return accumulator


arg_parser = ArgumentParser('python -m 2024.12.main', description="Advent of Code 2024 Day 12")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    garden = GardenMap(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = garden.esrap_lines()
        case 1:
            answer = answer1(garden)
        case 2:
            answer = answer2(garden)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
