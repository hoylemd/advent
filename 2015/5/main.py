from argparse import ArgumentParser

from utils import parse_input


def is_nice(string: str):
    naughty_strings = ['ab', 'cd', 'pq', 'xy']

    vowels = 0
    dupe = False
    prev = None
    for c in string:
        if c in 'aeiou': vowels += 1
        if prev:
            if prev + c in naughty_strings: return False
            if prev == c: dupe = True

        prev = c

    return vowels > 2 and dupe


def is_nice2(string: str):
    dupe = False
    repeat = False
    for i, c in enumerate(string):
        if i < 1: continue
        if not dupe and string[i - 1] + c in string[i + 1:]:
            dupe = True
        if i > 2 and not repeat and string[i - 2] == c:
            repeat = True

        if dupe and repeat: return True

    return False


def count_nice(rulebook, strings):
    nice = 0
    for string in strings:
        if rulebook(string):
            nice += 1

    return nice


arg_parser = ArgumentParser('python -m 2015.5.main', description="Advent of Code 2015 Day 5")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    input_path = argus.input_path
    if 'test' in input_path:
        input_path = f"{input_path[:-4]}{argus.part}{input_path[-4:]}"

    if argus.part == 1:
        rules = is_nice
    else:
        rules = is_nice2

    answer = count_nice(rules, parse_input(input_path))

    print(f"answer:\n{answer}")
