import os
from argparse import ArgumentParser
from typing import Iterator

from utils import logger, parse_input, coordinates, DIRECTION_MAP, INFINITY
from functools import cache


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

        self.key_map: dict[str, dict[str, list[str]]] = {}
        for key in self.all_keys:
            self.key_map[key] = {}
            for next_key in self.all_keys:
                first_pos = self.key_positions[key]
                last_pos = self.key_positions[next_key]

                disp = last_pos[0] - first_pos[0], last_pos[1] - first_pos[1]
                moves = self.disp_to_moves(*disp)
                potentials = [moves, ''.join(c for c in reversed(moves))]

                good_moves = [(move + 'A') for move in potentials if self.check_moves(first_pos, move)]
                self.key_map[key][next_key] = list(set(good_moves))

        # logger.info(self.print_key_map())

    def disp_to_moves(self, y: int, x: int) -> str:
        y_mag = abs(y)
        x_mag = abs(x)

        y_move = 'v' if y > 0 else '^'
        x_move = '>' if x > 0 else '<'

        return f"{x_move * x_mag}{y_move * y_mag}"

    def print_key_map(self) -> str:
        return '\n'.join(
            f"{key}: {map}"
            for key, map in self.key_map.items()
        )

    def check_moves(self, start_pos: coordinates, moves: str) -> bool:
        """Check if this move sequence would go over a gap, and if so reverse it"""
        y, x = start_pos
        for move in moves:
            dy, dx = ARROW_MAP[move]
            y = y + dy
            x = x + dx
            if self.keys[y][x] is None:
                return False

        return True

    def find_sequences(self, code: str) -> Iterator[list[str]]:
        arm_at = self.start_Key

        for key in code:
            yield self.key_map[arm_at][key]
            arm_at = key

    def find_sequence(self, code: str) -> str:
        return f"{''.join(opts[0] for opts in self.find_sequences(code))}"


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

    @cache
    def measure_sequence(self, sequence: str, depth: int) -> int:
        if depth < 1:
            # logger.debug('bottom reached at %s, length: %d', sequence, len(sequence))
            # breakpoint()
            return len(sequence)

        accumulator = 0

        # logger.debug("measuring %s, depth %d", sequence, depth)
        for seqs in self.find_sequences(sequence):
            # breakpoint()
            shortest_len = INFINITY
            for p_seq in seqs:
                if (p_len := self.measure_sequence(p_seq, depth - 1)) < INFINITY:
                    shortest_len = p_len
            accumulator += shortest_len

        return accumulator


class Keypad:
    def __init__(self, code: str, part: int = 1):
        self.part = part

        self.code = code

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def find_sequence(self) -> str:
        sequence = self.code
        robots = [NumericRobot(), *(DirectionalRobot() for i in range(25 if self.part == 2 else 2))]
        for i, robot in enumerate(robots):
            sequence = robot.find_sequences(sequence)
            logger.info("code: %s, robot: %d, length: %d", self.code, i, len(sequence))

        return sequence

    def complexity(self, sequence_length: int) -> int:
        return sequence_length * int(self.code[:-1])

    def measure_sequence(self, num_dir_bots=2) -> int:
        n_bot = NumericRobot()
        d_bot = DirectionalRobot()
        seq_length = 0
        logger.info("measuring for %s", self.code)
        for i, n_seqs in enumerate(n_bot.find_sequences(self.code)):
            shortest = INFINITY
            for n_seq in n_seqs:
                logger.info("sequence for %s: %s", self.code[i], n_seq)
                char_length = d_bot.measure_sequence(n_seq, num_dir_bots)
                if char_length < shortest:
                    logger.info("sequence length for %s: %d", n_seq, char_length)
                    shortest = char_length

            assert shortest != INFINITY
            seq_length += shortest
        return seq_length


def sum_complexities(keypads: list[Keypad], **_: dict) -> int:
    complexity = 0
    for keypad in keypads:
        sequence = keypad.find_sequence()
        logger.info(f"{keypad.code}: {sequence} ({len(sequence)})")
        complexity += keypad.complexity(len(sequence))

    return complexity


def sum_measured_complexities(keypads: list[Keypad], dir_bots: int) -> int:
    complexity = 0
    for keypad in keypads:
        length = keypad.measure_sequence(dir_bots)
        logger.info(f"{keypad.code}: {length}")
        complexity += keypad.complexity(length)

    return complexity

# region === reddit tutorial ===


dir_bot = DirectionalRobot()
num_bot = NumericRobot()


"""
buildSeq(keys, index, prevKey, currPath, result):
    if index is the length of keys:
        add the current path to the result
        return
    foreach path in the keypad graph from prevKey to the currKey:
        buildSeq(keys, index+1, keys[index], currPath + path + 'A', result)
"""


def build_seq(
    keys: str, index: int = 0, prev_key: str = 'A', curr_path: str = '', result: set[str] | None = None
) -> set[str]:
    if result is None:
        result = set()

    # logger.info("keys: %s, i: %d, prev: %s, curr_path: %s, res: %s", keys, index, prev_key, curr_path, result)
    if index == len(keys):
        # logger.info("build base case: keys: %s, result: %s, curr_path: %s", keys, result, curr_path)
        result.add(curr_path)
        return result

    key_map = dir_bot.key_map
    if keys[0] in NUM_KEYS:
        key_map = num_bot.key_map

    for path in key_map[prev_key][keys[index]]:
        # logger.info(path)
        result.update(build_seq(keys, index + 1, keys[index], curr_path + path, result))

    return result


# logger.warning(build_seq('vA', 0, 'A', ''))
# exit()

"""
shortestSeq(keys, depth, cache):
    if depth is 0:
        return the length of keys
    if keys, depth in the cache:
        return that value in cache
    split the keys into subKeys at 'A'
    foreach subKey in the subKeys list:
        build the sequence list for the subKey (buildSeq)
        for each sequence in the list:
            find the minimum of shortestSeq(sequence, depth-1, cache)
        add the minimum to the total
    set the total at keys, depth in the cache
    return total
"""


@cache
def shortest_seq(keys: str, depth: int) -> int:
    # logger.info("finding shortest for %s (at depth %d)", keys, depth)
    if depth < 1:
        # breakpoint()
        return len(keys)

    total = 0
    for subkey in keys[:-1].split('A'):
        subkey = subkey + 'A'
        shortest = INFINITY
        for seq in build_seq(subkey):
            if (length := shortest_seq(seq, depth - 1)) < shortest:
                shortest = length

        logger.info("shortest for %s from %s at depth %d: %d", subkey, keys, depth, shortest)
        # breakpoint()
        total += shortest

    return total


"""
solve(inputList, maxDepth):
    create the numpad graph
    create the dirpad graph
    foreach keys in the inputList:
        build the sequence list for the numpad keys
        for each sequence in the list:
            find the minimum of lowestSeq(sequence, maxDepth, cache)
        add to the total multiplied by num part of keys
    return total
"""


def solve(input_list: list[str], max_depth: int) -> int:
    total = 0
    for input in input_list:
        length = shortest_seq(input, max_depth)
        comp = length * int(input[:-1])
        logger.info("for %s, length: %s, complexity: %s", input, length, comp)
        # breakpoint()
        total += comp

    return total

# endregion


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
    lines = list(parse_input(argus.input_path))
    keypads = [Keypad(line, part=argus.part) for line in lines]
    dir_bots = 25 if argus.part == 2 else 2
    match argus.part:
        case -1:
            answer = '\n'.join(keypad.code for keypad in keypads)
        case _:
            # answer = solve(lines, dir_bots + 1)
            answer = sum_measured_complexities(keypads, dir_bots)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
