# shebang will automaticaly be set to the pip venv
import logging
import argparse

from compiler.lex import runInteractiveLex, runLex
from compiler.yacc import runInteractiveYacc, runYacc


def runInteractive(args):
    if args.lex:
        runInteractiveLex()
        return
    elif args.yacc:
        runInteractiveYacc()
        return
    else:
        # give final compiled result in interactive
        # on interactive whait for "END" statement to process it
        NotImplemented


def run(args):
    fileContent = ''
    with open(args.file, 'r') as fd:
        fileContent = fd.read()

    if args.lex:
        return runLex(fileContent)
    elif args.yacc:
        return runYacc(fileContent)
    else:
        # give final compiled result in interactive
        # on interactive whait for "END" statement to process it
        NotImplemented


def main():
    logging.basicConfig(level=logging.DEBUG)
    doc = """
        compile code to ASM Mindusty (named Mindustry Logic)
        can have intermediate lex and yacc with options
        if no file name specified, will run interactive
    """
    parser = argparse.ArgumentParser(
        description=doc, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('file', type=str, help='input file name', nargs='?')

    parser.add_argument('--lex', help='show tokenised code',
                        action='store_const', const=True)
    parser.add_argument('--yacc', help='run Interactive Yacc',
                        action='store_const', const=True)
    parser.add_argument('--ctrlC', help='copie compiled ASM to clipboard (Ctrl-C), juste what you need',
                        action='store_const', const=True)

    args = parser.parse_args()
    if args.lex and args.yacc:  # not true together
        print("can't use option --lex and --yacc together")
        return
    isInteractive = args.file is None
    toClipboard = args.ctrlC is not None
    if isInteractive and toClipboard:
        return print("can't copy to clipbord interactive, must specifie file name to compile it")

    if isInteractive:
        runInteractive(args)
    else:
        result = run(args)
        if toClipboard:
            NotImplemented
        else:
            print(result)


if __name__ == '__main__':
    main()
