import pytest
from app import parse
from app.terms import Or, And, Var, Not


class TestDisjunction:

    def test_basic_disjunction(self):
        # Проверка строкового представления
        expr = Or(Var('A'), Var('B'))
        assert str(expr) == 'A | B'

        # Проверка через парсер
        parsed_expr = parse('A | B')
        assert parsed_expr.eque(expr)

    def test_disjunction_translation(self):
        # Базовая дизъюнкция
        expr = Or(Var('A'), Var('B'))
        assert expr.translate() == 'A или B'

        # Дизъюнкция с отрицанием
        expr_with_not = Or(Not(Var('A')), Var('B'))
        assert expr_with_not.translate() == 'не A или B'

    def test_implication_negation_form(self):
        # Базовая дизъюнкция
        expr = Or(Var('A'), Var('B'))
        impl_neg = expr.implication_negation()
        assert str(impl_neg) == '!A > B'

        # Дизъюнкция с отрицанием
        expr_with_not = Or(Not(Var('A')), Var('B'))
        impl_neg_with_not = expr_with_not.implication_negation()
        assert str(impl_neg_with_not) == '!!A > B'

    def test_complex_disjunction(self):
        # Дизъюнкция с тремя переменными
        expr = Or(Or(Var('A'), Var('B')), Var('C'))
        assert str(expr) == '(A | B) | C'
        assert expr.translate() == '(A или B) или C'

        # Дизъюнкция с отрицаниями
        expr = Or(Not(Var('A')), Not(Var('B')))
        assert str(expr) == '!A | !B'
        assert expr.translate() == 'не A или не B'

    def test_nested_disjunction(self):
        expr = parse('(A | B) | (C | D)')
        assert isinstance(expr, Or)
        assert isinstance(expr.arg1, Or)
        assert isinstance(expr.arg2, Or)
        assert str(expr) == '(A | B) | (C | D)'

    def test_disjunction_with_variables(self):
        variables = ['A', 'B', 'C', 'D', 'E']
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                expr = Or(Var(variables[i]), Var(variables[j]))
                assert str(expr) == f'{variables[i]} | {variables[j]}'
                assert expr.translate() == f'{variables[i]} или {variables[j]}'

    def test_disjunction_properties(self):
        # Идемпотентность
        expr1 = parse('A | A')
        expr2 = Or(Var('A'), Var('A'))
        assert expr1.eque(expr2)

        # Коммутативность не поддерживается в текущей реализации
        expr1 = parse('A | B')
        expr2 = parse('B | A')
        assert not expr1.eque(expr2)

    def test_disjunction_with_nested_operations(self):
        expr = parse('(!A | B) | (C | !D)')
        assert isinstance(expr, Or)
        assert str(expr) == '(!A | B) | (C | !D)'
        assert expr.translate() == '(не A или B) или (C или не D)'

    @pytest.mark.parametrize("test_input,expected_str,expected_translation", [
        ("A | B", "A | B", "A или B"),
        ("!A | B", "!A | B", "не A или B"),
        ("A | !B", "A | !B", "A или не B"),
        ("!A | !B", "!A | !B", "не A или не B"),
        ("(A | B) | C", "(A | B) | C", "(A или B) или C"),
        ("A | (B | C)", "A | (B | C)", "A или (B или C)"),
    ])
    def test_disjunction_patterns(self, test_input, expected_str, expected_translation):
        expr = parse(test_input)
        assert str(expr) == expected_str
        assert expr.translate() == expected_translation

    def test_disjunction_precedence(self):
        # Проверяем приоритет операторов
        expr = parse('A | B * C')
        assert isinstance(expr, Or)
        assert isinstance(expr.arg1, Var)  # Первый аргумент должен быть переменной A
        assert isinstance(expr.arg2, And)  # Второй аргумент должен быть конъюнкцией B * C

        # Проверка с отрицанием
        expr = parse('!A | B')
        assert isinstance(expr, Or)
        assert isinstance(expr.arg1, Not)

    def test_invalid_disjunction(self):
        # Проверка на неправильное количество операндов
        with pytest.raises(Exception):
            parse("A |")

        # Проверка на неправильный синтаксис
        with pytest.raises(Exception):
            parse("| A")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])