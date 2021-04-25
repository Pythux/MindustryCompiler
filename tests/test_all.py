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


def testCodeAsm():
    codeResult('code->ASM')
    codeResult('webExemples')


def codeResult(folder):
    folderPath = PurePath(os.path.dirname(__file__), folder)
    (boa(os.listdir(folderPath))
        .filter(lambda file: file.split('.')[-1] == 'code')
        .sort()
        .map(lambda file: boa({'file': file}))
        .map(lambda file: file.update({'filePath': PurePath(folderPath, file.file)}))
        .map(lambda file: file.update({'content': getContent(file.filePath)}))
        .map(splitCodeASM)
        .map(checkCodeToASM))


def splitCodeASM(file):
    code, asm = re.match(r'([\s|\S]*)\n+-{6}[-]+\n+([\s|\S]*)', file.content).groups()
    return file.update({'code': code, 'asm': asm})


def checkCodeToASM(file):
    try:
        assert runYacc(file.code, clearContext=True) == file.asm
    except: # noqa
        print('\nfail runYacc on file: {}\n'.format(file.file))
        raise SystemError()
