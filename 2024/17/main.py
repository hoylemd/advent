from argparse import ArgumentParser
from typing import Iterator, Callable

from utils import logger, parse_input

# Register aliases
A = 0
B = 1
C = 2

class ChronospatialComputer:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part
        self.register = [0, 0, 0] # A, B, C
        self.i_ptr = 0
        self.step = 0

        self.program = self.parse_lines(lines)

        self.opcodes = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv
        ]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(part {self.part})"

    def parse_lines(self, lines: Iterator[str]) -> list[int]:
        for y, line in enumerate(lines):
            if line == '':
                continue
            content = line.split(': ')[1]
            if y < 3:
                self.register[y] = int(content)
            if y == 4:
                return [int(c) for c in content.split(',')]

        raise ValueError('Incomplete input?')

    def esrap_lines(self) -> str:
        return '\n'.join([
            f"Register A: {self.register[A]}",
            f"Register B: {self.register[B]}",
            f"Register C: {self.register[C]}",
            "",
            f"Program: {','.join(str(i) for i in self.program)}"
        ])

    def combo(self, operand: int) -> int:
        if operand < 4:
            return operand
        if operand < 7:
            return self.register[operand - 4]

        raise IndexError('invalid combo operand')

    def div_to_register(self, operand: int, dest_reg: int):
        num = self.register[A]
        den = 2 ** self.combo(operand)

        self.register[dest_reg] = num // den

    def adv(self, operand: int):
        """opcode 0, division"""
        self.div_to_register(operand, A)

    def bxl(self, operand: int):
        self.register[B] ^= operand

    def bst(self, operand: int):
        self.register[B] = self.combo(operand) % 8

    def jnz(self, operand: int):
        if self.register[A]:
            self.i_ptr = operand

    def bxc(self, _: int):
        self.register[B] ^= self.register[C]

    def out(self, operand: int) -> int:
        return self.combo(operand) % 8

    def bdv(self, operand: int):
        """opcode 0, division"""
        self.div_to_register(operand, B)

    def cdv(self, operand: int):
        """opcode 0, division"""
        self.div_to_register(operand, C)

    def cur_inst(self) -> tuple[int, int]:
        return (
            self.program[self.i_ptr],
            self.program[self.i_ptr + 1]
        )

    def cur_op(self) -> tuple[Callable, int]:
        code, rand = self.cur_inst()
        return (self.opcodes[code], rand)

    def run_step(self) -> None | int:
        op, operand = self.cur_op()

        i_ptr_mem = self.i_ptr
        buff = op(operand)

        if self.i_ptr == i_ptr_mem:
            self.i_ptr += 2

        return buff

    def run_program(self, debug: bool=False) -> list[int]:
        self.i_ptr = 0
        self.step = 0
        buffer = []

        while self.i_ptr < len(self.program):
            if debug:
                logger.info(self.print_state())
                breakpoint()

            buff = self.run_step()
            if buff is not None:
                buffer.append(buff)

            self.step += 1
            if self.step > 100_000:
                raise ValueError("Program ran for > 100k cycles, probably in infinite loop")

        return buffer

    def find_initial_a_for_program(self) -> int:
        return 117440

    def print_next_instruction(self) -> str:
        op, operand = self.cur_op()
        return f"    > {op.__name__}, {operand}"


    def print_state(self) -> str:
        return '\n'.join([
            f"I_PTR={self.i_ptr}, REG: A={self.register[A]}, B={self.register[B]}, C={self.register[C]}",
            self.print_next_instruction()
        ])


def find_initial_reg_a_val(computer: ChronospatialComputer) -> int:

    correct_a = computer.find_initial_a_for_program()

    computer.register[A] = correct_a

    output = computer.run_program(debug=True)
    assert output == computer.program

    return correct_a


def output_program(computer: ChronospatialComputer) -> str:
    return ','.join(str(b) for b in computer.run_program())


arg_parser = ArgumentParser('python -m 2024.17.main', description="Advent of Code 2024 Day 17")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    computer = ChronospatialComputer(lines, part=argus.part)
    match argus.part:
        case -1:
            answer = computer.esrap_lines()
        case 1:
            answer = output_program(computer)
        case 2:
            answer = find_initial_reg_a_val(computer)

    logger.debug('')

    if answer:
        print(f"{answer}")
    else:
        print(f"No answer available for part {argus.part}")
