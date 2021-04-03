
from ._start import grammar, YaccProduction, context


def runFunc(p: YaccProduction):
    '''lines : ID OpenParenthesis argumentsCall CloseParenthesis'''


def defFun(p: YaccProduction):
    '''noLine : DefFun funName funScope OpenParenthesis arguments CloseParenthesis OpenCurlyBracket lines CloseCurlyBracket'''
