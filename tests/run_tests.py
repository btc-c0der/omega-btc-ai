#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
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

# -*- coding: utf-8 -*-

"""
Test runner script for the OMEGA CLI DIVINE PORTAL tests.
"""

import unittest
import sys
import os

def run_tests():
    """Run all tests in the test suite."""
    # Add the project root directory to the Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)
    
    # Add the tests directory to the Python path
    tests_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, tests_dir)
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Discover tests in the portal directory
    loader = unittest.TestLoader()
    portal_tests = loader.discover(os.path.join(tests_dir, 'portal'), pattern='test_*.py')
    suite.addTests(portal_tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 