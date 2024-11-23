import pytest
from app.terms import Or, And, Var, Not, Arrow, Equal, Xor
from app.parser import parse


class TestParser:

    def test_basic_disjunction(self):
        s = "A | B"
        or_elem = Or(Var("A"), Var("B"))
        assert parse(s).eque(or_elem)
        assert str(parse(s)) == "A | B"

    def test_basic_conjunction(self):
        s = "A * B"
        and_elem = And(Var("A"), Var("B"))
        assert parse(s).eque(and_elem)
        assert str(parse(s)) == "A * B"

    def test_basic_implication(self):
        s = "A > B"
        impl_elem = Arrow(Var("A"), Var("B"))
        assert parse(s).eque(impl_elem)
        assert str(parse(s)) == "A > B"

    def test_basic_negation(self):
        s = "!A"
        not_elem = Not(Var("A"))
        assert parse(s).eque(not_elem)
        assert str(parse(s)) == "!A"

    def test_parentheses(self):
        s = "(A | B)"
        or_elem = Or(Var("A"), Var("B"))
        assert parse(s).eque(or_elem)

        s = "(A * B)"
        and_elem = And(Var("A"), Var("B"))
        assert parse(s).eque(and_elem)

    def test_complex_expression(self):
        s = "A | (B * C)"
        expr = parse(s)
        assert isinstance(expr, Or)
        assert isinstance(expr.arg2, And)

        s = "(A | B) * C"
        expr = parse(s)
        assert isinstance(expr, And)
        assert isinstance(expr.arg1, Or)

    def test_operator_precedence(self):
        s = "A * B | C"
        expr = parse(s)
        assert isinstance(expr, Or)
        assert isinstance(expr.arg1, And)

        s = "A > B * C"
        expr = parse(s)
        assert isinstance(expr, Arrow)
        assert isinstance(expr.arg2, And)

    def test_nested_expressions(self):
        s = "((A | B) * C) | D"
        expr = parse(s)
        assert isinstance(expr, Or)
        assert isinstance(expr.arg1, And)
        assert isinstance(expr.arg1.arg1, Or)

    def test_invalid_expressions(self):
        invalid_expressions = [
            "A |",  # Incomplete
            "| A",  # Missing left operand
            "(A | B",  # Unclosed parenthesis
            "A || B",  # Double operator
            "A B",  # Missing operator
        ]
        for expr in invalid_expressions:
            with pytest.raises(Exception):
                parse(expr)

    def test_whitespace(self):
        variants = [
            "A|B",
            "A | B",
            " A | B ",
            "A  |  B"
        ]
        expected = Or(Var("A"), Var("B"))
        for expr in variants:
            assert parse(expr).eque(expected)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])