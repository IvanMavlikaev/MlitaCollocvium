from .term import Term
from app.utils import is_unar_operator
from .operator import Operator



class BinaryOperator(Operator):
    _symbol: str

    def __init__(self, arg1: Term, arg2: Term) -> None:
        super().__init__(arg1, arg2)

    def __str__(self):
        if is_unar_operator(self.arg1):
            left = str(self.arg1)
        else:
            left = f'({self.arg1})'

        if is_unar_operator(self.arg2):
            right = str(self.arg2)
        else:
            right = f'({self.arg2})'

        return f'{left} {self._symbol} {right}'

    @property
    def arg1(self) -> Term:
        return self._args[0]

    @arg1.setter
    def arg1(self, value: Term) -> None:
        self._args[0] = value

    @property
    def arg2(self) -> Term:
        return self._args[1]

    @arg2.setter
    def arg2(self, value: Term) -> None:
        self._args[1] = value
