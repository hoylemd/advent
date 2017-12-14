import argparse

parser = argparse.ArgumentParser(description='solve an advent  puzzle')
parser.add_argument('path', type=str, help='path to the input file')


def solve(data):
    """Implement solution here"""
    return data


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        lines = fp.readlines()

    # process input here
    data = '\n'.join(lines)

    print(solve(data))


if __name__ == '__main__':
    main()
