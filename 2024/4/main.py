from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator, Generator


def parse_line(line: str):
    return line.split()


class WordSearch:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.lines = [line for line in lines]
        self.dimension = len(self.lines)

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def horizontal_lines(self):
        """Lines like -"""
        for line in self.lines:
            yield line

    def vertical_lines(self):
        """Lines like |"""
        for y in range(self.dimension):
            yield ''.join(line[y] for line in self.lines)

    def get_diagonal_line(self, origin: tuple[int, int], direction: tuple[int, int]) -> Generator[str]:
        for i in range(self.dimension):
            y = origin[0] + direction[0] * i
            x = origin[1] + direction[1] * i

            # was_neg = False
            try:
                if y < 0 or x < 0:  # treat negative index as out of bounds
                    # was_neg = True

                    #print('NEG')
                    raise IndexError

                yield self.lines[y][x]
            except IndexError:
                # if not was_neg:
                # print('POS')
                break  # out of bounds, done with this line

    def left_diagonal_lines(self):
        """lines like /"""
        DIRECTION = (-1, 1)  # (y, x)

        #top-left half
        for y in range(self.dimension):
            line = ''.join(c for c in self.get_diagonal_line((0 + y, 0), DIRECTION))
            print(line)
            yield line

        #bottom-right half
        for x in range(1, self.dimension):  # skip first line of this half, already done
            line = ''.join(c for c in self.get_diagonal_line((y, 0 + x), DIRECTION))
            print(line)
            yield line

    def right_diagonal_lines(self):
        """lines like \\"""
        DIRECTION = (-1, -1)  # (y, x)

        #top-right half
        for y in range(self.dimension):
            line = ''.join(c for c in self.get_diagonal_line((0 + y, self.dimension - 1), DIRECTION))
            print(line)
            yield line

        #bottom-left half
        for x in range(2, self.dimension + 1):  # skip first line of this half, already done
            line = ''.join(c for c in self.get_diagonal_line((y, self.dimension - x), DIRECTION))
            print(line)
            yield (line)

    def x_mases_at(self, coordinates: tuple[int, int]) -> int:
        y, x = coordinates
        found = 0
        try:
            if self.lines[y][x] != 'A':
                return 0  # gotta be an A in the middle

            if y == 0 or x == 0:
                # on an edge, can't be
                return 0

            # check cardinal
            """
            HEY GUESS WHAT A + ISNT AN X ISNT THAT A SURPRISE
            h_adj = ''.join(sorted([self.lines[y][x - 1], self.lines[y][x + 1]]))
            v_adj = ''.join(sorted([self.lines[y - 1][x], self.lines[y + 1][x]]))
            if (h_adj == v_adj == 'MS'):
                print('cardinal')
                print('\n'.join([
                    '.' + self.lines[y - 1][x] + '.',
                    self.lines[y][x - 1:x + 2],
                    '.' + self.lines[y + 1][x] + '.',
                ]))
                found += 1
            """

            # check diagonal
            l_adj = ''.join(sorted([self.lines[y - 1][x + 1], self.lines[y + 1][x - 1]]))
            r_adj = ''.join(sorted([self.lines[y - 1][x - 1], self.lines[y + 1][x + 1]]))

            if (l_adj == r_adj == 'MS'):
                print('diagonal')
                print('\n'.join([
                    self.lines[y - 1][x - 1] + '.' + self.lines[y - 1][x + 1],
                    '.' + self.lines[y][x] + '.',
                    self.lines[y + 1][x - 1] + '.' + self.lines[y + 1][x + 1],
                ]))
                found += 1

            if found > 0:
                print()

        except IndexError:
            return 0  # if we go out of bounds, definitely no X-MAS there

        return found

    def translate_coordinates(self, coordinates: tuple[int, int], scheme: str) -> tuple[int, int]:
        """always from horizontal coordinates"""
        y, x = coordinates
        match scheme:
            case 'horizontal':
                return (y, x)
            case 'vertical':
                return (coordinates[1], coordinates[0])
            case 'left_diagonal':
                if y < self.dimension // 2:
                    pass
            case 'right_diagonal':
                pass

        raise ValueError(f"{scheme} not a valid coordinate scheme")


def count_x_mases(word_search: WordSearch) -> int:
    accumulator = 0
    n_a = 0

    for y in range(1, word_search.dimension - 1):
        for x in range(1, word_search.dimension - 1):
            if word_search.lines[y][x] == 'A':
                n_a += 1
                count = word_search.x_mases_at((y, x))
                if count > 0:
                    print('\n'.join([
                        word_search.lines[y - 1][x - 1:x + 2],
                        word_search.lines[y][x - 1:x + 2],
                        word_search.lines[y + 1][x - 1:x + 2],
                    ]))
                    print(f"{count=}, {accumulator=}, ({y=}, {x=})")
                accumulator += count

    print(n_a)
    return accumulator


def count_in_line(line: str) -> int:
    return line.count('XMAS') + line.count('SAMX')


def count_xmas_and_samx(word_search: WordSearch) -> int:
    accumulator = 0
    """
    print('horizontal')
    print('\n'.join(word_search.horizontal_lines()))
    print()

    print('vertical')
    print('\n'.join(word_search.vertical_lines()))
    print()

    print('left diagonals')
    print('\n'.join(word_search.left_diagonal_lines()))
    print()

    print('right_diagonals')
    print('\n'.join(word_search.right_diagonal_lines()))
    """
    # solve part 1
    accumulator += sum(count_in_line(line) for line in word_search.horizontal_lines())

    accumulator += sum(count_in_line(line) for line in word_search.vertical_lines())
    accumulator += sum(count_in_line(line) for line in word_search.left_diagonal_lines())
    accumulator += sum(count_in_line(line) for line in word_search.right_diagonal_lines())

    return accumulator


arg_parser = ArgumentParser('python -m 2024.4.main', description="Advent of Code 2024 Day 4")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    word_search = WordSearch(lines, part=argus.part)
    if argus.part == 1:
        answer = count_xmas_and_samx(word_search)
    else:
        answer = count_x_mases(word_search)

    logger.debug('')

    print(f"answer:\n{answer}")
