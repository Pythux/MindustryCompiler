
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, KeyWord


@grammar
def setResult(p: YaccProduction):
    '''line : set ID info info EndLine'''
    p[0] = AsmInst(KeyWord(p[1]), [p[2], Variable(p[3])])


@grammar
def set_mustBeID(p: YaccProduction):
    '''line : set error'''
    raise err.mustBeVar(p, 2, p[2])


def set_MaybeArgsNotEnought(p: YaccProduction):
    '''line : set error'''
    raise err.maybeNotEnoughtArgs(p, 1, p[2])


def set_MaybeArgsNotEnought(p: YaccProduction):
    '''line : set ID info error'''
    raise err.tooManyArgs(p, 1)
