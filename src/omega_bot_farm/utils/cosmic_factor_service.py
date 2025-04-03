#!/usr/bin/env python3

"""
Cosmic Factor Service

A configurable service for calculating and applying cosmic influences to trading decisions.
This service allows for individual cosmic factors to be enabled/disabled and weighted
for testing and production use.
"""

import logging
from typing import Dict, Any, Optional, List, Union
import datetime
from enum import Enum
import yaml
import os
import copy

logger = logging.getLogger("cosmic_factor_service")

# Enum definitions from existing code
class MoonPhase(Enum):
    NEW_MOON = "new_moon"
    WAXING_CRESCENT = "waxing_crescent"
    FIRST_QUARTER = "first_quarter"
    WAXING_GIBBOUS = "waxing_gibbous"
    FULL_MOON = "full_moon"
    WANING_GIBBOUS = "waning_gibbous"
    LAST_QUARTER = "last_quarter"
    WANING_CRESCENT = "waning_crescent"

class SchumannFrequency(Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    BASELINE = "baseline"
    ELEVATED = "elevated"
    HIGH = "high"
    VERY_HIGH = "very_high"

class MarketLiquidity(Enum):
    DRY = "dry"
    RESTRICTED = "restricted"
    NORMAL = "normal"
    FLOWING = "flowing"
    ABUNDANT = "abundant"

class GlobalSentiment(Enum):
    DESPAIR = "despair"
    PESSIMISTIC = "pessimistic"
    CAUTIOUS = "cautious"
    NEUTRAL = "neutral"
    OPTIMISTIC = "optimistic"
    EUPHORIC = "euphoric"
    FEARFUL = "fearful"

class CosmicFactorService:
    """Service for managing cosmic factor calculations and application."""
    
    DEFAULT_CONFIG = {
        "enabled": True,
        "factors": {
            "moon_phase": {
                "enabled": True,
                "weight": 1.0
            },
            "schumann_resonance": {
                "enabled": True,
                "weight": 1.0
            },
            "market_liquidity": {
                "enabled": True,
                "weight": 1.0
            },
            "global_sentiment": {
                "enabled": True,
                "weight": 1.0
            },
            "mercury_retrograde": {
                "enabled": True,
                "weight": 1.0
            },
            "geographic_influence": {
                "enabled": True,
                "weight": 1.0
            },
            "time_cycle": {
                "enabled": True,
                "weight": 1.0
            },
            "circadian_rhythm": {
                "enabled": True,
                "weight": 1.0
            }
        },
        "application": {
            "risk_appetite": True,
            "confidence": True,
            "insight_level": True,
            "emotional_intensity": True,
            "position_size": True,
            "entry_threshold": True,
            "exit_impulse": True
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the cosmic factor service with configuration."""
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    # Deep merge user config with default config
                    self._merge_config(self.config, user_config)
                logger.info(f"Loaded cosmic factor configuration from {config_path}")
            except Exception as e:
                logger.error(f"Error loading cosmic factor configuration: {e}")
        else:
            logger.info("Using default cosmic factor configuration")
    
    def _merge_config(self, base: Dict, override: Dict) -> None:
        """Recursively merge override config into base config."""
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def is_enabled(self) -> bool:
        """Check if cosmic factors are globally enabled."""
        return self.config.get("enabled", False)
    
    def is_factor_enabled(self, factor_name: str) -> bool:
        """Check if a specific cosmic factor is enabled."""
        if not self.is_enabled():
            return False
            
        factor_config = self.config.get("factors", {}).get(factor_name, {})
        return factor_config.get("enabled", False)
    
    def get_factor_weight(self, factor_name: str) -> float:
        """Get the weight for a specific cosmic factor."""
        if not self.is_factor_enabled(factor_name):
            return 0.0
            
        factor_config = self.config.get("factors", {}).get(factor_name, {})
        return factor_config.get("weight", 0.0)
    
    def calculate_cosmic_influences(self, current_conditions: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate cosmic influences based on current conditions and configuration.
        
        Args:
            current_conditions: Dict containing current cosmic conditions
                moon_phase: MoonPhase enum value
                schumann_frequency: SchumannFrequency enum value
                market_liquidity: MarketLiquidity enum value
                global_sentiment: GlobalSentiment enum value
                mercury_retrograde: Boolean
                trader_latitude: Float
                trader_longitude: Float
                day_of_week: Int (0=Monday, 6=Sunday)
                hour_of_day: Int (0-23)
        
        Returns:
            Dict of calculated influence values
        """
        if not self.is_enabled():
            return {
                "risk_appetite_mod": 0.0,
                "confidence_mod": 0.0,
                "mistake_probability": 0.0,
                "emotional_intensity": 0.0,
                "insight_potential": 0.0,
                "vitality": 0.0
            }
        
        influences = {}
        
        # Calculate moon phase influence
        if self.is_factor_enabled("moon_phase"):
            moon_type, moon_value = self._calculate_moon_influence(current_conditions)
            moon_weight = self.get_factor_weight("moon_phase")
            influences["moon_influence"] = moon_value * moon_weight
        else:
            influences["moon_influence"] = 0.0
        
        # Calculate Schumann resonance influence
        if self.is_factor_enabled("schumann_resonance"):
            schumann_type, schumann_value = self._calculate_schumann_influence(current_conditions)
            schumann_weight = self.get_factor_weight("schumann_resonance")
            influences["schumann_influence"] = schumann_value * schumann_weight
        else:
            influences["schumann_influence"] = 0.0
        
        # Calculate market liquidity influence
        if self.is_factor_enabled("market_liquidity"):
            liquidity_value = self._calculate_liquidity_influence(current_conditions)
            liquidity_weight = self.get_factor_weight("market_liquidity")
            influences["liquidity_influence"] = liquidity_value * liquidity_weight
        else:
            influences["liquidity_influence"] = 0.0
        
        # Calculate global sentiment influence
        if self.is_factor_enabled("global_sentiment"):
            sentiment_value = self._calculate_sentiment_influence(current_conditions)
            sentiment_weight = self.get_factor_weight("global_sentiment")
            influences["sentiment_influence"] = sentiment_value * sentiment_weight
        else:
            influences["sentiment_influence"] = 0.0
        
        # Calculate Mercury retrograde influence
        if self.is_factor_enabled("mercury_retrograde"):
            mercury_value = self._calculate_mercury_influence(current_conditions)
            mercury_weight = self.get_factor_weight("mercury_retrograde")
            influences["mercury_influence"] = mercury_value * mercury_weight
        else:
            influences["mercury_influence"] = 0.0
        
        # Calculate geographic influence
        if self.is_factor_enabled("geographic_influence"):
            geo_influences = self._calculate_geographic_influence(current_conditions)
            geo_weight = self.get_factor_weight("geographic_influence")
            influences["geographic_influence"] = {
                k: v * geo_weight for k, v in geo_influences.items()
            }
        else:
            influences["geographic_influence"] = {}
        
        # Calculate time cycle influence
        if self.is_factor_enabled("time_cycle"):
            time_value = self._calculate_time_cycle_influence(current_conditions)
            time_weight = self.get_factor_weight("time_cycle")
            influences["time_cycle_influence"] = time_value * time_weight
        else:
            influences["time_cycle_influence"] = 0.0
        
        # Calculate circadian rhythm influence
        if self.is_factor_enabled("circadian_rhythm"):
            circadian_influences = self._calculate_circadian_influence(current_conditions)
            circadian_weight = self.get_factor_weight("circadian_rhythm")
            influences["circadian_influence"] = {
                k: v * circadian_weight for k, v in circadian_influences.items()
            }
        else:
            influences["circadian_influence"] = {}
        
        # Calculate combined influences
        combined = self._calculate_combined_influences(influences)
        
        return combined
    
    def _calculate_moon_influence(self, conditions: Dict[str, Any]) -> tuple:
        """Calculate lunar influence on trading psychology."""
        moon_phase = conditions.get("moon_phase", MoonPhase.FULL_MOON)
        
        influences = {
            MoonPhase.NEW_MOON: ("risk_reset", 0.0),
            MoonPhase.WAXING_CRESCENT: ("confidence", 0.2),
            MoonPhase.FIRST_QUARTER: ("decisiveness", 0.3),
            MoonPhase.WAXING_GIBBOUS: ("clarity", 0.4),
            MoonPhase.FULL_MOON: ("emotional_intensity", 0.5),
            MoonPhase.WANING_GIBBOUS: ("reflection", 0.3),
            MoonPhase.LAST_QUARTER: ("reevaluation", 0.2),
            MoonPhase.WANING_CRESCENT: ("completion", 0.1)
        }
        
        return influences.get(moon_phase, ("neutral", 0.0))
    
    def _calculate_schumann_influence(self, conditions: Dict[str, Any]) -> tuple:
        """Calculate electromagnetic influence on trading psychology."""
        schumann_frequency = conditions.get("schumann_frequency", SchumannFrequency.BASELINE)
        
        influences = {
            SchumannFrequency.VERY_LOW: ("cautious", -0.3),
            SchumannFrequency.LOW: ("balanced", -0.1),
            SchumannFrequency.BASELINE: ("neutral", 0.0),
            SchumannFrequency.ELEVATED: ("risk_seeking", 0.2),
            SchumannFrequency.HIGH: ("impulsive", 0.4),
            SchumannFrequency.VERY_HIGH: ("highly_impulsive", 0.6)
        }
        
        return influences.get(schumann_frequency, ("neutral", 0.0))
    
    def _calculate_liquidity_influence(self, conditions: Dict[str, Any]) -> float:
        """Calculate market liquidity influence."""
        market_liquidity = conditions.get("market_liquidity", MarketLiquidity.NORMAL)
        
        liquidity_values = {
            MarketLiquidity.DRY: -0.3,
            MarketLiquidity.RESTRICTED: -0.1,
            MarketLiquidity.NORMAL: 0.0,
            MarketLiquidity.FLOWING: 0.1,
            MarketLiquidity.ABUNDANT: 0.2
        }
        
        return liquidity_values.get(market_liquidity, 0.0)
    
    def _calculate_sentiment_influence(self, conditions: Dict[str, Any]) -> float:
        """Calculate global sentiment influence."""
        global_sentiment = conditions.get("global_sentiment", GlobalSentiment.NEUTRAL)
        
        sentiment_values = {
            GlobalSentiment.DESPAIR: -0.5,
            GlobalSentiment.PESSIMISTIC: -0.3,
            GlobalSentiment.CAUTIOUS: -0.1,
            GlobalSentiment.NEUTRAL: 0.0,
            GlobalSentiment.OPTIMISTIC: 0.2,
            GlobalSentiment.EUPHORIC: 0.4,
            GlobalSentiment.FEARFUL: -0.3
        }
        
        return sentiment_values.get(global_sentiment, 0.0)
    
    def _calculate_mercury_influence(self, conditions: Dict[str, Any]) -> float:
        """Calculate Mercury retrograde influence."""
        mercury_retrograde = conditions.get("mercury_retrograde", False)
        return 0.2 if mercury_retrograde else 0.0
    
    def _calculate_geographic_influence(self, conditions: Dict[str, Any]) -> Dict[str, float]:
        """Calculate geographic influence based on position and season."""
        # Extract latitude and longitude
        latitude = conditions.get("trader_latitude", 0.0)
        longitude = conditions.get("trader_longitude", 0.0)
        
        # Get current month
        month = datetime.datetime.now().month
        winter_north = month in [11, 12, 1, 2] 
        winter_south = month in [5, 6, 7, 8]
        
        # Check for equatorial region (minimal seasonal effects)
        is_equatorial = abs(latitude) < 10.0
        
        # Determine hemisphere and season
        is_north = latitude > 0
        is_winter = (is_north and winter_north) or (not is_north and winter_south)
        
        # Create a dictionary of seasonal influences
        if is_equatorial:
            # Equatorial regions have minimal seasonal variations
            influences = {
                "vitality": 0.1,          # Minimal seasonal effect
                "risk_tolerance": 0.1,    # Minimal seasonal effect
                "patience": -0.05,        # Minimal seasonal effect
                "focus": 0.0,             # Minimal seasonal effect
                "social_trading": 0.1,    # Minimal seasonal effect
                "introspection": 0.0,     # Minimal seasonal effect
                "extroversion": 0.1       # Minimal seasonal effect
            }
        else:
            # Non-equatorial regions have stronger seasonal effects
            influences = {
                "vitality": -0.2 if is_winter else 0.3,       # Winter reduces vitality
                "risk_tolerance": -0.1 if is_winter else 0.2,  # Winter = conservative
                "patience": 0.2 if is_winter else -0.1,        # Winter increases patience
                "focus": 0.1 if is_winter else -0.05,          # Better focus in winter
                "social_trading": -0.1 if is_winter else 0.2,  # More social in summer
                "introspection": 0.3 if is_winter else -0.1,   # Winter increases introspection
                "extroversion": -0.2 if is_winter else 0.3     # Summer increases extroversion
            }
        
        # Longitude effect: different trading times relative to major markets
        longitude_factor = abs(longitude) / 180.0 * 0.1
        
        # Apply longitude factor to all influences
        for key in influences:
            influences[key] += longitude_factor
            
        return influences
    
    def _calculate_time_cycle_influence(self, conditions: Dict[str, Any]) -> float:
        """Calculate influence of day/time on trading psychology."""
        day_of_week = conditions.get("day_of_week", 0)
        hour_of_day = conditions.get("hour_of_day", 12)
        
        # Monday and Friday effects
        if day_of_week == 0:  # Monday
            day_effect = -0.15  # More cautious at start of week
        elif day_of_week == 4:  # Friday
            day_effect = 0.1  # More risk-taking before weekend
        else:
            day_effect = 0.0
            
        # Time of day effects (market open/close)
        if hour_of_day in [9, 10]:  # Market open
            hour_effect = 0.1  # More active at market open
        elif hour_of_day in [15, 16]:  # Market close
            hour_effect = 0.15  # More impulsive near close
        else:
            hour_effect = 0.0
            
        return day_effect + hour_effect
    
    def _calculate_circadian_influence(self, conditions: Dict[str, Any]) -> Dict[str, float]:
        """Calculate circadian rhythm influences on trading psychology."""
        hour_of_day = conditions.get("hour_of_day", 12)
        
        # Base influence values
        influences = {
            "alertness": 0.0,     # Mental sharpness
            "patience": 0.0,      # Trading patience
            "analysis": 0.0,      # Analytical ability
            "intuition": 0.0,     # Intuitive insights
            "impulsivity": 0.0,   # Impulsive decision making
            "discipline": 0.0     # Trading discipline
        }
        
        hour = hour_of_day
        
        # Early morning (1-4 AM): Low alertness, high intuition
        if hour >= 1 and hour <= 4:
            influences["alertness"] = -0.3
            influences["patience"] = -0.2
            influences["analysis"] = -0.3
            influences["intuition"] = 0.3
            influences["impulsivity"] = 0.2
            influences["discipline"] = -0.1
            
        # Morning (5-9 AM): Rising alertness 
        elif hour >= 5 and hour <= 9:
            influences["alertness"] = 0.1
            influences["patience"] = 0.1
            influences["analysis"] = 0.0
            influences["intuition"] = 0.1
            influences["impulsivity"] = -0.1
            influences["discipline"] = 0.0
            
        # Midday (10 AM - 2 PM): Peak alertness, good analysis
        elif hour >= 10 and hour <= 14:
            influences["alertness"] = 0.3
            influences["patience"] = 0.0
            influences["analysis"] = 0.3
            influences["intuition"] = -0.1
            influences["impulsivity"] = -0.2
            influences["discipline"] = 0.1
            
        # Afternoon (3-5 PM): Slight dip
        elif hour >= 15 and hour <= 17:
            influences["alertness"] = 0.1
            influences["patience"] = -0.1
            influences["analysis"] = 0.1
            influences["intuition"] = 0.0
            influences["impulsivity"] = 0.1
            influences["discipline"] = 0.0
            
        # Evening (6-9 PM): Second wind
        elif hour >= 18 and hour <= 21:
            influences["alertness"] = 0.2
            influences["patience"] = -0.1
            influences["analysis"] = 0.0
            influences["intuition"] = 0.2
            influences["impulsivity"] = 0.0
            influences["discipline"] = -0.05
            
        # Night (10 PM - 12 AM): Winding down
        else:
            influences["alertness"] = -0.1
            influences["patience"] = -0.2
            influences["analysis"] = -0.2
            influences["intuition"] = 0.2
            influences["impulsivity"] = 0.1
            influences["discipline"] = -0.1
            
        return influences
    
    def _calculate_combined_influences(self, influences: Dict[str, Any]) -> Dict[str, float]:
        """Calculate combined cosmic influences on trader psychology."""
        # Extract individual influences
        moon_influence = influences.get("moon_influence", 0.0)
        schumann_influence = influences.get("schumann_influence", 0.0)
        liquidity_influence = influences.get("liquidity_influence", 0.0)
        sentiment_influence = influences.get("sentiment_influence", 0.0)
        mercury_influence = influences.get("mercury_influence", 0.0)
        time_cycle_influence = influences.get("time_cycle_influence", 0.0)
        
        # Extract geographic influences
        geo_influences = influences.get("geographic_influence", {})
        geo_risk = geo_influences.get("risk_tolerance", 0.0)
        geo_vitality = geo_influences.get("vitality", 0.0)
        
        # Extract circadian influences
        circadian_influences = influences.get("circadian_influence", {})
        
        # Calculate combined effects
        combined = {
            "risk_appetite_mod": moon_influence + schumann_influence + geo_risk + sentiment_influence + liquidity_influence,
            "confidence_mod": sentiment_influence + time_cycle_influence + moon_influence + geo_vitality,
            "mistake_probability": mercury_influence + (0.1 if influences.get("moon_phase") == MoonPhase.FULL_MOON else 0.0),
            "emotional_intensity": moon_influence * 2 + schumann_influence + abs(sentiment_influence) * 0.5,
            "insight_potential": 0.3 if influences.get("moon_phase") == MoonPhase.NEW_MOON else 0.0,
            "vitality": geo_vitality,
            "alertness": circadian_influences.get("alertness", 0.0),
            "discipline": circadian_influences.get("discipline", 0.0)
        }
        
        return combined
    
    def apply_cosmic_factors(self, trading_decision: Dict[str, Any], 
                          cosmic_influences: Dict[str, float]) -> Dict[str, Any]:
        """
        Apply cosmic influences to a trading decision based on configuration.
        
        Args:
            trading_decision: Original trading decision
            cosmic_influences: Calculated cosmic influences
            
        Returns:
            Modified trading decision with cosmic influences applied
        """
        if not self.is_enabled():
            return trading_decision
        
        # Create a deep copy to avoid modifying the original
        decision = copy.deepcopy(trading_decision)
        
        # Extract influence values
        risk_mod = cosmic_influences.get("risk_appetite_mod", 0.0)
        confidence_mod = cosmic_influences.get("confidence_mod", 0.0)
        emotional_intensity = cosmic_influences.get("emotional_intensity", 0.0)
        
        # Apply risk appetite modification to position size if enabled
        if self.config.get("application", {}).get("position_size", True):
            # Calculate the factor to apply to position size
            position_factor = 1.0 + risk_mod
            
            # Apply the factor (ensure it doesn't go too low or high)
            position_factor = max(0.5, min(2.0, position_factor))
            
            # Apply to position size
            if "position_size" in decision:
                decision["position_size"] = decision["position_size"] * position_factor
        
        # Apply confidence modification to entry threshold if enabled
        if self.config.get("application", {}).get("entry_threshold", True):
            # Calculate the factor to apply to entry threshold
            threshold_factor = 1.0 - confidence_mod
            
            # Apply the factor (ensure it doesn't go too low or high)
            threshold_factor = max(0.7, min(1.3, threshold_factor))
            
            # Apply to entry threshold
            if "entry_threshold" in decision:
                decision["entry_threshold"] = decision["entry_threshold"] * threshold_factor
        
        # Apply emotional intensity to exit impulse if enabled
        if self.config.get("application", {}).get("exit_impulse", True):
            # Calculate the factor to apply to exit impulse
            impulse_factor = 1.0 + emotional_intensity
            
            # Apply the factor (ensure it doesn't go too low or high)
            impulse_factor = max(0.8, min(1.5, impulse_factor))
            
            # Apply to exit impulse
            if "exit_impulse" in decision:
                decision["exit_impulse"] = decision["exit_impulse"] * impulse_factor
        
        return decision
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate a status report of enabled cosmic factors and weights."""
        report = {
            "enabled": self.is_enabled(),
            "factors": {}
        }
        
        for factor_name in self.config.get("factors", {}):
            report["factors"][factor_name] = {
                "enabled": self.is_factor_enabled(factor_name),
                "weight": self.get_factor_weight(factor_name)
            }
        
        return report 