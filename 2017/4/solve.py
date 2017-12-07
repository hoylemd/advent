import argparse

parser = argparse.ArgumentParser(description='solve an advent  puzzle')
parser.add_argument('path', type=str, help='path to the input file')
parser.add_argument('--part_2', '-2', action='store_true',
                    help='part 2 flag')


def validate(phrase):
    """ensure contains no duplicate words"""
    return False


def solve(phrases, part_2=False):
    """Implement solution here"""
    return len(phrase for phrase in phrases if validate(phrase))


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        phrases = fp.readlines()

    print(solve(phrases, part_2=args.part_2))


if __name__ == '__main__':
    main()
