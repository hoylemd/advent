import fileinput

def parse_input():
    return (line.strip().split(' ') for line in fileinput.input())

if __name__ == '__main__':
    rounds = parse_input()

    for round in rounds:
        print(f"{round[0]} vs {round[1]}")
