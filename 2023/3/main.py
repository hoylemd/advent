from argparse import ArgumentParser
from utils import parse_input
from math import prod


def chunk_has_symbol(line: str, lbound: int, rbound: int):
    print(f"{lbound}:{rbound}: {line[lbound:rbound]}")
    for c in line[lbound:rbound]:
        if c == '.' or c.isdigit():
            continue
        return True
    return False


def has_adjacent_symbols(num_chars: list, schematic: list, y: int, x: int):
    lbound = max(x - (len(num_chars) + 1), 0)
    rbound = min(x + 1, len(schematic[0]))

    print()
    print(f"checking for [{schematic[y][lbound:rbound]}]")

    # check previous line
    if y > 0 and chunk_has_symbol(schematic[y - 1], lbound, rbound):
        return True

    # check current line
    if chunk_has_symbol(schematic[y], lbound, rbound):
        return True

    # check next line
    if y + 1 < len(schematic) and chunk_has_symbol(schematic[y + 1], lbound, rbound):
        return True

    # nope
    return False


def sum_part_numbers(schematic: list):
    accumulator = 0
    for y, line in enumerate(schematic):
        num_buffer = []
        for x, char in enumerate(line):
            if char.isdigit():
                num_buffer.append(char)
                continue

            if num_buffer:
                print(f"found number: {''.join(num_buffer)}")
            if num_buffer and has_adjacent_symbols(num_buffer, schematic, y, x):
                accumulator += int(''.join(num_buffer))
                print(f"Is part number! so far: {accumulator}")

            num_buffer = []

        # handle right-aligned number
        if num_buffer:
            print(f"found number (right): {''.join(num_buffer)}")
        if num_buffer and has_adjacent_symbols(num_buffer, schematic, y, x + 1):  # x + 1 accommodate right edge
            accumulator += int(''.join(num_buffer))
            print(f"Is part number! so far: {accumulator}")

    return accumulator


def get_num_at(schematic: list, x: int, y: int):
    if x < 0 or x >= len(schematic[y]) or not schematic[y][x].isdigit():
        return None

    # parse backward to find start
    start = x
    while start - 1 >= 0 and schematic[y][start - 1].isdigit():
        start -= 1

    end = x
    while end + 1 < len(schematic[y]) and schematic[y][end + 1].isdigit():
        end += 1

    return int(schematic[y][start:end + 1])


def get_nums_around(schematic: list, x: int, y:int):
    found_numbers = set()
    for target in [x - 1, x, x + 1]:
        if (candidate := get_num_at(schematic, target, y)) is None:
            continue
        found_numbers.add(candidate)
    return found_numbers


def gear_ratio(schematic: list, x: int, y: int):
    found_numbers = set()
    # check previous line
    if y > 0:
        found_numbers.update(get_nums_around(schematic, x, y - 1))

    # check current line
    found_numbers.update(get_nums_around(schematic, x, y))

    # check next line
    if y + 1 < len(schematic):
        found_numbers.update(get_nums_around(schematic, x, y + 1))

    if len(found_numbers) == 2:
        print(f"gear found: {found_numbers}")
        return prod(found_numbers)

    print(f"not a gear: {found_numbers}")
    return 0


def sum_gear_ratios(schematic):
    accumulator = 0

    for y, line in enumerate(schematic):
        for x, char in enumerate(line):
            if char == '*':
                print(f"potential gear found at {x},{y}")
                accumulator += gear_ratio(schematic, x, y)

    return accumulator


arg_parser = ArgumentParser('python -m 2023.3.main', description="Advent of Code 2023 Day 3")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    schematic = [line for line in parse_input(argus.input_path)]
    if argus.part == 1:
        answer = sum_part_numbers(schematic)
    else:
        answer = sum_gear_ratios(schematic)

    print(f"answer:\n{answer}")
