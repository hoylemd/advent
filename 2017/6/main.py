def realloc(battery):
    """Rebalance a memory battery

    :param list battery: The battery to rebalance
    :returns list: the rebalanced battery
    """
    return battery


def count_rebalances(battery):
    """Determine how many reallocations until dupe found

    :param list battery: The memory battery to balance
    :returns int: number of steps before seen config is found
    """
    hashmap = {}

    while hashmap.get(tuple(battery)) is None:
        hashmap[tuple(battery)] = True
        battery = realloc(battery)

    return len(hashmap)


def main():
    with open('input.txt') as fp:
        battery = fp.read().split()

    print(count_rebalances(battery))


if __name__ == '__main__':
    main()
