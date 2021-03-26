# import pytest
import os
from compiler.yacc.mainYacc import runYacc
from pathlib import PurePath


# with pytest.raises(AnExcetion):
#     ...


def getCode(fileNameNoExtention):
    fileName = fileNameNoExtention + '.code'
    return getContent(fileName)


def getAsm(fileNameNoExtention):
    fileName = fileNameNoExtention + '.asm'
    return getContent(fileName)


def getContent(fileName):
    filePath = PurePath(os.path.dirname(__file__), 'identicalCode', fileName)
    with open(filePath, 'r') as fd:
        return fd.read()


def codeTestEq(fileNameNoExtention):
    getCode(fileNameNoExtention)
    getAsm(fileNameNoExtention)


def test_subset():
    content = getContent('1-subset.code')
    assert content == runYacc(content)


def codeEqual(fileNameNoExtention):
    assert getCode(fileNameNoExtention) == getAsm(fileNameNoExtention)


def test_jump():
    assert runYacc(getCode('2-refJump')) == getCode('1-subset')


def test_comments():
    assert runYacc(getCode('3-comments')) == runYacc(getCode('2-refJump'))
    assert runYacc(getCode('3-comments')) == getCode('1-subset')
