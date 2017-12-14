#!/usr/bin/env python


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
