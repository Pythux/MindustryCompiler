

from ._start import grammar, YaccProduction

from ..Imports import imports


@grammar
def importStd(p: YaccProduction):
    '''noLine : Import ToImports'''
    toImports = p[2]
    imports.toImport(toImports)


@grammar
def toImports_one(p: YaccProduction):
    '''ToImports : ID'''
    p[0] = [p[1]]


@grammar
def toImports_many(p: YaccProduction):
    '''ToImports : ToImports Comma ID'''
    p[0] = p[1] + [p[3]]
