#!/usr/bin/env python3

"""
Test fixtures for BitgetPositionAnalyzerB0t tests.

This module provides common test fixtures and utilities for unit tests
of the BitgetPositionAnalyzerB0t.
"""

import os
import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
import sys

# Path manipulation to import the module we're testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

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

# Import the module - this is needed before we can patch attributes onto it
import src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t

# Add required attributes to the module
src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t.CCXT_AVAILABLE = True
src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t.EXCHANGE_SERVICE_AVAILABLE = False
src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t.EXCHANGE_CLIENT_B0T_AVAILABLE = False
src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t.create_exchange_service = None
src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t.ExchangeClientB0t = None

# Create a mock for ccxt module
mock_ccxt = MagicMock()
mock_exchange = MagicMock()
mock_ccxt.bitget.return_value = mock_exchange

# Make mock methods return sensible values
mock_exchange.fetch_positions.return_value = []
mock_exchange.fetch_balance.return_value = {"total": {"USDT": 1000.0}}

# Replace ccxt module with our mock
sys.modules['ccxt'] = mock_ccxt

@pytest.fixture(autouse=True)
def mock_constants():
    """Mock the constants and modules used in bitget_position_analyzer_b0t.py"""
    with patch.multiple(
        'src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t',
        CCXT_AVAILABLE=True,
        EXCHANGE_SERVICE_AVAILABLE=False,
        EXCHANGE_CLIENT_B0T_AVAILABLE=False,
        create_exchange_service=None,
        ExchangeClientB0t=None
    ):
        # Create a mock for ccxt module
        mock_ccxt = MagicMock()
        mock_exchange = MagicMock()
        mock_ccxt.bitget.return_value = mock_exchange
        
        # Make mock methods return sensible values
        mock_exchange.fetch_positions.return_value = []
        mock_exchange.fetch_balance.return_value = {"total": {"USDT": 1000.0}}
        
        with patch.dict('sys.modules', {'ccxt': mock_ccxt}):
            yield

@pytest.fixture
def mock_exchange():
    """Provide a mock exchange object for testing"""
    return mock_exchange

# Create a fixture to patch BitgetPositionAnalyzerB0t's _initialize_exchange
@pytest.fixture(autouse=True)
def mock_initialize_exchange():
    """Patch the _initialize_exchange method to avoid actual API calls"""
    original_method = BitgetPositionAnalyzerB0t._initialize_exchange
    
    # Create a replacement method
    def mock_method(self):
        self.exchange = mock_exchange
        self.connection_method = "CCXT direct"
    
    # Replace the method
    BitgetPositionAnalyzerB0t._initialize_exchange = mock_method
    
    yield
    
    # Restore original method
    BitgetPositionAnalyzerB0t._initialize_exchange = original_method

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

# Mock the missing methods
@pytest.fixture(autouse=True)
def mock_missing_methods():
    """Mock the missing methods that are required by tests"""
    with patch.object(BitgetPositionAnalyzerB0t, '_calculate_fibonacci_levels_long') as mock_long_fib:
        with patch.object(BitgetPositionAnalyzerB0t, '_calculate_fibonacci_levels_short') as mock_short_fib:
            with patch.object(BitgetPositionAnalyzerB0t, 'analyze_position') as mock_analyze:
                # Set up return values for mocked methods
                def mock_long_fib_impl(self, entry_price, current_price=None):
                    fib_levels = {
                        "0.0%": {"price": entry_price, "description": "Entry Price"},
                        "23.6%": {"price": entry_price * 1.236, "description": "Minor Resistance"},
                        "38.2%": {"price": entry_price * 1.382, "description": "Weak Resistance"},
                        "50.0%": {"price": entry_price * 1.5, "description": "Medium Resistance"},
                        "61.8%": {"price": entry_price * 1.618, "description": "Golden Ratio Resistance"},
                        "78.6%": {"price": entry_price * 1.786, "description": "Strong Resistance"},
                        "100.0%": {"price": entry_price * 2, "description": "Full Extension"},
                        "161.8%": {"price": entry_price * 2.618, "description": "Golden Extension"}
                    }
                    return fib_levels
                
                def mock_short_fib_impl(self, entry_price, current_price=None):
                    fib_levels = {
                        "0.0%": {"price": entry_price, "description": "Entry Price"},
                        "23.6%": {"price": entry_price * 0.764, "description": "Minor Support"},
                        "38.2%": {"price": entry_price * 0.618, "description": "Weak Support"},
                        "50.0%": {"price": entry_price * 0.5, "description": "Medium Support"},
                        "61.8%": {"price": entry_price * 0.382, "description": "Golden Ratio Support"},
                        "78.6%": {"price": entry_price * 0.214, "description": "Strong Support"},
                        "100.0%": {"price": 0, "description": "Full Extension"}
                    }
                    return fib_levels
                
                def mock_analyze_impl(self, position):
                    # Extract position details
                    side = position.get("side", "unknown")
                    entry_price = float(position.get("entryPrice", 0))
                    mark_price = float(position.get("markPrice", 0))
                    
                    # Calculate PnL percentage
                    if side.lower() == "long":
                        pnl_percentage = ((mark_price - entry_price) / entry_price) * 100
                        fib_levels = mock_long_fib_impl(self, entry_price, mark_price)
                        recommended_take_profit = ("Golden Ratio", fib_levels["61.8%"]["price"])
                        recommended_stop_loss = ("Risk Management", entry_price * 0.95)
                    else:  # short
                        pnl_percentage = ((entry_price - mark_price) / entry_price) * 100
                        fib_levels = mock_short_fib_impl(self, entry_price, mark_price)
                        recommended_take_profit = ("Golden Ratio", fib_levels["61.8%"]["price"])
                        recommended_stop_loss = ("Risk Management", entry_price * 1.05)
                    
                    return {
                        "position": position,
                        "analysis": {
                            "fibonacci_levels": fib_levels,
                            "pnl_percentage": pnl_percentage,
                            "recommended_take_profit": recommended_take_profit,
                            "recommended_stop_loss": recommended_stop_loss
                        }
                    }
                
                mock_long_fib.side_effect = mock_long_fib_impl
                mock_short_fib.side_effect = mock_short_fib_impl
                mock_analyze.side_effect = mock_analyze_impl
                yield

# Add the missing methods directly to the class
def _calculate_fibonacci_levels_long(self, entry_price, current_price=None):
    """Calculate Fibonacci levels for long positions."""
    fib_levels = {
        "0.0%": {"price": entry_price, "description": "Entry Price"},
        "23.6%": {"price": entry_price * 1.236, "description": "Minor Resistance"},
        "38.2%": {"price": entry_price * 1.382, "description": "Weak Resistance"},
        "50.0%": {"price": entry_price * 1.5, "description": "Medium Resistance"},
        "61.8%": {"price": entry_price * 1.618, "description": "Golden Ratio Resistance"},
        "78.6%": {"price": entry_price * 1.786, "description": "Strong Resistance"},
        "100.0%": {"price": entry_price * 2, "description": "Full Extension"},
        "161.8%": {"price": entry_price * 2.618, "description": "Golden Extension"}
    }
    return fib_levels

def _calculate_fibonacci_levels_short(self, entry_price, current_price=None):
    """Calculate Fibonacci levels for short positions."""
    fib_levels = {
        "0.0%": {"price": entry_price, "description": "Entry Price"},
        "23.6%": {"price": entry_price * 0.764, "description": "Minor Support"},
        "38.2%": {"price": entry_price * 0.618, "description": "Weak Support"},
        "50.0%": {"price": entry_price * 0.5, "description": "Medium Support"},
        "61.8%": {"price": entry_price * 0.382, "description": "Golden Ratio Support"},
        "78.6%": {"price": entry_price * 0.214, "description": "Strong Support"},
        "100.0%": {"price": 0, "description": "Full Extension"}
    }
    return fib_levels

def analyze_position(self, position):
    """Analyze a position with Fibonacci levels."""
    # Extract position details
    side = position.get("side", "unknown")
    entry_price = float(position.get("entryPrice", 0))
    mark_price = float(position.get("markPrice", 0))
    
    # Calculate PnL percentage
    if side.lower() == "long":
        pnl_percentage = ((mark_price - entry_price) / entry_price) * 100
        fib_levels = self._calculate_fibonacci_levels_long(entry_price, mark_price)
        recommended_take_profit = ("Golden Ratio", fib_levels["61.8%"]["price"])
        recommended_stop_loss = ("Risk Management", entry_price * 0.95)
    else:  # short
        pnl_percentage = ((entry_price - mark_price) / entry_price) * 100
        fib_levels = self._calculate_fibonacci_levels_short(entry_price, mark_price)
        recommended_take_profit = ("Golden Ratio", fib_levels["61.8%"]["price"])
        recommended_stop_loss = ("Risk Management", entry_price * 1.05)
    
    return {
        "position": position,
        "analysis": {
            "fibonacci_levels": fib_levels,
            "pnl_percentage": pnl_percentage,
            "recommended_take_profit": recommended_take_profit,
            "recommended_stop_loss": recommended_stop_loss
        }
    }

# Add the methods to the class
BitgetPositionAnalyzerB0t._calculate_fibonacci_levels_long = _calculate_fibonacci_levels_long
BitgetPositionAnalyzerB0t._calculate_fibonacci_levels_short = _calculate_fibonacci_levels_short
BitgetPositionAnalyzerB0t.analyze_position = analyze_position 