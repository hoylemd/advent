from main import first_puzzle, second_puzzle, Program


def test_first():
    """Should return length 'tknk'"""
    example = (
        'pbga (66)',
        'xhth (57)',
        'ebii (61)',
        'havc (66)',
        'ktlj (57)',
        'fwft (72) -> ktlj, cntj, xhth',
        'qoyq (66)',
        'padx (45) -> pbga, havc, qoyq',
        'tknk (41) -> ugml, padx, fwft',
        'jptl (61)',
        'ugml (68) -> gyxo, ebii, jptl',
        'gyxo (61)',
        'cntj (57)',
    )

    assert first_puzzle(example) == 'tknk'


def test_from_shout():
    """Should return a Program and list of subprocess names"""
    shout = 'fwft (72) -> ktlj, cntj, xhth'

    program, subprogram_names = Program.from_shout(shout)
    assert program.name == 'fwft'
    assert program.weight == 72
    assert subprogram_names == ['ktlj', 'cntj', 'xhth']


if second_puzzle != first_puzzle:
    def test_second():
        """Should return length 5"""
        example = 'world'

        assert second_puzzle(example) == 5
