from app.utils import is_unar_operator
from .abstract.unary_operator import UnaryOperator
from .variable import Var
from .abstract.term import Term
from copy import copy

class Not(UnaryOperator):
    def __str__(self) -> str:
        if is_unar_operator(self.arg):
            return f'!{self.arg}'
        return f'!({self.arg})'

    def translate(self):
        if isinstance(self.arg, Var):
            return f'не {self.arg.translate()}'
        return f'не ({self.arg.translate()})'

    def implication_negation(self) -> 'Not':
        return self.__class__(self.arg.implication_negation())

    def eque(self, other_term: Term) -> bool:
        """Сравнение с другим термом по переводу"""
        return isinstance(other_term, Not) and self.arg.translate() == other_term.arg.translate()
    
    def eque_exclude_not(self, other_term: Term) -> bool:
        """Сравнение с другим термом без учета нот по переводу"""
        return f'{self.arg}' == f'{other_term}'

    def isinstance(self, object):
        """Проверка на принадлежность к тому же типу"""
        if type(self) == type(object):
            return True
        return False