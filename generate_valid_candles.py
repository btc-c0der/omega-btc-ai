#!/usr/bin/env python3

"""
Generate valid candle data for the market trends monitor
This script focuses on creating properly structured candle data for
the market_trends_monitor module.
"""

import os
import sys
import json
import redis
import random
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
TIMEFRAMES = [1, 5, 15, 30, 60, 240, 720, 1444]  # Timeframes in minutes
CANDLE_COUNT = 100  # Number of candles to generate per timeframe
TREND_BIAS = 0.2  # Slight upward trend bias

def generate_price_series(count, start_price=BASE_PRICE, volatility=0.01, trend_bias=TREND_BIAS):
    """Generate a realistic price series with trend bias"""
    prices = [start_price]
    
    for _ in range(count - 1):
        # Calculate price change with trend bias
        change_pct = np.random.normal(trend_bias, volatility)
        new_price = prices[-1] * (1 + change_pct)
        
        # Ensure price is positive
        if new_price <= 0:
            new_price = prices[-1] * 0.99  # Fallback to a small decline
            
        prices.append(new_price)
    
    return prices

def generate_candles(timeframe, count=CANDLE_COUNT):
    """Generate realistic candles for a specific timeframe"""
    now = datetime.now(timezone.utc)
    
    # Generate closing prices with higher volatility for larger timeframes
    vol_factor = min(1.0, 0.01 + (timeframe / 1000) * 0.05)
    trend = TREND_BIAS * (1 + timeframe / 100)  # Larger timeframes have stronger trends
    
    close_prices = generate_price_series(count, BASE_PRICE, vol_factor, trend)
    
    candles = []
    for i, close_price in enumerate(close_prices):
        # Calculate timestamp for this candle
        timestamp = now - timedelta(minutes=timeframe * (count - i))
        
        # Generate realistic OHLC values based on close price
        if i > 0:
            # Calculate realistic open price based on previous close
            open_price = close_prices[i - 1]
        else:
            # For the first candle, create a small random offset from close
            open_price = close_price * (1 + random.uniform(-0.003, 0.003))
        
        # Generate high and low around open/close
        price_range = max(close_price, open_price) * vol_factor
        high_price = max(close_price, open_price) + random.uniform(0, price_range)
        low_price = min(close_price, open_price) - random.uniform(0, price_range)
        
        # Ensure high >= max(open, close) and low <= min(open, close)
        high_price = max(high_price, close_price, open_price)
        low_price = min(low_price, close_price, open_price)
        
        # Generate volume (higher for larger price moves)
        price_change_pct = abs((close_price - open_price) / open_price)
        base_volume = random.uniform(0.5, 5.0) * (1 + timeframe / 60)
        volume = base_volume * (1 + price_change_pct * 10)
        
        # Create candle object
        candle = {
            "timestamp": timestamp.isoformat(),
            "open": float(open_price),
            "high": float(high_price),
            "low": float(low_price),
            "close": float(close_price),
            "volume": float(volume)
        }
        
        candles.append(candle)
    
    return candles

def generate_price_movements(timeframe):
    """Generate price movements data specifically for analyze_price_trend"""
    # Format required for analyze_price_trend:
    # [{"price": float, "timestamp": datetime_str}, ...]
    
    candles = generate_candles(timeframe)
    
    # Convert to price movements format
    movements = []
    for candle in candles:
        movement = {
            "price": candle["close"],
            "timestamp": candle["timestamp"],
            "timeframe": f"{timeframe}min"
        }
        movements.append(movement)
    
    return movements

def store_data_in_redis(redis_conn):
    """Store generated data in Redis"""
    # First, generate and store current price
    current_price = round(BASE_PRICE * (1 + random.uniform(-0.05, 0.05)), 2)
    redis_conn.set("last_btc_price", str(current_price))
    logger.info(f"Set current BTC price: ${current_price:.2f}")
    
    # Generate and store candles for each timeframe
    for timeframe in TIMEFRAMES:
        # Generate candles
        candles = generate_candles(timeframe)
        redis_key = f"btc_candles_{timeframe}min"
        redis_conn.set(redis_key, json.dumps(candles))
        logger.info(f"Stored {len(candles)} candles for {timeframe}min timeframe")
        
        # Generate price movements
        movements = generate_price_movements(timeframe)
        movements_key = f"btc_price_movements_{timeframe}min"
        redis_conn.set(movements_key, json.dumps(movements))
        logger.info(f"Stored {len(movements)} price movements for {timeframe}min timeframe")
    
    # Generate Fibonacci levels
    high = current_price * 1.2
    low = current_price * 0.8
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
    redis_conn.set("fibonacci_levels", json.dumps(fib_levels))
    logger.info(f"Stored Fibonacci levels with high: ${high:.2f}, low: ${low:.2f}")
    
    # Generate additional market data
    
    # 24h volume
    volume_24h = random.uniform(10000, 30000)
    redis_conn.set("btc_24h_volume", str(volume_24h))
    logger.info(f"Stored 24h volume: {volume_24h:.2f} BTC")
    
    # Volatility
    volatility = random.uniform(0.01, 0.05)
    redis_conn.set("btc_volatility", str(volatility))
    logger.info(f"Stored volatility: {volatility:.4f}")
    
    # Schumann resonance
    schumann_freq = 7.83 + random.uniform(-0.2, 0.2)
    schumann_data = {
        "frequency": schumann_freq,
        "amplitude": random.uniform(0.7, 1.3),
        "alignment": random.choice(["aligned", "misaligned", "neutral"]),
        "market_influence": random.uniform(-0.5, 0.5)
    }
    redis_conn.set("schumann_resonance", json.dumps(schumann_data))
    logger.info(f"Stored Schumann resonance data: {schumann_freq:.2f} Hz")
    
    # Price trend data for analyze_price_trend
    for timeframe in TIMEFRAMES:
        # Create a realistic trend for this timeframe (bullish/bearish)
        is_bullish = random.random() > 0.4  # Slight bullish bias for testing
        change_pct = random.uniform(0.5, 5.0) if is_bullish else random.uniform(-5.0, -0.5)
        
        # Store the trend key that analyze_price_trend will look for
        trend_data = {
            "trend": "bullish" if is_bullish else "bearish",
            "change_pct": change_pct,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        trend_key = f"trend_data_{timeframe}min"
        redis_conn.set(trend_key, json.dumps(trend_data))
        logger.info(f"Stored trend data for {timeframe}min: {trend_data['trend']} ({change_pct:.2f}%)")

def setup_database_structures(redis_conn):
    """Set up any database structures needed by the market trends monitor"""
    # Store BTC movement data counts (needed by the monitor)
    for timeframe in TIMEFRAMES:
        # Set count key for each timeframe
        count_key = f"btc_movement_count_{timeframe}min"
        redis_conn.set(count_key, str(CANDLE_COUNT))
        logger.info(f"Set movement count for {timeframe}min: {CANDLE_COUNT}")
    
    # Store total movement count
    redis_conn.set("btc_movement_total_count", str(CANDLE_COUNT * len(TIMEFRAMES)))
    logger.info(f"Set total movement count: {CANDLE_COUNT * len(TIMEFRAMES)}")

def main():
    """Main function to generate and store valid candle data"""
    # Connect to Redis
    try:
        redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_conn.ping()
        logger.info("Connected to Redis successfully")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        sys.exit(1)
    
    # Generate and store data
    store_data_in_redis(redis_conn)
    
    # Set up database structures
    setup_database_structures(redis_conn)
    
    logger.info("Data generation complete!")

if __name__ == "__main__":
    main() 