from app import *

class Axiom():
    def __init__(self):
        self.count = 0

    def A4(self, expression):
        and_elem = And(Var("A"), Var("B"))
        arrow_elem = Arrow(Var("C"), Var("D"))

        if arrow_elem.isinstance(expression) and and_elem.isinstance(expression.arg1) and expression.arg2.eque(expression.arg1.arg1):
            return True

        return False

    def A5(self, expression):
        and_elem = And(Var("A"), Var("B"))
        arrow_elem = Arrow(Var("C"), Var("D"))

        if arrow_elem.isinstance(expression) and and_elem.isinstance(expression.arg1) and expression.arg2.eque(expression.arg1.arg2):
            return True

        return False

    def A6(self, expression):
        and_elem = And(Var("A"), Var("B"))
        arrow_elem = Arrow(Var("C"), Var("D"))

        if (
            arrow_elem.isinstance(expression) and arrow_elem.isinstance(expression.arg2) and and_elem.isinstance(expression.arg2.arg2) and
            expression.arg1.eque(expression.arg2.arg2.arg1) and expression.arg2.arg1.eque(expression.arg2.arg2.arg2)
        ):
            return True

        return False

    def A7(self, expression):
        or_elem = Or(Var("A"), Var("B"))
        arrow_elem = Arrow(Var("C"), Var("D"))

        if arrow_elem.isinstance(expression) and or_elem.isinstance(expression.arg2) and expression.arg1.eque(expression.arg2.arg1):
            return True

        return False

    def A8(self, expression):
        or_elem = Or(Var("A"), Var("B"))
        arrow_elem = Arrow(Var("C"), Var("D"))

        if arrow_elem.isinstance(expression) and or_elem.isinstance(expression.arg2) and expression.arg1.eque(expression.arg2.arg2):
            return True

        return False

    def A9(self, expression):
        or_elem = Or(Var("A"), Var("B"))
        arrow_elem = Arrow(Var("C"), Var("D"))

        if (
            arrow_elem.isinstance(expression) and arrow_elem.isinstance(expression.arg1) and arrow_elem.isinstance(expression.arg2) and
            arrow_elem.isinstance(expression.arg2.arg1) and arrow_elem.isinstance(expression.arg2.arg2) and or_elem.isinstance(expression.arg2.arg2.arg1) and
            expression.arg1.arg1.eque(expression.arg2.arg2.arg1.arg1) and expression.arg2.arg1.arg1.eque(expression.arg2.arg2.arg1.arg2) and
            expression.arg1.arg2.eque(expression.arg2.arg1.arg2) and expression.arg1.arg2.eque(expression.arg2.arg2.arg2)
        ):
            return True

        return False

    def A10(self, expression):
        not_elem = Not(Var("A"))
        arrow_elem = Arrow(Var("C"), Var("D"))

        if (
            arrow_elem.isinstance(expression) and not_elem.isinstance(expression.arg1) and arrow_elem.isinstance(expression.arg2)
            and expression.arg1.eque_exclude_not(expression.arg2.arg1)
        ):
            return True

        return False

    def A11(self, expression):
        or_elem = Or(Var("A"), Var("B"))
        not_elem = Not(Var("C"))
        #print(expression.arg2.eque(expression.arg1), expression.arg2, 'eq', expression.arg1)

        if or_elem.isinstance(expression) and not_elem.isinstance(expression.arg2) and expression.arg2.eque(expression.arg1):
            return True

        return False



class BasicAxiom():
    def __init__(self):
        self.count = 0

    # A→(B→A)
    def A1(self, expression):
        A = Arrow(Var("X"), Var("Y"))
        if A.isinstance(expression) and A.isinstance(expression.arg2) and expression.arg2.arg2.eque(expression.arg1):
            return True
        return False

    def generateA1(self, A, B):
        return Arrow(A, Arrow(B, A))


    # ((A→(B→C))→((A→B)→(A→C)))
    def A2(self, expression):
        arrow_elem = Arrow(Var("C"), Var("D"))
        if arrow_elem.isinstance(expression) and arrow_elem.isinstance(expression.arg1)\
            and arrow_elem.isinstance(expression.arg2) and arrow_elem.isinstance(expression.arg1.arg2)\
                and arrow_elem.isinstance(expression.arg2.arg1) and arrow_elem.isinstance(expression.arg2.arg2)\
                    and expression.arg1.arg1.eque(expression.arg2.arg1.arg1) and expression.arg1.arg1.eque(expression.arg2.arg2.arg1)\
                        and expression.arg1.arg2.arg1.eque(expression.arg2.arg1.arg2) and  expression.arg1.arg2.arg2.eque(expression.arg2.arg2.arg2):
            return True
        return False

    def generateA2(self, A, B, C):
        return Arrow(Arrow(A, Arrow(B, C)), Arrow(Arrow(A, B), Arrow(A, C)))


    # ((⅂B→⅂A)→((⅂B→A)→B))
    def A3(self, expression):
        arrow_elem = Arrow(Var("C"), Var("D"))
        not_elem = Not(Var("A"), Var("B"))
        if arrow_elem.isinstance(expression) and arrow_elem.isinstance(expression.arg1)\
            and arrow_elem.isinstance(expression.arg2) and arrow_elem.isinstance(expression.arg2.arg1)\
                and not_elem.isinstance(expression.arg1.arg1) and not_elem.isinstance(expression.arg1.arg2)\
                    and not_elem.isinstance(expression.arg2.arg1.arg1)\
                        and expression.arg1.arg1.arg.eque(expression.arg2.arg1.arg1.arg)\
                            and expression.arg1.arg1.arg.eque(expression.arg2.arg2)\
                                and expression.arg1.arg2.arg.eque(expression.arg2.arg1.arg2):
            return True
        return False

    def generateA3(self, A, B):
        return Arrow(Arrow(Not(B), Not(A)), Arrow(Arrow(Not(B), A), B))
