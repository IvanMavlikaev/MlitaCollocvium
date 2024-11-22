from app.terms import Arrow, Var, Not


def test_str():
    assert str(Arrow(Var('A'), Var('B'))) == 'A > B'


def test_humanize():
    assert Arrow(Var('A'), Var('B')).translate() == 'если A, то B'
