from solve import validate

tests = {
    'first': (validate, True, ['aa bb cc dd ee']),
    'second': (validate, False, ['aa bb cc dd aa']),
    'third': (validate, True, ['aa bb cc dd aaa']),
}


def compose_result(result, expected=None):
    if expected is None:
        expected = True

    if result == expected:
        return 'Pass'

    return (
        'Fail: actual: {result}, expected: {expected}'
        .format(result=result, expected=expected)
    )


def main():
    for label, spec in tests.items():
        test, expected, args = spec
        args = args or []

        print('{}: {}'.format(
            label,
            compose_result(test(*args), expected)
        ))


if __name__ == '__main__':
    main()
