from solve import solve


def io_test(*args, **kwargs):
    result = solve(*args, **kwargs)

    return result


tests = {
    'test_center': (io_test, 0, [1], None),
    'test_adjecent': (io_test, 1, [4], None),
    'test_side': (io_test, 3, [12], None),
    'test_corner': (io_test, 4, [13], None),
    'test_last': (io_test, 6, [49], None),
    'test_first': (io_test, 3, [10], None)
}


def compose_result(result, expected):
    if result == expected:
        return 'Pass'

    return (
        'Fail: actual: {result}, expected: {expected}'
        .format(result=result, expected=expected)
    )


def main():
    for label, spec in tests.items():
        test, expected, args, kwargs = spec
        args = args or []
        kwargs = kwargs or {}

        print('{}: {}'.format(
            label,
            compose_result(test(*args, **kwargs), expected)
        ))


if __name__ == '__main__':
    main()
