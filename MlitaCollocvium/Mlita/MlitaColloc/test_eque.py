import pytest
from app.terms import Equal, Var, Not, And, Or
from app import parse


class TestEquivalence:
    """Tests for equivalence operations"""

    def test_basic_equivalence(self):
        """Test basic equivalence creation and string representation"""
        # Простая эквивалентность
        expr = Equal(Var('A'), Var('B'))
        assert str(expr) == 'A = B'

        # Эквивалентность через парсер
        parsed_expr = parse('A = B')
        assert str(parsed_expr) == 'A = B'
        assert parsed_expr.eque(expr)

    def test_equivalence_translation(self):
        """Test Russian translation of equivalence expressions"""
        # Простая эквивалентность
        expr = Equal(Var('A'), Var('B'))
        assert expr.translate() == 'A эквивалентно B'

        # Эквивалентность с отрицанием
        expr = Equal(Not(Var('A')), Var('B'))
        assert expr.translate() == 'не A эквивалентно B'

        expr = Equal(Var('A'), Not(Var('B')))
        assert expr.translate() == 'A эквивалентно не B'

        # Эквивалентность с двумя отрицаниями
        expr = Equal(Not(Var('A')), Not(Var('B')))
        assert expr.translate() == 'не A эквивалентно не B'

    def test_equivalence_with_complex_terms(self):
        """Test equivalence with complex expressions"""
        # Эквивалентность с конъюнкцией
        expr = Equal(And(Var('A'), Var('B')), Var('C'))
        assert str(expr) == '(A * B) = C'
        assert expr.translate() == '(A и B) эквивалентно C'

        # Эквивалентность с дизъюнкцией
        expr = Equal(Var('A'), Or(Var('B'), Var('C')))
        assert str(expr) == 'A = (B | C)'
        assert expr.translate() == 'A эквивалентно (B или C)'

        # Сложное выражение с обеих сторон
        expr = Equal(And(Var('A'), Var('B')), Or(Var('C'), Var('D')))
        assert str(expr) == '(A * B) = (C | D)'
        assert expr.translate() == '(A и B) эквивалентно (C или D)'

    def test_equivalence_equality(self):
        """Test equality of equivalence expressions"""
        # Одинаковые выражения
        expr1 = Equal(Var('A'), Var('B'))
        expr2 = Equal(Var('A'), Var('B'))
        assert expr1.eque(expr2)

        # Разные выражения
        expr3 = Equal(Var('B'), Var('C'))
        assert not expr1.eque(expr3)

        # Эквивалентность с одинаковыми сложными выражениями
        expr4 = Equal(And(Var('A'), Var('B')), Var('C'))
        expr5 = Equal(And(Var('A'), Var('B')), Var('C'))
        assert expr4.eque(expr5)

        # Порядок важен
        expr6 = Equal(Var('B'), Var('A'))
        assert not expr1.eque(expr6)

    def test_equivalence_implication_negation(self):
        """Test conversion of equivalence to implication-negation form"""
        # Простая эквивалентность
        expr = Equal(Var('A'), Var('B'))
        impl_neg = expr.implication_negation()
        assert isinstance(impl_neg, Not)

        # Эквивалентность с отрицанием
        expr = Equal(Not(Var('A')), Var('B'))
        impl_neg = expr.implication_negation()
        assert isinstance(impl_neg, Not)

        # Проверка, что результат содержит только импликации и отрицания
        result_str = str(impl_neg)
        assert '=' not in result_str
        assert '*' not in result_str
        assert '|' not in result_str
        assert all(op in ['>', '!', '(', ')'] or op.isalpha() or op.isspace() for op in result_str)

    def test_isinstance_check(self):
        """Test isinstance checks for equivalence"""
        expr = Equal(Var('A'), Var('B'))

        # Проверка с тем же типом
        assert expr.isinstance(expr)
        assert expr.isinstance(Equal(Var('C'), Var('D')))

        # Проверка с другими типами
        assert not expr.isinstance(And(Var('A'), Var('B')))
        assert not expr.isinstance(Or(Var('A'), Var('B')))
        assert not expr.isinstance(Not(Var('A')))

    @pytest.mark.parametrize("expr1,expr2,expected", [
        ('A = B', 'A = B', True),
        ('A = B', 'B = A', False),  # Порядок важен
        ('!A = B', '!A = B', True),
        ('A = B', 'A = C', False),
        ('(A * B) = C', '(A * B) = C', True),
        ('A = (B | C)', 'A = (B | C)', True),
        ('(A * B) = (C | D)', '(C | D) = (A * B)', False),
    ])
    def test_equivalence_patterns(self, expr1, expr2, expected):
        """Test various equivalence patterns"""
        parsed1 = parse(expr1)
        parsed2 = parse(expr2)
        assert parsed1.eque(parsed2) == expected

    def test_nested_equivalence(self):
        """Test nested equivalence expressions"""
        # Вложенные выражения
        expr = Equal(
            Equal(Var('A'), Var('B')),
            Equal(Var('C'), Var('D'))
        )
        assert isinstance(expr, Equal)
        assert isinstance(expr.arg1, Equal)
        assert isinstance(expr.arg2, Equal)

        # Проверка строкового представления
        assert str(expr) == '(A = B) = (C = D)'

        # Проверка перевода
        assert expr.translate() == '(A эквивалентно B) эквивалентно (C эквивалентно D)'

    def test_equivalence_with_parentheses(self):
        """Test equivalence with different parentheses combinations"""
        # Простые выражения не требуют скобок
        expr1 = Equal(Var('A'), Var('B'))
        assert str(expr1) == 'A = B'

        # Сложные выражения требуют скобок
        expr2 = Equal(And(Var('A'), Var('B')), Or(Var('C'), Var('D')))
        assert str(expr2) == '(A * B) = (C | D)'

        # Отрицания не требуют скобок
        expr3 = Equal(Not(Var('A')), Not(Var('B')))
        assert str(expr3) == '!A = !B'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])