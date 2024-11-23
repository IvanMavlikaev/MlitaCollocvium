from app import Or, And, Var, parse, Not, Arrow, replace_arguments, to_or_not
from copy import deepcopy
from axioms import Axiom, BasicAxiom

flag4 = 0
flag5 = 0
flag6 = 0
flag7 = 0
flag8 = 0
flag9 = 0
flag10 = 0
flag11 = 0


def deduction(expression, step):
    arrow_elem = Arrow(Var("A"), Var("B"))
    ex = expression
    while arrow_elem.isinstance(ex):
        if arrow_elem.isinstance(ex.arg2):
            ex = ex.arg2
        else:
            if step == 1:
                return ex.arg2
            else:
                return to_or_not(ex)

def modus_ponens(ax: Axiom, basic_axiom: BasicAxiom):
    global flag4
    global flag5
    global flag6
    global flag7
    global flag8
    global flag9
    global flag10
    global flag11
    if not flag4 and ax.A4(basic_axiom.arg2):
        print("Аксиома 4 доказана:\n", basic_axiom.arg1.translate(), "\n", basic_axiom.translate(), "\nПо modus ponens\n",
        basic_axiom.arg2.translate(), "\n")
        flag4 = 1
    if not flag5 and ax.A5(basic_axiom.arg2):
        print("Аксиома 5 доказана:\n",basic_axiom.arg1.translate(), "\n", basic_axiom.translate(), "\nПо modus ponens\n",
        basic_axiom.arg2.translate(), "\n")
        flag5 = 1
    if not flag6 and ax.A6(basic_axiom.arg2):
        print("Аксиома 6 доказана:\n", basic_axiom.arg1.translate(), "\n", basic_axiom.translate(), "\nПо modus ponens\n",
        basic_axiom.arg2.translate(), "\n")
        flag6 = 1
    if not flag7 and ax.A7(basic_axiom.arg2):
        print("Аксиома 7 доказана:\n", basic_axiom.arg1.translate(), "\n", basic_axiom.translate(), "\nПо modus ponens\n",
        basic_axiom.arg2.translate(), "\n")
        flag7 = 1
    if not flag8 and ax.A8(basic_axiom.arg2):
        print("Аксиома 8 доказана:\n", basic_axiom.arg1.translate(), "\n", basic_axiom.translate(), "\nПо modus ponens\n",
        basic_axiom.arg2.translate(), "\n")
        flag8 = 1
    if not flag9 and ax.A9(basic_axiom.arg2):
        print("Аксиома 9 доказана:\n", basic_axiom.arg1.translate(), "\n", basic_axiom.translate(), "\nПо modus ponens\n",
        basic_axiom.arg2.translate(), "\n")
        flag9 = 1
    if not flag10 and ax.A10(basic_axiom.arg2):
        print("Аксиома 10 доказана:\n", basic_axiom.arg1.translate(), "\n", basic_axiom.translate(), "\nПо modus ponens\n",
        basic_axiom.arg2.translate(), "\n")
        flag10 = 1
    #print(not flag11, (ax.A11(basic_axiom.arg2), ax.A11(deduction(basic_axiom, 2))), deduction(basic_axiom, 2))
    if not flag11 and (ax.A11(basic_axiom.arg2) or ax.A11(deduction(basic_axiom, 2))):
        if ax.A11(basic_axiom.arg2):
            print("Аксиома 11 доказана:\n", basic_axiom.arg1.translate(), "\n", basic_axiom.translate(), "\nПо modus ponens\n",
        basic_axiom.arg2.translate(), "\n")
        else:
            print("Аксиома 11 доказана:\nПо теореме о дедукции из ", basic_axiom, "\nсдедует\n", deduction(basic_axiom, 2), "\n")
        flag11 = 1


if __name__ == '__main__':
    d = ["A * B", "B", "A", "!A", "!B", "!C", "A | B", "!A > A", "A > (A > A)", "A > A"]
    new_d = []
    for i in range (len(d)):
        new_d.append(parse(d[i]))
        #print(new_d[i].implication_negation())
    for i in range (len(new_d)):
        for j in range (len(new_d)):
            if j== i:
                continue
            arrow_elem = Arrow(Var("A"), Var("B"))
            and_elem = And(Var("A"), Var("B"))
            or_elem = Or(Var("A"), Var("B"))
            ax = Axiom()
            axiom1 = BasicAxiom().generateA1(new_d[i], new_d[j])
            modus_ponens(ax, axiom1)
            arg2_for_ponens = deduction(axiom1, 2)
            axiom3 = BasicAxiom().generateA3(new_d[i], new_d[j])
            modus_ponens(ax, axiom3)