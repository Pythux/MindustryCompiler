
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, KeyWord


# draw stroke 0 0 0 255 0 0
@grammar
def drawResult(p: YaccProduction):
    '''ligne : draw drawKeyWord instrArgs EndLine'''
    args = p[3]
    nbArgs = 6
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [p[2], *args])


@grammar
def drawKeyword_error(p: YaccProduction):
    '''ligne : draw error'''
    raise err.invalideSubInstr(p)


@grammar
def drawKeyWord(p: YaccProduction):
    '''drawKeyWord : stroke
                   | clear
                   | color
                   | line
                   | rect
                   | lineRect
                   | image
                   | poly
                   | linePoly
                   | triangle
    '''
    p[0] = KeyWord(p[1])


@grammar
def drawArgs_error(p: YaccProduction):
    '''ligne : draw drawKeyWord instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, 6)
