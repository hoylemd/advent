import os
from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input


def parse_range(range: str) -> tuple[str, str]:
    parts = range.split('-')
    return (parts[0], parts[1])


def parse_ranges(line, part=1):
    range_specs = line.split(',')
    return (parse_range(spec) for spec in range_specs)


def esrap_range(range: tuple[str, str]) -> str:
    return f"{range[0]}-{range[1]}"


def esrap_ranges(ranges):
    return ','.join(esrap_range(range) for range in ranges)


def get_ticker(id_sample: str) -> int:
    assert len(id_sample) % 2 == 0, "Cannot get ticker for odd-length number"
    half = len(id_sample) // 2

    return int(f"1{'0' * (half - 1)}1")


def first_half(id_sample: str) -> str:
    assert len(id_sample) % 2 == 0, "Cannot first half for odd-length number"
    return id_sample[:len(id_sample) // 2]


def is_repeat(number: str):
    if len(number) % 2:
        return False  # even = cant be repeat

    first_half = number[:len(number) // 2]

    return first_half * 2 == number


def adjust_range(first: str, last: str) -> tuple[str, str]:
    lower_bound = first
    if len(first) % 2:
        part_len = len(first) // 2
        # it's odd, so round up to first repeat of length
        lower_bound = f"1{'0' * part_len}" * 2

    assert len(lower_bound) % 2 == 0, "Lower bound is not even after adjustment?"

    # adjust lbound to next repeat
    lower_bound = first_half(lower_bound) * 2
    if (int(lower_bound) < int(first)):
        lower_bound = f"{(int(first_half(lower_bound)) + 1)}" * 2

    assert is_repeat(lower_bound), "Lower bound is not a repeat after adjustment?"
    assert int(lower_bound) >= int(first), "Lower bound is less than original first?"

    upper_bound = last
    if len(last) % 2:
        part_len = len(last) // 2
        # it's odd so round down to last repeat of length
        upper_bound = f"{'9' * part_len}" * 2

    assert len(upper_bound) % 2 == 0, "Upper bound is not even after adjustment?"

    # adjust ubound to previous repeat
    upper_bound = first_half(upper_bound) * 2
    if (int(upper_bound) > int(last)):
        upper_bound = f"{(int(first_half(upper_bound)) - 1)}" * 2

    assert is_repeat(lower_bound), "Upper bound is not a repeat after adjustment?"
    assert int(upper_bound) <= int(last), "Upper bound is greater than original last?"

    return lower_bound, upper_bound


def get_invalid_ids(first: str, last: str) -> list[int]:
    invalids = []

    lbound, ubound = adjust_range(first, last)
    ticker = get_ticker(lbound)

    if len(lbound) > len(ubound):
        return []  # whole range must be valid

    logger.debug(f"{first, last} -> {lbound}, {ubound}: {ticker=}")

    return invalids


def answer2(ranges: Iterator[tuple[str, str]], **_: dict) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def answer1(ranges: Iterator[tuple[str, str]], **_: dict) -> int:
    accumulator = 0

    # solve part 1
    for range in ranges:
        invalid_ids = get_invalid_ids(*range)
        logger.info(f"{esrap_range(range)} has {len(invalid_ids)} invalid ids, {invalid_ids}")

        accumulator += sum(invalid_ids)

    return accumulator


INPUT_PARAMS = {
    ('test.txt'): {
    },
    ('input.txt'): {
    }
}


arg_parser = ArgumentParser('python -m 2025.2.main', description="Advent of Code 2025 Day 2")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    params = INPUT_PARAMS[os.path.basename(argus.input_path)]
    lines = parse_input(argus.input_path)
    ranges = parse_ranges([line for line in lines][0], part=argus.part)
    match argus.part:
        case -1:
            answer = esrap_ranges(ranges)
        case 1:
            answer = answer1(ranges, **params)
        case 2:
            answer = answer2(ranges, **params)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
