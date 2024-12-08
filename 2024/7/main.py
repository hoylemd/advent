from argparse import ArgumentParser
from typing import Iterator, Callable, Generator, Any
from itertools import product

from utils import logger, parse_input


def parse_line(line: str) -> tuple[int, list[int]]:
    test_value, operands_s = line.split(': ')
    operands = [int(o) for o in operands_s.split(' ')]
    return int(test_value), operands


def esrap_line(test_value: int, operands: list[int]) -> str:
    return f"{test_value}: {' '.join(str(o) for o in operands)}"


type ops_list = tuple[str, ...]
type ops_genny = Generator[ops_list, Any, Any]


def op_plus(left: int, right: int) -> int:
    return left + right


def op_times(left: int, right: int) -> int:
    return left * right


def op_cat(left: int, right: int) -> int:
    return int(f"{left}{right}")


OPERATIONS = {
    '+': op_plus,
    '*': op_times,
    '||': op_cat
}


class Equation:

    def __init__(self, test_value: int, operands: list[int], valid_ops):
        self.test_value = test_value
        self.operands = operands
        self.valid_ops = valid_ops
        self.num_ops = len(operands) - 1
        self.num_tried = 0

    def validate_operators(self, operators: ops_list):
        if len(operators) != (self.num_ops):
            raise ValueError(f"incorrect # of operators (exp: {self.num_ops}, got {len(operators)})")

    def enumerate_ops(self, operators: ops_list) -> Iterator[tuple[int, tuple[str, int]]]:
        for i, op in enumerate(operators):
            yield i, (op, self.operands[i + 1])

    def compute(self, operators: ops_list) -> int:
        self.validate_operators(operators)

        accumulator = self.operands[0]
        for i, (op, operand) in self.enumerate_ops(operators):
            accumulator = OPERATIONS[op](accumulator, operand)

        return accumulator

    def __str__(self) -> str:
        return f"{self.test_value}: {self.operands} ({self.num_ops} ops, combos: {self.n_combos()})"

    def print_with_ops(self, ops: ops_list) -> str:
        parts = [f"{self.test_value}: {self.operands[0]}"
                 ] + [f" {op} {operand}" for _, (op, operand) in self.enumerate_ops(ops)]

        return ''.join(parts)

    def esrap(self) -> tuple[int, list[int]]:
        return (self.test_value, self.operands)

    def n_combos(self) -> int:
        return len(self.valid_ops)**self.num_ops

    def calibrate(self, tryer: ops_genny) -> ops_list | None:
        for try_ops in tryer:
            self.num_tried += 1
            logger.info(f"  Trying {self.print_with_ops(try_ops)}")
            test_val = self.compute(try_ops)
            logger.info(f"    result: {test_val} =? {self.test_value}")
            if test_val == self.test_value:
                return try_ops

        return None

    def op_combos(self) -> ops_genny:
        for combo in product(self.valid_ops, repeat=self.num_ops):
            yield combo


class Calibrator:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        valid_ops = ['+', '*']
        if self.part > 1:
            valid_ops.append('||')

        self.equations = [Equation(*parse_line(line), valid_ops) for line in lines]

        self.most_combos = (0, 0)

        self.correct_eqs: list[tuple[Equation, ops_list]] = []

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def esrap(self) -> str:
        return '\n'.join(esrap_line(*e.esrap()) for e in self.equations)

    def calibrate(self, strategy: Callable[[Equation], ops_genny]) -> Iterator[int]:
        for i, eq in enumerate(self.equations):
            logger.warn(f"processed {i + 1} of {len(self.equations)}")
            if eq.n_combos() > self.most_combos[1]:
                self.most_combos = i, eq.n_combos()
            logger.info(f"equation {i}: {eq}")
            correct_ops = eq.calibrate(strategy(eq))

            if correct_ops is not None:
                self.correct_eqs.append((eq, correct_ops))
                logger.info(f"valid with ops {correct_ops} after {eq.num_tried} tries")
                yield eq.test_value
            else:
                yield 0


def brute_force(eq: Equation) -> ops_genny:
    """brute force to find a valid operator sequence"""
    return eq.op_combos()


def sum_valid(calibrator: Calibrator) -> int:
    accumulator = sum(calibrator.calibrate(brute_force))
    total_combos = sum(eq.n_combos() for eq in calibrator.equations)
    most_combos_i, most_combos_n = calibrator.most_combos
    logger.info(f"Most combos: {calibrator.equations[most_combos_i]}: {most_combos_n}")
    logger.info(f"Total combos: {total_combos}")

    return accumulator


def answer2(calibrator: Calibrator) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


arg_parser = ArgumentParser('python -m 2024.7.main', description="Advent of Code 2024 Day 7")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    calibrator = Calibrator(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = calibrator.esrap()
        case 1:
            answer = sum_valid(calibrator)
        case 2:
            answer = sum_valid(calibrator)

    logger.debug('')

    print(answer)
