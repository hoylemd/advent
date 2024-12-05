from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


def parse_rule(line: str) -> tuple[int, int]:
    precedent, antecedent = line.split('|')
    return int(precedent), int(antecedent)


def parse_update(line: str) -> list[int]:
    return [int(u) for u in line.split(',')]


class Rulebook:

    def __init__(self, lines: list[str], part: int = 1):
        self.part = part
        self.rules = {}

        for line in lines:
            precedent, antecedent = parse_rule(line)
            extant_deps = self.rules.get(precedent, [])
            self.rules[precedent] = extant_deps + [antecedent]

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def check_update(self, update: list[int]) -> bool:
        seen = set()
        for page in update:
            seen.add(page)
            if page not in self.rules:
                continue

            for antecedent in self.rules[page]:
                if antecedent in seen:
                    print(f"page {page} printing after {antecedent}!")
                    return False

        return True


def answer2(rulebook: Rulebook) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def sum_middle_ordered_pages(rulebook: Rulebook, updates: Iterator[list[int]]) -> int:
    accumulator = 0

    for update in updates:
        if rulebook.check_update(update):
            print(f"update {update} is good!")
            accumulator += update[len(update) // 2]

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

    if argus.part == 1:
        answer = sum_middle_ordered_pages(rulebook, (parse_update(line) for line in update_lines))
    else:
        answer = answer2(rulebook)

    logger.debug('')

    print(f"answer:\n{answer}")
