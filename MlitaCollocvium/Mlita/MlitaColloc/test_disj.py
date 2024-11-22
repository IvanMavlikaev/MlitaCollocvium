from  app.terms import Or, Var, Not


def test_str():
    assert str(Or(Var('A'), Var('B'))) == 'A | B'

def test_translate():
    assert Or(Var('A'), Var('B')).humanize() == 'A или B'


def test_implication_negation():
    assert str(Or(Var('A'), Var('B')).implication_negation()) == '!A > B'



if __name__ == '__main__':
    print(test_str())
    print(test_translate())
    print(test_implication_negation())