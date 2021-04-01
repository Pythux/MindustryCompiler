
from ply.yacc import YaccProduction
from compiler.lex.mainLex import LexToken

from compiler.yacc.generateYacc import grammar, precedence

from .contextAndClass import context


# starting grammar
from . import lines  # noqa
# lines is the starting grammar


__all__ = [YaccProduction, LexToken, grammar, context]


# precedence((
#     # ('nonassoc', 'LESSTHAN', 'GREATERTHAN'),  # Nonassociative operators
#     ('left', 'lines'),
# ))
