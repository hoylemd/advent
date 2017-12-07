import argparse

parser = argparse.ArgumentParser(description='solve an advent  puzzle')
parser.add_argument('path', type=str, help='path to the input file')
parser.add_argument('--part_2', '-2', action='store_true',
                    help='part 2 flag')


def validate(phrase):
    pass


def solve(data, part_2=False):
    """Implement solution here"""
    return data


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        lines = fp.readlines()

    # process input here
    data = '\n'.join(lines)

    print(solve(data, part_2=args.part_2))


if __name__ == '__main__':
    main()
