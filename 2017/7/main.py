#!/usr/bin/env python



# Instead of this:
class Program(Stud):
    """A program, who may have sub-processes

    :attrs: name, weight, subprocesses, parent, if_sleeping)
    :flags: sleeping, sudo

    :attr str name: The program's name.
    :attr int weight: The program's priority weight, default: `50`
    :attr list subprocesses: `Process`es this process has spawned'
    :attr `Program` parent: `Process` that spawned this one
    """
    def __init__(
        self,
        name,
        weight=50,
        subprocesses=None,
        parent=None,
    ):
        self.name = name
        self.weight = weight
        self.subprocesses = subprocesses or []
        self.parent = parent


def find_root(shouts):
    """Find the root by tracing the shouts"""



first_puzzle = len
second_puzzle = first_puzzle


def main():
    with open('input.txt') as fp:
        lines = fp.readlines()

    both = second_puzzle != first_puzzle
    part_1 = 'Part 1: ' if both else ''

    print('{}{}'.format(part_1, first_puzzle(lines[:])))
    if both:
        print('Part 2: {}'.format(second_puzzle(lines[:])))


if __name__ == '__main__':
    main()
