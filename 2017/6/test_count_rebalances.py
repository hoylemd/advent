from main import count_rebalances


def test_provided_case():
    initial_bank = [0, 2, 7, 0]

    assert count_rebalances(initial_bank) == 5
