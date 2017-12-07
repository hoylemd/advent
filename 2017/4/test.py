from solve import validate

tests = {
    'example': (int, '1', 1),
}

test_cases = {
    validate: {
        ("abcde fghij", True),
        ("abcde xyz ecdab", False),
        ("a ab abc abd abf abj", True),
        ("iiii oiii ooii oooi oooo", True),
        ("oiii ioii iioi iiio", False),
    }
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


def execute_test(label, test, expected=None, args=[]):
    if _is_str_or_noniterable(args):
        args = [args]

    return '{}: {}'.format(
        label,
        compose_result(test(*args), expected)
    )


def run_tests(tests):
    for label, spec in tests.items():
        test, expected, args = spec
        args = args or []

        print(execute_test(label, test, expected, args))


def run_test_cases(test_cases):
    for test, cases in test_cases.items():
        for args, expected in cases:
            label = '{}({})'.format(test.__name__, args)

            print(execute_test(label, test, expected, args))


def main():
    run_tests(tests)
    run_test_cases(test_cases)


if __name__ == '__main__':
    main()
