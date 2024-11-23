import pytest
from app.terms import Or, And, Var, Not, Arrow
from app import parse
from axioms import Axiom, BasicAxiom


class TestBasicAxioms:
    """Tests for basic axioms (A1-A3)"""

    def setup_method(self):
        """Setup for each test method"""
        self.basic_axiom = BasicAxiom()
        self.axiom = Axiom()

    def test_generate_A1(self):
        """Test generation of axiom A1: A→(B→A)"""
        # Тест с простыми переменными
        result = self.basic_axiom.generateA1(Var('A'), Var('B'))
        assert isinstance(result, Arrow)
        assert str(result) == "A > (B > A)"
        assert result.translate() == "если A, то (если B, то A)"

        # Тест с другими переменными
        result = self.basic_axiom.generateA1(Var('P'), Var('Q'))
        assert str(result) == "P > (Q > P)"

        # Тест со сложными выражениями
        expr1 = And(Var('A'), Var('B'))
        expr2 = Or(Var('C'), Var('D'))
        result = self.basic_axiom.generateA1(expr1, expr2)
        assert isinstance(result, Arrow)
        assert isinstance(result.arg2, Arrow)
        assert str(result) == "(A * B) > ((C | D) > (A * B))"

    def test_generate_A2(self):
        """Test generation of axiom A2: ((A→(B→C))→((A→B)→(A→C)))"""
        # Тест с простыми переменными
        result = self.basic_axiom.generateA2(Var('A'), Var('B'), Var('C'))
        assert isinstance(result, Arrow)
        assert str(result) == "(A > (B > C)) > ((A > B) > (A > C))"

        # Тест с другими переменными
        result = self.basic_axiom.generateA2(Var('P'), Var('Q'), Var('R'))
        assert str(result) == "(P > (Q > R)) > ((P > Q) > (P > R))"

        # Тест со сложными выражениями
        expr1 = And(Var('X'), Var('Y'))
        expr2 = Or(Var('Z'), Var('W'))
        expr3 = Not(Var('V'))
        result = self.basic_axiom.generateA2(expr1, expr2, expr3)
        assert isinstance(result, Arrow)
        assert str(result) == "((X * Y) > ((Z | W) > !V)) > (((X * Y) > (Z | W)) > ((X * Y) > !V))"

    def test_generate_A3(self):
        """Test generation of axiom A3: ((⅂B→⅂A)→((⅂B→A)→B))"""
        # Тест с простыми переменными
        result = self.basic_axiom.generateA3(Var('A'), Var('B'))
        assert isinstance(result, Arrow)
        assert str(result) == "(!B > !A) > ((!B > A) > B)"

        # Тест с другими переменными
        result = self.basic_axiom.generateA3(Var('P'), Var('Q'))
        assert str(result) == "(!Q > !P) > ((!Q > P) > Q)"

        # Тест со сложными выражениями
        expr1 = And(Var('X'), Var('Y'))
        expr2 = Or(Var('Z'), Var('W'))
        result = self.basic_axiom.generateA3(expr1, expr2)
        assert isinstance(result, Arrow)
        assert str(result) == "(!(Z | W) > !(X * Y)) > ((!(Z | W) > (X * Y)) > (Z | W))"

    def test_verification_of_generated_axioms(self):
        """Test that generated axioms verify correctly"""
        # A1
        a1_result = self.basic_axiom.generateA1(Var('A'), Var('B'))
        assert self.basic_axiom.A1(a1_result)

        # Verify A1 with complex expressions
        complex_a1 = self.basic_axiom.generateA1(And(Var('X'), Var('Y')), Not(Var('Z')))
        assert str(complex_a1) == "(X * Y) > (!Z > (X * Y))"
        assert self.basic_axiom.A1(complex_a1)

    def test_generate_nested_axioms(self):
        """Test generation of nested axioms"""
        # Generate A1 inside A2
        inner_a1 = self.basic_axiom.generateA1(Var('A'), Var('B'))
        result = self.basic_axiom.generateA2(inner_a1, Var('C'), Var('D'))
        assert isinstance(result, Arrow)
        assert isinstance(result.arg1, Arrow)

        # Generate A2 with A1 components
        a1_expr = self.basic_axiom.generateA1(Var('X'), Var('Y'))
        result = self.basic_axiom.generateA2(a1_expr, Var('P'), Var('Q'))
        assert isinstance(result, Arrow)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])