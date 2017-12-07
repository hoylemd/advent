import argparse

parser = argparse.ArgumentParser(description='solve an advent  puzzle')
parser.add_argument('path', type=str, help='path to the input file')
parser.add_argument('--part_2', '-2', action='store_true',
                    help='part 2 flag')


def odd(n):
    return 2 * n + 1


class Ring:
    def __init__(self, index):
        self.index = index
        self.diameter = self._diameter()
        self.radius = self._radius()
        self.max = self._max()
        self.min = self._min()

    def _diameter(self):
        return odd(self.index)

    def _radius(self):
        return int(self.diameter / 2)

    def _max(self):
        return self.diameter ** 2

    def _min(self):
        if self.index > 0:
            return get_ring(self.index - 1).max
        return 0

    def __len__(self):
        return self.max - self.min

    def get_sector_from_address(self, address):
        offset = address - self.min
        if offset < 0 or offset > len(self):
            raise IndexError()

        period = self.index * 2
        try:
            offset = offset % period
        except ZeroDivisionError:
            return 0

        return abs(offset - self.index)


rings = [Ring(0)]


def get_ring(index):
    try:
        ring = rings[index]
    except IndexError:
        for i in range(len(rings), index):
            rings.append(Ring(i))
        rings.append(Ring(index))
        return rings[-1]
    return ring


class Address:
    def __init__(self, address):
        self.address = address

        self.ring = get_ring(0)
        while self.ring.max < self.address:
            self.ring = get_ring(self.ring.index + 1)

        self.track = self._track()
        self.sector = self._sector()
        self.manhatten_distance = self._manhatten_distance()

    def _track(self):
        return self.ring.index

    def _sector(self):
        return self.ring.get_sector_from_address(self.address)

    def _manhatten_distance(self):
        return self.track + self.sector


def address_to_path_dims(address):
    """
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
    """
    pass


def solve(address, part_2=False):
    """Implement solution here"""
    return Address(address).manhatten_distance


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
