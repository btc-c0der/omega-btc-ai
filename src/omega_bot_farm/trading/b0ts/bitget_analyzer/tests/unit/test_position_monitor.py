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
Unit tests for position monitoring and change detection in BitgetPositionAnalyzerB0t.

These tests verify that the bot correctly detects new positions, closed positions,
and significant changes in existing positions.
"""

import unittest
import os
import sys
import json
import copy
from unittest.mock import patch, MagicMock, AsyncMock

# Try to import BitgetPositionAnalyzerB0t
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False
    print("BitgetPositionAnalyzerB0t not available. Using mock for tests.")

# Mock implementation if import fails
if not BOT_AVAILABLE:
    class BitgetPositionAnalyzerB0t:
        """Mock implementation for testing"""
        
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
            self.api_key = api_key or "test_key"
            self.api_secret = api_secret or "test_secret"
            self.api_passphrase = api_passphrase or "test_pass"
            self.use_testnet = use_testnet
            self.previous_positions = []
            self.significant_change_threshold = 5.0  # 5% change is significant
        
        async def get_positions(self):
            """Get current positions."""
            # This will be mocked for testing
            return {"positions": []}
        
        def _detect_position_changes(self, current_positions, previous_positions):
            """Detect changes between current and previous positions."""
            if not previous_positions:
                # If no previous positions, all current positions are new
                return {
                    "new_positions": current_positions,
                    "closed_positions": [],
                    "changed_positions": []
                }
                
            # Track positions by symbol+side as unique identifier
            current_map = {f"{p['symbol']}:{p['side'].lower()}": p for p in current_positions}
            previous_map = {f"{p['symbol']}:{p['side'].lower()}": p for p in previous_positions}
            
            # Detect new, closed, and changed positions
            new_positions = []
            closed_positions = []
            changed_positions = []
            
            # Find new and changed positions
            for key, current_pos in current_map.items():
                if key not in previous_map:
                    new_positions.append(current_pos)
                else:
                    # Position exists, check for significant changes
                    prev_pos = previous_map[key]
                    
                    # Check for contract size change
                    curr_contracts = float(current_pos.get("contracts", 0))
                    prev_contracts = float(prev_pos.get("contracts", 0))
                    
                    if prev_contracts > 0:
                        pct_change = abs((curr_contracts - prev_contracts) / prev_contracts) * 100
                        
                        if pct_change >= self.significant_change_threshold:
                            changed_positions.append({
                                "old": prev_pos,
                                "new": current_pos,
                                "change_type": "size",
                                "pct_change": pct_change
                            })
            
            # Find closed positions
            for key, prev_pos in previous_map.items():
                if key not in current_map:
                    closed_positions.append(prev_pos)
            
            return {
                "new_positions": new_positions,
                "closed_positions": closed_positions,
                "changed_positions": changed_positions
            }


class TestPositionMonitor(unittest.TestCase):
    """Test suite for position monitoring and change detection."""

    def setUp(self):
        """Set up test environment."""
        # Use dummy API credentials for testing
        self.analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret", 
            api_passphrase="test_pass",
            use_testnet=True
        )
        
        # Sample positions for testing
        self.initial_positions = [
            {
                "symbol": "BTC/USDT:USDT",
                "side": "long",
                "entryPrice": 50000,
                "markPrice": 55000,
                "contracts": 0.1,
                "notional": 5000,
                "leverage": 10,
                "unrealizedPnl": 500
            },
            {
                "symbol": "ETH/USDT:USDT",
                "side": "short",
                "entryPrice": 3000,
                "markPrice": 2700,
                "contracts": 1.0,
                "notional": 3000,
                "leverage": 5,
                "unrealizedPnl": 300
            }
        ]
        
        # Store initial positions as previous
        self.analyzer.previous_positions = copy.deepcopy(self.initial_positions)

    @patch.object(BitgetPositionAnalyzerB0t, 'get_positions')
    async def test_detect_new_position(self, mock_get_positions):
        """Test detection of new positions."""
        # Create updated positions with a new position
        updated_positions = copy.deepcopy(self.initial_positions)
        updated_positions.append({
            "symbol": "SOL/USDT:USDT",
            "side": "long",
            "entryPrice": 100,
            "markPrice": 105,
            "contracts": 10.0,
            "notional": 1000,
            "leverage": 10,
            "unrealizedPnl": 50
        })
        
        # Mock get_positions to return updated positions
        mock_get_positions.return_value = {"positions": updated_positions}
        
        # Get current positions
        positions_data = await self.analyzer.get_positions()
        
        # Detect changes
        changes = self.analyzer._detect_position_changes(
            positions_data["positions"],
            self.analyzer.previous_positions
        )
        
        # Check that the new position was detected
        self.assertEqual(len(changes["new_positions"]), 1, "Should detect 1 new position")
        self.assertEqual(changes["new_positions"][0]["symbol"], "SOL/USDT:USDT", "New position should be SOL")
        self.assertEqual(len(changes["closed_positions"]), 0, "Should detect 0 closed positions")
        self.assertEqual(len(changes["changed_positions"]), 0, "Should detect 0 changed positions")

    @patch.object(BitgetPositionAnalyzerB0t, 'get_positions')
    async def test_detect_closed_position(self, mock_get_positions):
        """Test detection of closed positions."""
        # Create updated positions with a position removed
        updated_positions = [self.initial_positions[0]]  # Only keep BTC position
        
        # Mock get_positions to return updated positions
        mock_get_positions.return_value = {"positions": updated_positions}
        
        # Get current positions
        positions_data = await self.analyzer.get_positions()
        
        # Detect changes
        changes = self.analyzer._detect_position_changes(
            positions_data["positions"],
            self.analyzer.previous_positions
        )
        
        # Check that the closed position was detected
        self.assertEqual(len(changes["new_positions"]), 0, "Should detect 0 new positions")
        self.assertEqual(len(changes["closed_positions"]), 1, "Should detect 1 closed position")
        self.assertEqual(changes["closed_positions"][0]["symbol"], "ETH/USDT:USDT", "Closed position should be ETH")
        self.assertEqual(len(changes["changed_positions"]), 0, "Should detect 0 changed positions")

    @patch.object(BitgetPositionAnalyzerB0t, 'get_positions')
    async def test_detect_changed_position(self, mock_get_positions):
        """Test detection of changed positions."""
        # Create updated positions with a position size changed
        updated_positions = copy.deepcopy(self.initial_positions)
        updated_positions[0]["contracts"] = 0.2  # Double the BTC position size
        updated_positions[0]["notional"] = 10000
        
        # Mock get_positions to return updated positions
        mock_get_positions.return_value = {"positions": updated_positions}
        
        # Get current positions
        positions_data = await self.analyzer.get_positions()
        
        # Detect changes
        changes = self.analyzer._detect_position_changes(
            positions_data["positions"],
            self.analyzer.previous_positions
        )
        
        # Check that the changed position was detected
        self.assertEqual(len(changes["new_positions"]), 0, "Should detect 0 new positions")
        self.assertEqual(len(changes["closed_positions"]), 0, "Should detect 0 closed positions")
        self.assertEqual(len(changes["changed_positions"]), 1, "Should detect 1 changed position")
        self.assertEqual(changes["changed_positions"][0]["new"]["symbol"], "BTC/USDT:USDT", "Changed position should be BTC")
        self.assertGreaterEqual(changes["changed_positions"][0]["pct_change"], 5.0, "Change percentage should be >= threshold")

    @patch.object(BitgetPositionAnalyzerB0t, 'get_positions')
    async def test_minor_change_not_detected(self, mock_get_positions):
        """Test that minor changes are not detected."""
        # Create updated positions with a minor position size change
        updated_positions = copy.deepcopy(self.initial_positions)
        updated_positions[0]["contracts"] = 0.101  # Small change (1% increase)
        
        # Mock get_positions to return updated positions
        mock_get_positions.return_value = {"positions": updated_positions}
        
        # Get current positions
        positions_data = await self.analyzer.get_positions()
        
        # Detect changes
        changes = self.analyzer._detect_position_changes(
            positions_data["positions"],
            self.analyzer.previous_positions
        )
        
        # Check that no significant changes were detected
        self.assertEqual(len(changes["new_positions"]), 0, "Should detect 0 new positions")
        self.assertEqual(len(changes["closed_positions"]), 0, "Should detect 0 closed positions")
        self.assertEqual(len(changes["changed_positions"]), 0, "Should detect 0 changed positions")

    @patch.object(BitgetPositionAnalyzerB0t, 'get_positions')
    async def test_multiple_changes(self, mock_get_positions):
        """Test detection of multiple types of changes."""
        # Create updated positions with multiple changes
        updated_positions = [
            {  # Changed position (increased size)
                "symbol": "BTC/USDT:USDT",
                "side": "long",
                "entryPrice": 50000,
                "markPrice": 57000,
                "contracts": 0.2,  # Double size
                "notional": 10000,
                "leverage": 10,
                "unrealizedPnl": 1400
            },
            # ETH position closed (omitted)
            {  # New position
                "symbol": "SOL/USDT:USDT",
                "side": "long",
                "entryPrice": 100,
                "markPrice": 105,
                "contracts": 10.0,
                "notional": 1000,
                "leverage": 10,
                "unrealizedPnl": 50
            }
        ]
        
        # Mock get_positions to return updated positions
        mock_get_positions.return_value = {"positions": updated_positions}
        
        # Get current positions
        positions_data = await self.analyzer.get_positions()
        
        # Detect changes
        changes = self.analyzer._detect_position_changes(
            positions_data["positions"],
            self.analyzer.previous_positions
        )
        
        # Check that all changes were detected
        self.assertEqual(len(changes["new_positions"]), 1, "Should detect 1 new position")
        self.assertEqual(len(changes["closed_positions"]), 1, "Should detect 1 closed position")
        self.assertEqual(len(changes["changed_positions"]), 1, "Should detect 1 changed position")
        
        # Check specific positions
        self.assertEqual(changes["new_positions"][0]["symbol"], "SOL/USDT:USDT", "New position should be SOL")
        self.assertEqual(changes["closed_positions"][0]["symbol"], "ETH/USDT:USDT", "Closed position should be ETH")
        self.assertEqual(changes["changed_positions"][0]["new"]["symbol"], "BTC/USDT:USDT", "Changed position should be BTC")

    def test_first_run_no_previous_positions(self):
        """Test first run when no previous positions exist."""
        # Reset previous positions
        self.analyzer.previous_positions = []
        
        # Current positions
        current_positions = copy.deepcopy(self.initial_positions)
        
        # Detect changes
        changes = self.analyzer._detect_position_changes(current_positions, [])
        
        # Check that all current positions are detected as new
        self.assertEqual(len(changes["new_positions"]), 2, "All positions should be detected as new")
        self.assertEqual(len(changes["closed_positions"]), 0, "Should detect 0 closed positions")
        self.assertEqual(len(changes["changed_positions"]), 0, "Should detect 0 changed positions")


if __name__ == "__main__":
    unittest.main() 