from solve import solve


def test_sample():
    expected = 6

    result = solve(6)

    return result, expected


tests = {
    'sample_test': test_sample,
}


def compose_result(result, expected):
    if result == expected:
        return 'Pass'

    return (
        'Fail: actual: {result}, expected: {expected}'
        .format(result=result, expected=expected)
    )


def main():
    for label, test in tests.items():
        print('{}: {}'.format(label, compose_result(*test())))


if __name__ == '__main__':
    main()
