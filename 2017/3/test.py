from solve import solve


def io_test(*args, **kwargs):
    result = solve(*args, **kwargs)

    return result


def test_sample():
    result = solve(6)

    return result


def count_it_up(max=50, min=1):
    print('address | distance')
    print('--------|---------')
    for i in range(min, max):
        print('{:7^} | {}'.format(i, solve(i)))


tests = {
    'test_1': (io_test, 0, [1], None),
    'test_4': (io_test, 1, [4], None),
    'test_12': (io_test, 3, [12], None),
    'test_23': (io_test, 2, [23], None),
    'test_1024': (io_test, 31, [1024], None),
    # 'count_em_up': (count_it_up, None, None, None),
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
