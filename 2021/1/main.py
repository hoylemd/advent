import fileinput

readings = [int(line.strip()) for line in fileinput.input()]


def calc_windows(readings):
    windows = []
    for i in range(len(readings) - 2):
        windows += [sum(readings[i:i+3])]

    return windows


def count_increases(values):
    prev = None
    increases = 0
    for value in values:
        if prev is not None:
            if value > prev:
                increases += 1
        prev = value

    return increases


print(count_increases(calc_windows(readings)))
