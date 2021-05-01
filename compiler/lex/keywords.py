

# list of token reserved keywords


instr = [
    'op',
    'end',
    'set',
    'print',
    'printflush',
    'drawflush',
    'ubind',
    'read',
    'write',
    'sensor',
    'getlink',
]

op = [
    'add',
    'sub',
    'mul',
    'div',
    'idiv',
    'mod',
    'pow',

    'equal',
    'notEqual',
    'land',
    'lessThan',
    'lessThanEq',
    'greaterThan',
    'strictEqual',

    'shl',
    'shr',
    'or',
    'and',
    'xor',
    'not',

    'max',
    'min',
    'angle',
    'len',
    'noise',
    'abs',
    'log',
    'log10',
    'sin',
    'cos',
    'tan',
    'floor',
    'ceil',
    'sqrt',
    'rand',
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

    **{w: w for w in instr},
}

for instr in subInstr:
    for sub in subInstr[instr]:
        reserved[sub] = sub
