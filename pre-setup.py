import sys
from pathlib import Path

from tree_sitter import Language, Parser

if sys.platform == "win32":
    output_path = Path(__file__).parent / "tree_sitter_solidity" / "solidity.dll"
else:
    output_path = Path(__file__).parent / "tree_sitter_solidity" / "solidity.so"

Language.build_library(
    str(output_path),
    [Path(__file__).parent],
)
