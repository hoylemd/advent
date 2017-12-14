from main import realloc


def test_solve():
    initial_bank = [0, 2, 7, 0]

    assert realloc(initial_bank) == 5
