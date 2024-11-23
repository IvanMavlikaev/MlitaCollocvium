import pytest

from app import parse
from app.terms import And, Var, Not


class TestConjunction:

    def test_basic_conjunction(self):
        # Проверка строкового представления
        expr = And(Var('A'), Var('B'))
        assert str(expr) == 'A * B'

        # Проверка через парсер
        parsed_expr = parse('A * B')
        assert parsed_expr.eque(expr)

    def test_conjunction_translation(self):
        expr = And(Var('A'), Var('B'))
        assert expr.translate() == 'A и B'

        # Проверка с отрицанием
        expr_with_not = And(Not(Var('A')), Var('B'))
        assert expr_with_not.translate() == 'не A и B'

    def test_implication_negation_form(self):
        expr = And(Var('A'), Var('B'))
        impl_neg = expr.implication_negation()
        assert str(impl_neg) == '!(A > !B)'

        # Проверка с отрицанием
        expr_with_not = And(Not(Var('A')), Var('B'))
        impl_neg_with_not = expr_with_not.implication_negation()
        assert str(impl_neg_with_not) == '!(!A > !B)'

    def test_complex_conjunction(self):
        # Конъюнкция с тремя переменными
        expr = And(And(Var('A'), Var('B')), Var('C'))
        assert str(expr) == '(A * B) * C'
        assert expr.translate() == '(A и B) и C'

        # Конъюнкция с отрицаниями
        expr = And(Not(Var('A')), Not(Var('B')))
        assert str(expr) == '!A * !B'
        assert expr.translate() == 'не A и не B'

    def test_nested_conjunction(self):
        expr = parse('(A * B) * (C * D)')
        assert isinstance(expr, And)
        assert isinstance(expr.arg1, And)
        assert isinstance(expr.arg2, And)
        assert str(expr) == '(A * B) * (C * D)'

    def test_conjunction_with_variables(self):
        variables = ['A', 'B', 'C', 'D', 'E']
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                expr = And(Var(variables[i]), Var(variables[j]))
                assert str(expr) == f'{variables[i]} * {variables[j]}'
                assert expr.translate() == f'{variables[i]} и {variables[j]}'

    def test_conjunction_properties(self):
        expr1 = parse('A * A')  # Идемпотентность
        expr2 = And(Var('A'), Var('A'))
        assert expr1.eque(expr2)

        # Коммутативность не поддерживается в текущей реализации
        expr1 = parse('A * B')
        expr2 = parse('B * A')
        assert not expr1.eque(expr2)

    def test_conjunction_with_nested_operations(self):
        expr = parse('(!A * B) * (C * !D)')
        assert isinstance(expr, And)
        assert str(expr) == '(!A * B) * (C * !D)'
        assert expr.translate() == '(не A и B) и (C и не D)'

    @pytest.mark.parametrize("test_input,expected_str,expected_translation", [
        ("A * B", "A * B", "A и B"),
        ("!A * B", "!A * B", "не A и B"),
        ("A * !B", "A * !B", "A и не B"),
        ("!A * !B", "!A * !B", "не A и не B"),
    ])
    def test_conjunction_patterns(self, test_input, expected_str, expected_translation):
        expr = parse(test_input)
        assert str(expr) == expected_str
        assert expr.translate() == expected_translation


if __name__ == '__main__':
    pytest.main([__file__, '-v'])