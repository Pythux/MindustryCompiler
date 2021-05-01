
from ._start import grammar, YaccProduction
from . import asmError as err


## all asm instructions are handled in InstrASM folder


@grammar
def instrKey_error(p: YaccProduction):
    '''line : info error'''
    raise err.invalideInstr(p, line=p.lineno(2))


@grammar
def instrKey_error2(p: YaccProduction):
    '''line : error'''
    raise err.invalideInstr(p, line=p.lineno(1))
