import argparse

parser = argparse.ArgumentParser(description='solve an advent  puzzle')
parser.add_argument('path', type=str, help='path to the input file')
parser.add_argument('--part_2', '-2', action='store_true',
                    help='part 2 flag')


def odd(n):
    return 2 * n + 1


class Ring:
    def __init__(self, radius=0, previous=None):
        self.radius = radius
        self.sectors = []
        self.filled_sectors = 0

        self.previous = previous
        self.next = None

    @property
    def diameter(self):
        return odd(self.radius)

    @property
    def max(self):
        return self.diameter ** 2

    @property
    def min(self):
        return Ring(self.radius - 1).max

    @property
    def last_sector(self):
        return self.sectors[-1]

    def __len__(self):
        return self.max - self.min

    def get_corner(self, index):
        if index == -1:
            return self.sectors[-1]

        corner_mod = self.radius * 2
        offset_from_end = corner_mod * (3 - index)
        return self.sectors[-1 - offset_from_end]

    def get_adjacent_sectors_to_upper_ring_sector(self, sector):
        if sector.is_corner:
            # figure out which corner, same one as this
            from_end = sector.ring.max - sector.address
            corner_mod = sector.ring.radius * 2
            corner_n = 3 - int(from_end / corner_mod)
            return [self.get_corner(corner_n)]
        elif sector.d_from_corner == 1:



        if sector.offset = 0:
            return [self.sectors[-1], self.sectors[0]]
        if sector.offset = 1:
            return [self.sectors[-1], self.sectors[0], self.sectors[1]]



    def next_sector(self):
        index = self.filled_sectors
        self.filled_sectors += 1
        address = self.min + self.current_sector

        try:
            last = self.sectors[-1]
            value = last.value
            if last.is_corner:
                value += self.sectors[-2].value
        except IndexError:
            # Nothing from this ring
            value = 0

        sector = Sector(self, index, self.min + self.filled_sectors, value)
        self.sectors.append(sector)

        return sector

    def get_sector_from_address(self, address):
        offset = address - self.min
        if offset < 0:
            if self.previous:
                return self.previous.get_sector_from_address(address)
            raise IndexError()

        if offset > len(self):
            if self.next:
                return self.next.get_sector_from_address(address)
            raise IndexError()

        return self.sectors[offset]


class Sector:
    def __init__(self, ring, offset, address, value):
        self.ring = ring
        self.offset = offset
        self.address = address
        self.value = value

    @property
    def d_from_corner(self):
        d_from_max = self.ring.max - self.address
        corner_mod = self.ring.radius * 2
        dist = d_from_max % corner_mod
        if dist > self.ring.radius:
            dist = corner_mod - dist
        return dist

    @property
    def is_corner(self):
        """True if this sector is a corner"""
        return self.d_from_corner == 0


def solve(address, part_2=False):
    """Implement solution here"""
    ring = Ring(0)


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
