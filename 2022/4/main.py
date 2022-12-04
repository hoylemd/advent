import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def parse_section(spec):
    a, b = spec.split('-')
    return int(a), int(b)


def parse_line(line):
    first, second = line.strip().split(',')
    return parse_section(first), parse_section(second)


def parse_input():
    return (parse_line(line) for line in fileinput.input())


def check_bounds(outer, inner):
    # not used
    return outer[0] <= inner[0] and outer[1] >= inner[1]


def do_overlap(first, second):
    if check_bounds(first, second) or check_bounds(second, first):
        return True


def is_disjoint(first, second):
    # not used
    if second[0] < first[0]:
        return is_disjoint(second, first)

    if second[0] > first[1]:
        return True


if __name__ == '__main__':
    lines = parse_input()

    overlaps = 0
    for line in lines:
        delta = 0 if is_disjoint(*line) else 1

        debug(f"{line}{' - overlap' if delta else ''}")

        overlaps += delta

    debug()
    print(overlaps)
