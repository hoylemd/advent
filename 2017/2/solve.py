import argparse

parser = argparse.ArgumentParser(description='calculate spreadsheet checksum')
parser.add_argument('path', type=str, help='path to the spreadsheet file')
parser.add_argument('--part_2', '-2', action='store_true',
                    help='part 2 flag')


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        lines = fp.readlines()

    sheet = [[int(cell) for cell in line.split()] for line in lines]

    print(checksum(sheet, by_division=args.part_2))


def delta_greatest_minus_least(row):
    ordered = sorted(row)
    return ordered[-1] - ordered[0]


def delta_division(row):
    ordered = sorted(row)

    small = 0
    big = end = len(ordered) - 1

    while small < big:
        while big > small:
            if ordered[big] % ordered[small] == 0:
                return int(ordered[big] / ordered[small])
            big -= 1
        small += 1
        big = end

    raise Exception('could not find a pair of divisible numbers')


def checksum(spreadsheet, by_division=False):
    """Calculate checksum of a spreadsheet

    :param spreadsheet: Spreadsheet to check
    :type spreadsheet: 2d tuple of tuples
    :param by_division: Set for part 2, optional
    :type by_division: boolean
    :return: checksum
    :rtype: int
    """
    print(by_division)
    find_delta = delta_division if by_division else delta_greatest_minus_least
    deltas = [find_delta(row) for row in spreadsheet]
    print(deltas)
    return sum(deltas)


if __name__ == '__main__':
    main()
