from app.terms import And, Var, Not


def test_str():
    return str(And(Var('A'), Var('B'))) == 'A * B'


def test_translation():
    return And(Var('A'), Var('B')).translate() == 'A и B'


def test_implication_negation():
    return str(And(Var('A'), Var('B')).implication_negation()) == '!(A > !B)'


if __name__ == '__main__':
    print(test_str())
    print(test_translation())
    print(test_implication_negation())