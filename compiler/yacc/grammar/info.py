

from ._start import grammar, YaccProduction
from ..classes import Variable, Value


@grammar
def info_id(p: YaccProduction):
    '''info : ID'''
    p[0] = Variable(p[1])


@grammar
def info(p: YaccProduction):
    '''info : Number
            | String
            | ArobasedInfo
            | True
            | False
    '''
    p[0] = Value(p[1])
