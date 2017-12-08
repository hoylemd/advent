from math import sqrt, floor
import argparse

parser = argparse.ArgumentParser(description='solve an advent  puzzle')
parser.add_argument('path', type=str, help='path to the input file')


def vector_wheel(index=0):
    """Generator that infinitely rotates through vectors

    This could take in a number of dimenions, or even an arbitrary tuple of
    vectors...
    """
    wheel = ((1, 0), (0, -1), (-1, 0), (0, -1))
    while True:
        yield wheel[index]
        index = (index + 1) % len(wheel)


def odd(n):
    return 2 * n + 1


def print_disk(disk):
    pass


class Disk(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append(None)

    @property
    def radius(self):
        if len(self) < 2:
            return 0
        #This has something to do with finding odd square roots...
        return int(floor(sqrt(len(self))))

    def __str__(self):
        pass

    def get_next():
        pass

    def __len__(self):
        return super().__len__() - 1


def solve(address):
    """Implement solution here"""
    disk = Disk()
    # The None acts as padding so that addresses are equal to indexes
    x, y = 0, 0
    dx, dy = 0, 0
    vectors = vector_wheel(0)
    turns_left = 0
    radius = -1
    for i in range(1, address + 1):
        x, y = x + dx, y + dy
        disk.append([x, y])
        step = '{}: {} (r={}, d.r={})'.format(i, disk[-1], radius, disk.radius)

        if (
            abs(x * dx) + abs(y * dy) > radius  # if it's time to turn
            and not address == odd(radius) ** 2  # except if we just squared
        ):
            step += ', turning'
            dx, dy = next(vectors)
            if turns_left == 0:
                step += ', expanding'
                radius += 1
            turns_left = (turns_left - 1) % 5  # could move into class w wheel

        print(step)

    print_disk(disk)

    return abs(x) + abs(y)


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        lines = fp.readlines()

    # process input here
    data = '\n'.join(lines)

    print(solve(data))


if __name__ == '__main__':
    main()
