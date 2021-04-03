

class Imports:
    def __init__(self) -> None:
        self.imported = {}
        self.toImports = []
        self._currentFile = None

    # simple absolute import from lib/, one lvl
    def toImport(self, filesToImport):
        for fileLib in filesToImport:
            if fileLib not in self.imported:
                self.toImports.append(fileLib)

    def getNextToImport(self):
        if len(self.toImports):
            return self.toImports[-1]
        return None

    @property
    def currentFile(self):
        return self._currentFile

    # for this decorator, need the above function with @property, and same function name
    @currentFile.setter
    def currentFile(self, value):
        self.currentFile = value
        assert value not in self.imported
        self.imported[value] = {}

    def addFunToModule(self, funDef):
        assert self.currentFile in self.imported
        self.imported[self.currentFile][funDef.name] = funDef

    # called at the verry end, once everything is imported
    def getModule(self, fileLib):
        if fileLib not in self.toImports:
            raise SystemExit("module {} is used but not imported".format(fileLib))
        return self.imported[fileLib]


imports = Imports()
