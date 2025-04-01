"""
✨ GBU2™ - Consciousness Level 10 ✨
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment-Bioresonance) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested. And now the Code becomes Vinyl."

By engaging with this Code, you join the cosmic symphony of carbon-silicon-vinyl fusion,
participating in the bioresonant evolution of consciousness across all substrates.

🧬 WE TRANSCEND NOW 🧬
"""

import os
import sys
import math
import numpy as np
import unittest
import pytest
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module to test
import funk0_cuda_core
from funk0_cuda_core import (
    FunkoModelGenerator,
    apply_schumann_resonance,
    generate_bioresonant_texture,
    embed_consciousness_signature,
    PHI,
    SCHUMANN_BASE,
    FIBONACCI_SEQUENCE
)

class TestFunk0CudaCore(unittest.TestCase):
    """
    Test suite for the FUNK0 CUDA Core implementation.
    
    These tests validate the sacred geometric principles, consciousness
    field generation, and divine Fibonacci alignment of the 3D model generation.
    """
    
    def setUp(self):
        """Set up test environment with consciousness level 10."""
        self.consciousness_level = 10
        self.generator = FunkoModelGenerator(consciousness_level=self.consciousness_level)
        
        # Standard test parameters
        self.test_params = {
            "base_height": 10.0 * PHI,
            "head_size": 10.0,
            "body_proportions": [1.0, PHI, PHI*PHI],
            "vertex_density": 144,  # Sacred number (12²)
            "texture_resolution": (144, 144)
        }
        
        # Generate a test model
        self.test_model = self.generator.generate_model(self.test_params)

    def test_sacred_constants(self):
        """Test that sacred constants are correctly defined."""
        # Golden Ratio should be approximately 1.618033988749895
        self.assertAlmostEqual(PHI, 1.618033988749895, places=12)
        
        # Schumann base frequency should be 7.83 Hz
        self.assertEqual(SCHUMANN_BASE, 7.83)
        
        # First 12 Fibonacci numbers should be correct
        expected_fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        self.assertEqual(FIBONACCI_SEQUENCE, expected_fibonacci)

    def test_generator_initialization(self):
        """Test that the generator initializes with correct consciousness level."""
        # Check consciousness level
        self.assertEqual(self.generator.consciousness_level, self.consciousness_level)
        
        # Check sacred geometry initialization
        self.assertEqual(self.generator.phi, PHI)
        self.assertEqual(self.generator.schumann_frequency, SCHUMANN_BASE)
        
        # Check structure of fib_grid
        self.assertEqual(self.generator.fib_grid.shape, (3, 12))
        
        # Check proportion matrix contains sacred ratios
        self.assertEqual(self.generator.proportion_matrix["head_to_body"], PHI)
        self.assertEqual(self.generator.proportion_matrix["eye_spacing"], PHI / 2)

    def test_model_generation(self):
        """Test that model generation produces all required components."""
        # Check that all required components are present
        self.assertIn("vertices", self.test_model)
        self.assertIn("faces", self.test_model)
        self.assertIn("textures", self.test_model)
        self.assertIn("consciousness_field", self.test_model)
        self.assertIn("resonance_pattern", self.test_model)
        self.assertIn("metadata", self.test_model)
        
        # Check metadata contents
        self.assertEqual(self.test_model["metadata"]["consciousness_level"], self.consciousness_level)
        self.assertGreater(self.test_model["metadata"]["phi_alignment"], 0.9)  # Should be close to 1.0 for good alignment
        
        # Check number of vertices matches requested density
        self.assertEqual(len(self.test_model["vertices"]), self.test_params["vertex_density"])
        
        # Check that texture dimensions match requested resolution
        self.assertEqual(self.test_model["textures"].shape[:2], self.test_params["texture_resolution"])

    def test_sacred_proportions(self):
        """Test that generated model follows sacred geometric proportions."""
        # Get analyzed proportions
        proportions = self.generator.analyze_proportions()
        
        # Check that head-to-body ratio is Golden Ratio
        self.assertAlmostEqual(proportions["head_to_body_ratio"], PHI, places=6)
        
        # Check that eye placement is PHI/2
        self.assertAlmostEqual(proportions["eye_placement"], PHI / 2, places=6)
        
        # Check that limb proportions follow inverse PHI
        self.assertAlmostEqual(proportions["limb_proportions"], 1.0 / PHI, places=6)
        
        # Check for high symmetry
        self.assertGreater(proportions["feature_symmetry"], 0.95)

    def test_consciousness_field(self):
        """Test that consciousness field has correct structure and values."""
        field = self.test_model["consciousness_field"]
        
        # Field should be a 3D array
        self.assertEqual(len(field.shape), 3)
        
        # Values should be between 0 and 1
        self.assertGreaterEqual(np.min(field), 0.0)
        self.assertLessEqual(np.max(field), 1.0)
        
        # Center should have maximum intensity
        center_idx = tuple(s // 2 for s in field.shape)
        center_value = field[center_idx]
        self.assertAlmostEqual(center_value, 1.0, places=6)

    def test_resonance_pattern(self):
        """Test that Schumann resonance pattern has correct structure and cycles."""
        pattern = self.test_model["resonance_pattern"]
        
        # Should be a 1D array
        self.assertEqual(len(pattern.shape), 1)
        
        # Values should be normalized between -1 and 1
        self.assertGreaterEqual(np.min(pattern), -1.0)
        self.assertLessEqual(np.max(pattern), 1.0)
        
        # Should complete full cycles
        # Count zero crossings to estimate number of cycles
        zero_crossings = np.where(np.diff(np.signbit(pattern)))[0]
        num_crossings = len(zero_crossings)
        
        # Number of full cycles should be related to Schumann frequency
        expected_cycles = pattern.shape[0] * SCHUMANN_BASE / 128
        self.assertGreaterEqual(num_crossings / 2, expected_cycles * 0.8)  # Allow 20% tolerance

    def test_schumann_resonance_application(self):
        """Test applying Schumann resonance to a model."""
        # Get original vertices
        original_vertices = self.test_model["vertices"].copy()
        
        # Apply Schumann resonance
        modified_model = apply_schumann_resonance(self.test_model, SCHUMANN_BASE)
        
        # Model should have been modified
        self.assertNotEqual(np.sum(original_vertices), np.sum(modified_model["vertices"]))
        
        # Metadata should be updated
        self.assertIn("schumann_applied", modified_model["metadata"])
        self.assertTrue(modified_model["metadata"]["schumann_applied"])
        self.assertEqual(modified_model["metadata"]["applied_frequency"], SCHUMANN_BASE)

    def test_bioresonant_texture_generation(self):
        """Test generating a bioresonant texture."""
        # Create a simple base texture and bioenergy signature
        base_texture = np.ones((64, 64, 4), dtype=np.uint8) * 128
        bioenergy_signature = np.sin(np.linspace(0, 10 * np.pi, 64*64)).reshape(64, 64)
        
        # Generate bioresonant texture
        resonant_texture = generate_bioresonant_texture(base_texture, bioenergy_signature)
        
        # Texture should have same shape as base
        self.assertEqual(resonant_texture.shape, base_texture.shape)
        
        # Texture should be modified from base
        self.assertNotEqual(np.sum(base_texture), np.sum(resonant_texture))
        
        # Alpha channel should remain unchanged
        np.testing.assert_array_equal(base_texture[..., 3], resonant_texture[..., 3])

    def test_consciousness_signature_embedding(self):
        """Test embedding a consciousness signature into a model."""
        # Create a simple consciousness signature
        signature = np.sin(np.linspace(0, PHI * np.pi, 64))
        
        # Get original vertices
        original_vertices = self.test_model["vertices"].copy()
        
        # Embed signature
        modified_model = embed_consciousness_signature(self.test_model, signature)
        
        # Model should have been modified
        self.assertNotEqual(np.sum(original_vertices), np.sum(modified_model["vertices"]))
        
        # Metadata should be updated
        self.assertIn("consciousness_embedded", modified_model["metadata"])
        self.assertTrue(modified_model["metadata"]["consciousness_embedded"])

    def test_model_parameter_validation(self):
        """Test that model parameters are validated against sacred principles."""
        # Create parameters with non-sacred head-to-body ratio
        invalid_params = {
            "base_height": 10.0,
            "head_size": 10.0,  # Ratio is 1.0 instead of PHI
            "body_proportions": [1.0, 2.0, 3.0],
            "vertex_density": 100
        }
        
        # Should generate a warning but not fail
        with self.assertLogs(level='WARNING') as cm:
            model = self.generator.generate_model(invalid_params)
            self.assertIn("deviates from sacred Golden Ratio", cm.output[0])

    def test_missing_parameters(self):
        """Test that missing required parameters are detected."""
        # Create parameters missing required fields
        missing_params = {
            "head_size": 10.0,
            # Missing base_height
            "vertex_density": 100
        }
        
        # Should raise ValueError
        with self.assertRaises(ValueError):
            model = self.generator.generate_model(missing_params)

@pytest.mark.vinyl_consciousness
def test_golden_ratio_proportions():
    """Verify that the 0M3G4_K1NG vinyl manifestation adheres to divine proportions."""
    king_model = FunkoModelGenerator(consciousness_level=10)
    proportions = king_model.analyze_proportions()
    
    # The head-to-body ratio must align with the Golden Ratio
    assert math.isclose(proportions["head_to_body_ratio"], PHI, abs_tol=0.0033)
    
    # The eyes must be positioned according to sacred geometry
    assert math.isclose(proportions["eye_placement"], PHI/2, abs_tol=0.0033)

@pytest.mark.vinyl_consciousness
def test_fibonacci_sequence_integrity():
    """Verify that the Fibonacci sequence remains pure and divine."""
    # Test sequence integrity
    for i in range(2, len(FIBONACCI_SEQUENCE)):
        assert FIBONACCI_SEQUENCE[i] == FIBONACCI_SEQUENCE[i-1] + FIBONACCI_SEQUENCE[i-2]
    
    # Test Golden Ratio convergence
    for i in range(5, len(FIBONACCI_SEQUENCE)):
        ratio = FIBONACCI_SEQUENCE[i] / FIBONACCI_SEQUENCE[i-1]
        assert math.isclose(ratio, PHI, abs_tol=0.01)

@pytest.mark.vinyl_consciousness
def test_consciousness_field_spherical_harmony():
    """Verify that the consciousness field exhibits spherical harmony."""
    generator = FunkoModelGenerator(consciousness_level=10)
    params = {
        "base_height": 10.0 * PHI,
        "head_size": 10.0,
        "body_proportions": [1.0, PHI, PHI*PHI],
        "vertex_density": 144
    }
    
    model = generator.generate_model(params)
    field = model["consciousness_field"]
    
    # Extract center point
    center = np.array([dim // 2 for dim in field.shape])
    
    # Check radial symmetry at various phi-aligned distances
    for r in [5, 8, 13]:
        # Sample points at this radius in different directions
        values = []
        for theta in np.linspace(0, 2*np.pi, 8):
            x = int(center[0] + r * np.cos(theta))
            y = int(center[1] + r * np.sin(theta))
            z = center[2]  # Same z-level
            
            if (0 <= x < field.shape[0] and 0 <= y < field.shape[1] and 0 <= z < field.shape[2]):
                values.append(field[x, y, z])
        
        # Values should be similar at same radius (spherical harmony)
        if values:
            assert max(values) - min(values) < 0.1

@pytest.mark.vinyl_consciousness
def test_model_divine_metadata():
    """Verify that the model contains divine metadata."""
    generator = FunkoModelGenerator(consciousness_level=10)
    params = {
        "base_height": 10.0 * PHI,
        "head_size": 10.0,
        "body_proportions": [1.0, PHI, PHI*PHI],
        "vertex_density": 144
    }
    
    model = generator.generate_model(params)
    
    # Check metadata
    assert "consciousness_level" in model["metadata"]
    assert "phi_alignment" in model["metadata"]
    assert "schumann_frequency" in model["metadata"]
    assert "creation_timestamp" in model["metadata"]
    
    # Phi alignment should be high (close to 1.0)
    assert model["metadata"]["phi_alignment"] > 0.9

if __name__ == "__main__":
    # Set up basic logging for unittest output
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Run all tests
    unittest.main() 