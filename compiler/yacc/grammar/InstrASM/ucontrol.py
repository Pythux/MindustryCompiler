
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, KeyWord


# ucontrol move 0 0 0 0 0
@grammar
def ucontrolResult(p: YaccProduction):
    '''ligne : ucontrol ucontrolKeyWord instrArgs EndLine'''
    args = p[3]
    nbArgs = 5
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [p[2], *args])


@grammar
def ucontrolKeyword_error(p: YaccProduction):
    '''ligne : ucontrol error'''
    raise err.invalideSubInstr(p)


@grammar
def ucontrolArgs_error(p: YaccProduction):
    '''ligne : ucontrol ucontrolKeyWord instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, 5)


@grammar
def ucontrolKeyWord(p: YaccProduction):
    '''ucontrolKeyWord : idle
                       | stop
                       | move
                       | approach
                       | pathfind
                       | target
                       | targetp
                       | itemDrop
                       | itemTake
                       | payDrop
                       | payTake
                       | flag
                       | mine
                       | build
                       | getBlock
                       | within
                       | boost
    '''
    p[0] = KeyWord(p[1])
