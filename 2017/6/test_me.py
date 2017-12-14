from main import realloc, count_rebalances, size_loop


def test_realloc():
    initial_bank = [0, 2, 7, 0]

    assert realloc(initial_bank) == [2, 4, 1, 2]


def test_count_rebalances():
    initial_bank = [0, 2, 7, 0]

    assert count_rebalances(initial_bank) == 5


def test_size_loop():
    initial_bank = [0, 2, 7, 0]

    assert size_loop(initial_bank) == 4
