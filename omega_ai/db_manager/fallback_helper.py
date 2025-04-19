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
Fallback helper functions for market trends monitor
This module provides improved fallback mechanisms for trend analysis
when primary data sources are unavailable or insufficient.
"""

import logging
import json
import redis
from typing import Tuple, List, Dict, Any, Optional
from datetime import datetime, timezone

# Configure logger
logger = logging.getLogger(__name__)

# Redis connection (lazy initialized)
redis_conn = None

def get_redis_connection() -> Optional[redis.Redis]:
    """Get or initialize Redis connection"""
    global redis_conn
    if redis_conn is None:
        try:
            redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            redis_conn.ping()
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return None
    return redis_conn

def ensure_trend_data(timeframe: int) -> Tuple[str, float]:
    """
    Ensure trend data exists for a specific timeframe.
    If it doesn't exist, create it from candle data or fallback to defaults.
    
    Args:
        timeframe: Time interval in minutes
        
    Returns:
        Tuple of (trend_description, percent_change)
    """
    redis_conn = get_redis_connection()
    if not redis_conn:
        return "No Connection", 0.0
    
    # Define trend key at the beginning to avoid unbound variable issues
    trend_key = f"btc_trend_{timeframe}min"
    
    # Check if trend data already exists
    try:
        existing_trend = redis_conn.get(trend_key)
        
        if existing_trend:
            trend_data = json.loads(existing_trend)
            if "trend" in trend_data and "change_pct" in trend_data:
                # Ensure change_pct is a float
                change_pct = float(trend_data["change_pct"]) if isinstance(trend_data["change_pct"], (int, float, str)) else 0.0
                return trend_data["trend"], change_pct
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.warning(f"Error parsing existing trend data: {e}")
    
    # If we get here, we need to create trend data
    logger.info(f"Creating trend data for {timeframe}min timeframe")
    
    # Try to get candle data
    try:
        candle_key = f"btc_candles_{timeframe}min"
        candle_data = redis_conn.get(candle_key)
        
        if candle_data:
            candles = json.loads(candle_data)
            
            if isinstance(candles, list) and len(candles) > 1:
                # Get first and last candle
                oldest_candle = candles[0]
                newest_candle = candles[-1]
                
                # Calculate percent change
                if "close" in oldest_candle and "close" in newest_candle:
                    old_price = float(oldest_candle["close"])
                    new_price = float(newest_candle["close"])
                    
                    if old_price > 0:
                        change_pct = ((new_price - old_price) / old_price) * 100
                        
                        # Determine trend
                        if change_pct > 3.0:
                            trend = "Strongly Bullish"
                        elif change_pct > 0.5:
                            trend = "Bullish"
                        elif change_pct < -3.0:
                            trend = "Strongly Bearish"
                        elif change_pct < -0.5:
                            trend = "Bearish"
                        else:
                            trend = "Neutral"
                        
                        # Store the trend data
                        trend_data = {
                            "trend": trend,
                            "change_pct": change_pct,
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        
                        redis_conn.set(trend_key, json.dumps(trend_data))
                        logger.info(f"Created trend data for {timeframe}min: {trend} ({change_pct:.2f}%)")
                        
                        return trend, change_pct
    except Exception as e:
        logger.warning(f"Error creating trend data from candles: {e}")
    
    # If we get here, we need to use a fallback from nearby timeframes
    return get_fallback_from_nearby_timeframes(timeframe)

def get_fallback_from_nearby_timeframes(timeframe: int) -> Tuple[str, float]:
    """
    Get fallback trend data from nearby timeframes
    
    Args:
        timeframe: Time interval in minutes
        
    Returns:
        Tuple of (trend_description, percent_change)
    """
    redis_conn = get_redis_connection()
    if not redis_conn:
        return "No Connection", 0.0
    
    # Common timeframes
    timeframes = [1, 5, 15, 30, 60, 240, 720, 1444]
    
    # Sort by closest to our target
    timeframes.sort(key=lambda x: abs(x - timeframe))
    
    # Target trend key for our timeframe
    our_trend_key = f"btc_trend_{timeframe}min"
    
    # Try each timeframe (skip the first one as it's our target)
    for tf in timeframes[1:]:
        try:
            trend_key = f"btc_trend_{tf}min"
            existing_trend = redis_conn.get(trend_key)
            
            if existing_trend:
                trend_data = json.loads(existing_trend)
                if "trend" in trend_data and "change_pct" in trend_data:
                    logger.info(f"Using fallback data from {tf}min for {timeframe}min")
                    # Ensure change_pct is a float
                    change_pct = float(trend_data["change_pct"]) if isinstance(trend_data["change_pct"], (int, float, str)) else 0.0
                    
                    # Create a copy of the trend data for our timeframe
                    our_trend_data = {
                        "trend": trend_data["trend"],
                        "change_pct": change_pct,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "fallback_from": f"{tf}min"
                    }
                    
                    # Store it
                    redis_conn.set(our_trend_key, json.dumps(our_trend_data))
                    
                    return trend_data["trend"], change_pct
        except Exception as e:
            logger.warning(f"Error getting fallback data from {tf}min: {e}")
    
    # If all else fails, create a default neutral trend
    default_trend = "Neutral"
    default_change = 0.0
    
    default_data = {
        "trend": default_trend,
        "change_pct": default_change,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fallback": "default"
    }
    
    # Store the default
    try:
        redis_conn.set(our_trend_key, json.dumps(default_data))
    except Exception as e:
        logger.warning(f"Error storing default trend data: {e}")
    
    logger.warning(f"Using default neutral trend for {timeframe}min")
    return default_trend, default_change

def ensure_fibonacci_levels(current_price: float) -> Dict[str, Any]:
    """
    Ensure Fibonacci levels exist and are properly formatted
    
    Args:
        current_price: Current BTC price
        
    Returns:
        Dict with Fibonacci levels
    """
    redis_conn = get_redis_connection()
    if not redis_conn:
        # Return default levels based on current price
        high = current_price * 1.2
        low = current_price * 0.8
        return create_fibonacci_levels(high, low)
    
    # Check if levels exist
    try:
        fib_data = redis_conn.get("fibonacci_levels")
        
        if fib_data:
            levels = json.loads(fib_data)
            
            # Check if all required fields are present
            required_fields = ["high", "low", "fib_0", "fib_0.236", "fib_0.382", "fib_0.5", 
                              "fib_0.618", "fib_0.786", "fib_1", "fib_1.272", "fib_1.618"]
            
            missing_fields = [field for field in required_fields if field not in levels]
            
            if not missing_fields:
                # All fields present
                return levels
            
            # Some fields are missing, recreate from high and low if available
            if "high" in levels and "low" in levels:
                high = levels["high"]
                low = levels["low"]
                
                # Validate high and low
                if high <= low or high <= 0 or low <= 0:
                    # Invalid high/low, create new ones
                    high = current_price * 1.2
                    low = current_price * 0.8
            else:
                # Missing high/low, create new ones
                high = current_price * 1.2
                low = current_price * 0.8
                
            # Create and store new levels
            new_levels = create_fibonacci_levels(high, low)
            redis_conn.set("fibonacci_levels", json.dumps(new_levels))
            
            return new_levels
        else:
            # No levels exist, create new ones
            high = current_price * 1.2
            low = current_price * 0.8
            
            new_levels = create_fibonacci_levels(high, low)
            redis_conn.set("fibonacci_levels", json.dumps(new_levels))
            
            return new_levels
    except Exception as e:
        logger.warning(f"Error ensuring Fibonacci levels: {e}")
        
        # Return default levels
        high = current_price * 1.2
        low = current_price * 0.8
        return create_fibonacci_levels(high, low)

def create_fibonacci_levels(high: float, low: float) -> Dict[str, Any]:
    """
    Create Fibonacci levels from high and low
    
    Args:
        high: High price
        low: Low price
        
    Returns:
        Dict with Fibonacci levels
    """
    return {
        "high": high,
        "low": low,
        "fib_0": low,
        "fib_0.236": low + 0.236 * (high - low),
        "fib_0.382": low + 0.382 * (high - low),
        "fib_0.5": low + 0.5 * (high - low),
        "fib_0.618": low + 0.618 * (high - low),
        "fib_0.786": low + 0.786 * (high - low),
        "fib_1": high,
        "fib_1.272": low + 1.272 * (high - low),
        "fib_1.618": low + 1.618 * (high - low),
        "last_update": datetime.now(timezone.utc).isoformat()
    } 