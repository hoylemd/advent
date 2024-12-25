import os
from argparse import ArgumentParser

from utils import logger, parse_input, coordinates, DIRECTION_MAP


def disp_to_moves(y: int, x: int) -> str:
    y_mag = abs(y)
    x_mag = abs(x)

    y_move = 'v' if y > 0 else '^'
    x_move = '>' if x > 0 else '<'

    return f"{x_move * x_mag}{y_move * y_mag}"


class KeypadRobot:
    def __init__(self, keys: list[list[str | None]], start_key: str = 'A'):
        self.start_Key = start_key
        self.keys = keys
        self.all_keys = ''.join(
            ''.join(key for key in row if key is not None)
            for row in self.keys
        )

        self.key_positions = {}
        for y, row in enumerate(self.keys):
            for x, key in enumerate(row):
                self.key_positions[key] = (y, x)

        self.key_map = {}
        for key in self.all_keys:
            self.key_map[key] = {}
            for next_key in self.all_keys:
                first_pos = self.key_positions[key]
                last_pos = self.key_positions[next_key]

                disp = last_pos[0] - first_pos[0], last_pos[1] - first_pos[1]
                moves = disp_to_moves(*disp)

                self.key_map[key][next_key] = self.check_moves(first_pos, moves) + 'A'

        # logger.info(self.print_key_map())

    def print_key_map(self) -> str:
        return '\n'.join(
            f"{key}: {map}"
            for key, map in self.key_map.items()
        )

    def check_moves(self, start_pos: coordinates, moves: str):
        """Check if this move sequence would go over a gap, and if so reverse it"""
        y, x = start_pos
        for move in moves:
            dy, dx = ARROW_MAP[move]
            y = y + dy
            x = x + dx
            if self.keys[y][x] is None:
                return ''.join(c for c in reversed(moves))

        return moves

    def find_sequence(self, code: str) -> str:
        arm_at = self.start_Key

        subseqs = []

        for key in code:
            subseqs.append(self.key_map[arm_at][key])
            arm_at = key

        return f"{''.join(subseqs)}"


NUM_PAD = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
]
NUM_KEYS = ''.join(''.join(k for k in row if k is not None) for row in NUM_PAD)


class NumericRobot(KeypadRobot):
    def __init__(self):
        super().__init__(NUM_PAD)
        assert self.all_keys == NUM_KEYS


DIR_PAD = [
    [None, '^', 'A'],
    ['<', 'v', '>']
]
DIR_KEYS = '^A<v>'


ARROW_MAP = {arrow: DIRECTION_MAP[arrow] for arrow in '^<v>'}
MOVE_MAP = {DIRECTION_MAP[arrow]: arrow for arrow in '^<v>'}


class DirectionalRobot(KeypadRobot):
    def __init__(self):
        super().__init__(DIR_PAD)
        assert self.all_keys == DIR_KEYS


class Keypad:
    def __init__(self, code: str, part: int = 1):
        self.part = part

        self.code = code

        self.robots = [NumericRobot(), DirectionalRobot(), DirectionalRobot()]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def find_sequence(self) -> str:
        sequence = self.code
        for robot in self.robots:
            sequence = robot.find_sequence(sequence)

        return sequence

    def complexity(self, sequence: str) -> int:
        return len(sequence) * int(self.code[:-1])


def sum_complexities(keypads: list[Keypad], **_: dict) -> int:
    complexity = 0
    for keypad in keypads:
        sequence = keypad.find_sequence()
        logger.info(f"{keypad.code}: {sequence} ({len(sequence)})")
        complexity += keypad.complexity(sequence)

    return complexity


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
    keypads = [Keypad(line, part=argus.part) for line in parse_input(argus.input_path)]
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
