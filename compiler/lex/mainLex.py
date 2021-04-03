#!/usr/bin/env python

# ------------------------------------------------------------
# tokenizer with Lex
# ------------------------------------------------------------

# import ply.lex as lex

from ply import lex
from ply.lex import Lexer


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
    r'@\w+'
    return t


def t_stringDoubleQuote(t: LexToken):
    r'"[^"]*"'
    t.type = 'String'
    return t


def t_stringSimpleQuote(t: LexToken):
    r"'[^']*'"
    t.type = 'String'
    return t


previousIndentationLvl = 0
indentNb = None
tokens += ['OpenCurlyBracket', 'CloseCurlyBracket']
addCloseBracket = 0


# count indentation, indent could be spaces or tabs
def t_EndLine(t: LexToken):
    r'\n[ ]*\t*'
    if isEmptyEndLine(t):
        t.lexer.lineno += 1  # inc line number to track lines
        return

    global addCloseBracket
    if addCloseBracket > 0:
        return closeBracket(t)

    global indentNb
    if indentNb is None:
        if len(t.value[1:]) > 0:
            indentNb = len(t.value[1:])

    if indentNb is None:
        t.lexer.lineno += 1  # inc line number to track lines
        return t

    tok = handleIndent(t)
    if tok is not None:
        return tok


def isEmptyEndLine(t: LexToken):
    pos = t.lexer.lexpos
    length = len(t.value)
    data = t.lexer.lexdata
    return data[pos-1:pos-1+length+1] == '\n\n'


def closeBracket(t):
    # add CloseCurlyBracket as needed
    global addCloseBracket
    if addCloseBracket > 0:
        addCloseBracket -= 1
        t.type = 'CloseCurlyBracket'
        if addCloseBracket > 0:
            redoToken(t)
        return t


# rerun the same to create more than one token
def redoToken(t):
    t.lexer.lexpos -= len(t.value)


def handleIndent(t: LexToken):
    global indentNb, addCloseBracket, previousIndentationLvl

    nb = len(t.value[1:])
    if nb / indentNb != nb // indentNb:
        raise SystemExit('line {}, indentation incorrect to previous lines in file'.format(t.lineno))
    indentLvl = len(t.value[1:]) // indentNb

    if indentLvl > previousIndentationLvl:
        return indentUp(t, indentLvl)

    elif indentLvl < previousIndentationLvl:
        return indentDown(t, indentLvl)

    previousIndentationLvl = indentLvl
    t.lexer.lineno += 1  # inc line number to track lines
    return t


def indentUp(t: LexToken, indentLvl):
    global previousIndentationLvl
    if indentLvl > previousIndentationLvl + 1:
        raise SystemExit('too much indentation line {}'.format(t.lineno))
    t.type = 'OpenCurlyBracket'
    previousIndentationLvl = indentLvl
    t.lexer.lineno += 1  # inc line number to track lines
    return t


def indentDown(t: LexToken, indentLvl):
    global previousIndentationLvl, addCloseBracket
    t.type = 'EndLine'
    addCloseBracket = previousIndentationLvl - indentLvl
    redoToken(t)
    previousIndentationLvl = indentLvl
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
    'def': 'DefFun',
    'return': 'Return',
}
tokens += list(reserved.values())
tokens += ['ID']  # not reserved words


# function starting with t_ will be run for tokens even if not in tokens list
def t_Word(t: LexToken):
    r'''[^ \n.,()*{}'"]+'''
    # r'''[^ .,()'"*{}\n]+'''  # match words, including utf-8 characters
    if t.value[0] == '#':
        return None  # unofficial comments "#"

    t.type = reserved.get(t.value, 'ID')  # Check for reserved word, else ID
    return t


separator = {
    '(': 'OpenParenthesis',
    ')': 'CloseParenthesis',
    ',': 'Comma',
}
tokens += list(separator.values())


def t_Separator(t: LexToken):
    r'''[.,()*{}]'''
    t.type = separator[t.value]
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
