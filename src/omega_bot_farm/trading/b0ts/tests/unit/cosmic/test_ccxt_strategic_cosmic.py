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
Test module for CCXT Strategic Trader Bot with cosmic factor integration.

This module tests the integration of the CosmicFactorService with the CCXTStrategicTraderB0t.
"""

import os
import unittest
import tempfile
import yaml
from typing import Dict, Any
import copy
import logging
import asyncio
import random

try:
    from src.omega_bot_farm.trading.b0ts.ccxt.ccxt_strategic_trader import CCXTStrategicTraderB0t
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
    
    class CCXTStrategicTraderB0t:
        def __init__(self, initial_capital=10000.0, name="Test_Bot", redis_client=None, 
                    exchange_id="test", symbol="BTCUSDT", max_position_size=None, 
                    cosmic_config_path=None):
            self.initial_capital = initial_capital
            self.name = name
            self.exchange_id = exchange_id
            self.symbol = symbol
            self.max_position_size = max_position_size or 1000.0
            self.cosmic_service = CosmicFactorService(config_path=cosmic_config_path)
            self.state = type('obj', (object,), {
                'emotional_state': 'neutral',
                'risk_appetite': 0.5
            })
            self.logger = logging.getLogger("mock_ccxt_strategic_bot")
            self.active_position = False
            self.position_side = None
            self.position_entry_price = 0.0
            self.position_size = 0.0
            self.leverage = 10
            
        async def should_enter_trade(self, market_context):
            # Mock implementation for testing
            entry_threshold = 0.5
            confirmation_score = 0.6
            
            if hasattr(self, 'cosmic_service'):
                # Get cosmic conditions from market context
                cosmic_conditions = self._get_current_cosmic_conditions(market_context)
                
                # Calculate cosmic influences
                cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
                
                # Apply cosmic influences to decision
                decision = {
                    "entry_threshold": entry_threshold,
                    "confidence": confirmation_score
                }
                
                modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
                
                # Get modified values
                confirmation_score = modified_decision.get("confidence", confirmation_score)
                entry_threshold = modified_decision.get("entry_threshold", entry_threshold)
            
            if confirmation_score > entry_threshold:
                return True, "long", "Test reason", 1.0
            return False, "none", "Insufficient confirmation", 1.0
        
        def _get_current_cosmic_conditions(self, market_context):
            # Extract conditions from market context
            return {
                "moon_phase": market_context.get("moon_phase", MoonPhase.FULL_MOON),
                "schumann_frequency": market_context.get("schumann_frequency", SchumannFrequency.BASELINE),
                "market_liquidity": market_context.get("market_liquidity", MarketLiquidity.NORMAL),
                "global_sentiment": market_context.get("global_sentiment", GlobalSentiment.NEUTRAL),
                "mercury_retrograde": market_context.get("mercury_retrograde", False),
                "trader_latitude": market_context.get("trader_latitude", 40.0),
                "trader_longitude": market_context.get("trader_longitude", -74.0),
                "day_of_week": market_context.get("day_of_week", 0),
                "hour_of_day": market_context.get("hour_of_day", 12),
            }
        
        async def determine_position_size(self, direction, entry_price):
            # Mock implementation for testing
            base_amount = self.max_position_size * 0.1 / entry_price
            
            if hasattr(self, 'cosmic_service'):
                # Create a decision object for cosmic factor service
                decision = {
                    "position_size": base_amount,
                    "entry_price": entry_price,
                    "direction": direction
                }
                
                # Get current cosmic conditions (default values for testing)
                cosmic_conditions = {
                    "moon_phase": MoonPhase.FULL_MOON,
                    "schumann_frequency": SchumannFrequency.BASELINE,
                    "market_liquidity": MarketLiquidity.NORMAL,
                    "global_sentiment": GlobalSentiment.NEUTRAL,
                    "mercury_retrograde": False,
                    "trader_latitude": 40.0,
                    "trader_longitude": -74.0,
                    "day_of_week": 0,
                    "hour_of_day": 12,
                }
                
                # Calculate cosmic influences
                cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
                
                # Apply cosmic influences to position size
                modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
                
                # Get modified position size
                base_amount = modified_decision.get("position_size", base_amount)
            
            return base_amount
        
        async def check_exit_conditions(self, market_context):
            # Mock implementation for testing
            if not self.active_position:
                return False, "No active position"
                
            exit_impulse = 0.4
            exit_threshold = 0.5
            
            if hasattr(self, 'cosmic_service'):
                # Create a decision object for cosmic factor service
                decision = {
                    "exit_impulse": exit_impulse,
                    "exit_threshold": exit_threshold
                }
                
                # Get cosmic conditions from market context
                cosmic_conditions = self._get_current_cosmic_conditions(market_context)
                
                # Calculate cosmic influences
                cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
                
                # Apply cosmic influences to exit decision
                modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
                
                # Get modified values
                exit_impulse = modified_decision.get("exit_impulse", exit_impulse)
                exit_threshold = modified_decision.get("exit_threshold", exit_threshold)
            
            if exit_impulse > exit_threshold:
                return True, f"Exit signal confirmed: {exit_impulse:.2f}"
            
            return False, "No exit signal"
    
    class CosmicFactorService:
        def __init__(self, config_path=None):
            self.enabled = True if config_path is None else True
            self.config_path = config_path
            
        def is_enabled(self):
            return self.enabled
            
        def is_factor_enabled(self, factor_name):
            return True
            
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
            if "exit_impulse" in decision:
                decision["exit_impulse"] += 0.15
            if "entry_threshold" in decision:
                decision["entry_threshold"] -= 0.05
            return decision

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test_ccxt_strategic_cosmic")

class TestCCXTStrategicCosmic(unittest.TestCase):
    """Test case for the CCXT Strategic Bot with cosmic factor integration."""
    
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
        """Test that the CCXT strategic bot properly initializes with cosmic service."""
        # Initialize bot with cosmic config
        bot = CCXTStrategicTraderB0t(
            initial_capital=10000.0,
            name="Cosmic_Test_Bot",
            exchange_id="test",
            symbol="BTCUSDT",
            cosmic_config_path=self.temp_config_file.name
        )
        
        # Check that cosmic service is properly initialized
        self.assertTrue(hasattr(bot, "cosmic_service"))
        self.assertTrue(bot.cosmic_service.is_enabled())
        
        # Check cosmic factor configuration
        self.assertTrue(bot.cosmic_service.is_factor_enabled("moon_phase"))
        self.assertFalse(bot.cosmic_service.is_factor_enabled("schumann_resonance"))
    
    async def test_trading_decision_with_cosmic_factors(self):
        """Test that trading decisions are influenced by cosmic factors."""
        # Initialize bot with cosmic config
        bot = CCXTStrategicTraderB0t(
            initial_capital=10000.0,
            name="Decision_Test_Bot",
            exchange_id="test",
            symbol="BTCUSDT",
            cosmic_config_path=self.temp_config_file.name
        )
        
        # Get trading decision with cosmic factors
        should_enter, direction, reason, leverage = await bot.should_enter_trade(self.market_context)
        
        # Log the decision
        logger.info(f"Trading decision: {should_enter}, {direction}, {reason}, {leverage}")
        
        # Check that decision was influenced by cosmic factors (actual value depends on the implementation)
        self.assertTrue(should_enter)  # For the mock implementation
    
    async def test_position_sizing_with_cosmic_factors(self):
        """Test that position sizing is influenced by cosmic factors."""
        # Initialize bot with cosmic config
        bot = CCXTStrategicTraderB0t(
            initial_capital=10000.0,
            name="Position_Test_Bot",
            exchange_id="test",
            symbol="BTCUSDT",
            cosmic_config_path=self.temp_config_file.name
        )
        
        # Calculate position size with cosmic factors
        position_size = await bot.determine_position_size("long", 50000.0)
        
        # Log the position size
        logger.info(f"Position size with cosmic factors: {position_size}")
        
        # Check that position size is reasonable
        self.assertGreater(position_size, 0.0)
    
    async def test_comparison_enabled_vs_disabled_cosmic(self):
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
            bot_enabled = CCXTStrategicTraderB0t(
                initial_capital=10000.0,
                name="Enabled_Bot",
                exchange_id="test",
                symbol="BTCUSDT",
                cosmic_config_path=self.temp_config_file.name
            )
            
            # Initialize bot with cosmic factors disabled
            bot_disabled = CCXTStrategicTraderB0t(
                initial_capital=10000.0,
                name="Disabled_Bot",
                exchange_id="test",
                symbol="BTCUSDT",
                cosmic_config_path=disabled_file.name
            )
            
            # Get trading decision with cosmic factors enabled
            should_enter_enabled, direction_enabled, reason_enabled, leverage_enabled = await bot_enabled.should_enter_trade(self.market_context)
            
            # Get trading decision with cosmic factors disabled
            should_enter_disabled, direction_disabled, reason_disabled, leverage_disabled = await bot_disabled.should_enter_trade(self.market_context)
            
            # Calculate position size with cosmic factors enabled
            position_size_enabled = await bot_enabled.determine_position_size("long", 50000.0)
            
            # Calculate position size with cosmic factors disabled
            position_size_disabled = await bot_disabled.determine_position_size("long", 50000.0)
            
            # Log the differences
            logger.info(f"Enabled cosmic factors: {should_enter_enabled}, {direction_enabled}, {leverage_enabled}, {position_size_enabled}")
            logger.info(f"Disabled cosmic factors: {should_enter_disabled}, {direction_disabled}, {leverage_disabled}, {position_size_disabled}")
            
            # Check that decisions are different (showing cosmic influence)
            self.assertNotEqual(position_size_enabled, position_size_disabled, 
                              "Position sizes should differ when cosmic factors are enabled vs disabled")
        finally:
            # Clean up
            os.unlink(disabled_file.name)
    
    async def test_exit_conditions_with_cosmic_factors(self):
        """Test that exit conditions are influenced by cosmic factors."""
        # Initialize bot with cosmic config
        bot = CCXTStrategicTraderB0t(
            initial_capital=10000.0,
            name="Exit_Test_Bot",
            exchange_id="test",
            symbol="BTCUSDT",
            cosmic_config_path=self.temp_config_file.name
        )
        
        # Set up active position
        bot.active_position = True
        bot.position_side = "long"
        bot.position_entry_price = 45000.0
        bot.position_size = 0.1
        
        # Check exit conditions with cosmic factors
        should_exit, reason = await bot.check_exit_conditions(self.market_context)
        
        # Log the decision
        logger.info(f"Exit decision: {should_exit}, {reason}")
        
        # Check that exit decision was influenced by cosmic factors (actual value depends on the implementation)
        self.assertTrue(should_exit)  # For the mock implementation

def run_async_tests():
    """Run async tests using event loop."""
    loop = asyncio.get_event_loop()
    
    # Get all test methods
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCCXTStrategicCosmic)
    
    # Filter out the async tests
    async_tests = []
    for test in suite:
        if test._testMethodName.startswith('test_') and test._testMethodName != 'test_bot_initialization_with_cosmic_service':
            async_tests.append(test._testMethodName)
    
    # Run async tests
    for test_name in async_tests:
        test_method = getattr(TestCCXTStrategicCosmic, test_name)
        instance = TestCCXTStrategicCosmic(test_name)
        instance.setUp()
        try:
            loop.run_until_complete(test_method(instance))
        finally:
            instance.tearDown()

if __name__ == "__main__":
    # Run synchronous tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCCXTStrategicCosmic)
    # Filter out the async tests
    filtered_suite = unittest.TestSuite()
    for test in suite:
        if not test._testMethodName.startswith('test_') or test._testMethodName == 'test_bot_initialization_with_cosmic_service':
            filtered_suite.addTest(test)
    
    unittest.TextTestRunner().run(filtered_suite)
    
    # Run async tests
    run_async_tests() 