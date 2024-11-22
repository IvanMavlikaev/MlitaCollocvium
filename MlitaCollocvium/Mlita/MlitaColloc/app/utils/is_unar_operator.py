from ..terms.abstract import Term, UnaryOperator
from ..terms.variable import Var


def is_unar_operator(term: Term) -> bool:
    return isinstance(term, Var) or isinstance(term, UnaryOperator)

