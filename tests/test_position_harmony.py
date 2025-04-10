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
Tests for PositionHarmonyManager

This module tests the PositionHarmonyManager class that analyzes position harmony
based on Fibonacci principles.
"""

import pytest
import unittest.mock as mock
import os
import sys
import math

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the class to test
from position_harmony import PositionHarmonyManager

# Define constants similar to those in position_harmony.py
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
FIBONACCI_RATIOS = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]

class TestPositionHarmonyManager:
    """Tests for the PositionHarmonyManager class."""
    
    @pytest.fixture
    def manager(self):
        """Create a PositionHarmonyManager instance."""
        return PositionHarmonyManager()
    
    @pytest.fixture
    def mock_positions(self):
        """Create a set of mock positions for testing."""
        return [
            {
                "symbol": "BTCUSDT_UMCBL",
                "side": "long",
                "contracts": "0.1",
                "notional": "5000.0",
                "entryPrice": "50000.0",
                "markPrice": "51000.0",
                "unrealizedPnl": "100.0",
                "leverage": "10"
            },
            {
                "symbol": "ETHUSDT_UMCBL",
                "side": "short",
                "contracts": "1.0",
                "notional": "3000.0",
                "entryPrice": "3000.0",
                "markPrice": "2900.0",
                "unrealizedPnl": "100.0",
                "leverage": "5"
            }
        ]
    
    def test_init(self, manager):
        """Test the initialization of PositionHarmonyManager."""
        assert manager.phi == GOLDEN_RATIO
        assert manager.fibonacci_ratios == FIBONACCI_RATIOS
    
    def test_analyze_positions_empty(self, manager):
        """Test analyzing an empty positions list."""
        result = manager.analyze_positions([], 1000.0)
        
        # Should return a valid analysis structure
        assert isinstance(result, dict)
        assert "harmony_score" in result
        assert "harmony_state" in result
        assert "divine_advice" in result
        
        # With empty positions, score should be 0
        assert result["harmony_score"] == 0.0
        assert result["harmony_state"] == "UNBALANCED"
    
    def test_analyze_positions(self, manager, mock_positions):
        """Test analyzing positions."""
        result = manager.analyze_positions(mock_positions, 10000.0)
        
        # Should return a valid analysis structure
        assert isinstance(result, dict)
        assert "harmony_score" in result
        assert "harmony_state" in result
        assert "divine_advice" in result
        assert "recommendations" in result
        assert "ideal_position_sizes" in result
        
        # Harmony score should be between 0 and 1
        assert 0.0 <= result["harmony_score"] <= 1.0
        
        # Should have recommendations
        assert len(result["recommendations"]) > 0
        
        # Should have ideal position sizes
        assert len(result["ideal_position_sizes"]) > 0
    
    def test_calculate_position_harmony(self, manager, mock_positions):
        """Test calculating position harmony."""
        harmony = manager._calculate_position_harmony(mock_positions, 10000.0)
        
        # Score should be between 0 and 1
        assert 0.0 <= harmony["score"] <= 1.0
        assert isinstance(harmony["factors"], dict)
        
        # Should have positive and negative factors
        assert "position_size_alignment" in harmony["factors"]
        assert "position_balance" in harmony["factors"]
        assert "fibonacci_position_count" in harmony["factors"]
    
    def test_get_fibonacci_position_sizes(self, manager):
        """Test calculating Fibonacci position sizes."""
        account_balance = 10000.0
        position_sizes = manager.get_fibonacci_position_sizes(account_balance)
        
        # Should return a list of position sizes
        assert isinstance(position_sizes, list)
        assert len(position_sizes) > 0
        
        # Each size should have the expected structure
        for size in position_sizes:
            assert "fibonacci_relation" in size
            assert "absolute_size" in size
            assert "size_pct" in size
            assert "risk_category" in size
            
            # Values should make sense
            assert size["absolute_size"] > 0
            assert 0 < size["size_pct"] < 1
            assert size["risk_category"] in ["low", "moderate", "high"]
    
    def test_generate_divine_recommendations(self, manager, mock_positions):
        """Test generating divine recommendations."""
        harmony_score = 0.5
        position_sizes = manager.get_fibonacci_position_sizes(10000.0)
        
        recommendations = manager._generate_divine_recommendations(
            harmony_score,
            mock_positions,
            position_sizes,
            10000.0
        )
        
        # Should return a list of recommendations
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Each recommendation should have the expected structure
        for rec in recommendations:
            assert "description" in rec
            assert isinstance(rec["description"], str)
            assert len(rec["description"]) > 0
    
    def test_get_harmony_state(self, manager):
        """Test getting harmony state based on score."""
        # Test different score ranges
        assert manager._get_harmony_state(0.0) == "UNBALANCED"
        assert manager._get_harmony_state(0.3) == "DISHARMONIOUS"
        assert manager._get_harmony_state(0.6) == "HARMONIC"
        assert manager._get_harmony_state(0.8) == "RESONANT"
        assert manager._get_harmony_state(0.95) == "DIVINE"
    
    def test_get_divine_advice(self, manager):
        """Test getting divine advice based on harmony state."""
        # Test advice for each state
        unbalanced_advice = manager._get_divine_advice("UNBALANCED")
        assert len(unbalanced_advice) > 0
        
        disharmonious_advice = manager._get_divine_advice("DISHARMONIOUS")
        assert len(disharmonious_advice) > 0
        
        harmonic_advice = manager._get_divine_advice("HARMONIC")
        assert len(harmonic_advice) > 0
        
        resonant_advice = manager._get_divine_advice("RESONANT")
        assert len(resonant_advice) > 0
        
        divine_advice = manager._get_divine_advice("DIVINE")
        assert len(divine_advice) > 0
        
        # Unknown state should still return advice
        unknown_advice = manager._get_divine_advice("UNKNOWN")
        assert len(unknown_advice) > 0 