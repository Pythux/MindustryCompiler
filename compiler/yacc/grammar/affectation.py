

from ._start import grammar, YaccProduction


# x, y, z = ...
@grammar
def affect(p: YaccProduction):
    '''affectation : varsToAffect Affectaction'''
    p[0] = p[1]


@grammar
def varsToAffect_one(p: YaccProduction):
    '''varsToAffect : ID'''
    p[0] = [p[1]]


@grammar
def varsToAffect_many(p: YaccProduction):
    '''varsToAffect : varsToAffect Comma ID'''
    p[0] = p[1] + [p[3]]
