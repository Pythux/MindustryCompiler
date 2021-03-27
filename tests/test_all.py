# import pytest
import os
from compiler.yacc.mainYacc import runYacc
from pathlib import PurePath


# with pytest.raises(AnExcetion):
#     ...


def getContent(filePath):
    with open(filePath, 'r') as fd:
        return fd.read()


def test_identicalCode():
    folderPath = PurePath(os.path.dirname(__file__), 'identicalCode')
    asm = getContent(PurePath(folderPath, '1-vanilla.code'))
    files = os.listdir(folderPath)
    files.sort()
    for file in files:
        filePath = PurePath(folderPath, file)
        assert runYacc(getContent(filePath)) == asm
