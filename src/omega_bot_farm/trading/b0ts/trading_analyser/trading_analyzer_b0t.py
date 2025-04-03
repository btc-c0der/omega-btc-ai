#!/usr/bin/env python3

"""
Trading analyzer for Omega Bot Farm

This module provides market analysis utilities for the bot farm traders.
"""

import random
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any, Union

logger = logging.getLogger("trading_analyzer_b0t")

class TradingAnalyzerB0t:
    """Simplified trading analyzer for containerized bot environment."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize trading analyzer with optional random seed."""
        self.random = random.Random(seed)
        self.logger = logger
        
    def analyze_trend(self, prices: List[float], window: int = 20) -> str:
        """Determine market trend from price history."""
        if len(prices) < window:
            return "sideways"  # Not enough data
            
        # Calculate simple moving average
        sma = sum(prices[-window:]) / window
        
        # Calculate trend strength
        current_price = prices[-1]
        price_change = (current_price - prices[-window]) / prices[-window]
        
        if current_price > sma * 1.01 and price_change > 0.01:
            return "uptrend"
        elif current_price < sma * 0.99 and price_change < -0.01:
            return "downtrend"
        else:
            return "sideways"
            
    def calculate_volatility(self, prices: List[float], window: int = 20) -> float:
        """Calculate price volatility."""
        if len(prices) < window:
            return 0.0
            
        # Use numpy for efficient calculation if available
        try:
            return float(np.std(prices[-window:]))
        except:
            # Fallback if numpy isn't available
            mean = sum(prices[-window:]) / window
            variance = sum((p - mean) ** 2 for p in prices[-window:]) / window
            return variance ** 0.5
            
    def detect_support_resistance(self, prices: List[float], window: int = 50) -> Tuple[float, float]:
        """Detect basic support and resistance levels."""
        if len(prices) < window:
            current = prices[-1]
            return current * 0.98, current * 1.02  # Default fallback
            
        price_window = prices[-window:]
        support = min(price_window)
        resistance = max(price_window)
        
        return support, resistance
        
    def analyze_market_regime(self, 
                              prices: List[float], 
                              volumes: Optional[List[float]] = None) -> str:
        """Analyze overall market regime (bullish, bearish, neutral)."""
        if len(prices) < 30:
            return "neutral"  # Not enough data
            
        # Analyze price trend
        short_trend = self.analyze_trend(prices, window=10)
        long_trend = self.analyze_trend(prices, window=30)
        
        # Calculate volatility
        volatility = self.calculate_volatility(prices)
        avg_price = sum(prices[-30:]) / 30
        volatility_ratio = volatility / avg_price
        
        # Combine signals
        if short_trend == "uptrend" and long_trend == "uptrend":
            if volatility_ratio > 0.02:  # High volatility uptrend
                return "bullish_volatile"
            return "bullish"
        elif short_trend == "downtrend" and long_trend == "downtrend":
            if volatility_ratio > 0.02:  # High volatility downtrend
                return "bearish_volatile"
            return "bearish"
        elif long_trend == "uptrend" and short_trend == "downtrend":
            return "bullish_correction"
        elif long_trend == "downtrend" and short_trend == "uptrend":
            return "bearish_bounce"
        else:
            if volatility_ratio > 0.015:
                return "neutral_volatile"
            return "neutral"
            
    def calculate_risk_factor(self, market_context: Dict) -> float:
        """Calculate risk factor based on market conditions."""
        risk_factor = 0.5  # Default medium risk
        
        # Adjust for trend
        trend = market_context.get("trend", "sideways")
        if trend == "uptrend":
            risk_factor += 0.1
        elif trend == "downtrend":
            risk_factor -= 0.1
        
        # Adjust for volatility
        volatility = market_context.get("recent_volatility", 0.0)
        avg_price = market_context.get("price", 1.0)
        if volatility / avg_price > 0.02:  # High volatility
            risk_factor -= 0.1
        
        # Randomize slightly for more organic behavior
        risk_factor += self.random.uniform(-0.05, 0.05)
        
        # Constrain to valid range
        return max(0.1, min(0.9, risk_factor))
    
    def should_enter_market(self, 
                           market_context: Dict, 
                           trader_state: Dict,
                           risk_appetite: float = 0.5) -> Tuple[bool, str, float]:
        """
        Determine if a trade should be entered based on market conditions 
        and trader state.
        
        Returns:
            Tuple of (should_enter, direction, confidence)
        """
        # Extract key market information
        trend = market_context.get("trend", "sideways")
        price = market_context.get("price", 0.0)
        
        # Base probability on risk appetite
        base_probability = risk_appetite
        
        # Adjust for market trend
        if trend == "uptrend":
            direction = "long"
            probability = base_probability + 0.2
        elif trend == "downtrend":
            direction = "short"
            probability = base_probability + 0.1
        else:
            # In sideways markets, slightly prefer the random direction
            direction = "long" if self.random.random() > 0.5 else "short"
            probability = base_probability - 0.1
        
        # Apply trader psychology
        emotional_state = trader_state.get("emotional_state", "neutral")
        if emotional_state == "greedy":
            probability += 0.15
        elif emotional_state == "fearful":
            probability -= 0.25
        
        # Constrain probability
        probability = max(0.1, min(0.9, probability))
        
        # Determine if we should enter
        should_enter = self.random.random() < probability
        
        return should_enter, direction, probability
    
    def safe_float_convert(self, value: Any, default: float = 0.0) -> float:
        """Safely convert a value to float with fallback default."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default 