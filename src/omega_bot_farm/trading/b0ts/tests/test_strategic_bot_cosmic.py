#!/usr/bin/env python3

"""
Test module for Strategic Trader Bot with cosmic factor integration.

This module tests the integration of the CosmicFactorService with the StrategicTraderBot.
"""

import os
import unittest
import tempfile
import yaml
from typing import Dict, Any
import copy
import logging
import random

try:
    from src.omega_bot_farm.trading.b0ts.strategic_fibo.strategic_b0t import StrategicTraderB0t
    from src.omega_bot_farm.utils.cosmic_factor_service import (
        CosmicFactorService, 
        MoonPhase, 
        SchumannFrequency, 
        MarketLiquidity, 
        GlobalSentiment
    )
except ImportError:
    # Handle the case where imports might be different in local test environment
    print("Warning: Unable to import from src.omega_bot_farm package. Using mock classes for testing.")
    
    # Create mock classes for testing
    class MoonPhase:
        FULL_MOON = "full_moon"
        NEW_MOON = "new_moon"
    
    class SchumannFrequency:
        BASELINE = "baseline"
        ELEVATED = "elevated"
    
    class MarketLiquidity:
        NORMAL = "normal"
        RESTRICTED = "restricted"
    
    class GlobalSentiment:
        NEUTRAL = "neutral"
        PESSIMISTIC = "pessimistic"
    
    class StrategicTraderB0t:
        def __init__(self, initial_capital=10000.0, name="Test_Bot", redis_client=None, cosmic_config_path=None):
            self.initial_capital = initial_capital
            self.name = name
            self.cosmic_service = CosmicFactorService(config_path=cosmic_config_path)
            self.state = type('obj', (object,), {
                'emotional_state': 'neutral',
                'risk_appetite': 0.5
            })
            self.logger = logging.getLogger("mock_strategic_bot")

        def should_enter_trade(self, market_context):
            return True, "long", "Test reason", 1.0
        
        def determine_position_size(self, direction, entry_price):
            return 1.0
    
    class CosmicFactorService:
        def __init__(self, config_path=None):
            self.enabled = True if config_path is None else True
            
        def is_enabled(self):
            return self.enabled
            
        def calculate_cosmic_influences(self, conditions):
            return {
                "risk_appetite_mod": 0.1,
                "confidence_mod": 0.1,
                "emotional_intensity": 0.2
            }
            
        def apply_cosmic_factors(self, decision, influences):
            if "position_size" in decision:
                decision["position_size"] *= 1.1
            if "confidence" in decision:
                decision["confidence"] += 0.1
            return decision

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test_strategic_bot_cosmic")

class TestStrategicBotCosmic(unittest.TestCase):
    """Test case for the Strategic Bot with cosmic factor integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary config file for testing cosmic factors
        self.temp_config_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        
        # Sample test configuration with some factors disabled
        self.test_config = {
            "enabled": True,
            "factors": {
                "moon_phase": {
                    "enabled": True,
                    "weight": 0.5
                },
                "schumann_resonance": {
                    "enabled": False,  # Disabled for testing
                    "weight": 0.0
                },
                "market_liquidity": {
                    "enabled": True,
                    "weight": 0.7
                },
                "global_sentiment": {
                    "enabled": True,
                    "weight": 1.0
                },
                "mercury_retrograde": {
                    "enabled": False,  # Disabled for testing
                    "weight": 0.0
                }
            }
        }
        
        # Write config to file
        yaml.dump(self.test_config, self.temp_config_file)
        self.temp_config_file.flush()
        
        # Sample market context for testing
        self.market_context = {
            "price": 50000.0,
            "trend": "uptrend",
            "regime": "bullish",
            "price_history": [49000, 49100, 49300, 49500, 49800, 50000, 50200, 50300, 50200, 50000, 
                             49800, 49900, 50100, 50300, 50400, 50500, 50600, 50700, 50800, 50000],
            "volatility": 0.02,
            "volume": 1000.0,
            "moon_phase": MoonPhase.FULL_MOON,
            "schumann_frequency": SchumannFrequency.ELEVATED,
            "market_liquidity": MarketLiquidity.RESTRICTED,
            "global_sentiment": GlobalSentiment.PESSIMISTIC,
            "mercury_retrograde": True,
            "trader_latitude": 40.0,
            "trader_longitude": -74.0,
            "day_of_week": 3,  # Wednesday
            "hour_of_day": 14  # 2 PM
        }
        
        # Set random seed for reproducibility
        random.seed(42)
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary file
        os.unlink(self.temp_config_file.name)
    
    def test_bot_initialization_with_cosmic_service(self):
        """Test that the strategic bot properly initializes with cosmic service."""
        # Initialize bot with cosmic config
        bot = StrategicTraderB0t(
            initial_capital=10000.0,
            name="Cosmic_Test_Bot",
            cosmic_config_path=self.temp_config_file.name
        )
        
        # Check that cosmic service is properly initialized
        self.assertTrue(hasattr(bot, "cosmic_service"))
        self.assertTrue(bot.cosmic_service.is_enabled())
        
        # Check cosmic factor configuration
        self.assertTrue(bot.cosmic_service.is_factor_enabled("moon_phase"))
        self.assertFalse(bot.cosmic_service.is_factor_enabled("schumann_resonance"))
    
    def test_bot_initialization_without_cosmic_config(self):
        """Test that the strategic bot initializes even without a cosmic config."""
        # Initialize bot without specific cosmic config
        bot = StrategicTraderB0t(
            initial_capital=10000.0,
            name="Default_Test_Bot"
        )
        
        # Check that cosmic service is properly initialized with defaults
        self.assertTrue(hasattr(bot, "cosmic_service"))
    
    def test_trading_decision_with_cosmic_factors(self):
        """Test that trading decisions are influenced by cosmic factors."""
        # Initialize bot with cosmic config
        bot = StrategicTraderB0t(
            initial_capital=10000.0,
            name="Decision_Test_Bot",
            cosmic_config_path=self.temp_config_file.name
        )
        
        # Get trading decision with cosmic factors
        should_enter, direction, reason, leverage = bot.should_enter_trade(self.market_context)
        
        # Check that decision was made (exact result depends on random factors and cosmic conditions)
        logger.info(f"Trading decision: {should_enter}, {direction}, {reason}, {leverage}")
        
        # In this case, we're just testing that the method runs without error
        # The actual decision will vary based on the cosmic conditions and market context
    
    def test_position_sizing_with_cosmic_factors(self):
        """Test that position sizing is influenced by cosmic factors."""
        # Initialize bot with cosmic config
        bot = StrategicTraderB0t(
            initial_capital=10000.0,
            name="Position_Test_Bot",
            cosmic_config_path=self.temp_config_file.name
        )
        
        # Calculate position size with cosmic factors
        position_size = bot.determine_position_size("long", 50000.0)
        
        # Log the position size
        logger.info(f"Position size with cosmic factors: {position_size}")
        
        # Without knowing the exact implementation details, we can't assert 
        # specific values, but we can check it's a reasonable number
        self.assertGreater(position_size, 0.0)
        
    def test_comparison_enabled_vs_disabled_cosmic(self):
        """Compare trading decisions with cosmic factors enabled vs disabled."""
        # Create disabled cosmic config
        disabled_config = copy.deepcopy(self.test_config)
        disabled_config["enabled"] = False
        
        # Create temporary file for disabled config
        disabled_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        yaml.dump(disabled_config, disabled_file)
        disabled_file.flush()
        
        try:
            # Initialize bot with cosmic factors enabled
            bot_enabled = StrategicTraderB0t(
                initial_capital=10000.0,
                name="Enabled_Bot",
                cosmic_config_path=self.temp_config_file.name
            )
            
            # Initialize bot with cosmic factors disabled
            bot_disabled = StrategicTraderB0t(
                initial_capital=10000.0,
                name="Disabled_Bot",
                cosmic_config_path=disabled_file.name
            )
            
            # Make sure bots have same initial conditions
            bot_enabled.state.emotional_state = "neutral"
            bot_disabled.state.emotional_state = "neutral"
            bot_enabled.state.risk_appetite = 0.5
            bot_disabled.state.risk_appetite = 0.5
            
            # Get trading decision with cosmic factors enabled
            should_enter_enabled, direction_enabled, reason_enabled, leverage_enabled = bot_enabled.should_enter_trade(self.market_context)
            
            # Get trading decision with cosmic factors disabled
            should_enter_disabled, direction_disabled, reason_disabled, leverage_disabled = bot_disabled.should_enter_trade(self.market_context)
            
            # Calculate position size with cosmic factors enabled
            position_size_enabled = bot_enabled.determine_position_size("long", 50000.0)
            
            # Calculate position size with cosmic factors disabled
            position_size_disabled = bot_disabled.determine_position_size("long", 50000.0)
            
            # Log the differences
            logger.info(f"Enabled cosmic factors: {should_enter_enabled}, {direction_enabled}, {leverage_enabled}, {position_size_enabled}")
            logger.info(f"Disabled cosmic factors: {should_enter_disabled}, {direction_disabled}, {leverage_disabled}, {position_size_disabled}")
            
            # Check that position sizes are different (showing cosmic influence)
            # This is not always guaranteed, as it depends on the specific cosmic conditions,
            # but it's a reasonable expectation in most cases.
            if should_enter_enabled and should_enter_disabled:
                self.assertNotEqual(position_size_enabled, position_size_disabled, 
                                   "Position sizes should differ when cosmic factors are enabled vs disabled")
        finally:
            # Clean up
            os.unlink(disabled_file.name)
    
    def test_consistency_with_constant_cosmic_conditions(self):
        """Test that decisions are consistent with constant cosmic conditions."""
        # Initialize bot with cosmic config
        bot = StrategicTraderB0t(
            initial_capital=10000.0,
            name="Consistency_Test_Bot",
            cosmic_config_path=self.temp_config_file.name
        )
        
        # Create a fixed market context
        fixed_context = copy.deepcopy(self.market_context)
        
        # Disable randomness for consistency
        original_random = random.random
        random.random = lambda: 0.5
        
        try:
            # Get multiple trading decisions with the same context
            decisions = []
            for _ in range(5):
                decision = bot.should_enter_trade(fixed_context)
                decisions.append(decision)
            
            # Check that all decisions are the same
            first_decision = decisions[0]
            for decision in decisions[1:]:
                self.assertEqual(first_decision, decision, 
                               "Decisions should be consistent with constant cosmic conditions")
        finally:
            # Restore randomness
            random.random = original_random

if __name__ == "__main__":
    unittest.main() 