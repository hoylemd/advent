from solve_captcha import sum_matches


def test_next():
    cases = {
        '1122': 3,
        '1111': 4,
        '1234': 0,
        '91212129': 9,
    }

    for string, result in cases.items():
        result = sum_matches(string) == result
        print('{case} {passfail}'
              .format(case=string, passfail='Passed' if result else 'Failed'))


def test_opposite():
    cases = {
        '1212': 6,
        '1221': 0,
        '123425': 4,
        '123123': 12,
        '12131515': 4,
    }

    for string, result in cases.items():
        result = sum_matches(string, opposite=True) == result
        print('{case} {passfail}'
              .format(case=string, passfail='Passed' if result else 'Failed'))


def main():
    test_next()
    test_opposite()


if __name__ == '__main__':
    main()
