from main import realloc


def test_provided():
    initial_bank = [0, 2, 7, 0]

    assert realloc(initial_bank) == [2, 4, 1, 2]
