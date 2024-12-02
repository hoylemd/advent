from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator
from dataclasses import dataclass


def count_arrangements(state: str, groups: list[int]) -> int:
    if not (groups and state):
        logger.info(f"null case: {state}, {groups}")
        return 0  # no more groups to assign

    logger.info(f"checking for groups {groups} in {state}")
    arrangements = 1
    i = 0
    for g_n, group_size in enumerate(groups):
        if group_size > len(state[i:]):
            logger.info(f"group {group_size} cannot fit into {state[i:]}, aborting")
            return 0

        group = group_size
        logger.info(f"looking at {group} from {state[i:]} onwards...")
        # advance past ok springs
        while state[i] == '.':
            i += 1

        # advance past known broken
        while i < len(state) and state[i] == '#':
            i += 1
            group -= 1

        if group < group_size:
            logger.info(f"Group {group_size} must end at {i}")
            # we know the next group must be here, so advance past it
            # only one possibility for this group so dont change counter
            i += group + 1
            next

        # count the possibilities if next group starts here (i + j loop)
        while state[i] == '?':
            new_possibilities = count_arrangements(state[i:], groups[g_n:])
            arrangements += new_possibilities
            i += 1

        # if group could start at i + 1, try that (loop until it can't)
        # count the possibilities if next group starts at i + 1

    return arrangements


@dataclass
class InvalidState(Exception):
    """A state was checked that can't exist"""

    state: str
    groups: list[int]


def get_arrangements(state: str, groups: list[int], prefix: str = '') -> set[str]:
    states = set()
    prog_ind = f"<{prefix}|{state}>"

    if not (groups and state):
        logger.info(f"null case: {prog_ind}, {groups}")
        return states  # no more groups to assign
    elif not groups:
        # no more groups, but state remains:
        if '#' in state:
            # impossible - no groups remain, but there are known # left
            logger.error(f"invalid state: {prog_ind}, {groups}")
            raise InvalidState(state, groups)
        if '?' in state:
            # all remaining must be .
            logger.info(f"remaining ? in {prog_ind} must be .")
            states.add(f"{prefix}{state.replace('?', '.')}")
            return states

    current_group = None
    i = 0

    logger.info(f"checking for groups {groups} in {prog_ind}")

    while i < len(state):
        c = state[i]
        if c == '.':
            prefix += ''
        elif c == '#':
            current_group = groups[0]
            if '.' in state[i:current_group]:
                # current group can't be here
                logger.error(f"invalid state: <{prefix}|{state[i:]}>, {groups}")
                raise InvalidState(state, groups)

            logger.info(f"advancing past group of length {current_group}")
            prefix += ('#' * current_group) + '.'
            i += current_group
            groups = groups[1:]
        else:
            # it's ?

            try:
                states = states.union(get_arrangements('#' + state[i + 1:], groups, prefix))
            except InvalidState:
                logger.info('skip invalid state')

            try:
                states = states.union(get_arrangements('.' + state[i + 1:], groups, prefix))
            except InvalidState:
                logger.info('skip invalid state')

            return states

        i += 1

    states.add(prefix)

    logger.info('all done')
    return states


def parse_line(line: str):
    springs, damaged_spec = line.split()
    return springs, [int(group) for group in damaged_spec.split(',')]


class SpringRecord:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.rows = (parse_line(line) for line in lines)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def count_possible_arrangements(self) -> int:
        accumulator = 0
        for row in self.rows:
            arrs = get_arrangements(*row)
            ways = len(arrs)
            logger.info(f"{ways} ways for {row[0]}")
            breakpoint()
            accumulator += ways

        return accumulator


arg_parser = ArgumentParser('python -m 2023.12.main', description="Advent of Code 2023 Day 12")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    record = SpringRecord(lines)
    if argus.part == 1:
        answer = record.count_possible_arrangements()
    else:
        answer = 0

    logger.debug('')

    print(f"answer:\n{answer}")
