import fileinput

def parse_input():
    return (line.strip() for line in fileinput.input())


def find_dupe(line):
    """find the duplicate item"""
    # split in half
    radix = int(len(line) / 2)
    first, second = line[0:radix], line[radix:]
    # print(f"{line}")
    # print(f"{first} {second}")
    # find the intersect
    return set(first).intersection(set(second)).pop()


def prioritize(item):
    """calculate priority of item"""
    offset = 96  # ascii code for 'a'
    ascii_val = ord(item)

    if ascii_val < offset:  # it's capital
        offset = 38 # -64 to nullify ascii offset, +26 to be above lcase = 38

    return ascii_val - offset

if __name__ == '__main__':
    lines = parse_input()

    sum = 0
    for line in lines:
        dupe = find_dupe(line)
        sum += prioritize(dupe)

    print(sum)
        