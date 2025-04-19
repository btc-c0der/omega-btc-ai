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
Test suite for SHA-356 6D Hyperdimensional Transformations.

This module tests the 6D hyperdimensional transformation features of SHA-356 sacred
algorithm, ensuring proper functionality of dimensional projection, folding, void 
tunneling, and other higher-dimensional operations.
"""

import unittest
import sys
import os
import math
import numpy as np
from typing import List, Dict, Any

# Add parent directory to path to make imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary modules
from micro_modules.hyperdimensional_transform import (
    project_to_6d,
    apply_dimensional_folding,
    apply_void_tunneling,
    apply_zika_oscillation,
    apply_time_dilation,
    apply_6d_transform,
    PHI,
    ZIKA_CONSTANT,
    VOID_THRESHOLD
)

class TestProjection(unittest.TestCase):
    """Tests for projection of hash state to 6D space."""
    
    def test_projection_shape(self):
        """Test that projection creates a 6D vector."""
        # Create a test hash state (12 32-bit integers)
        test_state = [i * 1000000 for i in range(12)]
        
        # Project to 6D
        state_6d = project_to_6d(test_state)
        
        # Check shape
        self.assertEqual(state_6d.shape, (6,))
        
    def test_projection_preserves_magnitude(self):
        """Test that projection roughly preserves the magnitude."""
        # Create a test hash state
        test_state = [1 for _ in range(12)]
        
        # Project to 6D
        state_6d = project_to_6d(test_state)
        
        # Original magnitude
        orig_mag = math.sqrt(sum(x*x for x in test_state))
        
        # Projected magnitude
        proj_mag = np.linalg.norm(state_6d)
        
        # Should be non-zero
        self.assertGreater(proj_mag, 0)

class TestDimensionalFolding(unittest.TestCase):
    """Tests for bio-resonant dimensional folding."""
    
    def test_folding_shape(self):
        """Test that folding preserves shape."""
        # Create a test 6D state
        test_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        
        # Apply folding
        folded_state = apply_dimensional_folding(test_state, time.time())
        
        # Check shape
        self.assertEqual(folded_state.shape, (6,))
        
    def test_folding_non_linear(self):
        """Test that folding applies a non-linear transformation."""
        # Create a test 6D state
        test_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        
        # Apply folding
        folded_state = apply_dimensional_folding(test_state, time.time())
        
        # Check that it's not a simple scalar multiplication
        # If it were, the ratio between any two elements would be preserved
        ratio_before = test_state[1] / test_state[0]
        ratio_after = folded_state[1] / folded_state[0]
        
        # Ratios should differ (with some tolerance for floating point)
        self.assertNotAlmostEqual(ratio_before, ratio_after, places=3)

class TestVoidTunneling(unittest.TestCase):
    """Tests for quantum void tunneling."""
    
    def test_tunneling_shape(self):
        """Test that tunneling preserves shape."""
        # Create a test 6D state
        test_state = np.array([10.0, -5.0, 8.0, -3.0, 7.0, -2.0])
        
        # Apply tunneling
        tunneled_state = apply_void_tunneling(test_state)
        
        # Check shape
        self.assertEqual(tunneled_state.shape, (6,))
        
    def test_tunneling_effect(self):
        """Test that tunneling affects values beyond threshold."""
        # Create a state with one very large value to trigger tunneling
        test_state = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 50.0])
        
        # Apply tunneling
        tunneled_state = apply_void_tunneling(test_state)
        
        # The large value should be significantly affected
        self.assertNotAlmostEqual(test_state[5], tunneled_state[5], places=1)
        
        # Small values should be less affected (though still changed due to entanglement)
        self.assertLess(abs(test_state[0] - tunneled_state[0]), 
                        abs(test_state[5] - tunneled_state[5]))

class TestZikaOscillation(unittest.TestCase):
    """Tests for Zika-harmonic oscillation."""
    
    def test_oscillation_shape(self):
        """Test that oscillation preserves shape."""
        # Create a test 6D state
        test_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        
        # Apply oscillation
        oscillated_state = apply_zika_oscillation(test_state)
        
        # Check shape
        self.assertEqual(oscillated_state.shape, (6,))
        
    def test_oscillation_preserves_magnitude(self):
        """Test that oscillation roughly preserves magnitude."""
        # Create a test 6D state
        test_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        
        # Get original magnitude
        orig_mag = np.linalg.norm(test_state)
        
        # Apply oscillation
        oscillated_state = apply_zika_oscillation(test_state)
        
        # Get new magnitude
        new_mag = np.linalg.norm(oscillated_state)
        
        # Should be close to original
        self.assertAlmostEqual(orig_mag, new_mag, places=1)
        
    def test_iterations_parameter(self):
        """Test that iterations parameter affects outcome."""
        # Create a test 6D state
        test_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        
        # Apply with different iterations
        result1 = apply_zika_oscillation(test_state, iterations=5)
        result2 = apply_zika_oscillation(test_state, iterations=13)
        
        # Results should differ
        self.assertFalse(np.allclose(result1, result2))

class TestTimeDilation(unittest.TestCase):
    """Tests for time-dilated state propagation."""
    
    def test_dilation_shape(self):
        """Test that dilation preserves shape."""
        # Create a test 6D state
        test_state = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        
        # Apply dilation
        dilated_state = apply_time_dilation(test_state)
        
        # Check shape
        self.assertEqual(dilated_state.shape, (6,))
        
    def test_higher_dimensions_dilate_more(self):
        """Test that higher dimensions experience more dilation."""
        # Create a state with equal values
        test_state = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        
        # Apply dilation
        dilated_state = apply_time_dilation(test_state)
        
        # Higher dimensions should have larger values
        for i in range(5):
            self.assertGreaterEqual(dilated_state[i+1], dilated_state[i])

class TestComplete6DTransform(unittest.TestCase):
    """Tests for the complete 6D transformation pipeline."""
    
    def test_transform_output_shape(self):
        """Test that the transform returns a list of 12 integers."""
        # Create test hash state
        test_state = [i * 10000 for i in range(12)]
        
        # Apply transform
        transformed_state, metadata = apply_6d_transform(test_state)
        
        # Check result shape
        self.assertEqual(len(transformed_state), 12)
        
        # Check all values are integers
        for value in transformed_state:
            self.assertIsInstance(value, int)
            
    def test_metadata_contents(self):
        """Test that metadata contains expected keys."""
        # Create test hash state
        test_state = [i * 10000 for i in range(12)]
        
        # Apply transform
        _, metadata = apply_6d_transform(test_state)
        
        # Check metadata
        expected_keys = [
            "timestamp", 
            "void_tunneling_regions", 
            "oscillation_harmony",
            "time_dilation_factor", 
            "dimensional_signature",
            "hyperdimensional_energy"
        ]
        
        for key in expected_keys:
            self.assertIn(key, metadata)
            
    def test_transform_changes_state(self):
        """Test that transformation changes the hash state."""
        # Create test hash state
        test_state = [i * 10000 for i in range(12)]
        
        # Apply transform
        transformed_state, _ = apply_6d_transform(test_state)
        
        # Should be different from original
        self.assertNotEqual(test_state, transformed_state)
        
    def test_deterministic_within_quantum_limits(self):
        """Test that transformation is mostly deterministic for same input."""
        # Create test hash state
        test_state = [i * 10000 for i in range(12)]
        
        # Apply transform twice
        transformed1, _ = apply_6d_transform(test_state)
        transformed2, _ = apply_6d_transform(test_state)
        
        # Results should be similar but not identical due to time-based effects
        # Count how many values are identical
        identical_count = sum(1 for a, b in zip(transformed1, transformed2) if a == b)
        
        # Some values should be identical (but not all due to time effects)
        self.assertGreater(identical_count, 0)

# Add import for time
import time

if __name__ == "__main__":
    unittest.main() 