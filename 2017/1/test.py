from solve_captcha import sum_matches


def main():
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


if __name__ == '__main__':
    main()
