from solve import solve


def io_test(*arguments):
    result = solve(*arguments)

    return result


tests = {
    'example': (sorted, ['one', 'two', 'three'], ['one', 'three', 'two']),
}

test_cases = {
    sorted: (
        ("hello", ['e', 'h', 'l', 'l', 'o'],),
        ([2, -3, 12, 1], [-3, 1, 2, 12],),
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


def _is_str_or_noniterable(obj):
    if isinstance(obj, str):
        return True

    try:
        iter(obj)
    except TypeError:
        return True

    return False


def execute_test(label, test, expected=None, arguments=[]):
    if not isinstance(arguments, tuple):
        arguments = (arguments,)

    return '{}: {}'.format(
        label,
        compose_result(test(*arguments), expected)
    )


def run_tests(tests):
    for label, spec in tests.items():
        test, arguments, expected = spec
        arguments = arguments or tuple()

        print(execute_test(label, test, expected, arguments))


def run_test_cases(test_cases):
    for test, cases in test_cases.items():
        for arguments, expected in cases:
            label = '{}({})'.format(test.__name__, arguments)

            print(execute_test(label, test, expected, arguments))


def main():
    run_tests(tests)
    run_test_cases(test_cases)


if __name__ == '__main__':
    main()
