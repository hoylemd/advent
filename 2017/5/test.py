from solve import solve


def io_test(*arguments):
    result = solve(*arguments)

    return result


test_cases = {
    solve: (
        ([0, 3, 0, 1, -3], 5),
    )
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


def execute_test(label, test, expected=None, arguments=[]):
    if not isinstance(arguments, tuple):
        arguments = (arguments,)

    return '{}: {}'.format(
        label,
        compose_result(test(*arguments), expected)
    )


def run_test_cases(test_cases):
    for test, cases in test_cases.items():
        for arguments, expected in cases:
            label = '{}({})'.format(test.__name__, arguments)

            print(execute_test(label, test, expected, arguments))


def main():
    run_test_cases(test_cases)


if __name__ == '__main__':
    main()
