# import pytest
import os
from compiler.yacc.mainYacc import runYacc
from pathlib import PurePath
from boa import boa
import re


# with pytest.raises(AnExcetion):
#     ...


def getContent(filePath):
    with open(filePath, 'r') as fd:
        return fd.read()


def test_identicalCode():
    folderPath = PurePath(os.path.dirname(__file__), 'identicalCode')
    asm = getContent(PurePath(folderPath, '1-vanilla.code'))
    files = list(filter(lambda file: file.split('.')[-1] == 'code', os.listdir(folderPath)))
    files.sort()
    for file in files:
        filePath = PurePath(folderPath, file)
        assert runYacc(getContent(filePath), clearContext=True) == asm


def test_codeResult():
    folderPath = PurePath(os.path.dirname(__file__), 'code->ASM')
    (boa(os.listdir(folderPath))
        .filter(lambda file: file.split('.')[-1] == 'code')
        .sort()
        .map(lambda file: boa({'file': file}))
        .map(lambda obj: obj.update({'filePath': PurePath(folderPath, obj.file)}))
        .map(lambda obj: obj.update({'content': getContent(obj.filePath)}))
        .map(splitCodeASM)
        .map(checkCodeToASM))


def splitCodeASM(obj):
    code, asm = re.match(r'([\s|\S]*)\n+-{6}[-]+\n+([\s|\S]*)', obj.content).groups()
    return obj.update({'code': code, 'asm': asm})


def checkCodeToASM(obj):
    assert runYacc(obj.code, clearContext=True) == obj.asm
