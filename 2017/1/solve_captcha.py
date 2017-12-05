import argparse

parser = argparse.ArgumentParser(description='solve a quarantine captcha')
parser.add_argument('input_string', type=str, help='The input string')


def main():
    args = parser.parse_args()
    print(args.input_string)


if __name__ == '__main__':
    main()
