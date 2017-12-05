import argparse

parser = argparse.ArgumentParser(description='solve a quarantine captcha')
parser.add_argument('input_string', type=str, help='The input string')
parser.add_argument('--opposite', '-o', action='store_true',
                    help='True to do opposite comparisons')


def main():
    args = parser.parse_args()
    print(sum_matches(args.input_string, opposite=args.opposite))


def sum_matches(string, opposite=False):
    """Sum the matches in a number string

    :param opposite: True if a number should be summed if it matches it's
    opposite instead of the next one:
    """
    total = 0
    rot = int(len(string) / 2) if opposite else 1
    for i in range(len(string)):
        current = string[i]
        other_index = (i + rot) % len(string)

        other = string[other_index]

        if current == other:
            total += int(current)

    return total


if __name__ == '__main__':
    main()
