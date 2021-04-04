
from ._start import grammar, YaccProduction


# splitted x.y.z to liste [x, y, z]
@grammar
def dottedID_one(p: YaccProduction):
    '''dottedID : ID'''
    p[0] = [p[1]]


@grammar
def dottedID_many(p: YaccProduction):
    '''dottedID : dottedID Dot ID'''
    p[0] = p[1] + [p[3]]
