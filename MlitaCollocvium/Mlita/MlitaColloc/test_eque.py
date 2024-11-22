from app.terms import Equal, Var, Not


def test_str():
    return str(Equal(Var('A'), Var('B'))) == 'A = B'



def test_translate():
    return Equal(Var('A'), Var('B')).translate() == 'A эквивалентно B'

if __name__ == '__main__':
    print(test_str())
    print(test_translate())
