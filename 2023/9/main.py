from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


def parse_line(line: str) -> list[int]:
    return [int(value) for value in line.split()]


class Oasis:

    def __init__(self, histories: Iterator[str], part: int = 1):
        self.part = part

        self.histories = [parse_line(line) for line in histories]

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"


def find_derivatives(history: list[int]) -> list[list[int]]:
    derivatives = [history]

    logger.info(f"deriving from:\n{history}")

    while len(prev_level := derivatives[-1]) > 1:
        next_derivative = [prev_level[i] - prev_level[i - 1] for i in range(1, len(prev_level))]
        logger.info(f"{'  ' * len(derivatives)}{next_derivative}")
        derivatives.append(next_derivative)

        if len(set(next_derivative)) <= 1:
            break

    return derivatives


def predict_next_value(history: list[int]) -> int:
    derivatives = find_derivatives(history)

    prediction = 0
    for derivative in derivatives[::-1]:
        delta = derivative[-1]
        prediction += delta

    return prediction


def predict_first_value(history: list[int]) -> int:
    derivatives = find_derivatives(history)

    delta = 0
    for derivative in derivatives[::-1]:
        logger.info(f"predicting first value for {derivative}")
        delta = derivative[0] - delta
        logger.info(f"-> {delta}")

    return delta


def sum_predictions(oasis: Oasis, part: int = 1) -> int:
    strategy = predict_next_value if part == 1 else predict_first_value

    return sum(strategy(history) for history in oasis.histories)


arg_parser = ArgumentParser('python -m 2023.9.main', description="Advent of Code 2023 Day 9")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    histories = parse_input(argus.input_path)
    oasis = Oasis(histories)
    answer = sum_predictions(oasis, argus.part)

    logger.debug('')

    print(f"answer:\n{answer}")
