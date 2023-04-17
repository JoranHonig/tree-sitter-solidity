from pathlib import Path
from setuptools import setup


with Path(__file__).parent.joinpath("README.md").open() as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="abch_tree_sitter_solidity",
    version="1.0.4",
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
)
