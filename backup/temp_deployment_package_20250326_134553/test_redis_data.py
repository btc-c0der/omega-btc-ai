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
test_redis_data.py - Test script for populating Redis with sample data for testing
Part of the OMEGA BTC AI DIVINE COLLECTIVE

This script creates sample Redis data that simulates actual usage.
"""

import os
import time
import json
import random
import logging
from typing import Dict, Any
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our Redis manager
try:
    from redis_manager_cloud import RedisManager
    logger.info("Successfully imported RedisManager")
except ImportError as e:
    logger.error(f"Failed to import RedisManager: {e}")
    raise

def generate_btc_price() -> float:
    """Generate a realistic BTC price between $84,000 and $88,000."""
    return round(random.uniform(84000, 88000), 2)

def generate_price_series(count: int = 100) -> list:
    """
    Generate a realistic price series with small variations.
    
    Args:
        count: Number of price points to generate
        
    Returns:
        List of price points
    """
    base_price = generate_btc_price()
    prices = [base_price]
    
    for _ in range(count - 1):
        # Add a small random variation, max 0.5% change
        change_pct = random.uniform(-0.005, 0.005)
        new_price = prices[-1] * (1 + change_pct)
        prices.append(round(new_price, 2))
    
    return prices

def generate_fibonacci_levels(prices: list) -> Dict[str, float]:
    """
    Generate Fibonacci levels based on price history.
    
    Args:
        prices: List of price points
        
    Returns:
        Dictionary with Fibonacci levels
    """
    high = max(prices)
    low = min(prices)
    range_price = high - low
    
    return {
        "high": high,
        "low": low,
        "fib_0.0": low,
        "fib_0.236": round(low + 0.236 * range_price, 2),
        "fib_0.382": round(low + 0.382 * range_price, 2),
        "fib_0.5": round(low + 0.5 * range_price, 2),
        "fib_0.618": round(low + 0.618 * range_price, 2),
        "fib_0.786": round(low + 0.786 * range_price, 2),
        "fib_1.0": high,
        "fib_1.272": round(high + 0.272 * range_price, 2),
        "fib_1.618": round(high + 0.618 * range_price, 2)
    }

def generate_stats(prices: list) -> Dict[str, Any]:
    """
    Generate statistics based on price history.
    
    Args:
        prices: List of price points
        
    Returns:
        Dictionary with statistics
    """
    current_price = prices[-1]
    price_high = max(prices[-100:])
    price_low = min(prices[-100:])
    price_open = prices[-100]
    price_change = current_price - price_open
    price_change_pct = (price_change / price_open) * 100 if price_open > 0 else 0
    
    return {
        'price': current_price,
        'high': price_high,
        'low': price_low,
        'open': price_open,
        'change': price_change,
        'change_pct': round(price_change_pct, 2),
        'timestamp': int(time.time())
    }

def generate_trap_data() -> Dict[str, Any]:
    """
    Generate sample market maker trap data.
    
    Returns:
        Dictionary with trap data
    """
    trap_types = ["bull_trap", "bear_trap"]
    selected_type = random.choice(trap_types)
    
    if selected_type == "bull_trap":
        traps = {
            "bull_traps": [
                {
                    "index": 42,
                    "price": generate_btc_price(),
                    "confidence": round(random.uniform(60, 95), 2),
                    "description": "Potential bull trap: Price rising with increasing momentum above MA20"
                }
            ],
            "bear_traps": []
        }
    else:
        traps = {
            "bull_traps": [],
            "bear_traps": [
                {
                    "index": 24,
                    "price": generate_btc_price(),
                    "confidence": round(random.uniform(60, 95), 2),
                    "description": "Potential bear trap: Price falling with increasing momentum below MA20"
                }
            ]
        }
    
    return traps

def generate_price_prediction(current_price: float) -> Dict[str, Any]:
    """
    Generate a price prediction.
    
    Args:
        current_price: Current BTC price
        
    Returns:
        Dictionary with prediction data
    """
    direction = random.choice(["up", "down"])
    confidence = round(random.uniform(0.6, 0.9), 2)
    
    if direction == "up":
        predicted_price = current_price * (1 + random.uniform(0.01, 0.05))
    else:
        predicted_price = current_price * (1 - random.uniform(0.01, 0.05))
    
    return {
        "current_price": current_price,
        "prediction": round(predicted_price, 2),
        "direction": direction,
        "confidence": confidence,
        "accelerated": False
    }

def populate_test_data(redis_manager: RedisManager) -> None:
    """
    Populate Redis with test data.
    
    Args:
        redis_manager: RedisManager instance
    """
    logger.info("Populating Redis with test data...")
    
    # Generate price history
    prices = generate_price_series(200)
    current_price = prices[-1]
    
    # Set latest price
    redis_manager.set('btc:latest_price', current_price)
    redis_manager.set('btc:latest_update', int(time.time()))
    logger.info(f"Set latest price: {current_price}")
    
    # Set Fibonacci levels
    fib_levels = generate_fibonacci_levels(prices)
    redis_manager.set('btc:fibonacci_levels', json.dumps(fib_levels))
    logger.info(f"Set Fibonacci levels: High={fib_levels['high']}, Low={fib_levels['low']}")
    
    # Set statistics
    stats = generate_stats(prices)
    redis_manager.set('btc:stats', json.dumps(stats))
    logger.info(f"Set statistics: Price={stats['price']}, Change={stats['change_pct']}%")
    
    # Set trap data
    traps = generate_trap_data()
    redis_manager.set('btc:market_traps', json.dumps(traps))
    logger.info(f"Set market trap data")
    
    # Set price prediction
    prediction = generate_price_prediction(current_price)
    redis_manager.set('btc:price_prediction', json.dumps(prediction))
    logger.info(f"Set price prediction: {prediction['direction']} to {prediction['prediction']}")
    
    # Set price history
    for i in range(min(48, len(prices))):  # Last 48 hours (simulated)
        index = len(prices) - 48 + i
        if index >= 0:
            timestamp = int((datetime.now() - timedelta(hours=48-i)).timestamp())
            redis_manager.rpush('btc:price_history', json.dumps({
                'price': prices[index],
                'timestamp': timestamp
            }))
    
    logger.info("Test data population complete!")

def main() -> None:
    """Main function."""
    # Get Redis connection details from environment variables or use defaults
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', '6379'))
    redis_username = os.environ.get('REDIS_USERNAME')
    redis_password = os.environ.get('REDIS_PASSWORD', 'omegaredispass')
    redis_ssl = os.environ.get('REDIS_USE_TLS', 'false').lower() == 'true'
    redis_cert = os.environ.get('REDIS_CERT')
    
    logger.info(f"Connecting to Redis at {redis_host}:{redis_port}")
    
    # Create Redis manager
    try:
        redis_mgr = RedisManager(
            host=redis_host,
            port=redis_port,
            username=redis_username,
            password=redis_password,
            ssl=redis_ssl,
            ssl_ca_certs=redis_cert if redis_ssl else None
        )
        
        # Test ping
        if redis_mgr.ping():
            logger.info("Redis connection successful!")
            
            # Populate test data
            populate_test_data(redis_mgr)
        else:
            logger.error("Redis ping failed")
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")

if __name__ == "__main__":
    main() 