#!/usr/bin/env python
import re


class Program:
    """A program, who may have sub-programes

    :attrs: name, weight, children, parent,

    :attr str name: The program's name.
    :attr int weight: The program's priority weight, default: `50`
    :attr list children: `Program`es this program has spawned'
    :attr `Program` parent: `Program` that spawned this one
    """
    def __init__(
        self,
        name,
        weight=50,
        children=None,
        parent=None,
    ):
        self.name = name
        self.weight = weight
        self.children = children or []
        self.parent = parent

    @classmethod
    def from_shout(kls, shout):
        """Transform a shout into a Program and list of child names"""
        razor = ' -> '
        program_patt = r'([a-z]+) \((\d+)\)'

        try:
            program_str, children_str = shout.split(razor)
        except ValueError:
            program_str = shout
            children_str = ''

        try:
            name, weight_str = re.match(program_patt, program_str).groups()
        except AttributeError:
            import ipdb; ipdb.set_trace()
            print('hello')
        program = Program(name=name, weight=int(weight_str))

        return program, children_str.split(', ')

    def add_child(self, child):
        """Add a child to the process and register as child's parent"""
        self.children.append(child)
        child.parent = self


def find_root(shouts):
    """Find the root by tracing the shouts"""
    name_map = {}
    amber_alerts = {}

    for shout in shouts:
        if not shout:
            continue
        program, child_names = Program.from_shout(shout)
        name_map[program.name] = program

        for name in child_names:
            try:
                program.add_child(name_map[name])
            except KeyError:
                amber_alerts[name] = program

        parent = amber_alerts.get(program.name)
        if parent:
            parent.add_child(program)
            del amber_alerts[program.name]

    while program.parent:
        program = program.parent

    return program.name


first_puzzle = find_root
second_puzzle = first_puzzle


def main():
    with open('input.txt') as fp:
        lines = fp.read().split('\n')

    both = second_puzzle != first_puzzle
    part_1 = 'Part 1: ' if both else ''

    print('{}{}'.format(part_1, first_puzzle(lines[:])))
    if both:
        print('Part 2: {}'.format(second_puzzle(lines[:])))


if __name__ == '__main__':
    main()
