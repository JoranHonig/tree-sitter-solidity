#!/usr/bin/env python3
"""
Grammar updater script for tree-sitter-solidity.
Downloads and compares Solidity grammar versions to identify changes.
"""

import json
import shutil
import subprocess
from pathlib import Path

import click
import requests
from loguru import logger


@click.command()
@click.option(
    "--output-dir",
    default="tmp_claude",
    help="Directory for temporary files and outputs",
)
@click.option(
    "--version-file",
    default="last_grammar_version.json",
    help="Path to version file",
)
def main(output_dir: str, version_file: str):
    """Download Solidity grammar and generate diff between versions."""
    # Set up logging
    logger.info("Starting grammar update process")
    
    # Read last grammar version
    try:
        with open(version_file, "r") as f:
            data = json.load(f)
            last_version = data["version"]
        logger.info(f"Last grammar version: {last_version}")
    except Exception as e:
        logger.error(f"Failed to read version file: {e}")
        raise click.ClickException(f"Failed to read version file: {e}")
    
    # Set up output directory
    output_path = Path(output_dir)
    if output_path.exists():
        logger.info(f"Cleaning existing output directory: {output_path}")
        shutil.rmtree(output_path)
    output_path.mkdir(exist_ok=True)
    logger.info(f"Created output directory: {output_path}")
    
    # Clean up old files
    grammar_updates = Path("grammar_updates.md")
    if grammar_updates.exists():
        grammar_updates.unlink()
        logger.info("Removed existing grammar_updates.md")
    
    # Remove any existing SolidityParser files
    for parser_file in Path(".").glob("SolidityParser*.g4"):
        parser_file.unlink()
        logger.info(f"Removed {parser_file}")
    
    # Download current grammar
    current_url = "https://raw.githubusercontent.com/ethereum/solidity/develop/docs/grammar/SolidityParser.g4"
    current_file = output_path / "SolidityParser.new.g4"
    
    logger.info("Downloading current grammar from develop branch")
    try:
        response = requests.get(current_url)
        response.raise_for_status()
        current_file.write_text(response.text)
        logger.success(f"Downloaded current grammar to {current_file}")
    except Exception as e:
        logger.error(f"Failed to download current grammar: {e}")
        raise click.ClickException(f"Failed to download current grammar: {e}")
    
    # Download last grammar version
    old_url = f"https://raw.githubusercontent.com/ethereum/solidity/v{last_version}/docs/grammar/SolidityParser.g4"
    old_file = output_path / "SolidityParser.old.g4"
    
    logger.info(f"Downloading grammar version {last_version}")
    try:
        response = requests.get(old_url)
        response.raise_for_status()
        old_file.write_text(response.text)
        logger.success(f"Downloaded version {last_version} grammar to {old_file}")
    except Exception as e:
        logger.error(f"Failed to download old grammar: {e}")
        raise click.ClickException(f"Failed to download old grammar: {e}")
    
    # Generate diff
    diff_file = output_path / "grammar.diff"
    logger.info("Generating diff between grammar versions")
    
    try:
        # Run diff command
        result = subprocess.run(
            ["diff", "-u", str(old_file), str(current_file)],
            capture_output=True,
            text=True,
        )
        
        # diff returns 1 when files differ, which is expected
        if result.returncode not in [0, 1]:
            raise subprocess.CalledProcessError(result.returncode, result.args)
        
        # Save diff to file
        diff_file.write_text(result.stdout)
        
        if result.stdout:
            logger.success(f"Generated diff and saved to {diff_file}")
            logger.info(f"Diff contains {len(result.stdout.splitlines())} lines")
        else:
            logger.info("No differences found between grammar versions")
            
    except Exception as e:
        logger.error(f"Failed to generate diff: {e}")
        raise click.ClickException(f"Failed to generate diff: {e}")
    
    logger.success("Grammar update process completed")
    logger.info(f"Output files are in {output_path}/")


if __name__ == "__main__":
    main()