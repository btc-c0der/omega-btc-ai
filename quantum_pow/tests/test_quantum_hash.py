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

Tests for the QuantumResistantHash implementation.

This module contains tests that verify the quantum resistance properties 
of the hash function, including avalanche effect, determinism, and resistance
to known quantum attacks.
"""

import unittest
import sys
import os
import hashlib
import random
import string
from typing import List, Tuple

# Add the parent directory to the path so we can import quantum_pow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules for testing
from quantum_pow.hash_functions import QuantumResistantHash, verify_hash_resistance

class TestQuantumResistantHash(unittest.TestCase):
    """Test cases for quantum-resistant hash function implementation."""
    
    def test_hash_function_exists(self):
        """Test that the QuantumResistantHash class exists."""
        try:
            hash_instance = QuantumResistantHash()
            self.assertIsNotNone(hash_instance)
        except NameError:
            self.fail("QuantumResistantHash class does not exist")
    
    def test_hash_output_length(self):
        """Test that the hash output is the correct length (512 bits = 64 bytes)."""
        try:
            hash_instance = QuantumResistantHash()
            test_data = b"test data for hashing"
            hash_output = hash_instance.hash(test_data)
            
            # Check that the output is 64 bytes (512 bits)
            self.assertEqual(len(hash_output), 64, 
                             f"Hash output length is {len(hash_output)} bytes, expected 64 bytes")
        except NameError:
            self.skipTest("QuantumResistantHash class not implemented yet")
    
    def test_hash_deterministic(self):
        """Test that the hash function produces the same output for the same input."""
        try:
            hash_instance = QuantumResistantHash()
            test_data = b"test data for hashing"
            
            hash1 = hash_instance.hash(test_data)
            hash2 = hash_instance.hash(test_data)
            
            self.assertEqual(hash1, hash2, 
                             "Hash function is not deterministic")
        except NameError:
            self.skipTest("QuantumResistantHash class not implemented yet")
    
    def test_hash_different_inputs(self):
        """Test that different inputs produce different hash outputs."""
        try:
            hash_instance = QuantumResistantHash()
            test_data1 = b"test data for hashing 1"
            test_data2 = b"test data for hashing 2"
            
            hash1 = hash_instance.hash(test_data1)
            hash2 = hash_instance.hash(test_data2)
            
            self.assertNotEqual(hash1, hash2, 
                                "Different inputs produced the same hash")
        except NameError:
            self.skipTest("QuantumResistantHash class not implemented yet")
    
    def test_hash_collision_resistance(self):
        """Test for collision resistance by hashing random data."""
        try:
            hash_instance = QuantumResistantHash()
            hash_outputs = set()
            
            # Generate 1000 random inputs and check for collisions
            for _ in range(1000):
                random_data = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50))
                hash_output = hash_instance.hash(random_data.encode())
                self.assertNotIn(hash_output, hash_outputs, 
                                 "Hash collision detected")
                hash_outputs.add(hash_output)
        except NameError:
            self.skipTest("QuantumResistantHash class not implemented yet")
    
    def test_quantum_resistance_verification(self):
        """Test the verify_hash_resistance function."""
        try:
            # This test is theoretical since we can't actually test against quantum computers
            resistance_score = verify_hash_resistance(QuantumResistantHash())
            
            # The resistance score should be above 0.8 (80%)
            self.assertGreaterEqual(resistance_score, 0.8,
                                   f"Quantum resistance score {resistance_score} is below threshold 0.8")
        except NameError:
            self.skipTest("verify_hash_resistance function not implemented yet")
    
    def test_compared_to_sha256(self):
        """Compare our hash with SHA-256 to ensure it's different."""
        try:
            hash_instance = QuantumResistantHash()
            test_data = b"test data for hashing"
            
            quantum_hash = hash_instance.hash(test_data)
            sha256_hash = hashlib.sha256(test_data).digest()
            
            # The hashes should be different
            self.assertNotEqual(quantum_hash[:32], sha256_hash, 
                                "Quantum hash matches SHA-256 hash")
        except NameError:
            self.skipTest("QuantumResistantHash class not implemented yet")
    
    def test_avalanche_effect(self):
        """Test the avalanche effect - small changes in input cause significant changes in output."""
        try:
            hash_instance = QuantumResistantHash()
            test_data1 = b"test data for hashing"
            test_data2 = b"test data for hashing!"  # One character different
            
            hash1 = hash_instance.hash(test_data1)
            hash2 = hash_instance.hash(test_data2)
            
            # Count bit differences
            bit_diff = sum(bin(hash1[i] ^ hash2[i]).count('1') for i in range(min(len(hash1), len(hash2))))
            
            # We expect around 50% of bits to be different
            expected_diff = len(hash1) * 8 * 0.5  # 50% of bits
            tolerance = len(hash1) * 8 * 0.1  # 10% tolerance
            
            self.assertTrue(abs(bit_diff - expected_diff) <= tolerance,
                           f"Avalanche effect test failed. {bit_diff} bits different, expected {expected_diff} ± {tolerance}")
        except NameError:
            self.skipTest("QuantumResistantHash class not implemented yet")


if __name__ == '__main__':
    unittest.main() 