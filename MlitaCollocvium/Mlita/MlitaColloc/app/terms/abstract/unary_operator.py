from app.terms.abstract.term import Term
from .operator import Operator


class UnaryOperator(Operator):
    def __init__(self, arg: Term) -> None:
        super().__init__(arg)

    @property
    def arg(self) -> Term:
        return self._args[0]

    @arg.setter
    def arg(self, value: Term) -> None:
        self._args[0] = value

