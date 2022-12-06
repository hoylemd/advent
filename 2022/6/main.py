import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def parse_input():
    return ''.join(line.strip() for line in fileinput.input())  # one-line input


def is_sopm(frame):
    """given string check if all charsdifferent"""
    yesno = len(set(frame)) == len(frame)

    debug(f"checking frame: {frame} {yesno}")
    return yesno



def find_next_packet(stream):
    i = 3
    buffer = ''

    while i < len(stream):
        if is_sopm(stream[i-3:i+1]):
            break
        i += 1

    return i + 1


if __name__ == '__main__':
    stream = parse_input()

    print(find_next_packet(stream))
