import argparse

parser = argparse.ArgumentParser(description='solve an advent  puzzle')
parser.add_argument('path', type=str, help='path to the input file')


def validate(phrase):
    """ensure contains no duplicate anagrams"""
    seen_words = {}
    words = phrase.split()

    for word in words:
        dorw = ''.join(sorted(word))
        try:
            if seen_words[dorw]:
                return False
        except KeyError:
            seen_words[dorw] = True

    return True


def solve(phrases):
    """Implement solution here"""
    n_valid = 0
    for phrase in phrases:
        n_valid += 1 if validate(phrase) else 0

    return n_valid


def main():
    args = parser.parse_args()

    with open(args.path) as fp:
        phrases = fp.readlines()

    print(solve(phrases))


if __name__ == '__main__':
    main()
