import argparse

parser = argparse.ArgumentParser(description='solve an advent puzzle')
parser.add_argument('path', type=str, help='path to the input file')


def solve(instructions):
    fc, ip = 0, 0

    while ip > -1 and ip < len(instructions):
        offset = instructions[ip]
        instructions[ip] += -1 if offset > 2 else 1
        ip += offset
        fc += 1

    return fc


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        instructions = [int(line) for line in fp.readlines()]

    print(solve(instructions))


if __name__ == '__main__':
    main()
