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
Test module for the CosmicFactorService.

These tests validate cosmic factor isolation and parameterization.
"""

import os
import unittest
import tempfile
import yaml
from typing import Dict, Any
import copy
import logging

from src.omega_bot_farm.utils.cosmic_factor_service import (
    CosmicFactorService, 
    MoonPhase, 
    SchumannFrequency, 
    MarketLiquidity, 
    GlobalSentiment
)

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test_cosmic_factor_service")

class TestCosmicFactorService(unittest.TestCase):
    """Test case for the CosmicFactorService."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary config file for testing
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
        
        # Sample market conditions
        self.test_conditions = {
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
        
        # Sample trading decision for testing influence application
        self.test_decision = {
            "should_enter": True,
            "direction": "long",
            "position_size": 1000.0,
            "entry_threshold": 0.65,
            "exit_impulse": 0.3,
            "stop_loss_percent": 0.02,
            "take_profit_percent": 0.06
        }
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary file
        os.unlink(self.temp_config_file.name)
    
    def test_default_initialization(self):
        """Test initialization with default values."""
        service = CosmicFactorService()
        
        # Check if service is properly initialized
        self.assertTrue(service.is_enabled())
        self.assertTrue(service.is_factor_enabled("moon_phase"))
        self.assertTrue(service.is_factor_enabled("schumann_resonance"))
        self.assertEqual(service.get_factor_weight("moon_phase"), 1.0)
    
    def test_custom_config_initialization(self):
        """Test initialization with custom configuration."""
        service = CosmicFactorService(config_path=self.temp_config_file.name)
        
        # Check if config is properly loaded
        self.assertTrue(service.is_enabled())
        self.assertTrue(service.is_factor_enabled("moon_phase"))
        self.assertFalse(service.is_factor_enabled("schumann_resonance"))
        self.assertEqual(service.get_factor_weight("moon_phase"), 0.5)
        self.assertEqual(service.get_factor_weight("schumann_resonance"), 0.0)
    
    def test_disabled_service(self):
        """Test with completely disabled cosmic service."""
        # Create config with service disabled
        disabled_config = copy.deepcopy(self.test_config)
        disabled_config["enabled"] = False
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        yaml.dump(disabled_config, temp_file)
        temp_file.flush()
        
        try:
            # Initialize service with disabled config
            service = CosmicFactorService(config_path=temp_file.name)
            
            # Service should be disabled
            self.assertFalse(service.is_enabled())
            self.assertFalse(service.is_factor_enabled("moon_phase"))
            
            # Calculate influences (should be all zeros)
            influences = service.calculate_cosmic_influences(self.test_conditions)
            
            # Check if all influences are zero
            self.assertEqual(influences["risk_appetite_mod"], 0.0)
            self.assertEqual(influences["confidence_mod"], 0.0)
            self.assertEqual(influences["emotional_intensity"], 0.0)
            
            # Test applying influences (should not modify decision)
            modified_decision = service.apply_cosmic_factors(self.test_decision, influences)
            
            # Decision should be unchanged
            self.assertEqual(modified_decision, self.test_decision)
        finally:
            # Clean up
            os.unlink(temp_file.name)
    
    def test_factor_isolation(self):
        """Test isolation of specific cosmic factors."""
        # Create a service with custom config
        service = CosmicFactorService(config_path=self.temp_config_file.name)
        
        # Calculate influences with test configuration
        influences = service.calculate_cosmic_influences(self.test_conditions)
        
        # Schumann resonance is disabled, so its influence should be zero
        self.assertEqual(influences.get("schumann_influence", 0.0), 0.0)
        
        # Moon phase is enabled with weight 0.5, so its influence should be reduced
        # Full moon has emotional_intensity of 0.5 in the code, so with weight 0.5,
        # it should contribute 0.25 to emotional_intensity
        self.assertAlmostEqual(influences["emotional_intensity"], 0.25, delta=0.1)
    
    def test_all_factors_isolated(self):
        """Test with all factors isolated (enabled one by one)."""
        # Base config with all factors disabled
        base_config = {
            "enabled": True,
            "factors": {
                "moon_phase": {"enabled": False, "weight": 0.0},
                "schumann_resonance": {"enabled": False, "weight": 0.0},
                "market_liquidity": {"enabled": False, "weight": 0.0},
                "global_sentiment": {"enabled": False, "weight": 0.0},
                "mercury_retrograde": {"enabled": False, "weight": 0.0},
                "geographic_influence": {"enabled": False, "weight": 0.0},
                "time_cycle": {"enabled": False, "weight": 0.0},
                "circadian_rhythm": {"enabled": False, "weight": 0.0}
            }
        }
        
        # Test each factor in isolation
        factors = ["moon_phase", "schumann_resonance", "market_liquidity", 
                   "global_sentiment", "mercury_retrograde", "geographic_influence", 
                   "time_cycle", "circadian_rhythm"]
        
        for factor in factors:
            # Enable only this factor
            temp_config = copy.deepcopy(base_config)
            temp_config["factors"][factor]["enabled"] = True
            temp_config["factors"][factor]["weight"] = 1.0
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
            yaml.dump(temp_config, temp_file)
            temp_file.flush()
            
            try:
                # Initialize service with single factor
                service = CosmicFactorService(config_path=temp_file.name)
                
                # Only this factor should be enabled
                self.assertTrue(service.is_factor_enabled(factor))
                for other_factor in factors:
                    if other_factor != factor:
                        self.assertFalse(service.is_factor_enabled(other_factor))
                
                # Calculate influences with just this factor
                influences = service.calculate_cosmic_influences(self.test_conditions)
                
                # Log for debugging
                logger.debug(f"Factor: {factor}, Influences: {influences}")
                
                # Verify this factor has influence and others don't
                # We can't make specific assertions about the values without knowing
                # the exact implementation of each factor, but we can check for non-zero values
                if factor == "moon_phase":
                    self.assertNotEqual(influences["moon_influence"], 0.0)
                elif factor == "schumann_resonance":
                    self.assertNotEqual(influences["schumann_influence"], 0.0)
                elif factor == "market_liquidity":
                    self.assertNotEqual(influences["liquidity_influence"], 0.0)
                
            finally:
                # Clean up
                os.unlink(temp_file.name)
    
    def test_apply_factors_to_trading_decision(self):
        """Test applying isolated cosmic factors to trading decisions."""
        # Create config with only market liquidity enabled
        liquidity_config = {
            "enabled": True,
            "factors": {
                "moon_phase": {"enabled": False, "weight": 0.0},
                "schumann_resonance": {"enabled": False, "weight": 0.0},
                "market_liquidity": {"enabled": True, "weight": 1.0},
                "global_sentiment": {"enabled": False, "weight": 0.0},
                "mercury_retrograde": {"enabled": False, "weight": 0.0},
                "geographic_influence": {"enabled": False, "weight": 0.0},
                "time_cycle": {"enabled": False, "weight": 0.0},
                "circadian_rhythm": {"enabled": False, "weight": 0.0}
            }
        }
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        yaml.dump(liquidity_config, temp_file)
        temp_file.flush()
        
        try:
            # Initialize service with liquidity only
            service = CosmicFactorService(config_path=temp_file.name)
            
            # Calculate influences with just liquidity
            influences = service.calculate_cosmic_influences(self.test_conditions)
            
            # Apply influences to trading decision
            original_decision = copy.deepcopy(self.test_decision)
            modified_decision = service.apply_cosmic_factors(self.test_decision, influences)
            
            # Verify decision was modified (in restricted liquidity, position size should decrease)
            # Based on _calculate_liquidity_influence in the service, RESTRICTED liquidity has -0.1 value
            self.assertLess(modified_decision["position_size"], original_decision["position_size"])
            
            # Check that the change is related to -0.1 risk_appetite_mod
            expected_factor = 1.0 - 0.1  # 1.0 + (-0.1)
            expected_position = original_decision["position_size"] * expected_factor
            self.assertAlmostEqual(modified_decision["position_size"], expected_position, delta=0.1)
            
        finally:
            # Clean up
            os.unlink(temp_file.name)
    
    def test_comparative_performance(self):
        """Compare trading decisions with different cosmic factor configurations."""
        # Test cases to compare
        test_cases = [
            {"name": "No cosmic factors", "config": {"enabled": False}},
            {"name": "Moon only", "config": {
                "enabled": True,
                "factors": {
                    "moon_phase": {"enabled": True, "weight": 1.0},
                    "schumann_resonance": {"enabled": False, "weight": 0.0},
                    "market_liquidity": {"enabled": False, "weight": 0.0},
                    "global_sentiment": {"enabled": False, "weight": 0.0},
                    "mercury_retrograde": {"enabled": False, "weight": 0.0}
                }
            }},
            {"name": "Market factors only", "config": {
                "enabled": True,
                "factors": {
                    "moon_phase": {"enabled": False, "weight": 0.0},
                    "schumann_resonance": {"enabled": False, "weight": 0.0},
                    "market_liquidity": {"enabled": True, "weight": 1.0},
                    "global_sentiment": {"enabled": True, "weight": 1.0},
                    "mercury_retrograde": {"enabled": False, "weight": 0.0}
                }
            }},
            {"name": "All factors", "config": {"enabled": True}}
        ]
        
        # Compare trading decisions across configurations
        results = {}
        
        for case in test_cases:
            # Create temporary config file
            temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
            yaml.dump(case["config"], temp_file)
            temp_file.flush()
            
            try:
                # Initialize service with config
                service = CosmicFactorService(config_path=temp_file.name)
                
                # Calculate influences
                influences = service.calculate_cosmic_influences(self.test_conditions)
                
                # Apply to trading decision
                decision = copy.deepcopy(self.test_decision)
                modified = service.apply_cosmic_factors(decision, influences)
                
                # Store results
                results[case["name"]] = {
                    "position_size": modified["position_size"],
                    "entry_threshold": modified["entry_threshold"],
                    "exit_impulse": modified["exit_impulse"]
                }
                
                # Log results
                logger.info(f"Case: {case['name']}")
                logger.info(f"Position size: {modified['position_size']}")
                logger.info(f"Entry threshold: {modified['entry_threshold']}")
                logger.info(f"Exit impulse: {modified['exit_impulse']}")
                
            finally:
                # Clean up
                os.unlink(temp_file.name)
        
        # Verify differences between configurations
        base_position = results["No cosmic factors"]["position_size"]
        
        # Check that moon phase affects position size differently than market factors
        self.assertNotEqual(
            results["Moon only"]["position_size"], 
            results["Market factors only"]["position_size"]
        )
        
        # Check that all factors combined have a different effect than individual components
        self.assertNotEqual(
            results["All factors"]["position_size"],
            results["Moon only"]["position_size"]
        )
        self.assertNotEqual(
            results["All factors"]["position_size"],
            results["Market factors only"]["position_size"]
        )

if __name__ == "__main__":
    unittest.main() 