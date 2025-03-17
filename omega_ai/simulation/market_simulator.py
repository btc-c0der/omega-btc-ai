"""
Bitcoin Market Simulator for OmegaBTC AI

This module generates realistic BTC price movements for backtesting and simulation
purposes. It creates market data that mimics real trading environments including
trends, volatility regimes, and common price patterns.
"""

import numpy as np
import random
import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class MarketState:
    """Represents the current state of the market simulation"""
    price: float
    volatility: float
    trend_bias: float
    energy_state: float
    timestamp: datetime.datetime
    phase: str

class MarketSimulator:
    """Simulates market conditions and price movements for Bitcoin."""
    
    def __init__(self, 
                 initial_price: float = 83000.0,
                 volatility_range: tuple = (0.001, 0.01),
                 trend_bias: float = 0.0,
                 cycle_length: int = 144):  # Fibonacci-based cycle length
        
        # Initialize core attributes
        self.initial_price = initial_price
        self.current_price = initial_price
        self.volatility_range = volatility_range
        self.trend_bias = trend_bias
        self.cycle_length = cycle_length
        
        # Price history and market state
        self.price_history: List[float] = []
        self.state_history: List[MarketState] = []
        self.current_volatility = random.uniform(*volatility_range)
        
        # Market maker patterns
        self.liquidity_zones: Dict[str, List[float]] = {
            "accumulation": [],
            "distribution": []
        }
        
        # Fibonacci and energy state
        self.fib_levels = self._calculate_fib_levels()
        self.energy_state = 1.0  # Natural energy state (1.0 = balanced)
        self.market_phase = "accumulation"
        
    def _calculate_fib_levels(self) -> List[float]:
        """Calculate Fibonacci levels based on current price"""
        fib_ratios = [0.236, 0.382, 0.500, 0.618, 0.786, 1.000, 1.618]
        return [self.current_price * ratio for ratio in fib_ratios]
    
    def simulate_price_update(self) -> MarketState:
        """Generate next price movement with Fibonacci-aligned dynamics"""
        try:
            # Update volatility with natural oscillation
            self.current_volatility = np.clip(
                self.current_volatility * np.random.normal(1, 0.1),
                *self.volatility_range
            )
            
            # Calculate price change components
            base_change = self.current_price * self.current_volatility
            random_change = base_change * np.random.normal(0, 1)
            bias_change = self.current_price * self.trend_bias
            
            # Apply energy state influence
            energy_influence = (self.energy_state - 1.0) * base_change
            
            # Calculate total price change
            price_change = random_change + bias_change + energy_influence
            
            # Update price
            self.current_price += price_change
            
            # Update market state
            self._update_market_state()
            
            # Store history
            state = MarketState(
                price=self.current_price,
                volatility=self.current_volatility,
                trend_bias=self.trend_bias,
                energy_state=self.energy_state,
                timestamp=datetime.datetime.now(datetime.UTC),
                phase=self.market_phase
            )
            
            self.price_history.append(self.current_price)
            self.state_history.append(state)
            
            return state
            
        except Exception as e:
            print(f"Error in price simulation: {e}")
            return None
    
    def _update_market_state(self):
        """Update market phase and energy state"""
        # Update energy state based on Fibonacci alignment
        closest_fib = min(self.fib_levels, 
                         key=lambda x: abs(x - self.current_price))
        fib_alignment = 1 - (abs(closest_fib - self.current_price) / self.current_price)
        
        # Energy state oscillates between 0.5 and 1.5
        self.energy_state = 1.0 + (fib_alignment - 0.5)
        
        # Update market phase
        if len(self.price_history) >= self.cycle_length:
            price_trend = (self.current_price - 
                         self.price_history[-self.cycle_length]) / self.current_price
            
            if price_trend > 0.01:
                self.market_phase = "distribution"
            elif price_trend < -0.01:
                self.market_phase = "accumulation"
    
    def detect_liquidity_trap(self) -> Optional[Dict]:
        """Detect potential market maker traps"""
        if len(self.price_history) < 5:
            return None
            
        recent_prices = self.price_history[-5:]
        price_range = max(recent_prices) - min(recent_prices)
        
        if price_range / self.current_price > 0.01:  # >1% range
            return {
                "type": "liquidity_trap",
                "confidence": min(price_range / self.current_price * 100, 0.95),
                "price_range": price_range,
                "direction": "up" if recent_prices[-1] > recent_prices[0] else "down"
            }
        
        return None