from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Any
from .terms import Term, Var, Not, And, Or, Xor, Equal, Arrow


def to_or_not(arrow_elem: Arrow):
    return Or(Not(arrow_elem.arg1), arrow_elem.arg2)

def replace_arguments(or_elem: Or):
    return Or(or_elem.arg2, or_elem.arg1)