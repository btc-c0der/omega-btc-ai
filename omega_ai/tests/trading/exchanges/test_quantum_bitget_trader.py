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
🔮 QUANTUM BITGET TRADER TEST SUITE 🔮
=====================================

Test the quantum-enhanced BitGet trader with bio-energy and divine features.
May your tests reveal the truth of quantum trading! 🌟
"""

import pytest
import unittest
from datetime import datetime, timedelta
from typing import Dict, Any
from unittest.mock import patch, MagicMock
from omega_ai.trading.exchanges.quantum_bitget_trader import (
    QuantumBitGetTrader,
    BioEnergyState,
    BioEnergyMetrics
)

# ANSI color codes for divine output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class TestQuantumBitGetTrader:
    """Test suite for Quantum-Enhanced BitGet Trader."""
    
    @pytest.fixture
    def trader(self) -> QuantumBitGetTrader:
        """Create a quantum-enhanced trader instance."""
        return QuantumBitGetTrader(
            profile_type="strategic",
            api_key="test_key",
            secret_key="test_secret",
            passphrase="test_pass",
            use_testnet=True,
            initial_capital=10000.0
        )
    
    @pytest.fixture
    def market_context(self) -> Dict[str, Any]:
        """Create a divine market context for testing."""
        return {
            "price": 50000.0,
            "trend": "uptrend",
            "volatility": 0.02,
            "volume": 1000000,
            "timestamp": datetime.now(),
            "schumann_resonance": 7.44,
            "recent_volatility": 0.015,
            "regime": "bullish",
            "trend_strength": 0.8,
            "recent_trades": [
                {"price": 49800.0, "timestamp": datetime.now() - timedelta(minutes=5)},
                {"price": 49900.0, "timestamp": datetime.now() - timedelta(minutes=4)},
                {"price": 50000.0, "timestamp": datetime.now() - timedelta(minutes=3)},
                {"price": 50100.0, "timestamp": datetime.now() - timedelta(minutes=2)},
                {"price": 50200.0, "timestamp": datetime.now() - timedelta(minutes=1)}
            ]
        }
    
    def test_initialization(self, trader: QuantumBitGetTrader):
        """Test trader initialization with divine energy."""
        print(f"\n{CYAN}Testing TRADER INITIALIZATION...{RESET}")
        
        # Verify basic attributes
        assert trader.profile.name == "Strategic Fibonacci Trader"
        assert trader.use_testnet is True
        assert trader.profile.capital == 10000.0
        
        # Verify bio-energy metrics
        assert isinstance(trader.bio_energy, BioEnergyMetrics)
        assert trader.bio_energy.current_state == BioEnergyState.ITAL_BALANCE
        assert trader.bio_energy.fibonacci_resonance == 0.618  # Golden ratio
        assert trader.bio_energy.quantum_frequency == 7.44  # Schumann resonance
        assert trader.bio_energy.emotional_balance == 0.8
        
        print(f"{GREEN}✓ Trader initialization verified!{RESET}")
    
    def test_golden_ratio_delay(self, trader: QuantumBitGetTrader):
        """Test golden ratio-based retry delay calculation."""
        print(f"\n{MAGENTA}Testing GOLDEN RATIO DELAY...{RESET}")
        
        # Test initial delay
        delay = trader._calculate_golden_ratio_delay()
        assert delay == 1.0  # Base delay
        
        # Test increasing delays
        trader.retry_count = 1
        delay = trader._calculate_golden_ratio_delay()
        assert delay > 1.0  # Should increase with golden ratio
        
        trader.retry_count = 2
        delay = trader._calculate_golden_ratio_delay()
        assert delay > 1.618  # Should follow Fibonacci sequence
        
        # Test maximum delay cap
        trader.retry_count = 10
        delay = trader._calculate_golden_ratio_delay()
        assert delay <= 30.0  # Should be capped at 30 seconds
        
        print(f"{GREEN}✓ Golden ratio delay calculation verified!{RESET}")
    
    @patch('requests.request')
    def test_api_request_retry(self, mock_request, trader: QuantumBitGetTrader):
        """Test quantum retry logic for API requests."""
        print(f"\n{YELLOW}Testing API REQUEST RETRY...{RESET}")
        
        # Configure mock to fail twice then succeed
        mock_request.side_effect = [
            Exception("First failure"),
            Exception("Second failure"),
            MagicMock(status_code=200, json=lambda: {"code": "00000"})
        ]
        
        # Make API request
        response = trader._make_api_request(
            method="GET",
            endpoint="/test",
            params={"test": "data"}
        )
        
        # Verify retry behavior
        assert mock_request.call_count == 3
        assert response is not None
        assert response["code"] == "00000"
        
        print(f"{GREEN}✓ API request retry logic verified!{RESET}")
    
    def test_bio_energy_update(self, trader: QuantumBitGetTrader, market_context: Dict[str, Any]):
        """Test bio-energy metrics update based on market conditions."""
        print(f"\n{CYAN}Testing BIO-ENERGY UPDATE...{RESET}")
        
        # Initial state
        initial_state = trader.bio_energy.current_state
        initial_resonance = trader.bio_energy.fibonacci_resonance
        
        # Update with positive market conditions
        market_context["volatility"] = 0.01  # Low volatility
        trader._update_bio_energy(market_context)
        
        # Verify state changes
        assert trader.bio_energy.current_state != initial_state
        assert trader.bio_energy.fibonacci_resonance != initial_resonance
        
        # Update with high volatility
        market_context["volatility"] = 0.05  # High volatility
        trader._update_bio_energy(market_context)
        
        # Verify quantum frequency adjustment
        assert trader.bio_energy.quantum_frequency == 7.83  # Higher frequency for high volatility
        
        print(f"{GREEN}✓ Bio-energy update verified!{RESET}")
    
    def test_energy_sensitive_stop_loss(self, trader: QuantumBitGetTrader, market_context: Dict[str, Any]):
        """Test energy-sensitive stop-loss calculation."""
        print(f"\n{MAGENTA}Testing ENERGY-SENSITIVE STOP-LOSS...{RESET}")
        
        # Test long position
        entry_price = 50000.0
        sl = trader._calculate_energy_sensitive_sl("LONG", entry_price, market_context)
        assert sl < entry_price  # Stop loss should be below entry for long
        
        # Test short position
        sl = trader._calculate_energy_sensitive_sl("SHORT", entry_price, market_context)
        assert sl > entry_price  # Stop loss should be above entry for short
        
        # Test different bio-energy states
        trader.bio_energy.current_state = BioEnergyState.DIVINE_FLOW
        sl_divine = trader._calculate_energy_sensitive_sl("LONG", entry_price, market_context)
        
        trader.bio_energy.current_state = BioEnergyState.BABYLON_TENSION
        sl_babylon = trader._calculate_energy_sensitive_sl("LONG", entry_price, market_context)
        
        # Divine flow should have wider stop-loss
        assert abs(sl_divine - entry_price) > abs(sl_babylon - entry_price)
        
        print(f"{GREEN}✓ Energy-sensitive stop-loss verified!{RESET}")
    
    @patch('omega_ai.trading.exchanges.quantum_bitget_trader.QuantumBitGetTrader._make_api_request')
    def test_execute_trade(self, mock_api_request, trader: QuantumBitGetTrader, market_context: Dict[str, Any]):
        """Test quantum-enhanced trade execution."""
        print(f"\n{YELLOW}Testing TRADE EXECUTION...{RESET}")
        
        # Configure mock API response
        mock_api_request.return_value = {
            "code": "00000",
            "data": {"orderId": "test_order_id"}
        }
        
        # Mock the strategic trader's should_enter_trade method to always return True
        with patch.object(trader.profile, 'should_enter_trade', return_value=(True, "Test entry", "LONG", 3.0)):
            # Execute trade
            position = trader.execute_trade(market_context)
            
            # Verify position details
            assert position is not None
            assert position["direction"] in ["LONG", "SHORT"]
            assert position["entry_price"] == market_context["price"]
            assert position["order_id"] == "test_order_id"
            assert "bio_energy_state" in position
            assert "fibonacci_resonance" in position
        
        print(f"{GREEN}✓ Trade execution verified!{RESET}")
    
    def test_get_bio_energy_metrics(self, trader: QuantumBitGetTrader):
        """Test bio-energy metrics retrieval."""
        print(f"\n{CYAN}Testing BIO-ENERGY METRICS RETRIEVAL...{RESET}")
        
        metrics = trader.get_bio_energy_metrics()
        
        # Verify metrics structure
        assert isinstance(metrics, dict)
        assert "state" in metrics
        assert "fibonacci_resonance" in metrics
        assert "quantum_frequency" in metrics
        assert "emotional_balance" in metrics
        assert "last_update" in metrics
        
        # Verify metric values
        assert metrics["fibonacci_resonance"] == trader.bio_energy.fibonacci_resonance
        assert metrics["quantum_frequency"] == trader.bio_energy.quantum_frequency
        assert metrics["emotional_balance"] == trader.bio_energy.emotional_balance
        
        print(f"{GREEN}✓ Bio-energy metrics retrieval verified!{RESET}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 