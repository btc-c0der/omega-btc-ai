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
Check if the market trends data in Redis is properly formatted for the market trends monitor
"""

import sys
import redis
import json
import logging
from datetime import datetime, timezone

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

def check_redis_connection():
    """Check if Redis is running and accessible"""
    try:
        redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_conn.ping()
        logger.info("✅ Redis connection successful")
        return redis_conn
    except redis.ConnectionError as e:
        logger.error(f"❌ Could not connect to Redis: {e}")
        sys.exit(1)

def check_current_price(redis_conn):
    """Check if the current BTC price is set in Redis"""
    price = redis_conn.get("last_btc_price")
    if price:
        try:
            price_float = float(price)
            logger.info(f"✅ Current BTC price available: ${price_float:.2f}")
        except ValueError:
            logger.error(f"❌ Invalid current BTC price format: {price}")
            logger.info("Fixing price format...")
            # Try to convert to float and store back
            try:
                # Remove any non-numeric characters
                price_clean = ''.join(c for c in price if c.isdigit() or c == '.')
                price_float = float(price_clean)
                redis_conn.set("last_btc_price", str(price_float))
                logger.info(f"✅ Fixed current BTC price: ${price_float:.2f}")
            except ValueError:
                logger.error("❌ Could not fix current BTC price")
    else:
        logger.error("❌ No current BTC price found in Redis")

def check_price_movements(redis_conn):
    """Check if price movement data exists for all timeframes"""
    for timeframe in TIMEFRAMES:
        key = f"btc_price_movements_{timeframe}min"
        data = redis_conn.get(key)
        if data:
            try:
                movements = json.loads(data)
                if isinstance(movements, list) and len(movements) > 0:
                    logger.info(f"✅ Found {len(movements)} price movements for {timeframe}min timeframe")
                    
                    # Check a sample movement
                    sample = movements[0]
                    required_fields = ["price", "timestamp", "timeframe"]
                    missing_fields = [field for field in required_fields if field not in sample]
                    
                    if missing_fields:
                        logger.warning(f"⚠️ Missing fields in price movements for {timeframe}min: {missing_fields}")
                    else:
                        logger.info(f"✅ Price movement data for {timeframe}min has all required fields")
                else:
                    logger.warning(f"⚠️ Invalid format for price movements for {timeframe}min")
            except json.JSONDecodeError:
                logger.error(f"❌ Invalid JSON data for price movements for {timeframe}min")
        else:
            logger.warning(f"⚠️ No price movement data found for {timeframe}min timeframe")

def check_trend_data(redis_conn):
    """Check if trend data exists and is properly formatted"""
    for timeframe in TIMEFRAMES:
        # Look for cached trend data
        key = f"btc_trend_{timeframe}min"
        data = redis_conn.get(key)
        if data:
            try:
                trend_data = json.loads(data)
                if isinstance(trend_data, dict) and "trend" in trend_data and "change_pct" in trend_data:
                    logger.info(f"✅ Found trend data for {timeframe}min: {trend_data['trend']} ({trend_data['change_pct']:.2f}%)")
                else:
                    logger.warning(f"⚠️ Invalid format for trend data for {timeframe}min")
            except json.JSONDecodeError:
                logger.error(f"❌ Invalid JSON data for trend data for {timeframe}min")
        else:
            # Check for direct trend keys
            key = f"trend_data_{timeframe}min"
            data = redis_conn.get(key)
            if data:
                try:
                    trend_data = json.loads(data)
                    if isinstance(trend_data, dict) and "trend" in trend_data:
                        logger.info(f"✅ Found alternative trend data for {timeframe}min: {trend_data['trend']}")
                        
                        # Create properly formatted trend data
                        change_pct = trend_data.get("change_pct", 0.0)
                        if not isinstance(change_pct, (int, float)):
                            try:
                                change_pct = float(change_pct)
                            except (ValueError, TypeError):
                                change_pct = 0.0
                                
                        formatted_data = {
                            "trend": trend_data["trend"],
                            "change_pct": change_pct,
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        
                        # Store in the standard format
                        redis_conn.set(f"btc_trend_{timeframe}min", json.dumps(formatted_data))
                        logger.info(f"✅ Created properly formatted trend data for {timeframe}min")
                    else:
                        logger.warning(f"⚠️ Invalid format for alternative trend data for {timeframe}min")
                except json.JSONDecodeError:
                    logger.error(f"❌ Invalid JSON data for alternative trend data for {timeframe}min")
            else:
                logger.warning(f"⚠️ No trend data found for {timeframe}min timeframe")

def check_fibonacci_levels(redis_conn):
    """Check if Fibonacci levels are set in Redis"""
    data = redis_conn.get("fibonacci_levels")
    if data:
        try:
            fib_levels = json.loads(data)
            required_fields = ["high", "low", "fib_0", "fib_0.236", "fib_0.382", "fib_0.5", 
                              "fib_0.618", "fib_0.786", "fib_1", "fib_1.272", "fib_1.618"]
            
            missing_fields = [field for field in required_fields if field not in fib_levels]
            
            if missing_fields:
                logger.warning(f"⚠️ Missing fields in Fibonacci levels: {missing_fields}")
            else:
                logger.info(f"✅ Fibonacci levels are properly set: {fib_levels['fib_0.618']:.2f} (0.618 level)")
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON data for Fibonacci levels")
    else:
        logger.warning(f"⚠️ No Fibonacci levels found in Redis")

def check_candle_data(redis_conn):
    """Check if candle data exists for all timeframes"""
    for timeframe in TIMEFRAMES:
        key = f"btc_candles_{timeframe}min"
        data = redis_conn.get(key)
        if data:
            try:
                candles = json.loads(data)
                if isinstance(candles, list) and len(candles) > 0:
                    logger.info(f"✅ Found {len(candles)} candles for {timeframe}min timeframe")
                    
                    # Check a sample candle
                    sample = candles[0]
                    required_fields = ["open", "high", "low", "close", "volume", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in sample]
                    
                    if missing_fields:
                        logger.warning(f"⚠️ Missing fields in candles for {timeframe}min: {missing_fields}")
                    else:
                        logger.info(f"✅ Candle data for {timeframe}min has all required fields")
                else:
                    logger.warning(f"⚠️ Invalid format for candles for {timeframe}min")
            except json.JSONDecodeError:
                logger.error(f"❌ Invalid JSON data for candles for {timeframe}min")
        else:
            logger.warning(f"⚠️ No candle data found for {timeframe}min timeframe")

def check_additional_data(redis_conn):
    """Check if additional market data exists"""
    # Check volume data
    volume = redis_conn.get("btc_24h_volume")
    if volume:
        try:
            volume_float = float(volume)
            logger.info(f"✅ 24h volume available: {volume_float:.2f} BTC")
        except ValueError:
            logger.error(f"❌ Invalid 24h volume format: {volume}")
    else:
        logger.warning("⚠️ No 24h volume data found in Redis")
    
    # Check volatility data
    volatility = redis_conn.get("btc_volatility")
    if volatility:
        try:
            volatility_float = float(volatility)
            logger.info(f"✅ Volatility available: {volatility_float:.4f}")
        except ValueError:
            logger.error(f"❌ Invalid volatility format: {volatility}")
    else:
        logger.warning("⚠️ No volatility data found in Redis")
    
    # Check Schumann resonance data
    schumann = redis_conn.get("schumann_resonance")
    if schumann:
        try:
            schumann_data = json.loads(schumann)
            if "frequency" in schumann_data:
                logger.info(f"✅ Schumann resonance data available: {schumann_data['frequency']:.2f} Hz")
            else:
                logger.warning("⚠️ Incomplete Schumann resonance data")
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON data for Schumann resonance")
    else:
        logger.warning("⚠️ No Schumann resonance data found in Redis")

def main():
    """Main function to check market trends data"""
    logger.info("Checking market trends data in Redis...")
    
    # Check Redis connection
    redis_conn = check_redis_connection()
    
    # Check current price
    check_current_price(redis_conn)
    
    # Check price movements
    check_price_movements(redis_conn)
    
    # Check trend data
    check_trend_data(redis_conn)
    
    # Check Fibonacci levels
    check_fibonacci_levels(redis_conn)
    
    # Check candle data
    check_candle_data(redis_conn)
    
    # Check additional data
    check_additional_data(redis_conn)
    
    logger.info("Market trends data check complete!")

if __name__ == "__main__":
    main() 