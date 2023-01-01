from argparse import ArgumentParser
from utils import logger, parse_input
from dataclasses import dataclass


@dataclass
class Box:
    length: int
    width: int
    height: int

    @classmethod
    def parse(cls, line: str):
        length, width, height = line.split('x')
        return Box(int(length), int(width), int(height))

    def render(self):
        return f"{self.length}x{self.width}x{self.height}"

    # region Surface area calculations
    @property
    def front_area(self):
        return self.height * self.width

    @property
    def side_area(self):
        return self.height * self.length

    @property
    def top_area(self):
        return self.length * self.width

    @property
    def surface_area(self):
        return 2 * self.front_area + 2 * self.side_area + 2 * self.top_area
    # endregion

    # region Perimeter calculations
    @property
    def front_perimeter(self):
        return 2 * self.height + 2 * self.width

    @property
    def side_perimeter(self):
        return 2 * self.height + 2 * self.length

    @property
    def top_perimeter(self):
        return 2 * self.length + 2 * self.width
    # endregion

    @property
    def volume(self):
        return self.length * self.width * self.height

    @property
    def required_paper(self):
        # calculate 'extra paper'
        extra = min([self.front_area, self.side_area, self.top_area])

        return self.surface_area + extra

    @property
    def required_ribbon(self):
        return min([self.front_perimeter, self.side_perimeter, self.top_perimeter]) + self.volume


class PresentPile:
    def __init__(self, lines, part):
        self.part = part
        self.boxes = self.parse(lines)

    def __str__(self):
        return f"Present Pile of {len(self.boxes)} presents"

    def parse(self, lines):
        return [Box.parse(line) for line in lines]

    def required_paper(self):
        return sum(box.required_paper for box in self.boxes)

    def required_ribbon(self):
        return sum(box.required_ribbon for box in self.boxes)


arg_parser = ArgumentParser('python -m 2015.2.main', description="Advent of Code 2015 Day 2")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    pile = PresentPile(parse_input(argus.input_path), argus.part)

    logger.info(pile)
    logger.debug('')

    if argus.part == 1:
        print(f"answer:\n{pile.required_paper()}")
    else:
        print(f"answer:\n{pile.required_ribbon()}")
