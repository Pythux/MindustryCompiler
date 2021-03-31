
from ._start import grammar, YaccProduction


# trac AsmLineNumber to #ref it
@grammar
def lines_one(p: YaccProduction):
    '''lines : line'''
    line = p[1]
    if line is None:
        p[0] = []
    else:
        p[0] = [p[1]]


@grammar
def lines_lines(p: YaccProduction):
    '''lines : lines lines'''
    p[0] = p[1] + p[2]


# no p[0] =, we don't bubble it, just dircarded
@grammar
def lines_empty(p: YaccProduction):
    '''line : noLine'''


# discard empty lines
@grammar
def noLine(p):
    '''noLine : EndLine'''
