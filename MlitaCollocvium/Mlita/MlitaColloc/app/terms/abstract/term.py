from abc import ABC, abstractmethod


class Term(ABC):
    """Term interface (abstract class) for all logic expressions"""

    @abstractmethod
    def __str__(self) -> str:
        return ''

    @abstractmethod
    def __copy__(self) -> 'Term':
        pass

    @abstractmethod
    def __deepcopy__(self, memo) -> 'Term':
        pass

    @abstractmethod
    def translate(self) -> str:
        """String in russian language"""
        return ''

    @abstractmethod
    def implication_negation(self) -> 'Term':
        """Equivalent term using only implication and negation"""
        return self

    @abstractmethod
    def substitute(self, **kwargs: dict[str, 'Term']) -> 'Term':
        """Substitute an Term instead of a Literal"""
        pass
