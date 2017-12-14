from main import first_puzzle, second_puzzle


def test_first():
    """Should return length 5"""
    example = 'hello'

    assert first_puzzle(example) == 5


def test_second():
    """Should return length 5"""
    example = 'world'

    if second_puzzle != first_puzzle:
        assert second_puzzle(example) == 5
