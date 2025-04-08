#!/usr/bin/env python3

"""
Test module for Omega Bot Farm core components.

This module discovers and runs all test cases for the core components.
Run this file directly to execute all tests in the suite.
"""

import os
import sys
import unittest

# Add the parent directory to sys.path to allow importing the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../')))


def run_tests():
    """Discover and run all tests in this package."""
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1) 