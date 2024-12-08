import collections
import functools
import itertools
from argparse import ArgumentParser
from typing import Iterator, Mapping

from utils import logger, parse_input, INFINITY, coordinates, CharGrid


def parse_line(line: str) -> Iterator[tuple[int, str]]:
    for x, c in enumerate(line):
        if c == '.':
            continue
        yield (x, c)


def antinode(first: coordinates, second: coordinates) -> coordinates:
    """Calculate the coordinates of the antinode for the two antennas that is
    twice the distance from the first
    """
    displacement = (second[0] - first[0], second[1] - first[1])

    return (second[0] + displacement[0], second[1] + displacement[1])


class AntennaMap(CharGrid):

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.antennas = collections.defaultdict(list)

        super().__init__(lines=lines)

    def parse_line(self, y: int, line: str) -> str:
        for x, c in parse_line(line):
            self.antennas[c].append((y, x))

        return line

    def esrap_line(self, y: int, annotations: Mapping[coordinates, str] = {}) -> str:
        annotations = {**self.reverse_map, **annotations}
        return super().esrap_line(y, annotations)

    @functools.cached_property
    def reverse_map(self) -> Mapping[coordinates, str]:
        rev_map = {}
        for c, coords in self.antennas.items():
            for coord in coords:
                rev_map[coord] = c

        return rev_map

    def antinodes_for_pair(self, first: coordinates, second: coordinates) -> Iterator[coordinates]:
        prev, curr = first, second
        while True:
            an = antinode(prev, curr)

            yield curr
            if self.is_out_of_bounds(an):
                break

            prev = curr
            curr = an

    def antinodes(self, skip=1, max=1) -> Iterator[coordinates]:
        for frequency, antennas in self.antennas.items():
            pairs = itertools.permutations(antennas, 2)
            logger.debug(f"Frequency {frequency} has antenna pairs at:")

            for pair in pairs:
                for i, an in enumerate(self.antinodes_for_pair(*pair)):
                    if i < skip:
                        continue
                    if i > max:
                        break
                    logger.debug(f"  - {pair[0], pair[1]}: antinode at {an}")
                    yield an


def count_resonant_antinodes(antenna_map: AntennaMap) -> int:
    seen = set()
    for coord in antenna_map.antinodes(0, INFINITY):
        seen.add(coord)

    return len(seen)


def count_antinodes(antenna_map: AntennaMap) -> int:
    seen = set()
    for coord in antenna_map.antinodes():
        seen.add(coord)

    return len(seen)


arg_parser = ArgumentParser('python -m 2024.8.main', description="Advent of Code 2024 Day 8")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    antenna_map = AntennaMap(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = antenna_map.esrap_lines()
        case 1:
            answer = count_antinodes(antenna_map)
        case 2:
            answer = count_resonant_antinodes(antenna_map)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
