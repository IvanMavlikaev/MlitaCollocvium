import pytest
from app.terms import Xor, Var, Not, And, Or
from app import parse


class TestXor:
    """Tests for XOR operations"""

    def test_basic_xor(self):
        """Test basic XOR creation and string representation"""
        # Простой XOR
        expr = Xor(Var('A'), Var('B'))
        assert str(expr) == 'A + B'

        # XOR через парсер
        parsed_expr = parse('A + B')
        assert str(parsed_expr) == 'A + B'
        assert parsed_expr.eque(expr)

    def test_xor_translation(self):
        """Test Russian translation of XOR expressions"""
        # Простой XOR
        expr = Xor(Var('A'), Var('B'))
        assert expr.translate() == 'либо A, либо B'

        # XOR с отрицанием
        expr = Xor(Not(Var('A')), Var('B'))
        assert expr.translate() == 'либо не A, либо B'

        # XOR с двумя отрицаниями
        expr = Xor(Not(Var('A')), Not(Var('B')))
        assert expr.translate() == 'либо не A, либо не B'

    def test_xor_with_complex_terms(self):
        """Test XOR with complex expressions"""
        # XOR с конъюнкцией
        expr = Xor(And(Var('A'), Var('B')), Var('C'))
        assert str(expr) == '(A * B) + C'
        assert expr.translate() == 'либо (A и B), либо C'

        # XOR с дизъюнкцией
        expr = Xor(Var('A'), Or(Var('B'), Var('C')))
        assert str(expr) == 'A + (B | C)'
        assert expr.translate() == 'либо A, либо (B или C)'

    def test_xor_equality(self):
        """Test equality of XOR expressions"""
        # Одинаковые выражения
        expr1 = Xor(Var('A'), Var('B'))
        expr2 = Xor(Var('A'), Var('B'))
        assert expr1.eque(expr2)

        # Разные выражения
        expr3 = Xor(Var('B'), Var('C'))
        assert not expr1.eque(expr3)

        # XOR с одинаковыми сложными выражениями
        expr4 = Xor(And(Var('A'), Var('B')), Var('C'))
        expr5 = Xor(And(Var('A'), Var('B')), Var('C'))
        assert expr4.eque(expr5)

    def test_xor_implication_negation(self):
        """Test conversion of XOR to implication-negation form"""
        # Простой XOR
        expr = Xor(Var('A'), Var('B'))
        impl_neg = expr.implication_negation()
        assert isinstance(impl_neg, Not)

        # XOR с отрицанием
        expr = Xor(Not(Var('A')), Var('B'))
        impl_neg = expr.implication_negation()
        assert isinstance(impl_neg, Not)

        # Проверка, что результат содержит только импликации и отрицания
        result_str = str(impl_neg)
        assert '+' not in result_str
        assert '*' not in result_str
        assert '|' not in result_str
        assert all(op in ['>', '!', '(', ')'] or op.isalpha() or op.isspace() for op in result_str)

    def test_isinstance_check(self):
        """Test isinstance checks for XOR"""
        expr = Xor(Var('A'), Var('B'))

        # Проверка с тем же типом
        assert expr.isinstance(expr)
        assert expr.isinstance(Xor(Var('C'), Var('D')))

        # Проверка с другими типами
        assert not expr.isinstance(And(Var('A'), Var('B')))
        assert not expr.isinstance(Or(Var('A'), Var('B')))
        assert not expr.isinstance(Not(Var('A')))

    @pytest.mark.parametrize("expr1,expr2,expected", [
        ('A + B', 'A + B', True),
        ('A + B', 'B + A', False),  # Порядок важен
        ('!A + B', '!A + B', True),
        ('A + B', 'A + C', False),
        ('(A * B) + C', '(A * B) + C', True),
        ('(A * B) + C', 'A + C', False),
    ])
    def test_xor_patterns(self, expr1, expr2, expected):
        """Test various XOR patterns"""
        parsed1 = parse(expr1)
        parsed2 = parse(expr2)
        assert parsed1.eque(parsed2) == expected

    def test_nested_xor(self):
        """Test nested XOR expressions"""
        # Вложенный XOR
        expr = parse('A + (B + C)')
        assert isinstance(expr, Xor)
        assert isinstance(expr.arg2, Xor)

        # Проверка строкового представления
        assert str(expr) == 'A + (B + C)'

        # Проверка перевода
        assert expr.translate() == 'либо A, либо (либо B, либо C)'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])