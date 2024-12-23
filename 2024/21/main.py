import os
from argparse import ArgumentParser

from utils import logger, parse_input


class Keypad:

    def __init__(self, code: str, part: int = 1):
        self.part = part

        self.code = code

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def find_sequence(self) -> str:
        self.sequence = self.code
        return self.sequence

    def complexity(self) -> int:
        return len(self.sequence) * int(self.code[:-1])


def answer2(keypads: list[Keypad], **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def sum_complexities(keypads: list[Keypad], **_: dict) -> int:
    for keypad in keypads:
        keypad.find_sequence()

    return sum(keypad.complexity() for keypad in keypads)


INPUT_PARAMS = {
    ('test.txt'): {
    },
    ('input.txt'): {
    }
}


arg_parser = ArgumentParser('python -m 2024.21.main', description="Advent of Code 2024 Day 21")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    params = INPUT_PARAMS[os.path.basename(argus.input_path)]
    keypads = [Keypad(line, part=argus.part) for line in parse_input(argus.path)]
    match argus.part:
        case -1:
            answer = '\n'.join(keypad.code for keypad in keypads)
        case 1:
            answer = sum_complexities(keypads, **params)
        case 2:
            answer = answer2(keypads, **params)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
