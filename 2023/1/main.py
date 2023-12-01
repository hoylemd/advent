from argparse import ArgumentParser
from utils import logger, parse_input


class Thing:
    def __init__(self, *args: tuple, part=1, **kwargs: dict):
        self.args = args
        self.kwargs = kwargs
        self.part = part

    @classmethod
    def parse_line(cls, line):
        return (word for word in line.split())

    @classmethod
    def parse(cls, lines, line_parser=None, part=1):
        line_parser = line_parser or cls.parse_line
        return cls(
            (line_parser(line) for line in lines),
            part=part)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def answer(self, *args, **kwargs):
        return 0


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
