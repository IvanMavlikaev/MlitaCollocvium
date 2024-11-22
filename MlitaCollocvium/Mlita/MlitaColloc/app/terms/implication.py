from .abstract import BinaryOperator
from app.utils.is_unar_operator import is_unar_operator
from .abstract.term import Term

class Arrow(BinaryOperator):
    _symbol = '>'

    def translate(self) -> str:
        if is_unar_operator(self.arg1):
            left = str(self.arg1.translate())
        else:
            left = f'({self.arg1.translate()})'

        if is_unar_operator(self.arg2):
            right = str(self.arg2.translate())
        else:
            right = f'({self.arg2.translate()})'

        return f'если {left}, то {right}'

    def implication_negation(self) -> 'Arrow':
        return self.__class__(*self._args.implication_negation())

    def isinstance(self, object) -> bool:
        """Проверка на принадлежность к тому же классу"""
        return type(self) == type(object)

    def eque(self, other_term: Term) -> bool:
        """Сравнение двух объектов Arrow по их аргументам"""
        if not isinstance(other_term, Arrow):
            return False
        return (self.arg1.translate() == other_term.arg1.translate() and
                self.arg2.translate() == other_term.arg2.translate())