import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def parse_input():
    return (line.strip() for line in fileinput.input())


if __name__ == '__main__':
    lines = parse_input()

    for line in lines:
        debug(line)
