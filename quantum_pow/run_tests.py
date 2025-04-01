#!/usr/bin/env python3
"""
Test runner for Quantum Proof-of-Work (qPoW) implementation.

JAH BLESS SATOSHI
"""
import os
import sys
import unittest
import argparse

def run_tests(verbosity=2, pattern="test_*.py"):
    """Run all tests matching the pattern."""
    # Add the parent directory to the path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    
    # Discover and run the tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("quantum_pow/tests", pattern=pattern)
    
    test_runner = unittest.TextTestRunner(verbosity=verbosity)
    result = test_runner.run(test_suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run qPoW tests")
    parser.add_argument("-v", "--verbosity", type=int, default=2,
                      help="Verbosity level (1-3)")
    parser.add_argument("-p", "--pattern", default="test_*.py",
                      help="Pattern for test file discovery")
    
    args = parser.parse_args()
    sys.exit(run_tests(args.verbosity, args.pattern)) 