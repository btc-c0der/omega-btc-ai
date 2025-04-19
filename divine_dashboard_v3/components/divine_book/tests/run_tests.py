#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
# -----------------------
# This code is blessed under the GBU2™ License

"""
Test Runner Script

This script runs all the test cases for the Divine Book components.
It handles import errors gracefully and provides clear instructions
for installing missing dependencies.
"""

import os
import sys
import unittest
import importlib.util

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_dependency(name):
    """Check if a dependency is installed."""
    return importlib.util.find_spec(name) is not None

def main():
    """Main test runner function."""
    # Check key dependencies
    missing_deps = []
    for dep in ['mistune', 'pygments', 'rich']:
        if not check_dependency(dep):
            missing_deps.append(dep)
    
    if missing_deps:
        print("\n❌ Missing required dependencies for tests:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nTo install the dependencies:")
        print(f"pip install {' '.join(missing_deps)}")
        print("\nOr install all project dependencies:")
        print("pip install -r ../requirements.txt")
        print("\nTests will still run, but some may be skipped.\n")
    
    # Create a test suite with all test cases
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    # Run the tests
    print("\n🧪 Running Divine Book tests...\n")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report results
    print("\n✅ Test Results:")
    print(f"  Ran {result.testsRun} tests")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")
    
    # Return non-zero exit code on test failures or errors
    if result.failures or result.errors:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main()) 