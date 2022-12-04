import fileinput


def parse_input():
    return (line.strip() for line in fileinput.input())


def find_badge(first, second, third):
    """find the common element"""
    return set(first).intersection(set(second)).intersection(set(third)).pop()


def prioritize(item):
    """calculate priority of item"""
    offset = 96  # ascii code for 'a'
    ascii_val = ord(item)

    if ascii_val < offset:  # it's capital
        offset = 38  # -64 to nullify ascii offset, +26 to be above lcase = 38

    return ascii_val - offset


if __name__ == '__main__':
    lines = parse_input()

    sum = 0
    group = []
    for line in lines:
        group.append(line)
        if len(group) == 3:
            badge = find_badge(*group)
            sum += prioritize(badge)
            group = []

    print(sum)