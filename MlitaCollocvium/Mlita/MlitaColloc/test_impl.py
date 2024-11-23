import pytest
from app import parse
from app.terms import Arrow, Var, Not, And, Or


class TestImplication:

    def test_basic_implication(self):
        # Проверка строкового представления
        expr = Arrow(Var('A'), Var('B'))
        assert str(expr) == 'A > B'

        # Проверка через парсер
        parsed_expr = parse('A > B')
        assert parsed_expr.eque(expr)

    def test_implication_translation(self):
        # Базовая импликация
        expr = Arrow(Var('A'), Var('B'))
        assert expr.translate() == 'если A, то B'

        # Импликация с отрицанием
        expr = Arrow(Not(Var('A')), Var('B'))
        assert expr.translate() == 'если не A, то B'

        expr = Arrow(Var('A'), Not(Var('B')))
        assert expr.translate() == 'если A, то не B'

    def test_implication_negation_form(self):
        # Базовая импликация уже в форме импликации-отрицания
        expr = Arrow(Var('A'), Var('B'))
        impl_neg = expr.implication_negation()
        assert str(impl_neg) == 'A > B'

        # Импликация с отрицанием
        expr = Arrow(Not(Var('A')), Var('B'))
        impl_neg = expr.implication_negation()
        assert str(impl_neg) == '!A > B'

    def test_complex_implication(self):
        # Импликация с тремя переменными
        expr = Arrow(Arrow(Var('A'), Var('B')), Var('C'))
        assert str(expr) == '(A > B) > C'
        assert expr.translate() == 'если (если A, то B), то C'

        # Импликация с отрицаниями
        expr = Arrow(Not(Var('A')), Not(Var('B')))
        assert str(expr) == '!A > !B'
        assert expr.translate() == 'если не A, то не B'

    def test_nested_implication(self):
        # Тест вложенных импликаций
        expr = parse('(A > B) > (C > D)')
        assert isinstance(expr, Arrow)
        assert isinstance(expr.arg1, Arrow)
        assert isinstance(expr.arg2, Arrow)
        assert str(expr) == '(A > B) > (C > D)'

    def test_implication_with_different_variables(self):
        variables = ['A', 'B', 'C', 'D', 'E']
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                expr = Arrow(Var(variables[i]), Var(variables[j]))
                assert str(expr) == f'{variables[i]} > {variables[j]}'
                assert expr.translate() == f'если {variables[i]}, то {variables[j]}'

    def test_implication_with_other_operations(self):
        # Импликация с конъюнкцией
        expr = parse('(A * B) > C')
        assert isinstance(expr, Arrow)
        assert isinstance(expr.arg1, And)
        assert str(expr) == '(A * B) > C'

        # Импликация с дизъюнкцией
        expr = parse('A > (B | C)')
        assert isinstance(expr, Arrow)
        assert isinstance(expr.arg2, Or)
        assert str(expr) == 'A > (B | C)'

    @pytest.mark.parametrize("test_input,expected_str,expected_translation", [
        ("A > B", "A > B", "если A, то B"),
        ("!A > B", "!A > B", "если не A, то B"),
        ("A > !B", "A > !B", "если A, то не B"),
        ("!A > !B", "!A > !B", "если не A, то не B"),
        ("(A > B) > C", "(A > B) > C", "если (если A, то B), то C"),
        ("A > (B > C)", "A > (B > C)", "если A, то (если B, то C)"),
    ])

    def test_implication_patterns(self, test_input, expected_str, expected_translation):
        expr = parse(test_input)
        assert str(expr) == expected_str
        assert expr.translate() == expected_translation

    def test_implication_precedence(self):
        # Импликация имеет низкий приоритет
        expr = parse('A * B > C')
        assert isinstance(expr, Arrow)
        assert isinstance(expr.arg1, And)
        assert isinstance(expr.arg2, Var)

        expr = parse('A > B * C')
        assert isinstance(expr, Arrow)
        assert isinstance(expr.arg1, Var)
        assert isinstance(expr.arg2, And)

    def test_implication_associativity(self):
        # A > (B > C) не эквивалентно (A > B) > C
        expr1 = parse('A > (B > C)')
        expr2 = parse('(A > B) > C')
        assert not expr1.eque(expr2)

    def test_invalid_implication(self):
        # Пропущенный операнд справа
        with pytest.raises(Exception):
            parse("A >")

        # Пропущенный операнд слева
        with pytest.raises(Exception):
            parse("> B")

        # Неправильный синтаксис
        with pytest.raises(Exception):
            parse("A > > B")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])