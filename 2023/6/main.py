from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator
from dataclasses import dataclass
from math import sqrt, ceil


def button_time_distance(race_time, button_time):
    return max((race_time - button_time) * button_time, 0)


def distance_button_time(race_time, distance):
    # let's get quadratic in heah
    return (
        ((race_time - sqrt(race_time ** 2 - 4 * distance)) / 2),
        ((race_time + sqrt(race_time ** 2 - 4 * distance)) / 2)
    )


@dataclass
class Race:
    time: int
    best_distance: int

    def __str__(self):
        return f"{self.time}ms Race: best: {self.best_distance}mm"

    @property
    def optimal_time(self):
        return self.time // 2

    @property
    def current_best_time(self):
        return distance_button_time(self.time, self.best_distance)[0]


class Scoreboard:
    def __init__(self, lines: Iterator[str]):
        time_line = next(lines)
        dist_line = next(lines)

        self.races = [Race(int(t), int(d)) for t, d in zip(time_line.split()[1:], dist_line.split()[1:])]


def answer_second_part(scoreboard: Scoreboard) -> int:
    accumulator = 0

    return accumulator


def race_options(race):
    logger.info(race)
    logger.info(f"  best distance held button for {race.current_best_time} ms")
    for i in range(race.time + 1):
        distance = button_time_distance(race.time, i)
        logger.info(f"Button held for {i}ms, distance: {distance}mm")


def mult_ways_to_win(scoreboard: Scoreboard) -> int:
    accumulator = 1

    for race in scoreboard.races:
        # optimal time is always `time / 2`
        # calculate time for current best
        # ways to win is optimal - current best * 2
        optimal_time = race.time / 2
        min_win_time = ceil(race.current_best_time)
        if min_win_time == race.current_best_time:
            min_win_time += 1
        ways_to_win = (
            (race.time + 1)  # total options
            - (min_win_time * 2)  # both sets of losing button times
        )
        logger.info(f"optimal: {optimal_time}, minimum win: {min_win_time}, ways to win: {ways_to_win}")
        accumulator *= ways_to_win
        # race_options(race)
        logger.info('')

    return accumulator


arg_parser = ArgumentParser('python -m 2023.6.main', description="Advent of Code 2023 Day 6")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    scoreboard = Scoreboard(parse_input(argus.input_path))
    if argus.part == 1:
        answer = mult_ways_to_win(scoreboard)
    else:
        answer = answer_second_part(scoreboard)

    logger.debug('')

    print(f"answer:\n{answer}")
