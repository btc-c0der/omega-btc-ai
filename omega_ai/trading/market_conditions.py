#!/usr/bin/env python3
"""
OMEGA BTC AI - Dynamic Market Condition Analyzer
=============================================

This module provides real-time analysis of market conditions
to dynamically adjust Fibonacci trading parameters based on:
1. Market volatility
2. Trend strength
3. Volume profile

Features:
- Real-time volatility calculation
- Trend strength analysis
- Dynamic Fibonacci level adjustments
- Risk parameter adaptation
"""

import numpy as np
import logging
from enum import Enum
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VolatilityState(Enum):
    """Market volatility states"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EXTREME = "EXTREME"

class TrendState(Enum):
    """Market trend states"""
    STRONG_UPTREND = "STRONG_UPTREND"
    WEAK_UPTREND = "WEAK_UPTREND"
    SIDEWAYS = "SIDEWAYS"
    WEAK_DOWNTREND = "WEAK_DOWNTREND"
    STRONG_DOWNTREND = "STRONG_DOWNTREND"

@dataclass
class MarketState:
    """Current market state combining volatility and trend"""
    volatility: VolatilityState
    trend: TrendState
    timestamp: datetime
    confidence: float

class MarketConditionAnalyzer:
    """Analyzes market conditions and provides dynamic parameter adjustments."""
    
    # Volatility thresholds (based on standard deviation of returns)
    VOLATILITY_THRESHOLDS = {
        'low': 0.01,    # 1% daily volatility
        'medium': 0.02, # 2% daily volatility
        'high': 0.04,   # 4% daily volatility
        'extreme': 0.08 # 8% daily volatility
    }
    
    # Trend strength thresholds
    TREND_THRESHOLDS = {
        'strong': 0.7,  # Strong trend
        'weak': 0.3     # Weak trend
    }
    
    def __init__(self, 
                 symbol: str = "BTCUSDT",
                 timeframe: str = "1h",
                 lookback_periods: int = 20,
                 volatility_window: int = 14,
                 trend_window: int = 14):
        """Initialize the market condition analyzer."""
        self.symbol = symbol
        self.timeframe = timeframe
        self.lookback_periods = lookback_periods
        self.volatility_window = volatility_window
        self.trend_window = trend_window
        
        # Initialize state
        self.price_history: List[Dict] = []
        self._volatility: float = 0.0
        self._trend_strength: float = 0.0
        self._last_update: Optional[datetime] = None
        
        logger.info(f"Initialized market analyzer for {symbol}")
    
    def update_price_history(self, price_data: List[Dict]) -> None:
        """Update price history with new data."""
        try:
            # Sort by timestamp
            sorted_data = sorted(price_data, key=lambda x: x['timestamp'])
            
            # Update price history
            self.price_history = sorted_data[-self.lookback_periods:]
            
            # Update market metrics
            self._volatility = self.calculate_volatility()
            self._trend_strength = self.calculate_trend_strength()
            self._last_update = datetime.now(timezone.utc)
            
            logger.debug(f"Updated price history with {len(price_data)} points")
            
        except Exception as e:
            logger.error(f"Error updating price history: {str(e)}")
    
    def calculate_volatility(self) -> float:
        """Calculate current market volatility."""
        try:
            if len(self.price_history) < 2:
                return 0.0
            
            # Calculate returns
            prices = np.array([p['price'] for p in self.price_history])
            returns = np.diff(np.log(prices))
            
            # Calculate volatility (standard deviation of returns)
            volatility = np.std(returns)
            
            logger.debug(f"Calculated volatility: {volatility:.4f}")
            return volatility
            
        except Exception as e:
            logger.error(f"Error calculating volatility: {str(e)}")
            return 0.0
    
    def calculate_trend_strength(self) -> float:
        """Calculate current trend strength [-1 to 1]."""
        try:
            if len(self.price_history) < self.trend_window:
                return 0.0
            
            # Get recent prices
            prices = np.array([p['price'] for p in self.price_history[-self.trend_window:]])
            
            # Calculate linear regression
            x = np.arange(len(prices))
            slope, _ = np.polyfit(x, prices, 1)
            
            # Normalize slope to [-1, 1]
            max_slope = np.max(np.abs(np.diff(prices)))
            trend_strength = np.clip(slope / max_slope if max_slope > 0 else 0, -1, 1)
            
            logger.debug(f"Calculated trend strength: {trend_strength:.4f}")
            return trend_strength
            
        except Exception as e:
            logger.error(f"Error calculating trend strength: {str(e)}")
            return 0.0
    
    def get_market_state(self) -> MarketState:
        """Get current market state classification."""
        try:
            # Classify volatility
            if self._volatility >= self.VOLATILITY_THRESHOLDS['extreme']:
                vol_state = VolatilityState.EXTREME
            elif self._volatility >= self.VOLATILITY_THRESHOLDS['high']:
                vol_state = VolatilityState.HIGH
            elif self._volatility >= self.VOLATILITY_THRESHOLDS['medium']:
                vol_state = VolatilityState.MEDIUM
            else:
                vol_state = VolatilityState.LOW
            
            # Classify trend
            if self._trend_strength >= self.TREND_THRESHOLDS['strong']:
                trend_state = TrendState.STRONG_UPTREND
            elif self._trend_strength >= self.TREND_THRESHOLDS['weak']:
                trend_state = TrendState.WEAK_UPTREND
            elif self._trend_strength <= -self.TREND_THRESHOLDS['strong']:
                trend_state = TrendState.STRONG_DOWNTREND
            elif self._trend_strength <= -self.TREND_THRESHOLDS['weak']:
                trend_state = TrendState.WEAK_DOWNTREND
            else:
                trend_state = TrendState.SIDEWAYS
            
            # Calculate confidence based on data quality
            confidence = min(1.0, len(self.price_history) / self.lookback_periods)
            
            return MarketState(
                volatility=vol_state,
                trend=trend_state,
                timestamp=datetime.now(timezone.utc),
                confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"Error getting market state: {str(e)}")
            return MarketState(
                volatility=VolatilityState.MEDIUM,
                trend=TrendState.SIDEWAYS,
                timestamp=datetime.now(timezone.utc),
                confidence=0.0
            )
    
    def get_fibonacci_adjustments(self) -> Dict[str, float]:
        """Get Fibonacci level adjustments based on market conditions."""
        try:
            state = self.get_market_state()
            
            # Base multipliers
            adjustments = {
                'extension_multiplier': 1.0,
                'retracement_multiplier': 1.0
            }
            
            # Adjust for volatility
            if state.volatility == VolatilityState.HIGH:
                adjustments['extension_multiplier'] *= 1.2
                adjustments['retracement_multiplier'] *= 1.2
            elif state.volatility == VolatilityState.EXTREME:
                adjustments['extension_multiplier'] *= 1.5
                adjustments['retracement_multiplier'] *= 1.5
            
            # Adjust for trend strength
            if state.trend in [TrendState.STRONG_UPTREND, TrendState.STRONG_DOWNTREND]:
                adjustments['extension_multiplier'] *= 1.1
                adjustments['retracement_multiplier'] *= 0.9  # Tighter stops in strong trends
            
            logger.debug(f"Fibonacci adjustments: {adjustments}")
            return adjustments
            
        except Exception as e:
            logger.error(f"Error calculating Fibonacci adjustments: {str(e)}")
            return {'extension_multiplier': 1.0, 'retracement_multiplier': 1.0}
    
    def get_risk_adjustments(self, base_risk_percent: float) -> Dict[str, float]:
        """Get risk parameter adjustments based on market conditions."""
        try:
            state = self.get_market_state()
            
            # Initialize adjustments
            adjustments = {
                'risk_percent': base_risk_percent,
                'position_size_multiplier': 1.0
            }
            
            # Adjust for volatility
            if state.volatility == VolatilityState.HIGH:
                adjustments['risk_percent'] *= 0.8
                adjustments['position_size_multiplier'] *= 0.8
            elif state.volatility == VolatilityState.EXTREME:
                adjustments['risk_percent'] *= 0.5
                adjustments['position_size_multiplier'] *= 0.5
            
            # Adjust for trend strength
            if state.trend in [TrendState.STRONG_UPTREND, TrendState.STRONG_DOWNTREND]:
                adjustments['risk_percent'] *= 1.2
                adjustments['position_size_multiplier'] *= 1.2
            
            logger.debug(f"Risk adjustments: {adjustments}")
            return adjustments
            
        except Exception as e:
            logger.error(f"Error calculating risk adjustments: {str(e)}")
            return {'risk_percent': base_risk_percent, 'position_size_multiplier': 1.0}
    
    def get_market_adjustments(self, base_risk_percent: float = 1.0) -> Dict[str, Any]:
        """Get comprehensive market condition adjustments."""
        try:
            state = self.get_market_state()
            
            return {
                'market_state': state,
                'fibonacci_adjustments': self.get_fibonacci_adjustments(),
                'risk_adjustments': self.get_risk_adjustments(base_risk_percent)
            }
            
        except Exception as e:
            logger.error(f"Error getting market adjustments: {str(e)}")
            return {
                'market_state': self.get_market_state(),
                'fibonacci_adjustments': {'extension_multiplier': 1.0, 'retracement_multiplier': 1.0},
                'risk_adjustments': {'risk_percent': base_risk_percent, 'position_size_multiplier': 1.0}
            }
    
    async def update_market_conditions(self, current_price: float) -> None:
        """Update market conditions with new price data."""
        try:
            # Create price point
            price_point = {
                'timestamp': int(datetime.now(timezone.utc).timestamp() * 1000),
                'price': current_price,
                'volume': 0.0  # No volume data for single price updates
            }
            
            # Update price history
            self.price_history.append(price_point)
            if len(self.price_history) > self.lookback_periods:
                self.price_history = self.price_history[-self.lookback_periods:]
            
            # Update metrics
            self._volatility = self.calculate_volatility()
            self._trend_strength = self.calculate_trend_strength()
            self._last_update = datetime.now(timezone.utc)
            
            logger.debug(f"Updated market conditions with price: {current_price}")
            
        except Exception as e:
            logger.error(f"Error updating market conditions: {str(e)}") 