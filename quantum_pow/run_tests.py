#!/usr/bin/env python3
"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

Test runner for Quantum Proof-of-Work (qPoW) implementation.

This script runs the comprehensive test suite for the qPoW system, including:
- Quantum-resistant hash function tests
- Block structure and manipulation tests 
- Mining process tests
- Ecosystem component tests
- Denarius-inspired feature tests

JAH BLESS SATOSHI
"""
import os
import sys
import unittest
import argparse

def run_tests(verbosity=2, pattern="test_*.py"):
    """
    Run qPoW test suite.
    
    Args:
        verbosity: Verbosity level (0-3)
        pattern: Pattern for test file discovery
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add parent directory to path for proper importing
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Discover and run tests
    loader = unittest.TestLoader()
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(test_dir, pattern=pattern)
    
    print(f"=== Running Quantum Proof-of-Work (qPoW) Tests ===")
    print(f"JAH BLESS SATOSHI")
    
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run qPoW test suite')
    parser.add_argument('-v', '--verbosity', type=int, default=2, 
                      help='Verbosity level (0-3)')
    parser.add_argument('-p', '--pattern', default='test_*.py',
                      help='Pattern for test file discovery')
    parser.add_argument('--denarius-only', action='store_true',
                      help='Run only Denarius-inspired feature tests')
    
    args = parser.parse_args()
    
    # Handle Denarius-only flag
    if args.denarius_only:
        pattern = 'test_denarius_features.py'
        print("Running only Denarius-inspired feature tests...")
    else:
        pattern = args.pattern
    
    sys.exit(run_tests(verbosity=args.verbosity, pattern=pattern)) 