

# list of token reserved keywords


instr = [
    'op',
    'end',
    'set',
    'print',
    'printflush',
    'draw',
    'drawflush',
    'ubind',
    'read',
    'write',
    'sensor',
    'getlink',
    'radar',
    'uradar',
    'jump',
    'control',
    'ucontrol',
    'ulocate',
]

radarTarget = ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss']
radarSort = ['distance', 'health', 'shield', 'armor', 'maxHealth']


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


draw = [
    'stroke',
    'clear',
    'color',
    'line',
    'rect',
    'lineRect',
    'image',
    'poly',
    'linePoly',
    'triangle',
]

jump = [
    'equal',
    'notEqual',
    'lessThan',
    'lessThanEq',
    'greaterThan',
    'greaterThanEq',
    'strictEqual',
    'always',
]

control = [
    'enabled',
    'configure',
    'shootp',
    'shoot',
    'color',
]

ucontrol = [
    'idle',
    'stop',
    'move',
    'approach',
    'pathfind',
    'target',
    'targetp',
    'itemDrop',
    'itemTake',
    'payDrop',
    'payTake',
    'flag',
    'mine',
    'build',
    'getBlock',
    'within',
    'boost',
]

ulocate = [
    'ore',
    'damaged',
    'spawn',
    'building',
]

ulocateBuildingType = [
    'core',
    'storage',
    'generator',
    'factory',
    'repair',
    'rally',
    'battery',
    'resupply',
    'reactor',
    'turret',
]

subInstr = {
    'op': op,
    'radar': radarTarget + radarSort,
    'draw': draw,
    'jump': jump,
    'control': control,
    'ucontrol': ucontrol,
    'ulocate': ulocate + ulocateBuildingType,
}


# the all reserved keyword list
reserved = {
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
