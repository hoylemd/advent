from argparse import ArgumentParser
from utils import logger, parse_input, INFINITY
from typing import Iterator, Optional
from dataclasses import dataclass


@dataclass
class Mapping:
    anchor: int
    trans: int
    length: int

    def __post_init__(self):
        self.offset = self.trans - self.anchor

    def map_value(self, value: int) -> Optional[int]:
        delta = value - self.anchor
        if delta >= 0 and delta < self.length:
            # in range
            return value + self.offset


class Map:
    def __init__(self, spec: str):
        self._spec = spec
        self.source, self.dest = spec.split()[0].split('-to-')
        self.mappings = []
        self._sorted = False

    def add_mapping(self, line: str):
        trans, anchor, length = (int(part) for part in line.split())
        self.mappings.append(Mapping(anchor, trans, length))

    def sort_mappings(self):
        self.mappings.sort(key=lambda mapping: mapping.anchor)
        self._sorted = True

    def map_value(self, value: int) -> int:
        logger.info(f"  Mapping {self.source} {value} to {self.dest}")
        for mapping in self.mappings:
            if (mapped := mapping.map_value(value)) is not None:
                logger.info(f"    mapped to {mapped}")
                return mapped

        # not mapped, so pass it through
        logger.info(f"    no mapping found, leaving as {value}")
        return value

    def __str__(self):
        return (
            f"{self.source}->{self.dest} map: "
            f"{'' if self._sorted else '(unsorted)'} "
            f"{len(self.mappings)} mappings"
        )


class Almanac:
    def __init__(self, lines: Iterator[str], part=1):
        self.part = part

        # get seed #s
        seeds_line = next(lines)
        self.seeds = [int(seed) for seed in seeds_line.split(': ')[1].split()]
        _ = next(lines)

        self.maps = {}   # will map dest category to Map object
        self.chain = []  # list of categories in the order they are mapped

        # parse maps out of remaining lines
        map = None
        for line in lines:
            if not line:  # empty line, this map is done
                map = None
                continue

            if map is None:  # new map line
                map = Map(line)
                self.chain.append(map.dest)
                self.maps[map.dest] = map
                continue

            # load in mappings
            map.add_mapping(line)

        # sort each map's mappings
        for _, map in self.maps.items():
            map.sort_mappings()

    def map_value(self, value: int):
        intermediate = value
        for resource in self.chain:
            intermediate = self.maps[resource].map_value(intermediate)

        return intermediate


def answer_second_part(almanac: Almanac) -> int:
    accumulator = 0

    for line in almanac:
        pass

    return accumulator


def find_lowest_location(almanac: Almanac) -> int:
    lowest_location = INFINITY

    for seed in almanac.seeds:
        location = almanac.map_value(seed)
        lowest_location = min(lowest_location, location)

    return lowest_location


arg_parser = ArgumentParser('python -m 2023.5.main', description="Advent of Code 2023 Day 5")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    almanac = Almanac(parse_input(argus.input_path), argus.part)
    if argus.part == 1:
        answer = find_lowest_location(almanac)
    else:
        answer = answer_second_part(almanac)

    logger.debug('')

    print(f"answer:\n{answer}")
