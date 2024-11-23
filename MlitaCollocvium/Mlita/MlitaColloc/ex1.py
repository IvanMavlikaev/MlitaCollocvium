from app import Or, And, Var, parse, Not, Arrow
from copy import deepcopy
from axioms import Axiom, BasicAxiom

flagA4 = 0
flagA5 = 0

if __name__ == '__main__':
    d = ["A * B", "B", "A", "!A", "!B", "!C", "A | B"]
    new_d = []
    for i in range (len(d)):
        new_d.append(parse(d[i]))
    for i in range (len(new_d)):
        for j in range (len(new_d)):
            if j== i:
                continue
            axiom1 = BasicAxiom().generateA1(new_d[i], new_d[j])
            ax = Axiom()
            axiom2 = BasicAxiom().generateA1(new_d[i], new_d[j])
            axiom3 = BasicAxiom().generateA1(new_d[i], new_d[j])
            if ax.A4(axiom1.arg2):
                print("Аксиома 4 доказана: По modus ponens\n", axiom1.arg1.translate(), "\n", axiom1.translate(), "\n", axiom1.arg2.translate())
                flagA4 = 1
            if ax.A5(axiom2.arg2):
                print("Аксиома 5 доказана: По modus ponens\n", axiom1.arg1.translate(), "\n", axiom1.translate(),  "\n", axiom1.arg2.translate())
                flagA5 = 1
            if ax.A11(axiom3.arg2):
                print("Аксиома 11 доказана: По modus ponens\n", axiom1.arg1.translate(), "\n", axiom1.translate(), "\n",  axiom1.arg2.translate())
