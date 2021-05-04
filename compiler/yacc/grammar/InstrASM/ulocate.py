
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, KeyWord
from compiler.lex import keywords


# ulocate building reactor true @copper outx outy found buildingResult
@grammar
def ulocateResult(p: YaccProduction):
    '''ligne : ulocate building buildingType instrArgs EndLine'''
    args = p[4]
    nbArgs = 6
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [p[2], p[3], *args])


# ulocate spawn null true null outx outy found buildingResult
@grammar
def ulocateResultKeyWord(p: YaccProduction):
    '''ligne : ulocate ulocateKeyWord instrArgs EndLine'''
    args = p[3]
    nbArgs = 7
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [p[2], *args])


@grammar
def ulocateKeyword_error(p: YaccProduction):
    '''ligne : ulocate error'''
    raise err.invalideSubInstr(p, valideKeys=keywords.ulocate)


@grammar
def ulocateBuildingType_error(p: YaccProduction):
    '''ligne : ulocate building error'''
    raise err.invalideSubInstr(p, valideKeys=keywords.ulocateBuildingType, indexErr=3)


@grammar
def ulocateBuildingArgs_error(p: YaccProduction):
    '''ligne : ulocate building buildingType instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, 6)


@grammar
def ulocateArgs_error(p: YaccProduction):
    '''ligne : ulocate ulocateKeyWord instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, 7)


@grammar
def ulocateKeyWord(p: YaccProduction):
    '''ulocateKeyWord : ore
                      | damaged
                      | spawn
    '''
    p[0] = KeyWord(p[1])


@grammar
def buildingType(p: YaccProduction):
    '''buildingType : core
                    | storage
                    | generator
                    | factory
                    | repair
                    | rally
                    | battery
                    | resupply
                    | reactor
                    | turret
    '''
    p[0] = KeyWord(p[1])
