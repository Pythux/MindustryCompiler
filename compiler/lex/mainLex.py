#!/usr/bin/env python

# ------------------------------------------------------------
# tokenizer with Lex
# ------------------------------------------------------------

# import ply.lex as lex

from ply import lex
from ply.lex import Lexer
from boa import boa


class LexToken:
    lexer: Lexer
    lineno: int  # will be updated by lexer
    type: str  # Token name
    value: str  # matched content, can be changed to anything


# List of token names.   This is always required
tokens = [
    # 'Plus',
]

# Regular expression rules for simple tokens
# will be check last (after functions)
# t_Plus = r'\+'


# add tokens from functions
tokens += [
    'Number',
    'ArobasedInfo',
    'String',
    'EndLine',
    'RefJump',
]


# catch numbers like 0, 1, -2, -26.465
def t_Number(t):
    r'[-]?\d+[.]?\d*'
    return t


def t_ArobasedInfo(t):
    r'@[\w-]+'
    return t


def t_stringDoubleQuote(t: LexToken):
    r'"[^"]*"'
    t.type = 'String'
    return t


def t_stringSimpleQuote(t: LexToken):
    r"'[^']*'"
    t.type = 'String'
    return t


tokens += ['OpenCurlyBracket', 'CloseCurlyBracket']
endLineContext = boa({})
endLineContext.addCloseBracket = 0
endLineContext.previousIndentationLvl = 0
endLineContext.indentNb = None
endLineContext.inOpenBracket = False


# count indentation, indent could be spaces or tabs
def t_EndLine(t: LexToken):
    r'\n[ ]*\t*'
    if endLineContext.inOpenBracket:
        t.lexer.lineno += 1
        return
    if isEmptyEndLine(t):
        t.lexer.lineno += 1  # inc line number to track lines
        return

    if endLineContext.addCloseBracket > 0:
        return closeBracket(t)

    if endLineContext.indentNb is None:
        if len(t.value[1:]) > 0:
            endLineContext.indentNb = len(t.value[1:])

    if endLineContext.indentNb is None:
        t.lexer.lineno += 1  # inc line number to track lines
        return t

    tok = handleIndent(t)
    if tok is not None:
        return tok


def isEmptyEndLine(t: LexToken):
    pos = t.lexer.lexpos
    length = len(t.value)
    if t.lexer.lexdata[pos-1:pos-1+length+1] == '\n\n':
        return True
    if t.lexer.lexdata[pos-1:pos-1+length+2] == '\n//':
        return True
    return False


def closeBracket(t):
    # add CloseCurlyBracket as needed
    if endLineContext.addCloseBracket > 0:
        endLineContext.addCloseBracket -= 1
        t.type = 'CloseCurlyBracket'
        if endLineContext.addCloseBracket > 0:
            redoToken(t)
        return t


# rerun the same to create more than one token
def redoToken(t):
    t.lexer.lexpos -= len(t.value)


def handleIndent(t: LexToken):
    nb = len(t.value[1:])
    if nb / endLineContext.indentNb != nb // endLineContext.indentNb:
        raise SystemExit('line {}, indentation incorrect to previous lines in file'.format(t.lineno))
    indentLvl = len(t.value[1:]) // endLineContext.indentNb

    if indentLvl > endLineContext.previousIndentationLvl:
        return indentUp(t, indentLvl)

    elif indentLvl < endLineContext.previousIndentationLvl:
        return indentDown(t, indentLvl)

    endLineContext.previousIndentationLvl = indentLvl
    t.lexer.lineno += 1  # inc line number to track lines
    return t


def indentUp(t: LexToken, indentLvl):
    if indentLvl > endLineContext.previousIndentationLvl + 1:
        raise SystemExit('too much indentation line {}'.format(t.lineno))
    t.type = 'OpenCurlyBracket'
    endLineContext.previousIndentationLvl = indentLvl
    t.lexer.lineno += 1  # inc line number to track lines
    return t


def indentDown(t: LexToken, indentLvl):
    t.type = 'EndLine'
    endLineContext.addCloseBracket = endLineContext.previousIndentationLvl - indentLvl
    redoToken(t)
    endLineContext.previousIndentationLvl = indentLvl
    return t


# match: '#ref st', '#Ref st', '#ref: st', '#Ref: st', '#ref é4sét$sr'
def t_RefJump(t: LexToken):
    r'[#][Rr]ef[:]?[ ][^0-9]\S*'
    t.value = t.value.split(' ')[-1]
    return t


# discards comments line (aka: '//')
# must be defined before SpecialWord to catch it
def t_CommentsSlashSlash(t):
    r'[\n]*[ ]*\/\/.*'
    # no return, token discarded


# discards comments line (aka: '# ')
def t_CommentsHashSpace(t):
    r'[#][ ].*'
    # no return, token discarded


comparison = {
    '==': 'equal',
    '===': 'strictEqual',
    '!=': 'notEqual',
    '>': 'greaterThan',
    '>=': 'greaterThanEq',
    '<': 'lessThan',
    '<=': 'lessThanEq',
}
tokens += ['Comparison', 'Affectaction']


def t_Comparison(t: LexToken):
    r'[=!<>]+'
    if t.value == '=':
        t.type = 'Affectaction'
        return t
    if t.value in comparison:
        t.type = 'Comparison'
        t.value = comparison[t.value]
        return t


# reserved keyword
reserved = {
    'jump': 'Jump',
    'if': 'If',
    'else': 'Else',
    'elif': 'ElseIf',
    'return': 'Return',
    'import': 'Import',
    'true': 'True',
    'false': 'False',
    'for': 'For',
}
tokens += list(reserved.values())
tokens += ['ID']  # not reserved words


# function starting with t_ will be run for tokens even if not in tokens list
def t_Word(t: LexToken):
    r'''[^ \n.,()*{}'"\[\]]+'''
    # r'''[^ .,()'"*{}\n]+'''  # match words, including utf-8 characters
    if t.value[0] == '#':
        return None  # unofficial comments "#"

    t.type = reserved.get(t.value, 'ID')  # Check for reserved word, else ID
    return t


separator = {
    '(': 'OpenParenthesis',
    ')': 'CloseParenthesis',
    ',': 'Comma',
    '.': 'Dot',
    '[': 'OpenBracket',
    ']': 'CloseBracket',
}
tokens += list(separator.values())


def t_Separator(t: LexToken):
    r'''[.,()*{}\[\]]'''
    t.type = separator[t.value]
    if t.value == '[':
        endLineContext.inOpenBracket = True
    if t.value == ']':
        endLineContext.inOpenBracket = False
    return t


def t_Space(t: LexToken):
    '''[ ]'''


# A string containing ignored characters, could be (spaces and tabs)
t_ignore = '\r'


# Error handling rule
def t_error(t: LexToken):
    if t.value[0] == ' ':
        t.lexer.skip(1)
    else:
        print("Illegal character '%s'" % t.value[0])
        print("line: {}".format(t.lineno))
        raise SystemExit()


# make a list of unique tokens
tokens = list(set(tokens))
# Build the lexer
lexer = lex.lex()
# debugging:
# lexer = lex.lex(debug=True)


def runLex(content):
    lexer.input(content)
    li = [tok for tok in lexer]
    lexer.lineno = 1
    return li


def runInteractiveLex():
    content = ''
    while True:
        try:
            s = input('Lex >> ')
        except EOFError:
            break
        if s != '':
            content += s + '\n'
            continue

        print(runLex(content))
        content = ''
