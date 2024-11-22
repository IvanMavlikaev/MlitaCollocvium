from app import  Or, And, Var, parse, Not, Arrow

def parse_disj():
    s = "A | B"
    or_elem = Or(Var("A"), Var("B"))
    if parse(s).eque(or_elem):
        return True
    return False


def parse_conj():
    s = "A * B"
    and_elem = And(Var("A"), Var("B"))
    if parse(s).eque(and_elem):
        return True
    return False

if __name__ == '__main__':
     print(parse_disj())
     print(parse_conj())
