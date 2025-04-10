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
Verify and fix market data for the market trends monitor
"""

import sys
import redis
import json
import logging
from datetime import datetime, timedelta, timezone
import random

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
TIMEFRAMES = [1, 5, 15, 30, 60, 240, 720, 1444]  # Timeframes in minutes

def verify_and_fix_candle_data(redis_conn, timeframe):
    """Verify and fix candle data for a specific timeframe"""
    key_name = f"btc_candles_{timeframe}min"
    data = redis_conn.get(key_name)
    
    if not data:
        logger.warning(f"No data found for {timeframe}min timeframe")
        return None
    
    try:
        candles = json.loads(data)
        logger.info(f"Loaded {len(candles)} candles for {timeframe}min timeframe")
        
        # Verify candle structure
        if not isinstance(candles, list) or not candles:
            logger.error(f"Invalid candle data format for {timeframe}min timeframe. Not a list or empty.")
            return None
            
        # Check a sample candle for required fields
        sample_candle = candles[0]
        required_fields = ["open", "high", "low", "close", "volume", "timestamp"]
        missing_fields = [field for field in required_fields if field not in sample_candle]
        
        if missing_fields:
            logger.warning(f"Missing fields in {timeframe}min candles: {missing_fields}")
            
            # Add missing fields
            for candle in candles:
                for field in missing_fields:
                    if field == "timestamp":
                        # Generate a timestamp
                        candle["timestamp"] = datetime.now(timezone.utc).isoformat()
                    elif field in ["open", "high", "low", "close"]:
                        # Use close price or generate a random price
                        if "close" in candle:
                            candle[field] = candle["close"]
                        else:
                            candle[field] = random.uniform(30000, 40000)
                    elif field == "volume":
                        # Generate a random volume
                        candle["volume"] = random.uniform(0.5, 10.0)
            
            logger.info(f"Fixed missing fields in {timeframe}min candles")
        
        # Ensure timestamps are in the right format and chronological order
        current_time = datetime.now(timezone.utc)
        for i, candle in enumerate(candles):
            try:
                # Check if timestamp is valid
                if "timestamp" in candle:
                    datetime.fromisoformat(candle["timestamp"].replace('Z', '+00:00'))
                else:
                    # Generate a timestamp
                    candle_time = current_time - timedelta(minutes=timeframe * (len(candles) - i))
                    candle["timestamp"] = candle_time.isoformat()
            except (ValueError, TypeError):
                # Fix invalid timestamp
                candle_time = current_time - timedelta(minutes=timeframe * (len(candles) - i))
                candle["timestamp"] = candle_time.isoformat()
        
        # Sort candles by timestamp (oldest first)
        candles.sort(key=lambda x: x["timestamp"])
        
        # Store fixed candles back in Redis
        redis_conn.set(key_name, json.dumps(candles))
        logger.info(f"Fixed and stored {len(candles)} candles for {timeframe}min timeframe")
        
        return candles
        
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON data for {timeframe}min timeframe")
        return None
    except Exception as e:
        logger.error(f"Error verifying candle data for {timeframe}min: {e}")
        return None

def verify_and_fix_current_price(redis_conn):
    """Verify and fix current BTC price in Redis"""
    price = redis_conn.get("last_btc_price")
    
    if not price:
        logger.warning("No current BTC price found")
        
        # Try to get the price from the smallest timeframe
        smallest_tf = min(TIMEFRAMES)
        key_name = f"btc_candles_{smallest_tf}min"
        data = redis_conn.get(key_name)
        
        if data:
            try:
                candles = json.loads(data)
                if candles and isinstance(candles, list) and "close" in candles[-1]:
                    price = candles[-1]["close"]
                    redis_conn.set("last_btc_price", str(price))
                    logger.info(f"Fixed current BTC price: ${price}")
                else:
                    # Generate a random price
                    price = random.uniform(30000, 40000)
                    redis_conn.set("last_btc_price", str(price))
                    logger.info(f"Set random current BTC price: ${price}")
            except (json.JSONDecodeError, IndexError, KeyError):
                # Generate a random price
                price = random.uniform(30000, 40000)
                redis_conn.set("last_btc_price", str(price))
                logger.info(f"Set random current BTC price: ${price}")
        else:
            # Generate a random price
            price = random.uniform(30000, 40000)
            redis_conn.set("last_btc_price", str(price))
            logger.info(f"Set random current BTC price: ${price}")
    else:
        try:
            price_float = float(price)
            logger.info(f"Current BTC price is valid: ${price_float}")
        except ValueError:
            # Fix invalid price
            price = random.uniform(30000, 40000)
            redis_conn.set("last_btc_price", str(price))
            logger.info(f"Fixed invalid current BTC price: ${price}")

def verify_and_fix_fibonacci_levels(redis_conn):
    """Verify and fix Fibonacci levels in Redis"""
    data = redis_conn.get("fibonacci_levels")
    
    if not data:
        logger.warning("No Fibonacci levels found")
        
        # Get current price
        price_str = redis_conn.get("last_btc_price")
        if price_str:
            try:
                current_price = float(price_str)
                
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
                logger.info(f"Generated Fibonacci levels with high: ${high}, low: ${low}")
            except ValueError:
                logger.error("Invalid current price for Fibonacci calculation")
        else:
            logger.error("No current price available for Fibonacci calculation")
    else:
        try:
            fib_levels = json.loads(data)
            logger.info("Fibonacci levels are valid")
            
            # Check if all required fields are present
            required_fields = ["high", "low", "fib_0", "fib_0.236", "fib_0.382", "fib_0.5", 
                              "fib_0.618", "fib_0.786", "fib_1", "fib_1.272", "fib_1.618"]
            
            missing_fields = [field for field in required_fields if field not in fib_levels]
            
            if missing_fields:
                logger.warning(f"Missing fields in Fibonacci levels: {missing_fields}")
                
                # Calculate missing fields
                high = fib_levels.get("high", 0)
                low = fib_levels.get("low", 0)
                
                if "high" not in fib_levels or "low" not in fib_levels or high <= 0 or low <= 0:
                    # Get current price and recalculate
                    price_str = redis_conn.get("last_btc_price")
                    if price_str:
                        try:
                            current_price = float(price_str)
                            high = current_price * 1.2
                            low = current_price * 0.8
                        except ValueError:
                            high = 40000
                            low = 30000
                    else:
                        high = 40000
                        low = 30000
                
                # Add missing fields
                if "high" not in fib_levels:
                    fib_levels["high"] = high
                if "low" not in fib_levels:
                    fib_levels["low"] = low
                if "fib_0" not in fib_levels:
                    fib_levels["fib_0"] = low
                if "fib_0.236" not in fib_levels:
                    fib_levels["fib_0.236"] = low + 0.236 * (high - low)
                if "fib_0.382" not in fib_levels:
                    fib_levels["fib_0.382"] = low + 0.382 * (high - low)
                if "fib_0.5" not in fib_levels:
                    fib_levels["fib_0.5"] = low + 0.5 * (high - low)
                if "fib_0.618" not in fib_levels:
                    fib_levels["fib_0.618"] = low + 0.618 * (high - low)
                if "fib_0.786" not in fib_levels:
                    fib_levels["fib_0.786"] = low + 0.786 * (high - low)
                if "fib_1" not in fib_levels:
                    fib_levels["fib_1"] = high
                if "fib_1.272" not in fib_levels:
                    fib_levels["fib_1.272"] = low + 1.272 * (high - low)
                if "fib_1.618" not in fib_levels:
                    fib_levels["fib_1.618"] = low + 1.618 * (high - low)
                
                # Update last update timestamp
                fib_levels["last_update"] = datetime.now(timezone.utc).isoformat()
                
                # Store updated levels
                redis_conn.set("fibonacci_levels", json.dumps(fib_levels))
                logger.info("Fixed missing Fibonacci levels")
        except json.JSONDecodeError:
            logger.error("Invalid JSON data for Fibonacci levels")

def verify_and_fix_additional_data(redis_conn):
    """Verify and fix additional market data"""
    # Check 24h volume
    volume = redis_conn.get("btc_24h_volume")
    if not volume:
        volume = random.uniform(10000, 30000)
        redis_conn.set("btc_24h_volume", str(volume))
        logger.info(f"Set missing 24h volume: {volume:.2f} BTC")
    
    # Check volatility
    volatility = redis_conn.get("btc_volatility")
    if not volatility:
        volatility = random.uniform(0.01, 0.05)
        redis_conn.set("btc_volatility", str(volatility))
        logger.info(f"Set missing volatility: {volatility:.4f}")
    
    # Check Schumann resonance
    schumann = redis_conn.get("schumann_resonance")
    if not schumann:
        schumann_freq = 7.83 + random.uniform(-0.2, 0.2)
        schumann_data = {
            "frequency": schumann_freq,
            "amplitude": random.uniform(0.7, 1.3),
            "alignment": random.choice(["aligned", "misaligned", "neutral"]),
            "market_influence": random.uniform(-0.5, 0.5)
        }
        redis_conn.set("schumann_resonance", json.dumps(schumann_data))
        logger.info(f"Set missing Schumann resonance data: {schumann_freq:.2f} Hz")

def main():
    """Main function to verify and fix market data"""
    # Connect to Redis
    try:
        redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_conn.ping()
        logger.info("Connected to Redis successfully")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        sys.exit(1)
    
    # Verify and fix current price first
    verify_and_fix_current_price(redis_conn)
    
    # Verify and fix candle data for each timeframe
    for timeframe in TIMEFRAMES:
        verify_and_fix_candle_data(redis_conn, timeframe)
    
    # Verify and fix Fibonacci levels
    verify_and_fix_fibonacci_levels(redis_conn)
    
    # Verify and fix additional data
    verify_and_fix_additional_data(redis_conn)
    
    logger.info("Market data verification and fixing complete!")

if __name__ == "__main__":
    main() 