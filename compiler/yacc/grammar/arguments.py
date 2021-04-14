

from ._start import grammar, YaccProduction


@grammar
def args_empty(p: YaccProduction):
    '''arguments : '''
    p[0] = []


@grammar
def args_one(p: YaccProduction):
    '''arguments : info'''
    p[0] = [p[1]]


@grammar
def args_many(p: YaccProduction):
    '''arguments : arguments Comma info'''
    p[0] = p[1] + [p[3]]


@grammar
def args_oneComma(p: YaccProduction):
    '''arguments : arguments Comma'''
    p[0] = p[1]
