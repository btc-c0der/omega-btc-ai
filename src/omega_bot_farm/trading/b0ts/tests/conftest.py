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
Test fixtures for BitgetPositionAnalyzerB0t tests.

This module provides common test fixtures and utilities for unit tests
of the BitgetPositionAnalyzerB0t.
"""

import os
import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock

# Constants for tests
PHI = 1.618034  # Golden Ratio
INV_PHI = 0.618034  # Inverse Golden Ratio

# Try to import BitgetPositionAnalyzerB0t
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False
    print("BitgetPositionAnalyzerB0t not available. Using mock for tests.")

# Define test positions
SAMPLE_POSITIONS = {
    # Long BTC position
    "btc_long": {
        "symbol": "BTC/USDT:USDT",
        "side": "long",
        "entryPrice": 50000,
        "markPrice": 55000,
        "contracts": 0.1,
        "notional": 5000,
        "leverage": 10,
        "unrealizedPnl": 500
    },
    # Short ETH position
    "eth_short": {
        "symbol": "ETH/USDT:USDT",
        "side": "short",
        "entryPrice": 3000,
        "markPrice": 2700,
        "contracts": 1.0,
        "notional": 3000,
        "leverage": 5,
        "unrealizedPnl": 300
    },
    # Long SOL position
    "sol_long": {
        "symbol": "SOL/USDT:USDT",
        "side": "long",
        "entryPrice": 100,
        "markPrice": 105,
        "contracts": 10.0,
        "notional": 1000,
        "leverage": 10,
        "unrealizedPnl": 50
    },
    # Short ADA position
    "ada_short": {
        "symbol": "ADA/USDT:USDT",
        "side": "short",
        "entryPrice": 1.0,
        "markPrice": 0.9,
        "contracts": 5000.0,
        "notional": 5000,
        "leverage": 5,
        "unrealizedPnl": 500
    }
}

@pytest.fixture
def mock_bot():
    """Fixture to create a mock BitgetPositionAnalyzerB0t for testing."""
    # If the real bot is available, use it with test credentials
    if BOT_AVAILABLE:
        bot = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret",
            api_passphrase="test_pass",
            use_testnet=True
        )
    else:
        # Create a mock bot with the same interface
        class MockBitgetPositionAnalyzerB0t:
            def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
                self.api_key = api_key or "test_key"
                self.api_secret = api_secret or "test_secret"
                self.api_passphrase = api_passphrase or "test_pass"
                self.use_testnet = use_testnet
                self.previous_positions = []
                self.significant_change_threshold = 5.0
                
            async def get_positions(self):
                """Mock get_positions method."""
                return {"positions": []}
                
            def _calculate_fibonacci_levels_long(self, entry_price, current_price=None):
                """Calculate Fibonacci levels for long positions."""
                levels = {}
                
                # Basic retracement levels
                levels["0.0%"] = {"price": entry_price, "percentage": 0.0}
                levels["23.6%"] = {"price": entry_price * (1 + 0.236), "percentage": 23.6}
                levels["38.2%"] = {"price": entry_price * (1 + 0.382), "percentage": 38.2}
                levels["50.0%"] = {"price": entry_price * (1 + 0.5), "percentage": 50.0}
                levels["61.8%"] = {"price": entry_price * (1 + 0.618), "percentage": 61.8}
                levels["78.6%"] = {"price": entry_price * (1 + 0.786), "percentage": 78.6}
                levels["100.0%"] = {"price": entry_price * 2, "percentage": 100.0}
                
                # Extension levels
                levels["161.8%"] = {"price": entry_price * (1 + 1.618), "percentage": 161.8}
                levels["261.8%"] = {"price": entry_price * (1 + 2.618), "percentage": 261.8}
                
                return levels
                
            def _calculate_fibonacci_levels_short(self, entry_price, current_price=None):
                """Calculate Fibonacci levels for short positions."""
                levels = {}
                
                # Basic retracement levels (downward)
                levels["0.0%"] = {"price": entry_price, "percentage": 0.0}
                levels["23.6%"] = {"price": entry_price * (1 - 0.236), "percentage": -23.6}
                levels["38.2%"] = {"price": entry_price * (1 - 0.382), "percentage": -38.2}
                levels["50.0%"] = {"price": entry_price * (1 - 0.5), "percentage": -50.0}
                levels["61.8%"] = {"price": entry_price * (1 - 0.618), "percentage": -61.8}
                levels["78.6%"] = {"price": entry_price * (1 - 0.786), "percentage": -78.6}
                levels["100.0%"] = {"price": 0, "percentage": -100.0}
                
                return levels
                
            def _calculate_position_harmony(self, position):
                """Calculate harmony score for a position."""
                return 0.75  # Mock value
                
            def _calculate_overall_harmony(self, positions):
                """Calculate overall harmony score for all positions."""
                if not positions:
                    return 0.5  # Neutral harmony if no positions
                return 0.75  # Mock value
                
            def _calculate_long_short_ratio(self, positions):
                """Calculate the ratio between long and short exposure."""
                long_exposure = sum(
                    float(p.get("notional", 0)) 
                    for p in positions if p.get("side", "").lower() == "long"
                )
                
                short_exposure = sum(
                    float(p.get("notional", 0)) 
                    for p in positions if p.get("side", "").lower() == "short"
                )
                
                # Prevent division by zero
                if short_exposure == 0:
                    if long_exposure == 0:
                        return 1.0  # Neutral if no positions
                    return float('inf')  # All long positions
                    
                return long_exposure / short_exposure
                
            def _calculate_exposure_to_equity_ratio(self, positions, equity):
                """Calculate the ratio of total exposure to equity."""
                total_exposure = sum(float(p.get("notional", 0)) for p in positions)
                
                # Prevent division by zero
                if equity == 0:
                    return float('inf') if total_exposure > 0 else 0.0
                    
                return total_exposure / equity
                
            def analyze_position(self, position):
                """Analyze a single position."""
                return {
                    "position": position,
                    "analysis": {
                        "fibonacci_levels": {},
                        "pnl_percentage": 10.0,
                        "recommended_take_profit": ("61.8%", 0),
                        "recommended_stop_loss": ("38.2%", 0),
                        "harmony_score": 0.75
                    }
                }
                
            def analyze_all_positions(self):
                """Analyze all positions."""
                return {
                    "position_analyses": [],
                    "harmony_score": 0.75,
                    "recommendations": [],
                    "account_stats": {
                        "balance": 10000,
                        "equity": 11000,
                        "long_exposure": 6000,
                        "short_exposure": 4000,
                        "long_short_ratio": 1.5,
                        "exposure_to_equity_ratio": 0.9
                    }
                }
        
        # Create instance of mock bot
        bot = MockBitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret",
            api_passphrase="test_pass",
            use_testnet=True
        )
        
    return bot

@pytest.fixture
def sample_positions():
    """Fixture to provide sample positions for testing."""
    return SAMPLE_POSITIONS

@pytest.fixture
def balanced_positions():
    """Fixture with balanced long/short positions."""
    return [SAMPLE_POSITIONS["btc_long"], SAMPLE_POSITIONS["eth_short"]]

@pytest.fixture
def long_biased_positions():
    """Fixture with long-biased positions."""
    return [
        SAMPLE_POSITIONS["btc_long"],
        SAMPLE_POSITIONS["sol_long"],
        SAMPLE_POSITIONS["eth_short"]
    ]

@pytest.fixture
def short_biased_positions():
    """Fixture with short-biased positions."""
    return [
        SAMPLE_POSITIONS["eth_short"],
        SAMPLE_POSITIONS["ada_short"],
        SAMPLE_POSITIONS["sol_long"]
    ]

@pytest.fixture
def golden_ratio_positions():
    """Fixture with positions in golden ratio balance."""
    # Modify the BTC position to get closer to PHI ratio
    btc_long = SAMPLE_POSITIONS["btc_long"].copy()
    btc_long["notional"] = 8090  # Make long exposure PHI times short exposure
    
    return [
        btc_long,
        SAMPLE_POSITIONS["sol_long"],
        SAMPLE_POSITIONS["eth_short"],
        SAMPLE_POSITIONS["ada_short"]
    ]

@pytest.fixture
def mock_exchange_response():
    """Fixture to mock exchange API responses."""
    return {
        "positions": [
            SAMPLE_POSITIONS["btc_long"],
            SAMPLE_POSITIONS["eth_short"]
        ],
        "account": {
            "balance": 10000,
            "equity": 11000,
            "long_exposure": 5000,
            "short_exposure": 3000,
            "long_short_ratio": 5000/3000,
            "exposure_to_equity_ratio": 8000/11000,
            "harmony_score": 0.75
        },
        "changes": {
            "new_positions": [],
            "closed_positions": [],
            "changed_positions": []
        },
        "timestamp": "2023-01-01T00:00:00Z"
    } 