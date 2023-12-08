from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator, Tuple


def parse_node_spec(line: str) -> Tuple[str, str, str]:
    node, path_spec = line.split(' = ')
    l_path, r_path = path_spec[1:-1].split(', ')
    return node, l_path, r_path


class NodeMap:
    def __init__(self, node_specs):
        self.nodes = {}

        for node, l_node, r_node in node_specs:
            self.nodes[node] = {'L': l_node, 'R': r_node}

    def walk_route(self, start: str, end: str, route: str):
        step = 0
        current_node = start

        while current_node != end:
            next_direction = route[step % len(route)]
            next_node = self.nodes[current_node][next_direction]
            logger.info(f"Step {step}: At {current_node}, going {next_direction}, to {next_node}")
            step += 1
            current_node = next_node

        return step


def answer_second_part(lines: Iterator[str]) -> int:
    accumulator = 0

    for line in lines:
        pass

    return accumulator


def count_steps(route: str, map: NodeMap) -> int:
    START_NODE = 'AAA'
    END_NODE = 'ZZZ'

    return map.walk_route(START_NODE, END_NODE, route)


arg_parser = ArgumentParser('python -m 2023.8.main', description="Advent of Code 2023 Day 8")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)

    route = next(lines)
    next(lines)
    map = NodeMap(parse_node_spec(line) for line in lines)

    if argus.part == 1:
        answer = count_steps(route, map)
    else:
        answer = answer_second_part(lines)

    logger.debug('')

    print(f"answer:\n{answer}")
