from .abstract.term import Term
from copy import copy


class Var(Term):
    """Boolean variable class"""

    def __init__(self, char: str):
        self.name = char

    def __copy__(self) -> 'Var':
        return self.__class__(self.name)

    def __deepcopy__(self, memo):
        return copy(self)

    def __str__(self):
        return self.name

    def translate(self):
        return str(self)

    def substitute(self, **kwargs: dict[str, Term]) -> Term:
        return kwargs.get(self.name, self.copy())

    def implication_negation(self):
        return copy(self)

    def eque(self, other_term: Term) -> bool:
        return self.translate() == other_term.translate()