from .terms import Not, Var, And, Or, Arrow
from .parser import parse
from .replacer import to_or_not, replace_arguments
import sys
import os

sys.path.append(os.path.abspath(__file__))
