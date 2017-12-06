import argparse

parser = argparse.ArgumentParser(description='calculate spreadsheet checksum')
parser.add_argument('path', type=str, help='path to the spreadsheet file')


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        lines = fp.readlines()

    sheet = [[int(cell) for cell in line.split()] for line in lines]

    print(checksum(sheet))


def delta_greatest_minus_least(row):
    ordered = sorted(row)
    return ordered[-1] - ordered[0]


def delta_division(row):
    pass


def checksum(spreadsheet, by_division=False):
    """Calculate checksum of a spreadsheet

    :param spreadsheet: Spreadsheet to check
    :type spreadsheet: 2d tuple of tuples
    :param by_division: Set for part 2, optional
    :type by_division: boolean
    :return: checksum
    :rtype: int
    """
    find_delta = delta_greatest_minus_least if by_division else delta_division
    return sum(find_delta(row) for row in spreadsheet)


if __name__ == '__main__':
    main()
