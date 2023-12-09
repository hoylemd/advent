from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Tuple
from dataclasses import dataclass
from math import lcm


def parse_node_spec(line: str) -> Tuple[str, str, str]:
    node, path_spec = line.split(' = ')
    l_path, r_path = path_spec[1:-1].split(', ')
    return node, l_path, r_path


class NodeMap:
    def __init__(self, node_specs):
        self.nodes = {}
        self.paths = {}

        for node, l_node, r_node in node_specs:
            self.nodes[node] = {'L': l_node, 'R': r_node}

    def walk_route(self, start: str, end: str, route: str) -> int:
        step = 0
        current_node = start

        while current_node != end:
            next_direction = route[step % len(route)]
            next_node = self.nodes[current_node][next_direction]
            logger.info(f"Step {step}: At {current_node}, going {next_direction}, to {next_node}")
            step += 1
            current_node = next_node

        return step

    def quantum_walk_route(self, route: str) -> int:
        ghosts = {node: Ghost(self, node, route) for node in self.nodes if node[-1] == 'A'}

        for _, ghost in ghosts.items():
            logger.info(ghost)

        # get least common multiple of cycle lengths?
        path_lengths = [sum(ghost.path_lengths) for ghost in ghosts.values()]
        return lcm(*path_lengths)



@dataclass
class GhostPath:
    start_node: str
    start_index: int
    length: int
    end_node: str

    def __str__(self) -> str:
        return f"({self.start_node}, {self.start_index})-({self.length})>{self.end_node}"


@dataclass
class Ghost:
    map: NodeMap
    start_node: str
    route: str

    def __post_init__(self):
        self.paths = []
        started = False
        current_node = self.start_node
        current_index = 0

        while not started or current_node != self.start_node and current_index:
            started = True
            if next_path := self.map.paths.get((current_node, current_index)):
                logger.info(f"seen {next_path}")
                # current situation seen before, skip on!
                current_node = next_path.end_node
                current_index = (current_index + next_path.length) % len(self.route)
            else:
                next_path = self.get_path(current_node, current_index)
                logger.info(f"new path {next_path}")
                self.map.paths[current_node, current_index] = next_path
            self.paths.append(next_path)

    def get_path(self, start_node: str, start_index: int) -> GhostPath:
        step = 0
        current_node = start_node
        started = False
        while not started or current_node[-1] != 'Z':
            started = True
            next_direction = self.route[(start_index + step) % len(self.route)]
            next_node = self.map.nodes[current_node][next_direction]
            logger.info(f"Step {step}: At {current_node}, going {next_direction}, to {next_node}")
            step += 1
            current_node = next_node

        return GhostPath(start_node, start_index, step, current_node)

    @property
    def path_lengths(self) -> list[int]:
        return [path.length for path in self.paths]

    def __str__(self) -> str:
        return f"Ghost {self.start_node} with {len(self.paths)} paths in cycle, of total length {sum(self.path_lengths)}"


def count_quantum_steps(route: str, map: NodeMap) -> int:
    return map.quantum_walk_route(route)


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
        answer = count_quantum_steps(route, map)

    logger.debug('')

    print(f"answer:\n{answer}")
