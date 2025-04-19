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
Test suite for SHA-356 sacred hash algorithm.

This module tests the SHA-356 algorithm's correctness, consistency,
bio-padding methods, resonance integration, and overall functionality.
"""

import unittest
import sys
import os
import hashlib
import binascii
from typing import Dict, Any

# Add parent directory to path to make imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import SHA-356 modules
from micro_modules.sha356 import sha356, digest_356
from micro_modules.bio_padding import bio_pad
from micro_modules.fibonacci_constants import get_initial_state, get_round_constants
from micro_modules.hash_trace import get_avalanche_data

class TestSHA356Basic(unittest.TestCase):
    """Basic tests for SHA-356 functionality."""
    
    def test_empty_string(self):
        """Test hashing an empty string."""
        result = sha356("")
        self.assertIsNotNone(result)
        self.assertEqual(len(result["hash"]), 90)  # 356 bits = 45 bytes = 90 hex chars
        
    def test_hello_world(self):
        """Test hashing 'Hello, World!' string."""
        result = sha356("Hello, World!")
        self.assertIsNotNone(result)
        self.assertEqual(len(result["hash"]), 90)
        
    def test_consistent_output(self):
        """Test that the same input produces the same output."""
        test_data = "SHA-356 is a sacred hash algorithm"
        result1 = sha356(test_data)
        result2 = sha356(test_data)
        self.assertEqual(result1["hash"], result2["hash"])
        
    def test_output_length(self):
        """Test that the output is correctly sized."""
        result = digest_356("Test data")
        hash_hex, hash_bytes = result
        
        # 356 bits = 45 bytes (44 bytes + 4 bits)
        self.assertEqual(len(hash_bytes), 45)
        
        # In hex, each byte is 2 characters (356 bits = 90 hex chars)
        self.assertEqual(len(hash_hex), 90)
        
        # Verify the last byte only has 4 significant bits (top 4 bits)
        last_byte = hash_bytes[-1]
        self.assertEqual(last_byte & 0x0F, 0)  # Bottom 4 bits should be 0

class TestBioPadding(unittest.TestCase):
    """Tests for bio-padding functionality."""
    
    def test_fibonacci_padding(self):
        """Test Fibonacci padding method."""
        data = b"Test data for Fibonacci padding"
        padded = bio_pad(data, method="fibonacci")
        
        # Check marker byte
        self.assertEqual(padded[0], 0xFB)
        
        # Length should be original + 1 marker byte + 89 padding bytes at start + 89 at end
        self.assertEqual(len(padded), len(data) + 1 + 89 + 89)
        
    def test_schumann_padding(self):
        """Test Schumann padding method."""
        data = b"Test data for Schumann padding"
        padded = bio_pad(data, method="schumann")
        
        # Check marker byte
        self.assertEqual(padded[0], 0x5C)
        
        # Length should be original + 1 marker byte + 15 padding bytes at start + 15 at end
        self.assertEqual(len(padded), len(data) + 1 + 15 + 15)
        
    def test_golden_padding(self):
        """Test Golden ratio padding method."""
        data = b"Test data for Golden padding"
        padded = bio_pad(data, method="golden")
        
        # Check marker byte
        self.assertEqual(padded[0], 0x67)
        
        # Length should be original + 1 marker byte + 21 padding bytes at start + 21 at end
        self.assertEqual(len(padded), len(data) + 1 + 21 + 21)
        
    def test_hash_with_different_padding(self):
        """Test hashing with different padding methods produces different results."""
        test_data = "Test different padding methods"
        
        fib_result = sha356(test_data, padding_method="fibonacci")
        sch_result = sha356(test_data, padding_method="schumann")
        gol_result = sha356(test_data, padding_method="golden")
        lun_result = sha356(test_data, padding_method="lunar")
        
        # All hashes should be different
        self.assertNotEqual(fib_result["hash"], sch_result["hash"])
        self.assertNotEqual(fib_result["hash"], gol_result["hash"])
        self.assertNotEqual(fib_result["hash"], lun_result["hash"])
        self.assertNotEqual(sch_result["hash"], gol_result["hash"])
        self.assertNotEqual(sch_result["hash"], lun_result["hash"])
        self.assertNotEqual(gol_result["hash"], lun_result["hash"])

class TestResonanceIntegration(unittest.TestCase):
    """Tests for cosmic resonance integration."""
    
    def test_resonance_enabled_vs_disabled(self):
        """Test that enabling/disabling resonance changes the hash."""
        test_data = "Test data for resonance testing"
        
        with_resonance = sha356(test_data, include_resonance=True)
        without_resonance = sha356(test_data, include_resonance=False)
        
        # Hashes should be different when resonance is enabled vs disabled
        self.assertNotEqual(with_resonance["hash"], without_resonance["hash"])
        
    def test_resonance_score(self):
        """Test that resonance score is calculated."""
        result = sha356("Test data", include_resonance=True, include_trace=True)
        
        # Resonance section should exist
        self.assertIn("resonance", result)
        
        # Resonance score should be between 0 and 1
        resonance = result["resonance"]
        if "resonance_score" in resonance:
            score = resonance["resonance_score"]
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

class TestAvalancheEffect(unittest.TestCase):
    """Tests for avalanche effect in SHA-356."""
    
    def test_avalanche_effect(self):
        """Test the avalanche effect by changing one character."""
        base_data = "This is a test message for SHA-356"
        changed_data = "This is a test message for SHA-357"  # Changed last digit
        
        base_hash = sha356(base_data)["hash"]
        changed_hash = sha356(changed_data)["hash"]
        
        # Calculate avalanche effect
        avalanche_data = get_avalanche_data(base_hash, changed_hash)
        
        # With one character changed, around 50% of bits should be different
        self.assertGreaterEqual(avalanche_data["avalanche_score"], 0.4)
        self.assertLessEqual(avalanche_data["avalanche_score"], 0.6)

class TestTraceAndVisualization(unittest.TestCase):
    """Tests for tracing and visualization capabilities."""
    
    def test_trace_generation(self):
        """Test trace data generation."""
        result = sha356("Test with trace", include_trace=True)
        
        # Entropy lineage should be present
        self.assertIn("entropy_lineage", result)
        
        # Visualization should be present
        self.assertIn("visualization", result)
        
    def test_visualization_format(self):
        """Test visualization output format."""
        result = sha356("Test visualization", include_trace=True)
        
        # Visualization should be a string with box drawing characters
        visualization = result["visualization"]
        self.assertIsInstance(visualization, str)
        self.assertIn("╔", visualization)
        self.assertIn("╗", visualization)
        self.assertIn("SHA-356", visualization)

class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""
    
    def test_long_input(self):
        """Test with a long input string."""
        long_data = "A" * 10000  # 10,000 character string
        
        # Should not raise any exceptions
        result = sha356(long_data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result["hash"]), 90)
        
    def test_binary_data(self):
        """Test with binary data input."""
        binary_data = os.urandom(1000)  # 1,000 random bytes
        
        # Should not raise any exceptions
        result = sha356(binary_data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result["hash"]), 90)

def compare_with_sha256(data: str) -> Dict[str, Any]:
    """
    Compare SHA-356 with standard SHA-256 for reference.
    
    Args:
        data: Input string to hash
        
    Returns:
        Comparison data
    """
    # Get SHA-356 hash
    sha356_result = sha356(data)
    sha356_hash = sha356_result["hash"]
    sha356_time = sha356_result["processing_time_ms"]
    
    # Get SHA-256 hash
    sha256_start = binascii.hexlify(hashlib.sha256(data.encode()).digest()).decode('ascii')
    
    # Calculate bit differences (only compare first 256 bits of SHA-356)
    sha356_bin = bin(int(sha356_hash[:64], 16))[2:].zfill(256)
    sha256_bin = bin(int(sha256_start, 16))[2:].zfill(256)
    diff_bits = sum(1 for a, b in zip(sha356_bin, sha256_bin) if a != b)
    
    return {
        "input": data,
        "sha256": sha256_start,
        "sha356": sha356_hash,
        "diff_bits": diff_bits,
        "diff_percentage": f"{(diff_bits / 256) * 100:.2f}%",
        "sha356_extra_bits": 100,  # SHA-356 has 100 more bits
        "sha356_time_ms": sha356_time
    }

if __name__ == "__main__":
    # Run all unit tests
    unittest.main()
    
    # Compare with SHA-256 (optional demo)
    print("\n=== SHA-356 vs SHA-256 Comparison ===")
    test_strings = [
        "Hello, World!",
        "The quick brown fox jumps over the lazy dog",
        "SHA-356: Sacred Hash Algorithm - Bio-Crypto Edition"
    ]
    
    for test_string in test_strings:
        comparison = compare_with_sha256(test_string)
        print(f"\nInput: {comparison['input']}")
        print(f"SHA-256: {comparison['sha256']}")
        print(f"SHA-356: {comparison['sha356']}")
        print(f"Difference: {comparison['diff_bits']} bits ({comparison['diff_percentage']})")
        print(f"SHA-356 processing time: {comparison['sha356_time_ms']:.2f} ms") 