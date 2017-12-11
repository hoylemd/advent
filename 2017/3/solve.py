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


class Disk(list):
    def __init__(self, fill=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append(None)
        self.direction = (0, 0)
        self.directions = VectorWheel(0)
        if fill is not None:
            self.fill_to(fill)

    @property
    def radius(self):
        r = 0
        while (r * 2 + 1) ** 2 < len(self):
            r += 1
        return r

    def get_grid(self):
        radius = self.radius
        diameter = radius * 2 + 1
        grid = [[' '] * diameter for _ in range(diameter)]
        i = 1
        for x, y in self[1:]:
            try:
                grid[y + radius][x + radius] = i
            except IndexError:
                pass
            i += 1
        return grid

    def __str__(self):
        cell_width = len(str(len(self)))
        cell_format = '{' + ':{}'.format(cell_width) + '}'

        grid = self.get_grid()

        return '\n'.join(
            ['|'.join(
                [cell_format.format(str(cell)) for cell in row]
            ) for row in grid]
        )

    def get_next(self):
        i = len(self)
        x, y = self[-1]
        dx, dy = self.direction
        x, y = x + dx, y + dy

        coords = (x, y,)
        self.append(coords)
        time_to_turn = (
            abs(x * dx) + abs(y * dy) >= self.radius  # time to turn
            and not (i == odd(self.radius) ** 2)  # unless we just squared
        )
        if time_to_turn or (dx == 0 and dx == 0):
            self.direction = next(self.directions)

        return coords

    def fill_to(self, address):
        while len(self) <= address:
            self.get_next()

    def __len__(self):
        return super().__len__() - 1


def solve(address):
    radius = 0

    while odd(radius) ** 2 < address:
        radius += 1

    side = odd(radius)
    try:
        from_end = ((side ** 2) - address) % (side - 1)
    except ZeroDivisionError:
        from_end = 0

    if from_end > radius:
        return from_end

    return (radius - from_end) + radius


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        val = int(fp.read())

    print(solve(val))


if __name__ == '__main__':
    main()
