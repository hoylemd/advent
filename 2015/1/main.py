from argparse import ArgumentParser
from utils import parse_input


def elevate(commands: str, stop_at=None):
    floor = 0
    for i, command in enumerate(commands):
        if command == '(':
            floor += 1
        else:
            floor -= 1

        if stop_at is None:
            continue

        if floor < stop_at:
            break

    return i, floor


def when_basement(commands: str):
    return elevate(commands, 0)


arg_parser = ArgumentParser('python -m {{year}}.{{day}}.main', description="Advent of Code {{ year }} Day {{ day }}")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    input_path = argus.input_path
    if 'test' in input_path:
        input_path = f"{input_path[:-4]}{argus.part}{input_path[-4:]}"

    input = ''.join(line for line in parse_input(input_path))

    if argus.part == 1:
        _, answer = elevate(input)
    else:
        answer, _ = when_basement(input)

    print(f"answer: {answer + 1}")
