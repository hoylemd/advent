import argparse

parser = argparse.ArgumentParser(description='solve an advent puzzle')
parser.add_argument('path', type=str, help='path to the input file')


def VectorWheel(index=0):
    """Generator that infinitely rotates through vectors

    This could take in a number of dimenions, or even an arbitrary tuple of
    vectors...
    """
    wheel = ((1, 0), (0, -1), (-1, 0), (0, 1))
    while True:
        yield wheel[index]
        index = (index + 1) % len(wheel)


def odd(n):
    return 2 * n + 1


def get_odd_square(n):
    try:
        return odd_squares[n]
    except IndexError:
        while len(odd_squares) <= n:
            odd_squares.append(odd(len(odd_squares) - 1) ** 2)
    return odd_squares[n]
odd_squares = [0, 1, 9, 25]


class Disk:
    def __init__(self, fill=None):
        self.coordinates = [None]
        self.values = [None]
        self.direction = (0, 0)
        self.directions = VectorWheel(0)
        if fill is not None:
            self.fill_to(fill)

    @property
    def radius(self):
        r = 0
        while get_odd_square(r) < len(self):
            r += 1
        return r

    def get_address_of_sector(self, x, y):
        radius = max(abs(x), abs(y))

        if x == y == radius:  # square corner
            return get_odd_square(radius)

        first = get_odd_square(radius - 1) + 1
        if x == radius:  # left
            xo, yo = self.coordinates[first]
            return first + (yo - y)

        first += odd(radius) - 1
        if y == - radius:  # top
            xo, yo = self.coordinates[first]
            return first + (x - xo)

        first += odd(radius) - 1
        if x == - radius:
            xo, yo = self.coordinates[first]
            return first + (y - yo)

        first += odd(radius) - 1
        if y == radius:
            return first + (xo - x)

    def get_grid(self):
        radius = self.radius
        diameter = radius * 2 + 1
        grid = [[' '] * diameter for _ in range(diameter)]
        i = 1
        for x, y in self.coordinates[1:]:  # Slice off the None at 0
            try:
                grid[y + radius][x + radius] = i
            except IndexError:
                pass
            i += 1
        return grid

    def get_next(self):
        i = len(self)
        if i:
            x, y = self.coordinates[-1]
        else:
            x, y = 0, 0
        dx, dy = self.direction
        x, y = x + dx, y + dy

        coords = (x, y,)
        self.coordinates.append(coords)
        time_to_turn = (
            abs(x * dx) + abs(y * dy) >= self.radius  # time to turn
            and not (i == get_odd_square(self.radius))  # unless we just square
        )
        if time_to_turn or (dx == 0 and dx == 0):
            self.direction = next(self.directions)

        return coords

    def fill_to(self, address):
        while len(self) <= address:
            self.get_next()

    def __len__(self):
        return len(self.coordinates) - 1

    def __str__(self):
        cell_width = len(str(len(self)))
        cell_format = '{' + ':{}'.format(cell_width) + '}'

        grid = self.get_grid()

        return '\n'.join(
            ['|'.join(
                [cell_format.format(str(cell)) for cell in row]
            ) for row in grid]
        )


def compute_coords(address):
    radius = 0

    while get_odd_square(radius) < address:
        radius += 1

    side = odd(radius)
    try:
        from_end = (get_odd_square(radius) - address) % (side - 1)
    except ZeroDivisionError:
        from_end = 0

    if from_end > radius:
        return (radius, from_end - radius)

    return (radius, radius - from_end)


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        val = int(fp.read())

    disk = Disk(25)
    print(disk.get_address_of_sector(2, -1))  # 10
    print(disk.get_address_of_sector(2, 0))  # 11
    print(disk.get_address_of_sector(0, -1))  # 4

if __name__ == '__main__':
    main()
