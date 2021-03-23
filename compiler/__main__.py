# shebang will automaticaly be set to the pip venv
import logging
import argparse

# from compiler.tokenize import tokens  # noqa
from compiler.yacc import runInteractiveYacc


def main():
    logging.basicConfig(level=logging.DEBUG)
    doc = """
        compile code to ASM Mindusty (named Mindustry Logic)
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
