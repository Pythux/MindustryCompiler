# shebang will automaticaly be set to the pip venv
import logging
import argparse

from compiler.lex import runInteractiveLex, runLex
from compiler.yacc.mainYacc import runInteractiveYacc, runYacc


def runInteractive(args):
    if args.lex:
        runInteractiveLex()
        return
    elif args.yacc:
        runInteractiveYacc()
        return
    else:
        # give final compiled result in interactive
        runInteractiveYacc()


def run(args):
    fileContent = ''
    with open(args.file, 'r') as fd:
        fileContent = fd.read()

    if args.lex:
        return '\n'.join(map(str, runLex(fileContent)))
    elif args.yacc:
        return runYacc(fileContent, debug=args.dbg)
    else:
        # give final compiled result in interactive
        return runYacc(fileContent, debug=args.dbg)


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

    parser.add_argument('--lex', help='end at tokenisation',
                        action='store_true')
    parser.add_argument('--yacc', help='end at parsing',
                        action='store_true')
    parser.add_argument('--ctrlC', help='copie resulted ASM to clipboard (Ctrl-C), just what you need',
                        action='store_true')
    parser.add_argument('-i', '--interactive', '--repl', help='run interactive mode',
                        action='store_true')
    parser.add_argument('--dbg', '--debug', help='run with debug flag',
                        action='store_true')

    # for faster debugging:
    # python -m pdb -c continue compiler/__main__.py -i

    args = parser.parse_args()
    if args.lex and args.yacc:  # not true together
        print("can't use option --lex and --yacc together")
        return
    isInteractive = args.interactive
    if not isInteractive and not args.file:
        parser.print_help()
        if args.lex or args.yacc:
            print("\ncan't run without file name or interactive option")
        return
    toClipboard = args.ctrlC
    if isInteractive and toClipboard:
        return print("can't copy to clipbord interactive, must specifie file name")

    if isInteractive:
        runInteractive(args)
    else:
        result = run(args)
        if toClipboard:
            import pyperclip
            pyperclip.copy(result)
        else:
            print(result)


if __name__ == '__main__':
    main()
