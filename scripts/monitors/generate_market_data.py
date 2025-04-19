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
Generate test market data for market trends monitor
"""

import sys
import redis
import time
import random
import json
import logging
from datetime import datetime, timedelta, timezone
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Constants
BASE_PRICE = 50000.0  # Base BTC price in USD
VOLATILITY = 0.02  # Volatility for price movements (2%)
TIMEFRAMES = [1, 5, 15, 30, 60, 240, 720, 1444]  # Timeframes in minutes
CANDLES_PER_TIMEFRAME = 100  # Number of candles to generate per timeframe

def generate_random_candle(base_price, timeframe_minutes):
    """Generate a random price candle with realistic parameters"""
    # Higher timeframes have larger movements
    vol_multiplier = 1.0 + (timeframe_minutes / 60) * 0.5
    
    # Calculate price fluctuation
    price_range = base_price * VOLATILITY * vol_multiplier
    
    # Generate random OHLC data
    open_price = base_price + random.uniform(-price_range/2, price_range/2)
    close_price = open_price + random.uniform(-price_range, price_range)
    high_price = max(open_price, close_price) + random.uniform(0, price_range/2)
    low_price = min(open_price, close_price) - random.uniform(0, price_range/2)
    
    # Generate random volume
    volume = random.uniform(0.5, 10.0) * (1 + timeframe_minutes / 60)
    
    return {
        "open": open_price,
        "high": high_price,
        "low": low_price,
        "close": close_price,
        "volume": volume
    }

def generate_price_movement(timeframe_minutes, num_candles, base_price):
    """Generate a series of candles with realistic price movement"""
    candles = []
    current_price = base_price
    
    # Create a trend bias (bullish or bearish) for this timeframe
    trend_bias = random.uniform(-0.5, 0.5)
    
    for i in range(num_candles):
        # Add some trend bias to make price movements more realistic
        price_bias = current_price * VOLATILITY * trend_bias
        
        # Generate a candle with the current price as base
        candle = generate_random_candle(current_price + price_bias, timeframe_minutes)
        
        # Update current price for next candle
        current_price = candle["close"]
        
        # Add timestamp
        now = datetime.now(timezone.utc)
        candle_time = now - timedelta(minutes=timeframe_minutes * (num_candles - i))
        candle["timestamp"] = candle_time.isoformat()
        
        candles.append(candle)
    
    return candles

def store_candles_in_redis(redis_conn, timeframe, candles):
    """Store candle data in Redis for a given timeframe"""
    # Create key name for the timeframe
    key_name = f"btc_candles_{timeframe}min"
    
    # Serialize candles to JSON
    candles_json = json.dumps(candles)
    
    # Store in Redis
    redis_conn.set(key_name, candles_json)
    logger.info(f"Stored {len(candles)} candles for {timeframe}min timeframe in Redis")
    
    # If this is a small timeframe, use the latest price as current BTC price
    if timeframe == min(TIMEFRAMES):
        latest_price = candles[-1]["close"]
        redis_conn.set("last_btc_price", str(latest_price))
        logger.info(f"Updated current BTC price: ${latest_price:.2f}")

def generate_additional_market_data(redis_conn):
    """Generate additional market data like volume and volatility"""
    # Generate 24h volume data
    volume_24h = random.uniform(10000, 30000)
    redis_conn.set("btc_24h_volume", str(volume_24h))
    logger.info(f"Set 24h volume: {volume_24h:.2f} BTC")
    
    # Generate volatility data
    volatility = random.uniform(0.01, 0.05)
    redis_conn.set("btc_volatility", str(volatility))
    logger.info(f"Set volatility: {volatility:.4f}")
    
    # Generate Schumann resonance influence (for fun)
    schumann_freq = 7.83 + random.uniform(-0.2, 0.2)
    schumann_data = {
        "frequency": schumann_freq,
        "amplitude": random.uniform(0.7, 1.3),
        "alignment": random.choice(["aligned", "misaligned", "neutral"]),
        "market_influence": random.uniform(-0.5, 0.5)
    }
    redis_conn.set("schumann_resonance", json.dumps(schumann_data))
    logger.info(f"Set Schumann resonance data: {schumann_freq:.2f} Hz")

def initialize_fibonacci_levels(redis_conn, current_price):
    """Initialize Fibonacci levels based on current price"""
    # Generate a high and low for Fibonacci calculations
    high = current_price * 1.2  # 20% above current price
    low = current_price * 0.8   # 20% below current price
    
    # Calculate Fibonacci levels
    fib_levels = {
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
    
    # Store in Redis
    redis_conn.set("fibonacci_levels", json.dumps(fib_levels))
    logger.info(f"Initialized Fibonacci levels with high: ${high:.2f}, low: ${low:.2f}")

def main():
    """Main function to generate test data"""
    # Connect to Redis
    try:
        redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_conn.ping()
        logger.info("Connected to Redis successfully")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        sys.exit(1)
    
    # Generate and store data for each timeframe
    current_price = BASE_PRICE
    for timeframe in TIMEFRAMES:
        logger.info(f"Generating data for {timeframe}min timeframe...")
        candles = generate_price_movement(timeframe, CANDLES_PER_TIMEFRAME, current_price)
        store_candles_in_redis(redis_conn, timeframe, candles)
        
        # Use the latest price as base for the next timeframe
        current_price = candles[-1]["close"]
    
    # Generate additional market data
    generate_additional_market_data(redis_conn)
    
    # Initialize Fibonacci levels
    initialize_fibonacci_levels(redis_conn, current_price)
    
    logger.info("Test data generation complete!")

if __name__ == "__main__":
    main() 