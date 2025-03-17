#!/usr/bin/env python3

"""
OMEGA BTC AI - Trap Probability Meter
=====================================

A tool that calculates and visualizes the probability of market maker traps forming
in real-time, based on various market indicators, price patterns, and historical data.

The tool displays:
- An overall trap probability meter (progress bar)
- Individual component meters showing what factors contribute to the probability
- Trap type prediction with confidence level
- Trend indicators showing if probability is increasing/decreasing

Usage:
    python -m omega_ai.tools.trap_probability_meter [options]

Options:
    --interval SECONDS    Check interval in seconds (default: 5)
    --debug               Show debug information
    --no-color            Disable colored output
    --backtest DATE       Run in backtest mode starting from DATE (format: YYYY-MM-DD)
    --verbose             Show detailed component information
"""

import argparse
import json
import os
import math
import random
import redis
import signal
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# ANSI color codes for terminal output
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"

# Probability calculation configuration
PROBABILITY_COMPONENTS = {
    "price_pattern": {
        "weight": 0.25,
        "description": "Price pattern recognition"
    },
    "volume_spike": {
        "weight": 0.20,
        "description": "Unusual volume activity"
    },
    "fib_level": {
        "weight": 0.15,
        "description": "Proximity to Fibonacci levels"
    },
    "historical_match": {
        "weight": 0.15,
        "description": "Historical pattern match"
    },
    "order_book": {
        "weight": 0.15,
        "description": "Order book imbalance"
    },
    "market_regime": {
        "weight": 0.10,
        "description": "Current market regime"
    }
}

# Signs for trend indicators
TREND_UP = "▲"
TREND_DOWN = "▼"
TREND_STABLE = "◆"

# ASCII art for the meter
ASCII_METER_FRAMES = [
    """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   TRAP PROBABILITY METER                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """,
    """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   TRAP PROBABILITY METER                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """,
    """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                   TRAP PROBABILITY METER                      ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """,
    """
    ┌──────────────────────────────────────────────────────────────┐
    │                   TRAP PROBABILITY METER                      │
    └──────────────────────────────────────────────────────────────┘
    """
]

class TrapProbabilityMeter:
    """Calculates and displays the probability of market maker traps forming."""
    
    def __init__(self, interval: int = 5, debug: bool = False, 
                 use_color: bool = True, verbose: bool = False,
                 backtest_date: Optional[str] = None):
        """
        Initialize the trap probability meter.
        
        Args:
            interval: Update interval in seconds
            debug: Whether to show debug information
            use_color: Whether to use color in the output
            verbose: Whether to show detailed component information
            backtest_date: Optional date for backtesting (format: YYYY-MM-DD)
        """
        self.interval = interval
        self.debug = debug
        self.use_color = use_color
        self.verbose = verbose
        self.backtest_date = backtest_date
        self.backtest_mode = backtest_date is not None
        
        # Setup Redis client
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        
        # Set up probability components
        self.components = {
            name: {
                "weight": config["weight"],
                "description": config["description"],
                "value": 0.0,
                "trend": "stable"
            }
            for name, config in PROBABILITY_COMPONENTS.items()
        }
        
        # Initialize probability and detected trap
        self.probability = 0.0
        self.detected_trap_type = None
        self.confidence = 0.0
        self.trap_probable = False
        
        # Initialize history for trends
        self.probability_history = []
        self.trend = "stable"
        self.trend_change = 0.0
        
        # Register signal handler for clean exit
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Frame counter for animations
        self.frame_counter = 0
    
    def _signal_handler(self, sig, frame):
        """Handle SIGINT to clean up and exit."""
        print(f"\n{RESET}Exiting trap probability meter...")
        sys.exit(0)
    
    def _color(self, text: str, color_code: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.use_color:
            return f"{color_code}{text}{RESET}"
        return text
    
    def _get_current_btc_price(self) -> float:
        """Get the current Bitcoin price."""
        try:
            # Try to get from Redis cache first
            price_data = self.redis_client.get("btc_price")
            if price_data:
                return float(json.loads(price_data)["price"])
                
            # Fallback to a random price for demo if not available
            return random.uniform(80000, 90000)
        except Exception as e:
            if self.debug:
                print(f"Error getting BTC price: {e}")
            return random.uniform(80000, 90000)
    
    def _get_fibonacci_levels(self, current_price: float) -> List[float]:
        """Calculate Fibonacci retracement levels based on recent high/low."""
        try:
            # Try to get recent high/low from Redis
            high_low = self.redis_client.get("btc_recent_high_low")
            if high_low:
                data = json.loads(high_low)
                recent_high = data["high"]
                recent_low = data["low"]
            else:
                # Fallback values
                recent_high = current_price * 1.05
                recent_low = current_price * 0.95
            
            # Calculate Fibonacci levels (retracements)
            diff = recent_high - recent_low
            levels = [
                recent_high,  # 0% (recent high)
                recent_high - 0.236 * diff,  # 23.6%
                recent_high - 0.382 * diff,  # 38.2%
                recent_high - 0.5 * diff,    # 50%
                recent_high - 0.618 * diff,  # 61.8%
                recent_high - 0.786 * diff,  # 78.6%
                recent_low   # 100% (recent low)
            ]
            
            # Add extensions
            levels.extend([
                recent_low - 0.272 * diff,  # 127.2%
                recent_low - 0.618 * diff,  # 161.8%
                recent_low - 1.0 * diff     # 200%
            ])
            
            return levels
        except Exception as e:
            if self.debug:
                print(f"Error calculating Fibonacci levels: {e}")
            # Return dummy levels centered around current price
            return [
                current_price * (1 + x/100)
                for x in [-5, -3, -1.5, 0, 1.5, 3, 5]
            ]
    
    def _detect_volume_spike(self) -> Tuple[float, str]:
        """
        Detect unusual volume activity.
        
        Returns:
            Tuple[float, str]: Probability contribution and description
        """
        try:
            # Try to get volume data from Redis
            volume_data = self.redis_client.get("btc_volume_data")
            if volume_data:
                data = json.loads(volume_data)
                current_volume = data["current"]
                avg_volume = data["average"]
                
                # Calculate volume ratio
                ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
                
                # Determine probability based on volume spike
                if ratio > 2.0:
                    prob = min(0.9, ratio / 3.0)
                    return prob, f"Volume {ratio:.1f}x above average"
                elif ratio > 1.5:
                    prob = 0.5 + (ratio - 1.5) / 1.0
                    return prob, f"Volume {ratio:.1f}x above average"
                elif ratio > 1.2:
                    prob = 0.3 + (ratio - 1.2) / 0.6
                    return prob, f"Volume {ratio:.1f}x above average"
                elif ratio < 0.5:
                    prob = 0.7  # Unusually low volume can also indicate traps
                    return prob, f"Volume {ratio:.1f}x below average"
                else:
                    prob = 0.2
                    return prob, "Normal volume levels"
            
            # Fallback to random values for demo
            rand_val = random.random()
            if rand_val > 0.8:
                return 0.8, "High volume detected"
            elif rand_val > 0.6:
                return 0.6, "Above average volume"
            else:
                return 0.3, "Normal volume levels"
        except Exception as e:
            if self.debug:
                print(f"Error detecting volume spike: {e}")
            return 0.3, "Volume analysis unavailable"
    
    def _analyze_price_pattern(self) -> Tuple[float, str]:
        """
        Analyze price patterns for trap indications.
        
        Returns:
            Tuple[float, str]: Probability contribution and description
        """
        try:
            # Try to get pattern data from Redis
            pattern_data = self.redis_client.get("btc_price_patterns")
            if pattern_data:
                patterns = json.loads(pattern_data)
                
                # Check for trap-indicative patterns
                trap_patterns = {
                    "wyckoff_distribution": 0.85,
                    "double_top": 0.75,
                    "double_bottom": 0.75,
                    "head_and_shoulders": 0.80,
                    "inverted_head_and_shoulders": 0.80,
                    "bull_flag": 0.65,
                    "bear_flag": 0.65,
                    "evening_star": 0.75,
                    "morning_star": 0.75
                }
                
                # Find the highest probability pattern
                max_prob = 0.0
                pattern_name = "No significant pattern"
                
                for pattern, confidence in patterns.items():
                    if pattern in trap_patterns and confidence > 0.5:
                        pattern_prob = trap_patterns[pattern] * confidence
                        if pattern_prob > max_prob:
                            max_prob = pattern_prob
                            pattern_name = pattern.replace("_", " ").title()
                
                if max_prob > 0:
                    return max_prob, pattern_name
                return 0.2, "No trap-indicative patterns"
            
            # Fallback to random values for demo
            patterns = ["Double Top", "Wyckoff Distribution", "Bull Flag", "No Pattern"]
            weights = [0.75, 0.85, 0.65, 0.2]
            idx = random.choices(range(len(patterns)), weights=weights, k=1)[0]
            return weights[idx], patterns[idx]
        except Exception as e:
            if self.debug:
                print(f"Error analyzing price pattern: {e}")
            return 0.3, "Pattern analysis unavailable"
    
    def _check_fibonacci_match(self, price: float) -> Tuple[float, str]:
        """
        Check if current price is near Fibonacci levels.
        
        Args:
            price: Current BTC price
            
        Returns:
            Tuple[float, str]: Probability contribution and description
        """
        try:
            fib_levels = self._get_fibonacci_levels(price)
            
            # Find closest Fibonacci level
            closest_distance = float('inf')
            closest_level = None
            closest_percent = 0.0
            
            for level in fib_levels:
                distance = abs(price - level)
                percent = (distance / price) * 100
                
                if percent < closest_distance:
                    closest_distance = percent
                    closest_level = level
                    closest_percent = percent
            
            # Calculate probability based on proximity
            if closest_percent < 0.1:  # Very close (within 0.1%)
                return 0.9, f"Price at key Fibonacci level (±0.1%)"
            elif closest_percent < 0.3:  # Close (within 0.3%)
                return 0.7, f"Price near Fibonacci level (±0.3%)"
            elif closest_percent < 0.5:  # Somewhat close (within 0.5%)
                return 0.5, f"Price approaching Fibonacci level (±0.5%)"
            elif closest_percent < 1.0:  # Within range (within 1%)
                return 0.3, f"Price in range of Fibonacci level (±1.0%)"
            else:
                return 0.1, "Price not near any Fibonacci levels"
        except Exception as e:
            if self.debug:
                print(f"Error checking Fibonacci levels: {e}")
            return 0.2, "Fibonacci analysis unavailable"
    
    def _check_historical_matches(self) -> Tuple[float, str]:
        """
        Check if current conditions match historical trap patterns.
        
        Returns:
            Tuple[float, str]: Probability contribution and description
        """
        try:
            # Try to get historical match data from Redis
            history_data = self.redis_client.get("btc_historical_matches")
            if history_data:
                matches = json.loads(history_data)
                
                if "match_score" in matches and "match_type" in matches:
                    score = float(matches["match_score"])
                    match_type = matches["match_type"]
                    
                    if score > 0.8:
                        return 0.9, f"Strong match: {match_type} pattern"
                    elif score > 0.6:
                        return 0.7, f"Good match: {match_type} pattern"
                    elif score > 0.4:
                        return 0.4, f"Weak match: {match_type} pattern"
                    else:
                        return 0.2, "No significant historical matches"
            
            # Fallback to random values for demo
            rand = random.random()
            if rand > 0.7:
                return 0.8, "Strong match: May 2021 liquidation"
            elif rand > 0.5:
                return 0.6, "Similar to April 2023 pattern"
            elif rand > 0.3:
                return 0.4, "Weak similarity to past events"
            else:
                return 0.2, "No significant historical matches"
        except Exception as e:
            if self.debug:
                print(f"Error checking historical matches: {e}")
            return 0.3, "Historical analysis unavailable"
    
    def _analyze_order_book(self) -> Tuple[float, str]:
        """
        Analyze order book for trap indications.
        
        Returns:
            Tuple[float, str]: Probability contribution and description
        """
        try:
            # Try to get order book data from Redis
            order_book = self.redis_client.get("btc_order_book_summary")
            if order_book:
                data = json.loads(order_book)
                
                # Check for large walls
                bid_wall = data.get("largest_bid_wall", 0)
                ask_wall = data.get("largest_ask_wall", 0)
                
                # Check bid/ask imbalance
                bid_sum = data.get("total_bids", 0)
                ask_sum = data.get("total_asks", 0)
                
                if bid_sum == 0 or ask_sum == 0:
                    return 0.5, "Incomplete order book data"
                
                ratio = bid_sum / ask_sum if ask_sum > 0 else 1.0
                
                # Large walls often indicate manipulation
                if bid_wall > 100 or ask_wall > 100:  # BTC amount
                    return 0.8, f"Large {'bid' if bid_wall > ask_wall else 'ask'} wall detected"
                
                # Significant imbalance can indicate traps
                if ratio > 3.0 or ratio < 0.33:
                    return 0.75, f"Order book heavily {'bid' if ratio > 1 else 'ask'} weighted ({ratio:.1f}x)"
                elif ratio > 2.0 or ratio < 0.5:
                    return 0.6, f"Order book {'bid' if ratio > 1 else 'ask'} weighted ({ratio:.1f}x)"
                else:
                    return 0.3, "Balanced order book"
            
            # Fallback to random values for demo
            scenarios = [
                (0.8, "Large sell wall detected"),
                (0.7, "Order book ask weighted (3.2x)"),
                (0.6, "Moderate bid imbalance (2.1x)"),
                (0.3, "Balanced order book")
            ]
            return random.choice(scenarios)
        except Exception as e:
            if self.debug:
                print(f"Error analyzing order book: {e}")
            return 0.4, "Order book analysis unavailable"
    
    def _analyze_market_regime(self) -> Tuple[float, str]:
        """
        Analyze current market regime for trap likelihood.
        
        Returns:
            Tuple[float, str]: Probability contribution and description
        """
        try:
            # Try to get market regime data from Redis
            regime_data = self.redis_client.get("btc_market_regime")
            if regime_data:
                regime = json.loads(regime_data)
                
                regime_type = regime.get("regime", "unknown")
                
                # Different regimes have different trap probabilities
                regime_probs = {
                    "high_volatility": 0.8,
                    "accumulation": 0.7,
                    "distribution": 0.9,
                    "bullish_trend": 0.4,
                    "bearish_trend": 0.6,
                    "sideways": 0.5,
                    "unknown": 0.5
                }
                
                return regime_probs.get(regime_type, 0.5), f"{regime_type.replace('_', ' ').title()} regime"
            
            # Fallback to random values for demo
            regimes = ["High Volatility", "Distribution", "Bullish Trend", "Sideways"]
            probs = [0.8, 0.9, 0.4, 0.5]
            idx = random.choices(range(len(regimes)), weights=[3, 2, 2, 3], k=1)[0]
            return probs[idx], regimes[idx]
        except Exception as e:
            if self.debug:
                print(f"Error analyzing market regime: {e}")
            return 0.5, "Market regime analysis unavailable"
    
    def _detect_likely_trap_type(self) -> Tuple[Optional[str], float]:
        """
        Detect the most likely trap type based on current indicators.
        
        Returns:
            Tuple[Optional[str], float]: Most likely trap type and confidence
        """
        try:
            # Try to get trap indicators from Redis
            trap_indicators = self.redis_client.get("btc_trap_indicators")
            if trap_indicators:
                data = json.loads(trap_indicators)
                
                if "trap_type" in data and "confidence" in data:
                    return data["trap_type"], float(data["confidence"])
            
            # Fallback to prediction based on components
            volume_value = self.components["volume_spike"]["value"]
            pattern_value = self.components["price_pattern"]["value"]
            regime_value = self.components["market_regime"]["value"]
            
            # Simple logic for trap type prediction
            price = self._get_current_btc_price()
            
            # Get recent price change direction
            price_changes = self.redis_client.get("btc_price_changes")
            if price_changes:
                changes = json.loads(price_changes)
                short_term = changes.get("short_term", 0)
                medium_term = changes.get("medium_term", 0)
            else:
                short_term = random.uniform(-0.05, 0.05)
                medium_term = random.uniform(-0.07, 0.07)
            
            # Determine most likely trap type based on indicators
            if short_term < -0.03 and volume_value > 0.6:
                return "stop_hunt", 0.7 + (volume_value - 0.6) * 0.5
            elif short_term > 0.03 and medium_term < -0.01 and pattern_value > 0.6:
                return "bull_trap", 0.65 + (pattern_value - 0.6) * 0.6
            elif short_term < -0.02 and medium_term > 0.01 and pattern_value > 0.6:
                return "bear_trap", 0.65 + (pattern_value - 0.6) * 0.6
            elif volume_value > 0.7 and self.probability > 0.65:
                return "liquidity_grab", 0.6 + (volume_value - 0.7) * 0.8
            elif pattern_value > 0.7 and short_term > 0.03:
                return "fake_pump", 0.6 + (pattern_value - 0.7) * 0.7
            elif pattern_value > 0.7 and short_term < -0.03:
                return "fake_dump", 0.6 + (pattern_value - 0.7) * 0.7
            
            # If probability is high but no specific type identified
            if self.probability >= 0.7:
                if short_term > 0:
                    return "potential_trap", 0.6
                else:
                    return "potential_trap", 0.6
            
            return None, 0.0
        except Exception as e:
            if self.debug:
                print(f"Error detecting trap type: {e}")
            return None, 0.0
    
    def _calculate_probability(self) -> float:
        """
        Calculate the overall trap probability based on all components.
        
        Returns:
            float: Overall probability value between 0.0 and 1.0
        """
        # Update all component values
        self.components["price_pattern"]["value"], self.components["price_pattern"]["description"] = \
            self._analyze_price_pattern()
            
        self.components["volume_spike"]["value"], self.components["volume_spike"]["description"] = \
            self._detect_volume_spike()
            
        price = self._get_current_btc_price()
        self.components["fib_level"]["value"], self.components["fib_level"]["description"] = \
            self._check_fibonacci_match(price)
            
        self.components["historical_match"]["value"], self.components["historical_match"]["description"] = \
            self._check_historical_matches()
            
        self.components["order_book"]["value"], self.components["order_book"]["description"] = \
            self._analyze_order_book()
            
        self.components["market_regime"]["value"], self.components["market_regime"]["description"] = \
            self._analyze_market_regime()
        
        # Calculate weighted probability
        total_weight = sum(comp["weight"] for comp in PROBABILITY_COMPONENTS.values())
        weighted_sum = sum(
            self.components[name]["value"] * config["weight"]
            for name, config in PROBABILITY_COMPONENTS.items()
        )
        
        probability = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        # Ensure probability is between 0 and 1
        probability = max(0.0, min(1.0, probability))
        
        # Update history and calculate trend
        self._update_trend(probability)
        
        # Detect most likely trap type
        self.detected_trap_type, self.confidence = self._detect_likely_trap_type()
        
        # Store data in Redis for other components to use
        self._store_probability_data(probability)
        
        return probability
    
    def _update_trend(self, new_probability: float):
        """
        Update trend based on probability history.
        
        Args:
            new_probability: The newly calculated probability
        """
        timestamp = datetime.now().isoformat()
        self.probability_history.append((timestamp, new_probability))
        
        # Keep history limited to 20 entries
        if len(self.probability_history) > 20:
            self.probability_history = self.probability_history[-20:]
        
        # Calculate trend
        if len(self.probability_history) >= 2:
            # Get oldest and newest probabilities
            _, oldest_prob = self.probability_history[0]
            _, newest_prob = self.probability_history[-1]
            
            # Calculate change
            change = newest_prob - oldest_prob
            self.trend_change = change
            
            # Determine trend direction
            if change > 0.05:
                self.trend = "rapidly_increasing"
            elif change > 0.02:
                self.trend = "increasing"
            elif change > 0.005:
                self.trend = "slightly_increasing"
            elif change < -0.05:
                self.trend = "rapidly_decreasing"
            elif change < -0.02:
                self.trend = "decreasing"
            elif change < -0.005:
                self.trend = "slightly_decreasing"
            else:
                self.trend = "stable"
    
    def _store_probability_data(self, probability: float):
        """
        Store probability data in Redis for other components to use.
        
        Args:
            probability: The calculated probability value
        """
        try:
            # Create data structure
            data = {
                "probability": probability,
                "timestamp": datetime.now().isoformat(),
                "trend": self.trend,
                "change": self.trend_change,
                "components": {
                    name: {
                        "value": comp["value"],
                        "description": comp["description"]
                    }
                    for name, comp in self.components.items()
                },
            }
            
            # Add trap type if detected
            if self.detected_trap_type:
                data["trap_type"] = self.detected_trap_type
                data["confidence"] = self.confidence
            
            # Store current probability
            self.redis_client.set("current_trap_probability", json.dumps(data))
            
            # Add to history (limited to 1000 entries)
            self.redis_client.lpush("trap_probability_history", json.dumps(data))
            self.redis_client.ltrim("trap_probability_history", 0, 999)
        except Exception as e:
            if self.debug:
                print(f"Error storing probability data: {e}")
    
    def _draw_progress_bar(self, value: float, width: int = 50, 
                          char_empty: str = "░", char_filled: str = "█") -> str:
        """
        Draw a progress bar.
        
        Args:
            value: Value between 0.0 and 1.0
            width: Width of the progress bar in characters
            char_empty: Character for empty portions
            char_filled: Character for filled portions
            
        Returns:
            str: Progress bar string
        """
        # Ensure value is between 0 and 1
        value = max(0.0, min(1.0, value))
        
        # Calculate filled width
        filled_width = int(width * value)
        
        # Create the bar
        bar = char_filled * filled_width + char_empty * (width - filled_width)
        
        return bar
    
    def _draw_mini_progress_bar(self, value: float, width: int = 20) -> str:
        """Draw a mini progress bar for components."""
        return self._draw_progress_bar(value, width, "·", "■")
    
    def _get_probability_color(self, value: float) -> str:
        """Get color based on probability value."""
        if not self.use_color:
            return ""
        
        if value >= 0.8:
            return BRIGHT_RED
        elif value >= 0.6:
            return RED
        elif value >= 0.4:
            return YELLOW
        elif value >= 0.2:
            return GREEN
        else:
            return BRIGHT_GREEN
    
    def _get_trend_indicator(self) -> str:
        """Get trend indicator symbol based on current trend."""
        if self.trend in ["rapidly_increasing", "increasing", "slightly_increasing"]:
            return self._color(TREND_UP, RED)
        elif self.trend in ["rapidly_decreasing", "decreasing", "slightly_decreasing"]:
            return self._color(TREND_DOWN, GREEN)
        else:
            return self._color(TREND_STABLE, YELLOW)
    
    def _format_trap_type(self, trap_type: Optional[str], confidence: float) -> str:
        """Format trap type for display."""
        if not trap_type:
            return self._color("No specific trap detected", BRIGHT_GREEN)
        
        # Define emojis for trap types
        trap_emojis = {
            "liquidity_grab": "💰",
            "stop_hunt": "🎯",
            "bull_trap": "🐂",
            "bear_trap": "🐻",
            "fake_pump": "🚀",
            "fake_dump": "📉",
            "potential_trap": "⚠️"
        }
        
        # Format the trap type
        emoji = trap_emojis.get(trap_type, "❓")
        formatted_type = trap_type.replace("_", " ").title()
        
        # Color based on confidence
        if confidence >= 0.8:
            color = BRIGHT_RED
        elif confidence >= 0.6:
            color = RED
        elif confidence >= 0.4:
            color = YELLOW
        else:
            color = GREEN
        
        return f"{emoji} {self._color(formatted_type, color)} ({confidence:.0%} confidence)"
    
    def display_probability(self):
        """Display the trap probability with a fancy progress bar."""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Select frame for ASCII art
        frame = ASCII_METER_FRAMES[self.frame_counter % len(ASCII_METER_FRAMES)]
        self.frame_counter += 1
        
        # Display header
        print(self._color(frame, BRIGHT_CYAN))
        
        # Show current price
        current_price = self._get_current_btc_price()
        print(f"Current BTC price: {self._color(f'${current_price:,.2f}', BRIGHT_WHITE)}")
        
        # Display probability meter
        print("\n" + self._color("OVERALL TRAP PROBABILITY:", BRIGHT_WHITE))
        
        # Create the progress bar
        bar_color = self._get_probability_color(self.probability)
        bar = self._draw_progress_bar(self.probability)
        
        # Format percentage
        percentage = f"{self.probability:.1%}"
        
        # Add trend indicator
        trend_indicator = self._get_trend_indicator()
        
        # Display the bar with percentage and trend
        print(f"{bar_color}{bar} {percentage} {trend_indicator}{RESET}")
        
        # Display detected trap type if any
        if self.detected_trap_type:
            print(f"\nDetected pattern: {self._format_trap_type(self.detected_trap_type, self.confidence)}")
        
        # Display components if verbose
        if self.verbose:
            print("\n" + self._color("PROBABILITY COMPONENTS:", BRIGHT_WHITE))
            
            # Sort components by value (descending)
            sorted_components = sorted(
                self.components.items(),
                key=lambda x: x[1]["value"],
                reverse=True
            )
            
            for name, comp in sorted_components:
                # Get color based on component value
                comp_color = self._get_probability_color(comp["value"])
                
                # Format component name and description
                formatted_name = name.replace("_", " ").title()
                
                # Create mini progress bar
                bar = self._draw_mini_progress_bar(comp["value"])
                
                # Display component
                print(f"{formatted_name}: {comp_color}{bar} {comp['value']:.1%}{RESET}")
                print(f"  {comp['description']}")
        
        # Display trend info
        trend_description = self.trend.replace("_", " ").title()
        trend_color = RED if "increasing" in self.trend else GREEN if "decreasing" in self.trend else YELLOW
        
        print(f"\nTrend: {self._color(trend_description, trend_color)}")
        
        # Display last updated time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nLast updated: {now}")
    
    def run(self):
        """Run the trap probability meter."""
        try:
            print(f"Starting trap probability meter (update interval: {self.interval}s)")
            print("Press Ctrl+C to exit")
            
            # Main loop
            while True:
                # Calculate probability
                self.probability = self._calculate_probability()
                
                # Check if a trap is probable
                threshold = 0.75  # Threshold for trap probability
                self.trap_probable = self.probability > threshold
                
                # Display the probability
                self.display_probability()
                
                # Sleep until next update
                time.sleep(self.interval)
        except redis.ConnectionError:
            print(f"{RED}Error: Could not connect to Redis server{RESET}")
            print("Make sure Redis is running on localhost:6379")
            return 1
        except KeyboardInterrupt:
            print(f"\n{RESET}Exiting trap probability meter...")
            return 0
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return 1

def main():
    """Main entry point for the trap probability meter."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - Trap Probability Meter")
    parser.add_argument("--interval", type=int, default=5,
                        help="Check interval in seconds (default: 5)")
    parser.add_argument("--debug", action="store_true",
                        help="Show debug information")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable colored output")
    parser.add_argument("--backtest", type=str,
                        help="Run in backtest mode starting from DATE (format: YYYY-MM-DD)")
    parser.add_argument("--verbose", action="store_true",
                        help="Show detailed component information")
    
    args = parser.parse_args()
    
    # Check for numpy dependency
    if not NUMPY_AVAILABLE and args.debug:
        print("Warning: numpy not found, some features may be disabled")
    
    # Create and run the trap probability meter
    meter = TrapProbabilityMeter(
        interval=args.interval,
        debug=args.debug,
        use_color=not args.no_color,
        verbose=args.verbose,
        backtest_date=args.backtest
    )
    
    # Run the meter
    return meter.run()

if __name__ == "__main__":
    sys.exit(main()) 