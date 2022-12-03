import fileinput

def parse_input():
    return (line.strip().split(' ') for line in fileinput.input())

if __name__ == '__main__':
    lines = parse_input()

    for line in lines:
        print(line)