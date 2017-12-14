#!/usr/bin/env python


def realloc(battery):
    """Rebalance a memory battery

    :param list battery: The battery to rebalance
    :returns list: the rebalanced battery
    """
    blocks = max(battery)
    i = battery.index(blocks)
    battery[i] = 0

    d_blocks = blocks % len(battery)
    common_blocks = (blocks - d_blocks) / len(battery)
    battery = [c_blocks + common_blocks for c_blocks in battery]

    while d_blocks:
        i = (i + 1) % len(battery)
        battery[i] += 1
        d_blocks -= 1

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


def size_loop(battery):
    """Determine how long until a battery config repeats

    :param list battery: The memory battery to balance
    :returns int: length of the loop
    """
    hashmap = {}
    i = 0

    while hashmap.get(tuple(battery)) is None:
        hashmap[tuple(battery)] = i
        battery = realloc(battery)
        i += 1

    return i - hashmap[tuple(battery)]


def main():
    with open('input.txt') as fp:
        battery = [int(string) for string in fp.read().split()]

    print('part 1: {}'.format(count_rebalances(battery[:])))
    print('part 2: {}'.format(size_loop(battery[:])))


if __name__ == '__main__':
    main()
