

from .ImportsContext import imports
from pathlib import PurePath
import os


# generator
def nextImportContent():
    for toImp in imports.nextToImport():
        yield getContent(toImp)


# from lib name, get libFile content
def getContent(libFile):
    libPath = PurePath(os.path.dirname(__file__), *['..' for _ in range(len(__package__.split('.')))], 'code', 'lib')
    filePath = libPath.joinpath(libFile)
    with open(filePath, 'r') as fd:
        print('get lib content')
        breakpoint()
        return fd.read()
