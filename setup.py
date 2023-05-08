import sys
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


class BuildPy(build_py):
    def run(self):
        from tree_sitter import Language

        if sys.platform == "win32":
            output_path = Path(__file__).parent / "tree_sitter_solidity" / "solidity.dll"
        else:
            output_path = Path(__file__).parent / "tree_sitter_solidity" / "solidity.so"

        Language.build_library(
            str(output_path),
            [Path(__file__).parent],
        )

        super().run()


with Path(__file__).parent.joinpath("README.md").open() as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="abch_tree_sitter_solidity",
    version="1.2.1",
    author="Ackee Blockchain",
    url="https://github.com/Ackee-Blockchain/tree-sitter-solidity",
    license="MIT",
    platforms=["any"],
    python_requires=">=3.7",
    install_requires=["abch-tree-sitter>=1.0.1"],
    setup_requires=["abch-tree-sitter>=1.0.1"],
    description="Solidity grammar for the Tree-sitter parsing library",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=["tree_sitter_solidity"],
    package_data={"tree_sitter_solidity": ["solidity.so", "solidity.dll"]},
    project_urls={"Source": "https://github.com/Ackee-Blockchain/tree-sitter-solidity"},
    cmdclass={"build_py": BuildPy},
    data_files=[("src", ["src/parser.c", "src/tree_sitter/parser.h"])],
)
