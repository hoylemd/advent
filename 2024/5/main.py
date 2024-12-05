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

    def find_error(self, update: list[int]) -> tuple[int, int]:
        """returns (index of ooo element, violated antecedent) or (-1, -1) if in correct order"""
        seen = set()
        for i, page in enumerate(update):
            seen.add(page)
            if page not in self.rules:
                continue

            for antecedent in self.rules[page]:
                if antecedent in seen:
                    logger.debug(f"page {page} printing after {antecedent}!")
                    return i, antecedent

        logger.debug(f"update {update} is good!")
        return -1, -1

    def check_update(self, update: list[int]) -> bool:
        return True if self.find_error(update) == (-1, -1) else False

    def enforce_update(self, update: list[int]) -> tuple[list[int], bool]:
        """returns the fixed(?) update, and whether it was fixed or not"""
        if (result := self.find_error(update)) == (-1, -1):
            return update, False

        ooo_index, ooo_antecedent = result
        ooo_element = update[ooo_index]

        removed = update[:ooo_index] + update[ooo_index + 1:]
        oooa_index = removed.index(ooo_antecedent)
        spliced = removed[:oooa_index] + [ooo_element] + removed[oooa_index:]

        double_checked, _ = self.enforce_update(spliced)
        logger.debug(f"{update=} enforced to {double_checked=}{'' if double_checked == spliced else f"from {spliced=}"}")

        return double_checked, True


def sum_middle_fixed_pages(rulebook: Rulebook, updated: Iterator[list[int]]) -> int:
    accumulator = 0

    for update in updates:
        enforced, was_enforced = rulebook.enforce_update(update)
        if was_enforced:
            accumulator += enforced[len(enforced) // 2]

    return accumulator


def sum_middle_ordered_pages(rulebook: Rulebook, updates: Iterator[list[int]]) -> int:
    accumulator = 0

    for update in updates:
        if rulebook.check_update(update):
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
    updates = (parse_update(line) for line in update_lines)

    if argus.part == 1:
        answer = sum_middle_ordered_pages(rulebook, updates)
    else:
        answer = sum_middle_fixed_pages(rulebook, updates)

    logger.debug('')

    print(f"answer:\n{answer}")
