

class Imports:
    def __init__(self) -> None:
        self.imported = {None: {}}  # None is main file
        self.toImports = []
        self._currentFile = None

    # simple absolute import from lib/, one lvl
    def toImport(self, filesToImport):
        for fileLib in filesToImport:
            if fileLib not in self.imported:
                self.currentFile = fileLib  # will pe processed
                self.toImports.append(fileLib)

    # generator
    def nextToImport(self):
        while len(self.toImports):
            yield self.toImports.pop()

    @property
    def currentFile(self):
        return self._currentFile

    # for this decorator, need the above function with @property, and same function name
    @currentFile.setter
    def currentFile(self, value):
        self.currentFile = value
        assert value not in self.imported
        self.imported[value] = {}  # functions will be stored here

    def addFunToModule(self, funDef):
        assert self.currentFile in self.imported
        self.imported[self.currentFile][funDef.name] = funDef

    # called at the verry end, once everything is imported
    def getModule(self, fileLib):
        if fileLib not in self.toImports:
            raise SystemExit("module {} is used but not imported".format(fileLib))
        return self.imported[fileLib]


imports = Imports()
