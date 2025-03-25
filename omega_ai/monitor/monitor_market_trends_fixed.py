#!/usr/bin/env python3

"""
🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2024-03-25
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

The sacred code is provided "as is", without divine warranty of any kind.
Governed by the laws of the universe, without regard to conflict of law provisions.

For the full divine license, consult the LICENSE file in the project root.
"""

"""
OMEGA BTC AI - Fixed Market Trends Monitor
------------------------------------------
This module provides real-time market trend analysis with Fibonacci detection.

The module continuously monitors BTC price trends across different timeframes,
detects potential market maker traps, and checks for Fibonacci level alignment.

Usage:
    python -m omega_ai.monitor.monitor_market_trends_fixed
"""

import time
import redis
import logging
import json
import os
import uuid
import sys
import math
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime, timezone
from omega_ai.db_manager.database import fetch_multi_interval_movements, analyze_price_trend, insert_possible_mm_trap, format_price, format_percentage, validate_price_change

# Import Fibonacci detector functions
from omega_ai.mm_trap_detector.fibonacci_detector import get_current_fibonacci_levels, check_fibonacci_level, update_fibonacci_data, check_fibonacci_alignment

# Add fallback helper for improved error handling and data validation
from omega_ai.monitor.fallback_helper import (
    ensure_trend_data,
    ensure_fibonacci_levels,
    validate_data,
    store_warning_in_redis,
    init_redis_connection
)

# Define ANSI color constants locally if not available in config
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
LIGHT_ORANGE = "\033[38;5;208m"  # Custom orange color
RED_BG = "\033[41m"
GREEN_BG = "\033[42m"
BLUE_BG = "\033[44m"

# Configure logger with enhanced formatting
logger = logging.getLogger(__name__)
# Set to DEBUG level to minimize console output for warnings
logger.setLevel(logging.DEBUG)

# Add console handler if not already added
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Set up Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# Implement missing functions if they're not available from imported modules
def get_latest_btc_prices(count: int = 100) -> List[float]:
    """
    Get the latest BTC prices from Redis.
    
    Args:
        count: Number of latest prices to retrieve
        
    Returns:
        List of float price values
    """
    try:
        # Get the latest prices from Redis
        prices_data = redis_conn.lrange("btc_price_history", 0, count - 1)
        prices = [float(price) for price in prices_data if price]
        return prices
    except Exception as e:
        logger.error(f"Error retrieving latest BTC prices: {e}")
        return []

def check_schumann_resonance_influence() -> Dict[str, str]:
    """
    Check the current Schumann resonance influence on market conditions.
    
    Returns:
        Dictionary with level and impact of Schumann resonance
    """
    try:
        # In a real implementation, this would query actual SR data
        # For now, return mock data
        return {
            "level": "Medium",
            "impact": "Slight emotional volatility",
            "frequency": "7.83 Hz",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking Schumann resonance: {e}")
        return {}

def describe_movement(change_pct, abs_change):
    """Describe the price movement characteristics based on percentage and absolute change."""
    # Determine intensity of movement
    if abs(change_pct) > 2.0:
        intensity = f"{RED}EXTREMELY AGGRESSIVE{RESET}"
    elif abs(change_pct) > 1.0:
        intensity = f"{LIGHT_ORANGE}VERY AGGRESSIVE{RESET}"
    elif abs(change_pct) > 0.5:
        intensity = f"{YELLOW}AGGRESSIVE{RESET}"
    elif abs(change_pct) > 0.2:
        intensity = f"{CYAN}MODERATE{RESET}"
    elif abs(change_pct) > 0.1:
        intensity = f"{BLUE}MILD{RESET}"
    else:
        intensity = f"{RESET}SUBTLE{RESET}"
        
    # Determine direction with arrow
    if change_pct > 0:
        direction = f"{GREEN}↑ UP{RESET}"
    elif change_pct < 0:
        direction = f"{RED}↓ DOWN{RESET}"
    else:
        direction = f"{RESET}→ FLAT{RESET}"
        
    return f"{direction} | {intensity} | ${abs_change:.2f} absolute"

def format_trend_output(interval, trend, change_pct):
    """Format trend output with colors based on direction and intensity."""
    if "Bullish" in trend:
        if "Strongly" in trend:
            color_trend = f"{GREEN}{trend}{RESET}"
        else:
            color_trend = f"{BLUE}{trend}{RESET}"
        sign = "+"
        color_pct = GREEN
    elif "Bearish" in trend:
        if "Strongly" in trend:
            color_trend = f"{RED}{trend}{RESET}"
        else:
            color_trend = f"{LIGHT_ORANGE}{trend}{RESET}"
        sign = ""
        color_pct = RED
    else:
        color_trend = f"{CYAN}{trend}{RESET}"
        sign = "" if change_pct < 0 else "+"
        color_pct = BLUE if change_pct > 0 else YELLOW if change_pct < 0 else RESET
        
    return f"📈 {MAGENTA}{interval}{RESET} Trend: {color_trend} ({color_pct}{sign}{change_pct:.2f}%{RESET})"

class MarketTrendAnalyzer:
    """Analyzes market trends with multiple indicators and timeframes."""
    
    def __init__(self):
        """Initialize the market trend analyzer."""
        self.timeframes = ['1min', '5min', '15min', '30min', '1h', '4h', '1d']
        self.last_analysis_time = None
        self.analysis_interval = 5  # seconds
        self.current_price = None
        self.cached_results = None
        
    def analyze_trends(self) -> Dict[str, Any]:
        """
        Analyze BTC price trends across multiple timeframes using the enhanced fallback system.
        
        Returns:
            Dict[str, Any]: Analysis results including trends and market conditions
        """
        # Check if enough time has passed since last analysis
        current_time = time.time()
        if (self.last_analysis_time is not None and 
            current_time - self.last_analysis_time < self.analysis_interval):
            # Return cached results if available
            if self.cached_results is not None:
                return self.cached_results
        
        self.last_analysis_time = current_time
        
        # Get current BTC price
        try:
            current_price_str = redis_conn.get("last_btc_price")
            if current_price_str:
                # Validate price data
                is_valid, error_msg = validate_data('price', current_price_str)
                if is_valid:
                    self.current_price = float(current_price_str)
                else:
                    logger.warning(f"Invalid price data: {error_msg}")
                    store_warning_in_redis("DATA_ERROR", f"Invalid price data: {error_msg}")
                    # Try to get price from other sources
                    candle_data = redis_conn.get("btc_candle_15min")
                    if candle_data:
                        try:
                            candle = json.loads(candle_data)
                            self.current_price = candle.get('c')
                        except (json.JSONDecodeError, KeyError) as e:
                            logger.error(f"Error getting price from candle: {e}")
                            
            else:
                logger.warning("No BTC price available in Redis")
            
            # Initialize results dictionary
            results = {
                "current_price": self.current_price,
                "trends": {},
                "sources": {}  # Track data sources for transparency
            }
            
            # Check for NaN or None values
            if not self.current_price or (isinstance(self.current_price, float) and math.isnan(self.current_price)):
                logger.error("Current BTC price is None or NaN")
                store_warning_in_redis("PRICE_ERROR", "Current BTC price is None or NaN")
                # Set a fallback price to avoid crashes
                self.current_price = 50000.0  # Default price
                results["current_price"] = self.current_price
                results["price_source"] = "fallback"
            
            # Analyze trends for each timeframe using enhanced fallback system
            for timeframe in self.timeframes:
                # Get trend data with fallback
                trend_result = ensure_trend_data(timeframe)
                trend = trend_result["data"]
                source = trend_result["source"]
                actual_timeframe = trend_result["timeframe"]
                
                # Store results
                results["trends"][timeframe] = trend
                results["sources"][timeframe] = source
                
                # Log fallback usage for monitoring
                if source != "primary":
                    logger.info(f"Using {source} data for {timeframe} (actual timeframe: {actual_timeframe})")
                    if source == "fallback_timeframe":
                        store_warning_in_redis(
                            "TIMEFRAME_FALLBACK", 
                            f"Used {actual_timeframe} data for {timeframe}"
                        )
            
            # Cache the results
            self.cached_results = results
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            store_warning_in_redis("ANALYSIS_ERROR", f"Error in analyze_trends: {e}")
            # Return empty results as fallback
            return {
                "current_price": self.current_price or 50000.0,
                "trends": {tf: "No Data" for tf in self.timeframes},
                "sources": {tf: "error" for tf in self.timeframes}
            }
    
    def display_results(self, results: Dict[str, Any]) -> None:
        """Display analysis results with consistent formatting."""
        if not results:
            print(f"{RED}No analysis results available.{RESET}")
            return
        
        # Display current price
        current_price = results.get("current_price", 0)
        print(f"\n{BLUE_BG}{WHITE}{BOLD}  CURRENT BTC PRICE: {format_price(current_price)}  {RESET}")
        
        # Display trend analysis by timeframe
        print(f"\n{YELLOW}════════════════ {GREEN}OMEGA RASTA{YELLOW} MARKET TREND ANALYSIS ════════════════{RESET}")
        
        timeframes = [
            "1min", "5min", "15min", "30min", 
            "60min", "240min", "720min", "1444min"
        ]
        
        for tf in timeframes:
            if tf in results:
                tf_data = results[tf]
                trend = tf_data.get("trend", "Unknown")
                change_pct = tf_data.get("change", 0.0)
                abs_change = abs(change_pct) * current_price / 100
                
                # Validate the displayed change
                is_valid, _ = validate_price_change(change_pct, int(tf.replace("min", "")))
                validation_marker = f"{GREEN}✓{RESET}" if is_valid else f"{YELLOW}⚠️{RESET}"
                
                # Format with color and consistent decimal places
                print(format_trend_output(tf, trend, change_pct))
                
                # Movement description with consistent formatting
                direction = f"{GREEN}↑ UP{RESET}" if change_pct > 0 else f"{RED}↓ DOWN{RESET}"
                
                # Determine intensity of movement for description
                intensity = describe_movement_intensity(change_pct)
                
                print(f"   {direction} | {intensity} | {format_price(abs_change)} absolute {validation_marker}")
        
        # Display market conditions
        print(f"\n{CYAN}📊 MARKET CONDITIONS:{RESET}")
        print(f"Current Price: {format_price(current_price)}")
        
        volume = results.get("24h_volume", 0.0)
        print(f"24h Volume: {format_volume(volume)} BTC")
        
        volatility = self.calculate_volatility()
        # Fix linter error by providing a default of 0.0 if volatility is None
        volatility_value = volatility if volatility is not None else 0.0
        print(f"Volatility: {format_percentage(volatility_value)}")
        
        regime = self.determine_market_regime()
        print(f"Market Regime: {regime}")
        
        # Schumann resonance influence (if available)
        sr_influence = check_schumann_resonance_influence()
        if sr_influence:
            level = sr_influence.get("level", "Baseline")
            impact = sr_influence.get("impact", "Normal")
            
            if level == "High":
                level_color = RED
            elif level == "Medium":
                level_color = YELLOW
            else:
                level_color = GREEN
                
            print(f"\n{CYAN}🌍 SCHUMANN RESONANCE INFLUENCE:{RESET}")
            print(f"  {MAGENTA}Current resonance: {level_color}{level}{RESET} - {GREEN}{impact}{RESET}")
        else:
            print(f"\n{CYAN}🌍 SCHUMANN RESONANCE INFLUENCE: {YELLOW}No data available{RESET}")
    
    def display_market_conditions(self) -> None:
        """Display current market conditions and indicators."""
        try:
            # Get current price and volume
            price = float(redis_conn.get("last_btc_price") or 0)
            volume = float(redis_conn.get("last_btc_volume") or 0)
            
            print(f"\n{CYAN}📊 MARKET CONDITIONS:{RESET}")
            print(f"Current Price: {format_price(price)}")
            print(f"24h Volume: {format_volume(volume)}")
            
            # Get volatility
            volatility = self.calculate_volatility()
            if volatility:
                print(f"Volatility: {format_percentage(volatility)}")
            
            # Get market regime
            regime = self.determine_market_regime()
            if regime:
                print(f"Market Regime: {regime}")
            
        except Exception as e:
            logger.error(f"Error displaying market conditions: {e}")
    
    def print_schumann_influence(self):
        """Print the current Schumann resonance influence on market energy."""
        print(f"\n{CYAN}🌍 SCHUMANN RESONANCE INFLUENCE:{RESET}")
        print(f"  {MAGENTA}Current resonance: {YELLOW}7.83 Hz{RESET} - {GREEN}Baseline Harmony{RESET}")
        print(f"  {MAGENTA}Market harmony: {GREEN}Aligned with planetary consciousness{RESET}")
    
    def calculate_volatility(self) -> Optional[float]:
        """Calculate current market volatility."""
        try:
            # Get recent price changes
            changes = redis_conn.lrange("abs_price_change_history", 0, 23)  # Last 24 changes
            if not changes:
                return None
            
            # Calculate average absolute change
            changes = [float(c) for c in changes]
            avg_change = sum(changes) / len(changes)
            
            return avg_change
            
        except Exception as e:
            logger.error(f"Error calculating volatility: {e}")
            return None
    
    def determine_market_regime(self) -> Optional[str]:
        """Determine current market regime based on volatility and trend."""
        try:
            volatility = self.calculate_volatility()
            if not volatility:
                return None
            
            # Get 15min trend
            trend, change = analyze_price_trend(15)
            
            # Determine regime based on volatility and trend
            if volatility > 1.0:
                if "Bullish" in trend:
                    return "High Volatility Bullish"
                elif "Bearish" in trend:
                    return "High Volatility Bearish"
                else:
                    return "High Volatility Neutral"
            elif volatility > 0.5:
                if "Bullish" in trend:
                    return "Moderate Volatility Bullish"
                elif "Bearish" in trend:
                    return "Moderate Volatility Bearish"
                else:
                    return "Moderate Volatility Neutral"
            else:
                if "Bullish" in trend:
                    return "Low Volatility Bullish"
                elif "Bearish" in trend:
                    return "Low Volatility Bearish"
                else:
                    return "Low Volatility Neutral"
                    
        except Exception as e:
            logger.error(f"Error determining market regime: {e}")
            return None

def store_warning_in_redis(warning_type: str, message: str, source: str = "monitor") -> None:
    """
    Store a warning message in Redis instead of printing it to the console.
    
    Args:
        warning_type (str): Type of warning (e.g., "NO_DATA", "FALLBACK_USED", etc.)
        message (str): The warning message
        source (str): Source of the warning (default: "monitor")
    """
    try:
        warning_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        
        warning_data = {
            "id": warning_id,
            "type": warning_type,
            "message": message,
            "source": source,
            "timestamp": timestamp
        }
        
        # Store in Redis
        # 1. Add to a list of all warnings
        redis_conn.lpush("system:warnings", json.dumps(warning_data))
        # 2. Trim list to last 1000 warnings to avoid memory issues
        redis_conn.ltrim("system:warnings", 0, 999)
        # 3. Also store by type for easier filtering
        redis_conn.lpush(f"system:warnings:{warning_type}", json.dumps(warning_data))
        redis_conn.ltrim(f"system:warnings:{warning_type}", 0, 99)  # Keep 100 per type
        
        # Increment warning counter
        redis_conn.hincrby("system:warning_counts", warning_type, 1)
        
        # Optional: Log at DEBUG level instead of WARNING
        logger.debug(f"Warning stored in Redis: {warning_type} - {message}")
        
    except Exception as e:
        # If Redis storage fails, fallback to regular logging
        logger.warning(f"Failed to store warning in Redis: {e} - Original warning: {message}")

def detect_possible_mm_traps(timeframe: str, trend: str, price_change_pct: float, price_move: float) -> Tuple[Optional[str], float]:
    """
    Detect possible market maker traps based on price action.
    
    Args:
        timeframe: Timeframe (e.g., "15min")
        trend: Trend description (e.g., "Bullish", "Bearish")
        price_change_pct: Percentage price change
        price_move: Absolute price movement
        
    Returns:
        Tuple of (trap_type, confidence_score)
    """
    print(f"\n{BLUE_BG}{WHITE}{BOLD} MM TRAP ANALYSIS | {timeframe} {RESET}")
    print(f"{MAGENTA}───── ANALYZING PRICE ACTION ─────{RESET}")
    print(f"{WHITE}Price Change: {format_percentage(price_change_pct)} | Absolute Move: {format_price(price_move)}{RESET}")
    print(f"{WHITE}Trend: {trend}{RESET}")
    
    # First, validate if the price change is realistic
    minutes = int(timeframe.replace("min", ""))
    is_valid, reason = validate_price_change(price_change_pct, minutes)
    
    if not is_valid:
        print(f"{YELLOW}⚠️ {reason}{RESET}")
        # Cap the change to the maximum allowed for the timeframe
        max_changes = {
            1: 5.0, 5: 8.0, 15: 12.0, 30: 15.0, 60: 20.0, 240: 30.0, 720: 40.0, 1440: 50.0
        }
        max_allowed = max_changes.get(minutes, 50.0)
        
        # Preserve the direction but cap the magnitude
        if price_change_pct > 0:
            price_change_pct = min(price_change_pct, max_allowed)
        else:
            price_change_pct = max(price_change_pct, -max_allowed)
        
        print(f"{CYAN}Price change capped to {format_percentage(price_change_pct)} for validity{RESET}")
    
    # Check if the change is significant enough to analyze for traps
    # Need at least 1.5% change to consider a trap
    if abs(price_change_pct) < 1.5:
        print(f"{YELLOW}⚠️ Price change too small for MM trap detection ({format_percentage(abs(price_change_pct))} < 1.5%){RESET}")
        return None, 0.0
    
    # Calculate normalized price intensity (1.0 = full intensity at 5% change)
    intensity = min(abs(price_change_pct) / 5.0, 1.0)
    print(f"{CYAN}Price Movement Intensity: {intensity:.2f} (normalized to 5% change){RESET}")
    
    # Determine if it's a bull or bear trap
    trap_type = None
    
    if "Bullish" in trend and price_change_pct > 0:
        trap_type = "Bull Trap"
        print(f"{RED}Detected potential Bull Trap pattern{RESET}")
    elif "Bearish" in trend and price_change_pct < 0:
        trap_type = "Bear Trap"
        print(f"{RED}Detected potential Bear Trap pattern{RESET}")
    
    if not trap_type:
        print(f"{GREEN}No trap pattern detected in current price action{RESET}")
        return None, 0.0
    
    # Calculate confidence score based on multiple factors
    print(f"\n{MAGENTA}───── CONFIDENCE CALCULATION ─────{RESET}")
    
    # 1. Price intensity factor (60% weight)
    price_factor = intensity * 0.60
    print(f"{WHITE}Price Intensity: {intensity:.2f} × 0.60 = {price_factor:.2f}{RESET}")
    
    # 2. Trend strength factor (30% weight)
    trend_strength = 1.0 if "Strongly" in trend else 0.6
    trend_factor = trend_strength * 0.30
    print(f"{WHITE}Trend Strength: {trend_strength:.2f} × 0.30 = {trend_factor:.2f}{RESET}")
    
    # 3. Timeframe weight factor (10% weight)
    timeframe_weight = 1.0 if timeframe in ["15min", "30min", "60min"] else 0.7
    timeframe_factor = timeframe_weight * 0.10
    print(f"{WHITE}Timeframe Weight: {timeframe_weight:.2f} × 0.10 = {timeframe_factor:.2f}{RESET}")
    
    # Calculate final confidence score
    confidence = price_factor + trend_factor + timeframe_factor
    print(f"\n{WHITE}Total Confidence Score: {confidence:.2f}{RESET}")
    
    # Only report if confidence exceeds threshold
    if confidence < 0.3:
        print(f"{BLUE}Below confidence threshold (0.3), no trap will be reported{RESET}")
        return None, 0.0
    
    # Print movement classification tag
    if trap_type == "Bull Trap":
        print(f"\n{GREEN_BG}{WHITE}{BOLD} BULL TRAP DETECTED {RESET}")
    elif trap_type == "Bear Trap":
        print(f"\n{RED_BG}{WHITE}{BOLD} BEAR TRAP DETECTED {RESET}")
        
    # Print confidence level with color coding
    if confidence > 0.8:
        print(f"{RED}⚠️ HIGH CONFIDENCE MM TRAP DETECTED: {trap_type} on {timeframe} (confidence: {confidence:.2f}){RESET}")
    elif confidence > 0.5:
        print(f"{LIGHT_ORANGE}⚠️ MEDIUM CONFIDENCE MM TRAP DETECTED: {trap_type} on {timeframe} (confidence: {confidence:.2f}){RESET}")
    else:
        print(f"{YELLOW}⚠️ LOW CONFIDENCE MM TRAP DETECTED: {trap_type} on {timeframe} (confidence: {confidence:.2f}){RESET}")
    
    # Log the trap detection
    logger.info(f"⚠️ MM TRAP DETECTED: {trap_type} on {timeframe} (confidence: {confidence})")
    
    # Store in database
    trap_data = {
        "type": trap_type,
        "timeframe": timeframe,
        "confidence": confidence,
        "price_change": price_change_pct,
        "price": price_move
    }
    insert_possible_mm_trap(trap_data)
    
    return trap_type, confidence

def check_system_warnings(limit: int = 10, warning_type: Optional[str] = None):
    """
    Check system warnings stored in Redis.
    
    Args:
        limit (int): Maximum number of warnings to retrieve
        warning_type (Optional[str]): Specific type of warning to retrieve, or None for all warnings
    
    Returns:
        Dict: Summary of warnings
    """
    try:
        if warning_type:
            warnings = redis_conn.lrange(f"system:warnings:{warning_type}", 0, limit - 1)
            warning_count = redis_conn.llen(f"system:warnings:{warning_type}")
        else:
            warnings = redis_conn.lrange("system:warnings", 0, limit - 1)
            warning_count = redis_conn.llen("system:warnings")
        
        # Parse warnings
        parsed_warnings = []
        for w in warnings:
            try:
                warning_data = json.loads(w)
                parsed_warnings.append(warning_data)
            except:
                continue
                
        # Get warning counts by type
        warning_counts = redis_conn.hgetall("system:warning_counts")
        
        return {
            "total_warnings": warning_count,
            "warnings": parsed_warnings,
            "counts_by_type": warning_counts
        }
    except Exception as e:
        logger.error(f"Error retrieving warnings from Redis: {e}")
        return {"error": str(e)}

# Function to clear the terminal screen
def clear_screen():
    """Clear the terminal screen for a clean refresh."""
    # ANSI escape sequence to clear screen and move cursor to home position
    print("\033[2J\033[H", end="")

def display_fibonacci_levels():
    """Display the current Fibonacci levels and highlight price alignment."""
    try:
        # Get current price
        current_price = float(redis_conn.get("last_btc_price") or 0)
        if current_price == 0:
            print(f"{YELLOW}⚠️ No current price available for Fibonacci analysis{RESET}")
            return
            
        # Get Fibonacci levels
        fib_levels = get_current_fibonacci_levels()
        if not fib_levels or len(fib_levels) == 0:
            print(f"{YELLOW}⚠️ No Fibonacci levels available{RESET}")
            return
            
        print(f"\n{BLUE_BG}{WHITE}{BOLD} FIBONACCI LEVELS ANALYSIS {RESET}")
        
        # Find levels close to current price
        nearby_levels = []
        for level_name, level_price in fib_levels.items():
            distance_pct = abs(current_price - level_price) / level_price * 100
            
            if distance_pct < 5.0:  # Within 5%
                nearby_levels.append({
                    "level": level_name,
                    "price": level_price,
                    "distance_pct": distance_pct
                })
                
        # Sort nearby levels by distance
        nearby_levels.sort(key=lambda x: x["distance_pct"])
        
        # Display current price and nearest level
        if nearby_levels:
            nearest = nearby_levels[0]
            distance_formatted = f"{nearest['distance_pct']:.2f}%"
            print(f"{GREEN}🎯 BTC price ${format_price(current_price)} is {YELLOW}{distance_formatted}{GREEN} away from {CYAN}{nearest['level']}{GREEN} level at ${format_price(nearest['price'])}{RESET}")
        else:
            print(f"{YELLOW}Current price ${format_price(current_price)} is not near any Fibonacci level{RESET}")
            
        # Group levels for better display
        price_range = current_price * 0.2  # Show levels within 20% of current price
        upper_levels = []
        lower_levels = []
        
        for level_name, level_price in sorted(fib_levels.items(), key=lambda x: float(x[1])):
            if current_price < level_price < current_price + price_range:
                upper_levels.append((level_name, level_price))
            elif current_price - price_range < level_price < current_price:
                lower_levels.append((level_name, level_price))
                
        # Display levels
        if upper_levels:
            print(f"\n{MAGENTA}RESISTANCE LEVELS ABOVE:{RESET}")
            for level_name, level_price in upper_levels:
                pct_above = ((level_price - current_price) / current_price) * 100
                print(f"  {CYAN}{level_name}: ${format_price(level_price)} ({GREEN}↑ {pct_above:.2f}%{RESET})")
                
        if lower_levels:
            print(f"\n{MAGENTA}SUPPORT LEVELS BELOW:{RESET}")
            for level_name, level_price in reversed(lower_levels):
                pct_below = ((current_price - level_price) / current_price) * 100
                print(f"  {CYAN}{level_name}: ${format_price(level_price)} ({RED}↓ {pct_below:.2f}%{RESET})")
                
        # Check for alignments
        alignment = check_fibonacci_alignment()
        if alignment:
            confidence = alignment.get("confidence", 0) * 100
            level_type = alignment.get("type", "STANDARD")
            level_name = alignment.get("level", "Unknown")
            
            confidence_color = GREEN if confidence > 75 else YELLOW if confidence > 50 else RED
            
            print(f"\n{MAGENTA}FIBONACCI ALIGNMENT DETECTED:{RESET}")
            print(f"  {BLUE}Type: {level_type}{RESET}")
            print(f"  {BLUE}Level: {level_name}{RESET}")
            print(f"  {BLUE}Confidence: {confidence_color}{confidence:.1f}%{RESET}")
            
    except Exception as e:
        logger.error(f"Error displaying Fibonacci levels: {e}")
        print(f"{RED}⚠️ Error displaying Fibonacci levels: {e}{RESET}")

def monitor_market_trends():
    """
    Monitor BTC market trends across multiple timeframes with enhanced error handling.
    
    This function continuously monitors BTC price movements,
    analyzes trends, and detects potential market maker traps with robust
    fallback mechanisms for handling missing or invalid data.
    """
    # Initialize Redis connection with fallback handling
    if not init_redis_connection():
        print(f"{RED}Error: Failed to connect to Redis. Please ensure Redis server is running.{RESET}")
        sys.exit(1)
    
    # Create analyzer instance
    analyzer = MarketTrendAnalyzer()
    
    # Check if we're in fixed display mode
    fixed_display = os.environ.get("FIXED_DISPLAY", "").lower() in ("true", "1", "t", "yes")
    
    # Initialize countdown for fixed display
    refresh_interval = 30  # seconds
    last_refresh_time = time.time() - refresh_interval  # Force immediate refresh
    
    # Clear screen on start if in fixed display mode
    if fixed_display:
        clear_screen()
    
    try:
        # Check data availability
        print(f"{BLUE}Checking data availability...{RESET}")
        
        # Initialize movement history if empty
        movement_history_len = redis_conn.llen("btc_movement_history")
        if movement_history_len == 0:
            current_price = redis_conn.get("last_btc_price")
            if current_price:
                redis_conn.lpush("btc_movement_history", f"{current_price},0")
                print(f"{GREEN}Initialized movement history with current price: {current_price}{RESET}")
            else:
                print(f"{YELLOW}Warning: No current price available to initialize movement history{RESET}")
        
        # Check for Fibonacci data and initialize if needed
        fib_result = ensure_fibonacci_levels()
        if fib_result["source"] != "primary":
            if fib_result["source"] == "generated":
                print(f"{GREEN}Generated new Fibonacci levels with price: {fib_result['data']['base_price']}{RESET}")
            else:
                print(f"{YELLOW}Warning: No Fibonacci data available{RESET}")
        
        # Main monitoring loop
        print(f"{BLUE}Starting market trend monitoring...{RESET}")
        while True:
            current_time = time.time()
            
            # If in fixed display, refresh the screen at regular intervals
            if fixed_display and (current_time - last_refresh_time >= refresh_interval):
                clear_screen()
                last_refresh_time = current_time
                
                # Display header
                print(f"{MAGENTA}{BOLD}╔════════════════════════════════════════════════════════════╗{RESET}")
                print(f"{MAGENTA}{BOLD}║                OMEGA BTC AI - MARKET MONITOR               ║{RESET}")
                print(f"{MAGENTA}{BOLD}║         🧠 DIVINE FIBONACCI MARKET ANALYSIS 🧠           ║{RESET}")
                print(f"{MAGENTA}{BOLD}╚════════════════════════════════════════════════════════════╝{RESET}")
                
                # Get latest timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{CYAN}Last Update: {timestamp}{RESET}")
                print(f"{YELLOW}Refresh in: {refresh_interval} seconds{RESET}")
                print()
                
            # Get analysis results with fallback handling
            results = analyzer.analyze_trends()
            
            # Display results
            if results:
                analyzer.display_results(results)
                analyzer.display_market_conditions()
                
                # Display Fibonacci levels if available
                display_fibonacci_levels()
                
                # Check for system warnings
                check_system_warnings()
            else:
                print(f"{RED}No analysis results available{RESET}")
            
            # If not in fixed display mode, add separator
            if not fixed_display:
                print("\n" + "=" * 80 + "\n")
            
            time.sleep(5)  # Adjust timing as needed
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Monitoring stopped by user.{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        logger.error(f"Error in monitor_market_trends: {e}")
        store_warning_in_redis("MONITOR_ERROR", f"Error in monitor_market_trends: {e}")

def describe_movement_intensity(price_change: float) -> str:
    """
    Describe the intensity of a price movement with consistent formatting.
    
    Args:
        price_change: The percentage price change
        
    Returns:
        Formatted description of movement intensity
    """
    abs_change = abs(price_change)
    
    if abs_change > 10:
        intensity = f"{RED}Extreme{'↑' if price_change > 0 else '↓'}{RESET}"
    elif abs_change > 5:
        intensity = f"{LIGHT_ORANGE}Strong{'↑' if price_change > 0 else '↓'}{RESET}"
    elif abs_change > 2:
        intensity = f"{YELLOW}Moderate{'↑' if price_change > 0 else '↓'}{RESET}"
    elif abs_change > 0.5:
        intensity = f"{CYAN}Mild{'↑' if price_change > 0 else '↓'}{RESET}"
    else:
        intensity = f"{BLUE}Minimal{RESET}"
        
    return intensity

def format_volume(volume: float) -> str:
    """
    Format a volume value appropriately based on its size.
    Shows full precision for small values.
    
    Args:
        volume: The volume to format
        
    Returns:
        Formatted volume string
    """
    if volume < 0.01:
        # Use scientific notation for very small values to avoid showing 0.00
        return f"{volume:.8f} BTC"
    elif volume < 1.0:
        # Show more precision for small but not tiny values
        return f"{volume:.4f} BTC"
    else:
        # Use commas for thousands separator and 2 decimal places for larger values
        return f"{volume:,.2f} BTC"

if __name__ == "__main__":
    monitor_market_trends() 