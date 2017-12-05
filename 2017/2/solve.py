import argparse

parser = argparse.ArgumentParser(description='calculate spreadsheet checksum')
parser.add_argument('path', type=str, help='path to the spreadsheet file')


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        lines = fp.readlines()

    sheet = [[int(cell) for cell in line.split()] for line in lines]

    print(checksum(sheet))


def checksum(spreadsheet):
    """Calculate checksum of a spreadsheet

    :param spreadsheet: Spreadsheet to check
    :type spreadsheet: 2d tuple of tuples
    :return: checksum
    :rtype: int
    """

    deltas = []

    for row in spreadsheet:
        ordered = sorted(row)
        print(ordered)

        deltas.append(0)

    return sum(deltas)


if __name__ == '__main__':
    main()
