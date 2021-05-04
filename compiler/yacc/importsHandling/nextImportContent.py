

from .ImportsContext import imports
from pathlib import PurePath, Path
import os


# generator
def nextImportContent():
    for toImp in imports.nextToImport():
        yield getContent(toImp)


# from lib name, get libFile content
def getContent(libFile):
    libFile = libFile + '.code'
    pathToPackageRoot = PurePath(os.path.dirname(__file__), *['..' for _ in range(len(__package__.split('.')))])
    libPathTryPackage = PurePath(pathToPackageRoot, 'compiler', 'code', 'lib')
    libPathTryLocal = PurePath(pathToPackageRoot, 'code', 'lib')
    libPath = libPathTryPackage if Path(libPathTryPackage).exists() else libPathTryLocal

    filePath = libPath.joinpath(libFile)
    with open(filePath, 'r') as fd:
        return fd.read()
