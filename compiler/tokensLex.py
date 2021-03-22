#!/usr/bin/env python

# ------------------------------------------------------------
# tokenizer
# ------------------------------------------------------------

# import ply.lex as lex

from ply import lex

from boa import boa


# List of token names.   This is always required
tokens = [
    'Plus',
    'Minus',
    'Multiply',
    'Divide',
    'LPAREN',
    'RPAREN',
]

# Regular expression rules for simple tokens
t_Plus = r'\+'
t_Minus = r'-'
t_Multiply = r'\*'
t_Divide = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# add functions:
tokens += [
    'Number',
    'Indent',
    'RefJump',
]


# A regular expression rule with some action code
def t_Number(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_Indent(t):
    r'\n(\t|[ ]{4})*'
    t.value = len(t.value[1:].replace(' '*4, '\t'))
    t.lexer.lineno += 1  # inc line number to track lines
    return t


def t_RefJump(t):
    r'[#]Ref:[ ][a-zA-Z_]\S*'
    t.value = t.value.split(' ')[-1]
    return t


reserved = {
    # new ones (or witch change)
    'if': 'If',
    'jump': 'Jump',
    'def': 'Function',
    'return': 'FunReturn',

    'not': 'NotEqual',

    # asm reserved
    'end': 'EndProg',
    'op': 'AsmOperation'
}
tokens += list(reserved.values())
tokens += ['Variable']  # words by default

reservedSpecial = {
    '==': 'Equal',
    '===': 'StrictEqual',
    '!=': 'NotEqual',
    '>': 'GreaterThan',
    '>=': 'GreaterThanOrEqual',
    '<': 'LowerThan',
    '<=': 'LowerThanOrEqual',
}
tokens += (reservedSpecial.values())


# function starting with t_ will be run for tokens even if not in tokens list
def t_Word(t):
    r'[a-zA-Z_]\S*'  # \S Matches anything other than a space, tab or newline.
    # print(t.type) == 'Word'
    t.type = reserved.get(t.value, 'Variable')  # Check for reserved words
    return t


startReservedSpecial = boa(list(reservedSpecial.keys())).map(lambda w: w[0])


# must be defined before SpecialWord, fuction exécute before const
def t_Commentaires(t):
    r'\/\/.*'
    # no return, token discarded


# catch everything else that function on trop don't catch
def t_SpecialWord(t):
    r'\S+'  # \S Matches anything other than a space, tab or newline
    if t.value[0] in startReservedSpecial:
        t.type = reservedSpecial[t.value]  # Check for reserved words
        return t
    print('SpecialWord not match: {}'.format(t))


# A string containing ignored characters (spaces and tabs)
t_ignore = ''


# Error handling rule
def t_error(t):
    if t.value[0] == ' ':
        t.lexer.skip(1)
    else:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


tokens = list(set(tokens))
# Build the lexer
lexer = lex.lex()

# debugging:
# lexer = lex.lex(debug=True)


def test():
    # Test it out
    data = '''
    // lulz // yo
    if true jump // lo
        yé
            4 >= 12

    #Ref: yoél
    iftruejump
    '''

    # Give the lexer some input
    lexer.input(data)

    for tok in lexer:
        print(tok)


if __name__ == '__main__':
    test()


def main():
    # main function which will either tokenize input read from standard input
    # or from a file specified on the command line
    lex.runmain()
