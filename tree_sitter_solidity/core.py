import sys
from pathlib import Path

from tree_sitter import Language, Parser


def get_language():
    lib_name = "solidity.dll" if sys.platform == "win32" else "solidity.so"
    return Language(
        str(Path(__file__).parent.joinpath(lib_name)),
        "solidity",
    )


def get_parser():
    parser = Parser()
    parser.set_language(get_language())
    return parser
