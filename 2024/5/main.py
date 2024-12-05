from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


def parse_line(line: str):
    return line.split()


class Rulebook:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.elements = (parse_line(line) for line in lines)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"


def answer2(rulebook: Rulebook) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def sum_middle_ordered_pages(rulebook: Rulebook) -> int:
    accumulator = 0

    # solve part 1

    return accumulator


def separate_rules_and_updates(lines: list[str]) -> tuple[list[str], list[str]]:
    separator_index = lines.index('')
    return lines[:separator_index], lines[separator_index + 1:]


arg_parser = ArgumentParser('python -m 2024.5.main', description="Advent of Code 2024 Day 5")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)

    rule_lines, update_lines = separate_rules_and_updates([line for line in lines])

    rulebook = Rulebook(rule_lines, part=argus.part)

    print('\n'.join(rule_lines))
    print()
    print('\n'.join(update_lines))
    if argus.part == 1:
        answer = sum_middle_ordered_pages(rulebook)
    else:
        answer = answer2(rulebook)

    logger.debug('')

    print(f"answer:\n{answer}")
