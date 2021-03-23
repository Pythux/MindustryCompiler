# shebang will automaticaly be set to the pip venv
import logging
import argparse

from compiler.tokensLex import tokens, main as mainLex
from compiler.parseYacc import runYacc


def main():
    logging.basicConfig(level=logging.DEBUG)
    doc = """
        compile code to ASM Mindusty
    """
    parser = argparse.ArgumentParser(
        description=doc, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "--lex",
        help='show tokenised code',
        )

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
