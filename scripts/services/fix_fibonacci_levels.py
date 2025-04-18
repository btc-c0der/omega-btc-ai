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
Fix Fibonacci levels in Redis for market trends monitor
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

def fix_fibonacci_levels():
    """Fix the Fibonacci levels in Redis"""
    try:
        # Connect to Redis
        redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_conn.ping()
        logger.info("Connected to Redis successfully")
        
        # Get current BTC price
        price_str = redis_conn.get("last_btc_price")
        if not price_str:
            logger.error("No current BTC price found in Redis")
            return
        
        # Convert to float
        try:
            current_price = float(price_str)
        except ValueError:
            logger.error(f"Invalid BTC price format: {price_str}")
            return
        
        logger.info(f"Current BTC price: ${current_price:.2f}")
        
        # Check existing Fibonacci levels
        existing_fib = redis_conn.get("fibonacci_levels")
        if existing_fib:
            try:
                fib_data = json.loads(existing_fib)
                logger.info("Found existing Fibonacci levels")
                
                # Get current values or set defaults
                high = fib_data.get("high", current_price * 1.2)
                low = fib_data.get("low", current_price * 0.8)
                
                # Ensure high and low are reasonable
                if high <= low or high <= 0 or low <= 0:
                    # Reset to defaults
                    high = current_price * 1.2
                    low = current_price * 0.8
                    logger.info("Reset high/low values to defaults")
            except json.JSONDecodeError:
                logger.warning("Invalid JSON data for Fibonacci levels")
                # Set defaults
                high = current_price * 1.2
                low = current_price * 0.8
        else:
            logger.info("No existing Fibonacci levels found, creating new ones")
            # Set defaults
            high = current_price * 1.2
            low = current_price * 0.8
        
        # Create complete Fibonacci levels
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
        
        logger.info(f"Fixed Fibonacci levels with high: ${high:.2f}, low: ${low:.2f}")
        logger.info(f"Key levels: 0.618 = ${fib_levels['fib_0.618']:.2f}, 0.5 = ${fib_levels['fib_0.5']:.2f}")
        
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
    except Exception as e:
        logger.error(f"Error fixing Fibonacci levels: {e}")

if __name__ == "__main__":
    fix_fibonacci_levels() 