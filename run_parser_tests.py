#!/usr/bin/env python3
"""
Test runner for parser functions.

This script provides an easy way to run parser tests individually or all at once.
"""

import subprocess
import sys
from pathlib import Path


def run_test(test_name=None, verbose=True):
    """Run parser tests."""
    if test_name:
        cmd = ["python", "-m", "pytest", f"tests/test_parser.py::TestParserFunctions::{test_name}"]
    else:
        cmd = ["python", "-m", "pytest", "tests/test_parser.py"]
    
    if verbose:
        cmd.append("-v")
    
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        print(f"Running specific test: {test_name}")
    else:
        test_name = None
        print("Running all parser tests")
    
    exit_code = run_test(test_name)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
