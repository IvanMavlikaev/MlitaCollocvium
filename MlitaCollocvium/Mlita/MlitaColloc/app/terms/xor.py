from .abstract import BinaryOperator
from .implication import Arrow
from .negation import Not
from .abstract.term import Term
from app.utils import is_unar_operator


class Xor(BinaryOperator):
    _symbol = '+'

    def translate(self) -> str:
        if is_unar_operator(self.arg1):
            left = str(self.arg1.translate())
        else:
            left = f'({self.arg1.translate()})'

        if is_unar_operator(self.arg2):
            right = str(self.arg2.translate())
        else:
            right = f'({self.arg2.translate()})'
        return f'либо {left}, либо {right}'

    def implication_negation(self):
        return Not(
            Arrow(
                Arrow(
                    Not(self.arg1.implication_negation()),
                    self.arg2.implication_negation()
                ),
                Not(
                    Arrow(
                        self.arg1.implication_negation(),
                        Not(self.arg2.implication_negation())
                    )
                )
            )
        )

    def isinstance(self, object) -> bool:
        """Проверка на принадлежность к тому же классу"""
        return type(self) == type(object)

    def eque(self, other_term: Term) -> bool:
        """Сравнение двух объектов Xor по их аргументам"""
        if not isinstance(other_term, Xor):
            return False
        return (self.arg1.translate() == other_term.arg1.translate() and
                self.arg2.translate() == other_term.arg2.translate())