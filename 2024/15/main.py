from argparse import ArgumentParser
from typing import Iterable

from utils import logger, parse_input, CharGrid, DIRECTION_MAP

type cell_content = str | Mobile


class Mobile:
    def __init__(self, parent: 'Warehouse', y: int, x: int):
        self.parent = parent
        self.y = y
        self.x = x

    def push(self, dy: int, dx: int) -> bool:
        ty, tx = self.y + dy, self.x + dx

        if self.parent.is_out_of_bounds((ty, tx)):
            return False

        dest_content = self.parent.lines[ty][tx]
        if dest_content == '.':
            self.move_to(ty, tx)
            return True
        elif dest_content == '#':
            return False
        else:  # is another Mobile
            assert isinstance(dest_content, Mobile)
            if dest_content.push(dy, dx):
                self.move_to(ty, tx)
                return True
            return False

    def move_to(self, y: int, x: int):
        self.parent.lines[self.y][self.x] = '.'
        self.parent.lines[y][x] = self
        self.y = y
        self.x = x


class Robot(Mobile):
    def __init__(self, parent: 'Warehouse', y: int, x: int):
        super().__init__(parent, y, x)
        self.instructions = ''
        self.counter = 0

    def __str__(self) -> str:
        return '@'

    def esrap_instructions(self, wrap_at: int) -> Iterable[str]:
        prev = 0
        next_break = wrap_at
        while next_break <= len(self.instructions):
            yield self.instructions[prev:next_break]
            prev = next_break
            next_break += wrap_at

    def step(self) -> bool:
        dy, dx = DIRECTION_MAP[self.instructions[self.counter]]

        self.counter = (self.counter + 1) % len(self.instructions)

        return self.push(dy, dx)

class Box(Mobile):
    def __init__(self, parent: 'Warehouse', id: int, y: int, x: int):
        self.id = id
        super().__init__(parent, y, x)

    def __str__(self) -> str:
        return 'O'

    def get_GPS(self):
        return 100* self.y + self.x


class Warehouse(CharGrid):

    def __init__(self, lines: list[str], part: int = 1):
        self.part = part
        self.robot = None
        self.boxes = []
        self.instructions_wrap = 0

        self.lines: list[list[cell_content]]
        super().__init__(lines)

    def parse_cell(self, y: int, x: int, c: str) -> cell_content:
        if c == 'O':
            new_box = Box(self, len(self.boxes), y, x)
            self.boxes.append(new_box)
            return new_box

        if c == '@':
            self.robot = Robot(self, y, x)
            return self.robot

        return c

    def parse_line(self, y: int, line: str) -> list[cell_content]:
        return [
            self.parse_cell(y, x, c)
            for x, c in enumerate(line)
        ]

    def parse_lines(self, lines: list[str]) -> Iterable[Iterable[cell_content]]:
        blank_index = lines.index('')
        map_lines = lines[:blank_index]

        grid = list(super().parse_lines(map_lines))

        assert self.robot is not None

        self.instructions_wrap = len(lines[blank_index + 1])
        self.robot.instructions = ''.join(line for line in lines[blank_index:])

        return grid

    def esrap_lines(self) -> str:
        grid = super().esrap_lines()

        assert self.robot is not None

        instructions = list(self.robot.esrap_instructions(self.instructions_wrap))
        parts = [grid, ''] + instructions
        return '\n'.join(parts)


def answer2(warehouse: Warehouse) -> int:
    accumulator = 0

    # solve part 2

    return accumulator


def simulate_robot(warehouse: Warehouse) -> int:
    assert warehouse.robot is not None

    for _ in warehouse.robot.instructions:
        warehouse.robot.step()

    return sum(box.get_GPS() for box in warehouse.boxes)


arg_parser = ArgumentParser('python -m 2024.15.main', description="Advent of Code 2024 Day 15")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = list(parse_input(argus.input_path))
    warehouse = Warehouse(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = warehouse.esrap_lines()
        case 1:
            answer = simulate_robot(warehouse)
        case 2:
            answer = answer2(warehouse)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
