
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, KeyWord


# control enabled block1 0 0 0 0
@grammar
def controlResult(p: YaccProduction):
    '''ligne : control controlKeyWord instrArgs EndLine'''
    args = p[3]
    nbArgs = 5
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [p[2], *args])


@grammar
def controlKeyword_error(p: YaccProduction):
    '''ligne : control error'''
    raise err.invalideSubInstr(p)


@grammar
def controlArgs_error(p: YaccProduction):
    '''ligne : control controlKeyWord instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, 5)


@grammar
def controlKeyWord(p: YaccProduction):
    '''controlKeyWord : enabled
                      | configure
                      | shootp
                      | shoot
                      | color
    '''
    p[0] = KeyWord(p[1])
