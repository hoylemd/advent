import argparse

parser = argparse.ArgumentParser(description='calculate spreadsheet checksum')
parser.add_argument('path', type=str, help='path to the spreadsheet file')


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        lines = fp.readline()

    sheet = (line.split() for line in lines)

    print(sheet)


def checksum(spreadsheet):
    """Calculate checksum of a spreadsheet

    :param spreadsheet: Spreadsheet to check
    :type spreadsheet: 2d tuple of tuples
    :return: checksum
    :rtype: int
    """
    pass


if __name__ == '__main__':
    main()
