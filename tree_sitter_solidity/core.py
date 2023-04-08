import sys

from tree_sitter import Language, Parser


def get_language():
    return Language(
        "solidity.dll" if sys.platform == "win32" else "solidity.so",
        "solidity",
    )


def get_parser():
    parser = Parser()
    parser.set_language(get_language())
    return parser
