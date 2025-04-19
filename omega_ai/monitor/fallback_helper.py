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

import os
import sys
import logging
import json
import time
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime

import redis

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ANSI Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Global Redis connection
redis_conn = None

# Fibonacci constants
PHI = 1.618033988749895
INV_PHI = 0.6180339887498949

# Data validation thresholds
DATA_VALIDATION = {
    'price': (lambda x: 1 <= x < 1000000, "Unrealistic BTC price"),
    'volume': (lambda x: x >= 0, "Negative volume detected"),
    'timestamp': (lambda x: x > 1000000000, "Invalid timestamp"),
    'change_pct': (lambda x: -100 <= x <= 100, "Unrealistic price change"),
}

class CosmicAlignmentError(Exception):
    """Exception raised when critical cosmic alignment is violated."""
    pass

class FibonacciViolation(Exception):
    """Exception raised when Fibonacci principles are violated."""
    pass

def fibonacci_retry(max_attempts=5):
    """
    Decorator for functions that need Fibonacci backoff retry logic.
    
    Args:
        max_attempts (int): Maximum number of retry attempts
        
    Returns:
        Decorator function that implements retry logic
    """
    # Fibonacci sequence for backoff delays
    fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i, delay in enumerate(fib_sequence[:max_attempts]):
                try:
                    return func(*args, **kwargs)
                except redis.RedisError as e:
                    if i == max_attempts - 1:
                        logger.error(f"Final attempt failed for {func.__name__}: {e}")
                        raise
                    logger.warning(f"Attempt {i+1} failed for {func.__name__}: {e}")
                    logger.info(f"Retrying in {delay} seconds (Fibonacci sequence)")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def validate_data(data_type: str, value: Any) -> Tuple[bool, str]:
    """
    Validate data based on predefined validation rules.
    
    Args:
        data_type (str): Type of data to validate (price, volume, etc.)
        value (Any): Value to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if data_type not in DATA_VALIDATION:
        return True, ""
    
    # Get validation function and error message
    validator_func, error_msg = DATA_VALIDATION[data_type]
    
    try:
        # Convert string to float if needed
        if isinstance(value, str):
            value = float(value)
        
        # Validate using the appropriate function
        if validator_func(value):
            return True, ""
        else:
            return False, error_msg
    except (ValueError, TypeError) as e:
        return False, f"Invalid {data_type} format: {e}"

@fibonacci_retry(max_attempts=3)
def get_redis_data(key: str, default: Any = None) -> Any:
    """
    Get data from Redis with error handling.
    
    Args:
        key (str): Redis key
        default (Any): Default value if key doesn't exist
        
    Returns:
        Any: Data from Redis or default value
    """
    global redis_conn
    if redis_conn is None:
        try:
            redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            redis_conn.ping()  # Check connection
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return default
    
    try:
        data = redis_conn.get(key)
        if data is None:
            return default
        
        # Try to parse JSON if it looks like JSON
        if isinstance(data, str) and (data.startswith('{') or data.startswith('[')):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        
        # Try to convert to float if it looks like a number
        if isinstance(data, str) and data.replace('.', '', 1).isdigit():
            return float(data)
        
        return data
    except Exception as e:
        logger.error(f"Error retrieving data from Redis key '{key}': {e}")
        return default

def ensure_trend_data(timeframe: str, use_fallback: bool = True) -> Dict[str, Any]:
    """
    Ensure trend data is available for the given timeframe, 
    falling back to nearby timeframes if necessary.
    
    Args:
        timeframe (str): Timeframe to get trend data for (e.g., '15min', '1h')
        use_fallback (bool): Whether to use fallback mechanisms
        
    Returns:
        Dict[str, Any]: Trend data with source information
    """
    # First try to get data for the exact timeframe
    trend_data = get_redis_data(f"btc_trend_{timeframe}")
    
    if trend_data is not None:
        return {
            "data": trend_data,
            "source": "primary",
            "timeframe": timeframe
        }
    
    if not use_fallback:
        return {
            "data": None,
            "source": "none",
            "timeframe": timeframe
        }
    
    # Define fallback timeframes in order of preference
    fallback_map = {
        '1min': ['5min', '15min', '3min'],
        '3min': ['5min', '1min', '15min'],
        '5min': ['3min', '15min', '1min'],
        '15min': ['5min', '30min', '1h'],
        '30min': ['15min', '1h', '4h'],
        '1h': ['30min', '2h', '4h', '15min'],
        '2h': ['1h', '4h', '30min'],
        '4h': ['2h', '1h', '6h', '1d'],
        '6h': ['4h', '8h', '12h'],
        '8h': ['6h', '12h', '4h'],
        '12h': ['8h', '1d', '6h'],
        '1d': ['12h', '4h', '3d']
    }
    
    # Get fallback timeframes for the requested timeframe
    fallbacks = fallback_map.get(timeframe, [])
    
    # Try each fallback timeframe
    for fallback in fallbacks:
        fallback_data = get_redis_data(f"btc_trend_{fallback}")
        if fallback_data is not None:
            logger.warning(f"Using fallback timeframe {fallback} for {timeframe}")
            return {
                "data": fallback_data,
                "source": "fallback_timeframe",
                "timeframe": fallback
            }
    
    # If still no data, try to infer from candle data
    candle_data = get_redis_data(f"btc_candle_{timeframe}")
    if candle_data is not None:
        # Infer trend from candle
        try:
            if candle_data['c'] > candle_data['o']:
                trend = "Bullish"
            elif candle_data['c'] < candle_data['o']:
                trend = "Bearish"
            else:
                trend = "Stable"
                
            logger.warning(f"Inferred trend for {timeframe} from candle data: {trend}")
            return {
                "data": trend,
                "source": "candle_inference",
                "timeframe": timeframe
            }
        except (KeyError, TypeError):
            pass
    
    # Last resort: use general market data or default to stable
    logger.error(f"No trend data available for {timeframe} after all fallbacks")
    return {
        "data": "Stable",  # Default to stable as safest option
        "source": "default",
        "timeframe": timeframe
    }

def ensure_fibonacci_levels() -> Dict[str, Any]:
    """
    Ensure Fibonacci levels are available, generating them if necessary.
    
    Returns:
        Dict[str, Any]: Fibonacci levels with source information
    """
    # Try to get existing Fibonacci levels
    fib_levels = get_redis_data("fibonacci_levels")
    
    if fib_levels is not None:
        # Validate the completeness of the Fibonacci levels
        required_keys = ['levels', 'base_price', 'direction', 'timestamp']
        if all(key in fib_levels for key in required_keys):
            # Check if levels have all required ratios
            required_ratios = ['0', '0.236', '0.382', '0.5', '0.618', '0.786', '1.0']
            if all(ratio in fib_levels['levels'] for ratio in required_ratios):
                # Check if timestamp is recent (within last 6 hours)
                try:
                    last_update = datetime.fromisoformat(fib_levels['timestamp'])
                    now = datetime.now()
                    time_diff = now - last_update
                    if time_diff.total_seconds() < 21600:  # 6 hours
                        return {
                            "data": fib_levels,
                            "source": "primary",
                            "timestamp": fib_levels['timestamp']
                        }
                except (ValueError, TypeError):
                    logger.warning("Invalid timestamp in Fibonacci levels")
    
    # Need to generate new Fibonacci levels
    logger.warning("Generating new Fibonacci levels")
    
    # Get current BTC price
    current_price = get_redis_data("last_btc_price")
    if current_price is None:
        # Try to get price from candle data
        candle_data = get_redis_data("btc_candle_15min")
        if candle_data is not None and 'c' in candle_data:
            current_price = candle_data['c']
    
    if current_price is None:
        logger.error("Cannot generate Fibonacci levels: No price data available")
        return {
            "data": None,
            "source": "none",
            "timestamp": datetime.now().isoformat()
        }
    
    # Create Fibonacci levels based on current price
    new_levels = create_fibonacci_levels(current_price)
    
    # Store in Redis
    try:
        if redis_conn is not None:
            redis_conn.set("fibonacci_levels", json.dumps(new_levels))
            redis_conn.set("fib_base_price", str(new_levels['base_price']))
            redis_conn.set("fib_last_update", new_levels['timestamp'])
            redis_conn.expire("fibonacci_levels", 21600)  # Expire after 6 hours
    except Exception as e:
        logger.error(f"Failed to store Fibonacci levels in Redis: {e}")
    
    return {
        "data": new_levels,
        "source": "generated",
        "timestamp": new_levels['timestamp']
    }

def create_fibonacci_levels(price: float, direction: str = "up") -> Dict[str, Any]:
    """
    Create Fibonacci levels based on current price.
    
    Args:
        price (float): Current price
        direction (str): Direction of trend ("up" or "down")
        
    Returns:
        Dict[str, Any]: Fibonacci levels
    """
    # For simplicity, assume swing high/low as percentage of current price
    if direction == "up":
        swing_high = price
        swing_low = price * 0.9  # Assuming swing low is 10% below current price
    else:
        swing_high = price * 1.1  # Assuming swing high is 10% above current price
        swing_low = price
    
    # Calculate Fibonacci levels
    fib_levels = {
        '0': swing_high,
        '0.236': swing_high - (0.236 * (swing_high - swing_low)),
        '0.382': swing_high - (0.382 * (swing_high - swing_low)),
        '0.5': swing_high - (0.5 * (swing_high - swing_low)),
        '0.618': swing_high - (0.618 * (swing_high - swing_low)),
        '0.786': swing_high - (0.786 * (swing_high - swing_low)),
        '1.0': swing_low,
        '1.618': swing_low - (0.618 * (swing_high - swing_low)),
        '2.618': swing_low - (1.618 * (swing_high - swing_low))
    }
    
    return {
        'base_price': price,
        'direction': direction,
        'levels': fib_levels,
        'swing_high': swing_high,
        'swing_low': swing_low,
        'timestamp': datetime.now().isoformat()
    }

def store_warning_in_redis(warning_type: str, message: str, source: str = "fallback_helper") -> None:
    """
    Store a warning in Redis for tracking and analysis.
    
    Args:
        warning_type (str): Type of warning (e.g., 'DATA_ERROR', 'REDIS_ERROR')
        message (str): Warning message
        source (str): Source of the warning
    """
    global redis_conn
    if redis_conn is None:
        try:
            redis_conn = redis.Redis(host='localhost', port=6379, db=0)
            redis_conn.ping()  # Check connection
        except redis.ConnectionError:
            logger.error("Failed to connect to Redis to store warning")
            return
    
    try:
        warning_id = int(time.time())
        warning_data = {
            "id": warning_id,
            "type": warning_type,
            "message": message,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store warning in Redis
        redis_conn.set(f"warning:{warning_id}", json.dumps(warning_data))
        redis_conn.lpush("recent_warnings", warning_id)
        redis_conn.ltrim("recent_warnings", 0, 99)  # Keep only 100 most recent warnings
        
        # Also log the warning
        logger.warning(f"{warning_type}: {message} (Source: {source})")
    except Exception as e:
        logger.error(f"Failed to store warning in Redis: {e}")

# Initialize Redis connection if needed
def init_redis_connection():
    """Initialize Redis connection."""
    global redis_conn
    if redis_conn is None:
        try:
            redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            redis_conn.ping()  # Check connection
            logger.info("Successfully connected to Redis")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return False
    return True 