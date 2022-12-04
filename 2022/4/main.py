import fileinput


def parse_input():
    return (line.strip().split(',') for line in fileinput.input())


def check_bounds(outer, inner):
    return outer[0] <= inner[0] and outer[1] >= inner[1]


def do_overlap(first, second):
    f_bounds = first.split('-')
    s_bounds = second.split('-')

    if check_bounds(f_bounds, s_bounds) or check_bounds(s_bounds, f_bounds):
        return True


if __name__ == '__main__':
    lines = parse_input()

    overlaps = 0
    for line in lines:
        delta = 1 if do_overlap(*line) else 0

        print(f"{line}{' - overlap' if delta else ''}")

        overlaps += delta

    print()
    print(overlaps)
