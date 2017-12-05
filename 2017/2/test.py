from solve import checksum


def test_simple():
    spreadsheet = (
        (5, 1, 9, 5),
        (7, 5, 3),
        (2, 4, 6, 8),
    )
    expected = 18

    result = checksum(spreadsheet)
    return result, expected


def compose_result(result, expected):
    if result == expected:
        return 'Pass'

    return (
        'Fail: actual: {result}, expected: {expected}'
        .format(result=result, expected=expected)
    )


def main():
    print('simple test: {}'.format(compose_result(*test_simple())))


if __name__ == '__main__':
    main()
