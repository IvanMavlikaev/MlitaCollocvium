from app import Or, And, Var, parse, Not, Arrow
from copy import deepcopy
from axioms import Axiom, BasicAxiom

if __name__ == '__main__':
    x = parse("A > B")
    y = parse("A > B")

    print(x.translate())
    print(x)
    a = Var('A')
    n = Not(a)
    s = deepcopy(n)
    ar = Or(a, n)
    print(ar)
    print(ar.translate())
    print(ar.implication_negation().implication_negation())
    b = Var('B')

    a = BasicAxiom()
    x1 = Var('A')
    x2 = Var('B')
    x3 = Var('C')
    n = Axiom()
    z = Arrow(Or(x1, x3), x3)
    print(n.A5(z))
    s  = parse("((A>(B>C))>((A>B)>(A>C)))")
    print(a.A2(s))
    s1 = parse("(!B>!A)>((!B>A)>B)")

    s = parse("((A>(B>C))>((A>B)>(A>C)))")
    print(a.A2(s))
    s = Or("A", Not("A"))
    print(n.A11(s))
    s = parse("A|!A")
    print(n.A11(s))
