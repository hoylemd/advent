def realloc(bank):
    """Determine how many reallocations until dupe found

    :param list bank: The memory bank to balance
    :returns int: number of steps before seen config is found
    """
    pass


def main():
    with open('input.txt') as fp:
        bank = fp.read().split()

    print(realloc(bank))


if __name__ == '__main__':
    main()
