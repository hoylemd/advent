from argparse import ArgumentParser
from utils import logger, parse_input, INFINITY
from typing import Iterator, Optional, Generator, Tuple
from dataclasses import dataclass


def expand_range(lbound, length):
    return f"{lbound}..{length}..{lbound+(length - 1)}"


@dataclass
class Mapping:
    anchor: int
    trans: int
    length: int

    def __post_init__(self):
        self.offset = self.trans - self.anchor
        self.end = self.anchor + (self.length - 1)

    def map_value(self, value: int) -> Optional[int]:
        delta = value - self.anchor
        if delta >= 0 and delta < self.length:
            # in range
            return value + self.offset

    def map_range(self, lbound: int, length: int) -> Optional[Tuple[int, int, int, int]]:
        skipped = 0

        if lbound < self.anchor:
            if lbound + length <= self.anchor:
                return None  # entire range is below this mapping

            skipped = self.anchor - lbound
            lbound = self.anchor

            assert skipped < length, "skipped more than in range?"
            length -= skipped

        if lbound > self.end:
            return None  # entire range is above this mapping

        remaining = 0
        rbound = lbound + (length - 1)
        if rbound > self.end:
            remaining = rbound - self.end
            length -= remaining

        return skipped, lbound + self.offset, length, remaining

    def __str__(self):
        return f"{expand_range(self.anchor, self.length)} -> {expand_range(self.trans, self.length)} ({self.offset})"


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

    def map_range(self, lbound: int, length: int):
        """given a range spec, return range specs in the next resource"""
        ranges = []

        for mapping in self.mappings:
            logger.info(f"  {mapping}")
            if length == 0:
                break  # whole range is mapped
            if (map_results := mapping.map_range(lbound, length)) is None:
                continue  # this mapping doesn't apply

            skipped, mapped_lbound, mapped_length, remaining = map_results
            logger.info(
                f"    matched! {skipped} skipped, "
                f"{expand_range(mapped_lbound, mapped_length)}, "
                f"{remaining} left"
            )

            if skipped:
                ranges.append((lbound, skipped,))
                lbound += skipped
                length -= skipped

            ranges.append((mapped_lbound, mapped_length,))
            lbound += mapped_length
            length -= mapped_length

            assert remaining == length, "remaining in range doesnt match updated length"

        if length:
            ranges.append((lbound, length))  # include remaining range

        return ranges

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

    def map_value(self, value: int) -> int:
        intermediate = value
        for resource in self.chain:
            intermediate = self.maps[resource].map_value(intermediate)

        return intermediate

    def map_range(self, lbound: int, length: int) -> int:
        """given a seed range, find the location ranges for it & return the least location value"""
        ranges = [(lbound, length)]

        for resource in self.chain:
            logger.info(f"ranges for {resource}: {[expand_range(*range) for range in ranges]}")
            logger.info(self.maps[resource])
            next_ranges = []

            for lb, ln in ranges:
                next_ranges.extend(self.maps[resource].map_range(lb, ln))

            next_ranges.sort(key=lambda rng: rng[0])
            ranges = next_ranges
            logger.info('')

        return ranges[0][0]

    @property
    def seed_ranges(self) -> Generator[Tuple[int, int], None, None]:
        for i in range(0, len(self.seeds), 2):
            yield self.seeds[i], self.seeds[i + 1]


def find_least_location_from_ranges(almanac: Almanac) -> int:
    lowest_location = INFINITY

    for lbound, length in almanac.seed_ranges:
        logger.info(f"{expand_range(lbound, length)}, current least: {lowest_location}")
        least_for_range = almanac.map_range(lbound, length)
        logger.info(f"least for range {expand_range(lbound, length)}: {least_for_range}")
        lowest_location = min(lowest_location, least_for_range)

    return lowest_location


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
        answer = find_least_location_from_ranges(almanac)

    logger.debug('')

    print(f"answer:\n{answer}")
