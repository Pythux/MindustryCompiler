

from .context import context

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
        context.AsmLineNumber += 1


# add a line to lines
@grammar
def lines_many(p: YaccProduction):
    '''lines : lines line'''
    line = p[2]
    if line is None:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[2]]
        context.AsmLineNumber += 1


# a line is ether a jump instruction or an asmInstr
@grammar
def line(p: YaccProduction):
    '''line : jump
            | asmInstr
    '''
    p[0] = p[1]


# no p[0] =, we don't bubble it, just dircarded
@grammar
def lines_empty(p: YaccProduction):
    '''line : noLine'''


# discard empty lines
@grammar
def noLine(p):
    '''noLine : EndLine'''
