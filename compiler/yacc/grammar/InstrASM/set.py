
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, KeyWord


@grammar
def setResult(p: YaccProduction):
    '''line : set ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 1
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def set_tooMuchArgs(p: YaccProduction):
    '''line : set ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def set_mustBeID(p: YaccProduction):
    '''line : set error'''
    raise err.mustBeVar(p, 2, p[2])
