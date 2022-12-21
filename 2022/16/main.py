from argparse import ArgumentParser
from utils import logger, parse_input


class Node:
    def __init__(self, value, graph=None):
        self.value = value
        self.graph = graph
        self.links = []

    def add_link(self, other, weight=1):
        self.links.append((other, weight))


class Graph:
    pass


class Thing:
    def __init__(self, lines, part):
        self.part = part
        self.input = self.parse(lines)

    def __str__(self):
        return '\n'.join(self.input)

    def parse(self, lines):
        return [line for line in lines]

    def answer(self, *args, **kwargs):
        return 0


arg_parser = ArgumentParser('python -m 16.main 16', description="Advent of Code Day 16")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    thing = Thing(parse_input(argus.input_path), argus.part)

    logger.info(thing)
    logger.debug('')

    print(f"answer:\n{thing.answer()}")
