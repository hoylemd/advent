from argparse import ArgumentParser
from utils import logger, parse_input


def getInt(string: str):
    try:
        return int(string)
    except ValueError:  # invalid literal for int
        return None


class Thing:
    def __init__(self, numbers, part=1):
        self.numbers = numbers
        self.part = part

    @classmethod
    def parse_line(cls, line, part=1):
        """extract the first and last digits, combine them into a new number"""
        li, ri = 0, -1
        lval, rval = None, None

        while (lval := getInt(line[li])) is None:
            li += 1

        while (rval := getInt(line[ri])) is None:
            ri -= 1

        return 10 * lval + rval

    @classmethod
    def parse(cls, lines, line_parser=None, part=1):
        line_parser = line_parser or cls.parse_line
        return cls(
            (line_parser(line, part) for line in lines),
            part=part)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def answer(self, *args, **kwargs):
        return sum(self.numbers)


arg_parser = ArgumentParser('python -m 2023.1.main', description="Advent of Code 2023 Day 1")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    thing = Thing.parse(parse_input(argus.input_path), part=argus.part)

    logger.info(str(thing))
    logger.debug('')

    answer = thing.answer(argus.part)
    print(f"answer:\n{answer}")
