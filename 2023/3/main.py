from argparse import ArgumentParser
from utils import parse_input
from dataclasses import dataclass


@dataclass
class Element:
    string: str
    offset: int
    line: int

    @property
    def value(self):
        try:
            return int(self.string)
        except ValueError:
            return self.string

    @property
    def is_symbol(self):
        try:
            int(self.string)
            return False
        except ValueError:
            return True

    def __str__(self):
        return f"{self.string}@{self.offset}"


def parse_line(line: str, n: int):
    """Parse a line, emitting elements

    :param str line: The line of the schematic to parse
    :param int n: line number
    :yields Element: Elements found on the line
    """
    current_number = []
    for i, char in enumerate(line):
        if char.isdigit():
            current_number.append(char)
            continue

        if current_number:
            yield Element(''.join(current_number), i - len(current_number), n)
            current_number = []

        if char == '.':
            continue

        yield Element(char, i, n)


def sum_part_numbers(schematic):
    for n, line in enumerate(schematic):
        print()
        print(f"===Line {n}===")
        for element in parse_line(line, n):
            print(element)

    return 0


arg_parser = ArgumentParser('python -m 2023.3.main', description="Advent of Code 2023 Day 3")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    if argus.part == 1:
        answer = sum_part_numbers(parse_input(argus.input_path))
    else:
        answer = None

    print(f"answer:\n{answer}")
