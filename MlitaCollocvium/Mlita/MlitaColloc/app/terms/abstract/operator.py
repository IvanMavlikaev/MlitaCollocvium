from .term import Term
from collections import UserList
from copy import deepcopy


class TermList(UserList[Term]):
    def translate(self) -> list[str]:
        """String in russian language"""
        return [term.translate() for term in self.data]

    def implication_negation(self) -> 'TermList':
        """Equivalent term using only implication and negation"""
        return TermList(term.implication_negation() for term in self.data)

    def substitute(self, **kwargs: dict[str, 'Term']) -> 'TermList':
        return TermList(term.substitute(**kwargs) for term in self.data)


class Operator(Term):
    """Boolean function abstract class"""

    _args: TermList

    def __init__(self, *args: tuple[Term]) -> None:
        self._args = TermList()
        for arg in args:
            if not isinstance(arg, Term):
                TypeError('Аргумент оператора должен быть Term или str')
            self._args.append(arg)

    def __copy__(self):
        raise NotImplementedError(
            'Оператор не подлежит копированию. Используйте вместо него deepcopy'
        )

    def __deepcopy__(self, memo) -> 'Term':
        return self.__class__(*deepcopy(self._args))

    def substitute(self, **kwargs: dict[str, 'Term']) -> Term:
        return self.__class__(*self._args.substitute(**kwargs))