import fileinput

readings = [int(line.strip()) for line in fileinput.input()]


def calc_windows(readings):
    for i in range(len(readings) - 2):
        pass


def count_increases(values):
    prev = None
    increases = 0
    for value in values:
        if prev is not None:
            if value > prev:
                increases += 1
        prev = value

    return increases

print(count_increases(readings))
