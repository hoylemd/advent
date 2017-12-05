from solve import checksum


def test_simple():
    spreadsheet = (
        (5, 1, 9, 5),
        (7, 5, 1),
        (2, 4, 6, 8),
    )
    expected = 18

    return checksum(spreadsheet) == expected


def result_label(result):
    if result:
        return 'Pass'
    return False


def main():
    print('simple test: {result}'.format(result=result_label(test_simple())))


if __name__ == '__main__':
    main()
