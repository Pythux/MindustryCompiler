

# list of token reserved keywords


def idTuple(li):
    return {w: w for w in li}


instr = [
    'op',
]

op = [
    'add',
]

subInstr = {
    'op': op,
}


# the all reserved keyword list
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

    **idTuple(instr),

    **idTuple(op),
}
