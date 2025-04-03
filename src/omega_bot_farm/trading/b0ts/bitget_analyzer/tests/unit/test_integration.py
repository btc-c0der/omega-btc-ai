#!/usr/bin/env python3

"""
Integration tests for BitgetPositionAnalyzerB0t.

These tests verify that the different components of the BitgetPositionAnalyzerB0t
work together correctly, using mocked API responses.
"""

import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

# Try to import BitgetPositionAnalyzerB0t
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False
    print("BitgetPositionAnalyzerB0t not available. Using mock for tests.")

# Skip all tests if BitgetPositionAnalyzerB0t is not available
pytestmark = pytest.mark.skipif(not BOT_AVAILABLE, reason="BitgetPositionAnalyzerB0t not available")

class TestBitgetPositionAnalyzerIntegration:
    """Integration tests for the BitgetPositionAnalyzerB0t."""

    @pytest.fixture
    def mock_exchange(self):
        """Mock the exchange client to return test data."""
        class MockExchange:
            async def fetch_balance(self, params=None):
                return {
                    "info": {},
                    "free": {"USDT": 5000},
                    "used": {"USDT": 5000},
                    "total": {"USDT": 10000}
                }
                
            async def fetch_positions(self, symbols=None, params=None):
                return [
                    {
                        "info": {},
                        "id": "1",
                        "symbol": "BTC/USDT:USDT",
                        "timestamp": 1609459200000,
                        "datetime": "2021-01-01T00:00:00.000Z",
                        "isolated": True,
                        "hedged": False,
                        "side": "long",
                        "contracts": 0.1,
                        "contractSize": 1,
                        "entryPrice": 50000,
                        "markPrice": 55000,
                        "notional": 5000,
                        "leverage": 10,
                        "collateral": 500,
                        "initialMargin": 500,
                        "maintenanceMargin": 250,
                        "initialMarginPercentage": 0.1,
                        "maintenanceMarginPercentage": 0.05,
                        "unrealizedPnl": 500,
                        "liquidationPrice": 45000,
                        "marginMode": "isolated",
                        "marginRatio": 0.05,
                        "percentage": 10
                    },
                    {
                        "info": {},
                        "id": "2",
                        "symbol": "ETH/USDT:USDT",
                        "timestamp": 1609459200000,
                        "datetime": "2021-01-01T00:00:00.000Z",
                        "isolated": True,
                        "hedged": False,
                        "side": "short",
                        "contracts": 1.0,
                        "contractSize": 1,
                        "entryPrice": 3000,
                        "markPrice": 2700,
                        "notional": 3000,
                        "leverage": 5,
                        "collateral": 600,
                        "initialMargin": 600,
                        "maintenanceMargin": 300,
                        "initialMarginPercentage": 0.2,
                        "maintenanceMarginPercentage": 0.1,
                        "unrealizedPnl": 300,
                        "liquidationPrice": 3300,
                        "marginMode": "isolated",
                        "marginRatio": 0.1,
                        "percentage": 10
                    }
                ]
        
        return MockExchange()

    @pytest.mark.asyncio
    async def test_full_workflow(self, mock_exchange):
        """Test the full workflow of position analysis."""
        # Create the analyzer with test credentials
        analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret",
            api_passphrase="test_pass",
            use_testnet=True
        )
        
        # Patch the exchange client to use our mock
        with patch.object(analyzer, '_initialize_exchange', return_value=mock_exchange):
            # Initialize exchange
            await analyzer._initialize_exchange()
            
            # Get positions
            positions_data = await analyzer.get_positions()
            
            # Verify position data
            assert "positions" in positions_data, "Should return positions"
            assert len(positions_data["positions"]) == 2, "Should return 2 positions"
            assert positions_data["positions"][0]["symbol"] == "BTC/USDT:USDT", "First position should be BTC"
            assert positions_data["positions"][1]["symbol"] == "ETH/USDT:USDT", "Second position should be ETH"
            
            # Verify account data
            assert "account" in positions_data, "Should return account data"
            assert "balance" in positions_data["account"], "Account should include balance"
            assert "equity" in positions_data["account"], "Account should include equity"
            
            # Analyze a single position
            btc_position = positions_data["positions"][0]
            analysis = analyzer.analyze_position(btc_position)
            
            # Verify position analysis
            assert "position" in analysis, "Should return position"
            assert "analysis" in analysis, "Should return analysis"
            assert "fibonacci_levels" in analysis["analysis"], "Analysis should include Fibonacci levels"
            assert "recommended_take_profit" in analysis["analysis"], "Analysis should include take profit recommendation"
            assert "recommended_stop_loss" in analysis["analysis"], "Analysis should include stop loss recommendation"
            assert "harmony_score" in analysis["analysis"], "Analysis should include harmony score"
            
            # Analyze all positions
            full_analysis = analyzer.analyze_all_positions()
            
            # Verify full analysis
            assert "position_analyses" in full_analysis, "Should return position analyses"
            assert len(full_analysis["position_analyses"]) == 2, "Should analyze 2 positions"
            assert "harmony_score" in full_analysis, "Should return overall harmony score"
            assert "recommendations" in full_analysis, "Should return recommendations"
            assert "account_stats" in full_analysis, "Should return account stats"
            
            # Verify specific metrics
            account_stats = full_analysis["account_stats"]
            assert "long_short_ratio" in account_stats, "Should calculate long-short ratio"
            assert "exposure_to_equity_ratio" in account_stats, "Should calculate exposure-equity ratio"
            
            # Store current positions for change detection
            analyzer.previous_positions = positions_data["positions"]
            
            # Create a modified position to test change detection
            modified_positions = positions_data["positions"].copy()
            modified_positions[0]["contracts"] = 0.2  # Double the BTC position size
            modified_positions[0]["notional"] = 10000
            
            # Mock the new position data
            with patch.object(mock_exchange, 'fetch_positions', return_value=modified_positions):
                # Get positions again
                new_positions_data = await analyzer.get_positions()
                
                # Verify change detection
                assert "changes" in new_positions_data, "Should return changes"
                changes = new_positions_data["changes"]
                assert len(changes["changed_positions"]) > 0, "Should detect changed position"
                assert changes["changed_positions"][0]["new"]["symbol"] == "BTC/USDT:USDT", "Changed position should be BTC"

    @pytest.mark.asyncio
    async def test_golden_ratio_detection(self, mock_exchange):
        """Test detection of golden ratio in portfolio metrics."""
        # Create the analyzer with test credentials
        analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret",
            api_passphrase="test_pass",
            use_testnet=True
        )
        
        # Create positions with golden ratio balance
        golden_positions = [
            {
                "symbol": "BTC/USDT:USDT",
                "side": "long",
                "entryPrice": 50000,
                "markPrice": 55000,
                "contracts": 0.162,
                "notional": 8090,  # ~PHI * 5000
                "leverage": 8
            },
            {
                "symbol": "SOL/USDT:USDT",
                "side": "short",
                "entryPrice": 100,
                "markPrice": 95,
                "contracts": 50.0,
                "notional": 5000,
                "leverage": 10
            }
        ]
        
        # Calculate long-short ratio
        ls_ratio = analyzer._calculate_long_short_ratio(golden_positions)
        
        # Should be close to PHI (1.618)
        assert 1.6 <= ls_ratio <= 1.65, f"Long-short ratio {ls_ratio} should be close to 1.618"
        
        # Analyze positions
        analyses = []
        for position in golden_positions:
            analyses.append(analyzer.analyze_position(position))
        
        # Check for harmony
        assert all(a["analysis"]["harmony_score"] > 0.5 for a in analyses), "Positions should have good harmony scores"


if __name__ == "__main__":
    pytest.main(['-xvs', __file__]) 