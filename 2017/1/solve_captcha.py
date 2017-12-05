import argparse

parser = argparse.ArgumentParser(description='solve a quarantine captcha')
parser.add_argument('input_string', type=str, help='The input string')


def main():
    args = parser.parse_args()
    print(sum_matches(args.input_string))


def sum_matches(string):
    total = 0
    for i in range(len(string)):
        current = string[i]
        try:
            next = string[i + 1]
        except IndexError:
            next = string[0]

        if current == next:
            total += int(current)

    return total


if __name__ == '__main__':
    main()
