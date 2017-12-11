from solve import solve, Disk
# Switch comments to turn on
# solve = sorted

test_cases = {
    solve: (
        (1, 0),
        (2, 1),
        (12, 3),
        (13, 4),
        (49, 6),
        (10, 3),
    ),
}


def compose_result(outcome, result, expected=None):
    """Translate test outputs into result message"""
    return 'Pass' if outcome else (
        "Fail: act: {result}, exp: {expected}"
        .format(result=result, expected=expected)
    )


def execute_test(test, expected=None, *args):
    """Runs the test method, and formats a test report"""
    result = test(*args)
    outcome = False

    if expected is True and result:
        outcome = True
    elif result == expected:
        outcome = True

    return '{}: {}'.format(
        '{}{}'.format(test.__name__, args),  # sorted('hello')
        compose_result(outcome, result, expected),
    )


def run_test_cases(test_cases):
    for test, cases in test_cases.items():
        # Split off the last arg, it's the expected output
        case_args = ((case[:-1], case[-1],) for case in cases)
        for arguments, expected in case_args:
            print(execute_test(test, expected, *arguments))


def main():
    run_test_cases(test_cases)


if __name__ == '__main__':
    main()
