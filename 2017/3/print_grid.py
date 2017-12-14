import argparse
from solve import Disk

parser = argparse.ArgumentParser(description='solve an advent puzzle')
parser.add_argument('address', type=int, help='path to the input file')


def main():
    args = parser.parse_args()

    disk = Disk(args.address)

    print(disk)



if __name__ == '__main__':
    main()
