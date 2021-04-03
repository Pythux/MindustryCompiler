

from .ImportsContext import imports


# generator
def nextImportContent():
    for toImp in imports.nextToImport():
        yield toImp
