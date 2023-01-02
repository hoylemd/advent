from argparse import ArgumentParser
from utils import logger, parse_input_line
import hashlib


class AdventMine:
    def __init__(self, key, part):
        self.part = part
        self.key = key

    def __str__(self):
        return f"Advent Mine with key {self.key}"

    def swing_pick(self, n: int):
        dig_spot = self.key + str(n)
        ore_chunk = hashlib.md5(dig_spot.encode())
        return ore_chunk.hexdigest()

    def find_magic_number(self):
        prefix = '0' * (4 + self.part)

        number = 0
        while True:
            chunk = self.swing_pick(number)
            if chunk.startswith(prefix): break
            number += 1

        return number


arg_parser = ArgumentParser('python -m 2015.4.main', description="Advent of Code 2015 Day 4")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    mine = AdventMine(parse_input_line(argus.input_path), argus.part)

    logger.info(mine)
    logger.debug('')

    print(f"answer:\n{mine.find_magic_number()}")
