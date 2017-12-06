import argparse

parser = argparse.ArgumentParser(description='solve an advent  puzzle')
parser.add_argument('path', type=str, help='path to the input file')
parser.add_argument('--part_2', '-2', action='store_true',
                    help='part 2 flag')


def manhatten_distance(x, y):
    return abs(x) + abs(y)


def ring_width(index):
    return 2 * index + 1


def ring_max(index):
    return ring_width(index) ** 2


def index_of_ring(address):
    index = 0
    while ring_max(index) < address:
        index += 1

    return index


def address_to_path_dims(address):
    ring = index_of_ring(address)

    d_ring = ring

    offset = (ring_max(ring) - address)
    radius = ring_width(ring) - 1
    try:
        from_corner = offset % radius
    except ZeroDivisionError:
        from_corner = 0
    d_spoke = from_corner - ring
    return d_ring, d_spoke


def solve(address, part_2=False):
    """Implement solution here"""
    return manhatten_distance(*address_to_path_dims(address))


def main():
    args = parser.parse_args()

    try:
        with open(args.path) as fp:
            data = int(fp.read())
    except Exception:
        data = int(args.path)

    print(solve(data, part_2=args.part_2))


if __name__ == '__main__':
    main()
