#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
Test Runner for Divine Book Components

This script discovers and runs all the test cases for Divine Book modules.
"""

import unittest
import os
import sys
import importlib.util

# Add the current directory to the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    """Discover and run all test cases."""
    print("=" * 70)
    print("RUNNING TEST CASES FOR DIVINE BOOK COMPONENTS")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    
    # Discover tests in current directory
    start_dir = os.path.dirname(os.path.abspath(__file__))
    test_suite = loader.discover(start_dir, pattern="test_*.py")
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(test_suite)
    
    # Print a summary
    print("\n" + "=" * 70)
    print(f"TEST SUMMARY: {result.testsRun} tests run")
    print(f"- SUCCESSES: {result.testsRun - len(result.errors) - len(result.failures)}")
    print(f"- FAILURES: {len(result.failures)}")
    print(f"- ERRORS: {len(result.errors)}")
    print("=" * 70)
    
    # Return success status for CI/CD pipelines
    return len(result.failures) == 0 and len(result.errors) == 0

def run_specific_test(test_file):
    """Run a specific test file."""
    test_path = os.path.join(current_dir, test_file)
    if not os.path.exists(test_path):
        print(f"Error: Test file {test_path} does not exist.")
        return False
    
    # Load the test module
    spec = importlib.util.spec_from_file_location("test_module", test_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    
    # Create test suite from the module
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    # Check if a specific test file was specified
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        success = run_tests()
    
    # Exit with appropriate status code for CI/CD systems
    sys.exit(0 if success else 1) 