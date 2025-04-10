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


"""
OMEGA RASTA VIBES - FIBONACCI SEQUENCE TESTS 🌿🔥

Divine tests that verify the spiritual harmony of the Fibonacci sequence.
JAH BLESS THE GOLDEN RATIO!
"""

import sys
import os
import unittest
import pytest
from pathlib import Path

# Add project root to path (divine path alignment)
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def test_fibonacci_sequence():
    """Test if Fibonacci sequence is correctly generated."""
    def generate_fibonacci(n):
        """Generate first n Fibonacci numbers."""
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
        
    expected = [1, 1, 2, 3, 5, 8, 13, 21]
    actual = generate_fibonacci(8)
    assert actual == expected, "JAH BLESS - Fibonacci sequence is divine harmony!"

def test_golden_ratio_approximation():
    """Test if Fibonacci sequence approaches the divine Golden Ratio."""
    def generate_fibonacci(n):
        """Generate first n Fibonacci numbers."""
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
        
    # Calculate ratio of consecutive Fibonacci numbers
    fib = generate_fibonacci(20)
    ratio = fib[-1] / fib[-2]
    
    # Golden ratio is approximately 1.618033988749895
    golden_ratio = 1.618033988749895
    
    # Assert ratio is within 0.01% of golden ratio
    assert abs(ratio - golden_ratio) < 0.0001, "Fibonacci sequence approaches divine golden ratio!"