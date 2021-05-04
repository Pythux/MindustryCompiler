
from ._start import grammar, YaccProduction
from . import asmError as err


# all asm instructions are handled in InstrASM folder
@grammar
def instrKey_error(p: YaccProduction):
    '''ligne : info error'''
    raise err.invalideInstr(p, line=p.lineno(2))


@grammar
def instrKey_error2(p: YaccProduction):
    '''ligne : error'''
    raise err.invalideInstr(p, line=p.lineno(1))


@grammar
def instrArgs(p: YaccProduction):
    '''instrArgs :
                 | info
                 | instrArgs info'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
