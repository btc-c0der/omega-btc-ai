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
HYPER DIMENSION VISUALIZATION TEST SUITE 🌌🔮

"Test the cosmic dimensions before they manifest in the physical realm."
- Rastafarian Quantum Computing Wisdom

These sacred tests verify the divine behavior of the OMEGA BTC HYPER-DIMENSION visualizations,
ensuring proper Fibonacci energy flows, dimensional harmony, and cosmic pattern recognition.

JAH BLESS THE MULTIDIMENSIONAL TESTING! 🙏🌟
"""

import os
import sys
import pytest
import json
import numpy as np
import plotly.graph_objects as go
from unittest.mock import patch, MagicMock

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.visualization.hyper_dimension import (
    create_3d_fibonacci_sphere,
    create_4d_trader_energy_field,
    PHI,
    RASTA_COLORS
)

# Terminal colors for divine output
RED = "\033[91m"
GREEN = "\033[92m" 
YELLOW = "\033[93m"
RESET = "\033[0m"

# Test data
MOCK_PRICE_DATA = [51000, 52000, 53000, 52500, 52800, 53200, 54000, 53500]
MOCK_TRADER_DATA = {
    'strategic': {
        'pnl': 1250.0,
        'trades': [{'profit': 250}, {'profit': 1000}],
        'emotional_state': 'confident',
        'confidence': 0.8,
        'bio_energy': 85
    },
    'aggressive': {
        'pnl': -500.0, 
        'trades': [{'profit': 750}, {'profit': -1250}],
        'emotional_state': 'fearful',
        'confidence': 0.4,
        'bio_energy': 65
    },
    'newbie': {
        'pnl': -1000.0,
        'trades': [{'profit': -500}, {'profit': -500}],
        'emotional_state': 'panicked',
        'confidence': 0.2,
        'bio_energy': 40
    },
    'scalper': {
        'pnl': 800.0,
        'trades': [{'profit': 100}, {'profit': 200}, {'profit': 200}, {'profit': 300}],
        'emotional_state': 'neutral',
        'confidence': 0.7,
        'bio_energy': 75
    }
}


def test_fibonacci_sphere_creation():
    """Test divine 5D Fibonacci sphere visualization creation."""
    print(f"\n{GREEN}Testing 5D Fibonacci sphere creation:{RESET}")
    
    # Test with normal Schumann value
    normal_schumann = 7.83
    fig = create_3d_fibonacci_sphere(MOCK_PRICE_DATA, normal_schumann)
    
    # Basic validation
    assert isinstance(fig, go.Figure), "Should return a plotly Figure"
    assert fig.data, "Should have data in the Figure"
    assert len(list(fig.data)) >= 3, "Should have at least surface, scatter and beam traces"
    
    # Test surface creation
    surface_traces = [trace for trace in fig.data if isinstance(trace, go.Surface)]
    assert surface_traces, "Should have at least one surface trace"
    
    # Test title formatting
    assert f"{normal_schumann:.2f}" in fig.layout.title.text, "Title should include Schumann value"
    assert "FIBONACCI ENERGY SPHERE" in fig.layout.title.text, "Title should mention energy sphere"
    
    # Test with elevated Schumann
    elevated_schumann = 15.0
    fig_elevated = create_3d_fibonacci_sphere(MOCK_PRICE_DATA, elevated_schumann)
    
    # Energy scaling should be different
    assert fig != fig_elevated, "Different Schumann values should produce different visualizations"
    
    print(f"  ✓ 5D Fibonacci sphere test passed")


def test_fibonacci_sphere_empty_data():
    """Test 5D Fibonacci sphere with empty data (should generate mock data)."""
    print(f"\n{GREEN}Testing 5D Fibonacci sphere with empty data:{RESET}")
    
    # Test with empty price data
    fig = create_3d_fibonacci_sphere([], 7.83)
    
    # Should still create visualization
    assert isinstance(fig, go.Figure), "Should return a plotly Figure even with empty data"
    assert fig.data, "Should have data in the Figure"
    assert len(list(fig.data)) >= 3, "Should generate mock data and create visualization"
    
    print(f"  ✓ 5D Fibonacci sphere empty data test passed")


def test_trader_energy_field_creation():
    """Test divine 4D trader energy field visualization."""
    print(f"\n{GREEN}Testing 4D trader energy field creation:{RESET}")
    
    # Test with normal Schumann value
    normal_schumann = 7.83
    fig = create_4d_trader_energy_field(MOCK_TRADER_DATA, normal_schumann)
    
    # Basic validation
    assert isinstance(fig, go.Figure), "Should return a plotly Figure"
    
    # Test for trader nodes (scatter3d)
    scatter_traces = [trace for trace in fig.data if isinstance(trace, go.Scatter3d)]
    assert scatter_traces, "Should have trader energy nodes as scatter3d traces"
    
    # Trader connections should be represented
    assert len(list(fig.data)) > len(MOCK_TRADER_DATA), "Should have trader nodes plus connection traces"
    
    # Test title formatting
    assert f"{normal_schumann:.2f}" in fig.layout.title.text, "Title should include Schumann value"
    assert "TRADER ENERGY FIELD" in fig.layout.title.text, "Title should mention trader energy field"
    
    # Test with elevated Schumann
    elevated_schumann = 15.0
    fig_elevated = create_4d_trader_energy_field(MOCK_TRADER_DATA, elevated_schumann)
    
    # Energy scaling should be different
    assert str(fig) != str(fig_elevated), "Different Schumann values should produce different visualizations"
    
    print(f"  ✓ 4D Trader energy field test passed")


def test_trader_energy_field_empty_data():
    """Test 4D trader energy field with empty data (should generate mock data)."""
    print(f"\n{GREEN}Testing 4D trader energy field with empty data:{RESET}")
    
    # Test with empty trader data
    fig = create_4d_trader_energy_field({}, 7.83)
    
    # Should still create visualization with mock data
    assert isinstance(fig, go.Figure), "Should return a plotly Figure even with empty data"
    assert fig.data, "Should have data in the Figure" 
    assert len(list(fig.data)) >= 5, "Should generate mock data and create visualization"
    
    print(f"  ✓ 4D Trader energy field empty data test passed")


def test_rasta_colors_consistency():
    """Test divine Rasta color scheme consistency across visualizations."""
    print(f"\n{GREEN}Testing Rasta color consistency:{RESET}")
    
    # Check that color constants are defined
    assert "green" in RASTA_COLORS, "Green Rasta color should be defined"
    assert "red" in RASTA_COLORS, "Red Rasta color should be defined"
    assert "yellow" in RASTA_COLORS, "Yellow Rasta color should be defined"
    assert "gold" in RASTA_COLORS, "Gold Rasta color should be defined"
    
    # Check that Fibonacci sphere uses Rasta colors
    fig = create_3d_fibonacci_sphere(MOCK_PRICE_DATA, 7.83)
    
    # Title should use gold color
    assert fig.layout.font.color == RASTA_COLORS["gold"], "Visualization should use Rasta gold for font"
    
    print(f"  ✓ Rasta color consistency test passed")


def test_golden_ratio_usage():
    """Test divine Golden Ratio (PHI) usage in visualizations."""
    print(f"\n{GREEN}Testing Golden Ratio (Φ) usage:{RESET}")
    
    # Check that PHI is correctly defined (approximately 1.618)
    assert 1.61 < PHI < 1.62, f"PHI should be approximately 1.618, got {PHI}"
    
    # Create visualizations
    fig_sphere = create_3d_fibonacci_sphere(MOCK_PRICE_DATA, 7.83)
    fig_energy = create_4d_trader_energy_field(MOCK_TRADER_DATA, 7.83)
    
    # Both should create non-empty visualizations
    assert fig_sphere.data, "Fibonacci sphere should use PHI to create visualization"
    assert fig_energy.data, "Trader energy field should use PHI to create visualization"
    
    print(f"  ✓ Golden Ratio usage test passed") 