from argparse import ArgumentParser
from typing import Iterable

from utils import logger, parse_input, CharGrid, DIRECTION_MAP, coordinates

type cell_content = str | Mobile


class Mobile:
    def __init__(self, parent: 'Warehouse', y: int, x: int, shape: list[coordinates] = []):
        self.parent = parent
        self.shape = shape if shape else [(0, 0)]
        self.y = y
        self.x = x
        self.symbols = '?'

    def can_push(self, dy: int, dx: int) -> bool:
        dests = [(self.y + sy + dy, self.x + sx + dx) for sy, sx in self.shape]

        contents = list(set(self.parent.lines[ty][tx] for ty, tx in dests))
        for dest_content in contents:
            if dest_content == '.':
                continue
            elif dest_content == '#':
                return False

        return True

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
        for py, px in self.shape:
            self.parent.lines[self.y + py][self.x + px] = '.'
            self.parent.lines[y + py][x + px] = self

        self.y = y
        self.x = x

    def esrap(self, y: int, x: int) -> str:
        for i, (sy, sx) in enumerate(self.shape):
            if (y, x) == (self.y + sy, self.x + sx):
                return self.symbols[i]

        raise ValueError(f"Tried to esrap invalid cell ({y, x}) on obj at ({self.y, self.x}) with shape: {self.shape}")

    def __str__(self) -> str:
        return self.symbols


class Robot(Mobile):
    def __init__(self, parent: 'Warehouse', y: int, x: int):
        super().__init__(parent, y, x)
        self.instructions = ''
        self.counter = 0
        self.symbols = '@'

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
    def __init__(self, parent: 'Warehouse', id: int, y: int, x: int, width: int = 1):
        self.id = id
        self.width = width
        shape = [(0, 0)] if width == 1 else [(0, 0), (0, 1)]
        super().__init__(parent, y, x, shape=shape)

        self.symbols = 'O' if width == 1 else '[]'

    def get_GPS(self):
        return 100 * self.y + self.x


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

    def parse_cell_wide(self, y: int, x: int, c: str) -> list[cell_content]:
        if c == 'O':
            new_box = Box(self, len(self.boxes), y, x * self.part, width=self.part)
            self.boxes.append(new_box)
            return [new_box, new_box]

        if c == '@':
            self.robot = Robot(self, y, x * self.part)
            return [self.robot, '.']

        return [c, c]

    def parse_line(self, y: int, line: str) -> list[cell_content]:
        content = []
        for x, c in enumerate(line):
            content += [self.parse_cell(y, x, c)] if self.part == 1 else self.parse_cell_wide(y, x, c)

        return content

    def parse_lines(self, lines: list[str]) -> Iterable[Iterable[cell_content]]:
        blank_index = lines.index('')
        map_lines = lines[:blank_index]

        grid = list(super().parse_lines(map_lines))
        self.width = self.width * self.part

        assert self.robot is not None

        self.instructions_wrap = len(lines[blank_index + 1])
        self.robot.instructions = ''.join(line for line in lines[blank_index:])

        return grid

    def esrap_cell(self, y: int, x: int) -> str:
        content = self.get(y, x)

        if isinstance(content, Mobile):
            return content.esrap(y, x)

        assert content is not None

        return content

    def esrap_lines(self) -> str:
        grid = super().esrap_lines()

        assert self.robot is not None

        instructions = list(self.robot.esrap_instructions(self.instructions_wrap))
        parts = [grid, ''] + instructions
        return '\n'.join(parts)


def simulate_robot(warehouse: Warehouse) -> int:
    assert warehouse.robot is not None

    logger.info(warehouse.esrap_lines())

    breakpoint()
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
        case _:
            answer = simulate_robot(warehouse)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
