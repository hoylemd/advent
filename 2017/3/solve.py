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


def solve(address):
    """Implement solution here"""
    disk = [None]  # This is the whole data structure...
    # The None acts as padding so that addresses are equal to indexes
    x, y = 0, 0
    dx, dy = 0, 0
    vectors = vector_wheel(-1)
    turns_left = 0
    radius = -1
    for i in range(1, address):
        x, y = x + dx, y + dy
        disk.append([x, y])

        if (
            abs(x * dx) + abs(y * dy) > radius  # if it's time to turn
            and not address == odd(radius) ** 2  # except if we just squared
        ):
            dx, dy = next(vectors)
            if turns_left == 0:
                radius += 1
            turns_left = (turns_left - 1) % 5  # could move into class w wheel

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
