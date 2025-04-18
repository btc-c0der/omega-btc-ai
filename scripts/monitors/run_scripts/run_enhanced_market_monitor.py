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
Enhanced Market Trends Monitor Runner
This script demonstrates the market trends monitor with improved fallback capabilities
"""

import sys
import time
import logging
import json
import argparse
from datetime import datetime, timezone
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

try:
    from omega_ai.db_manager.fallback_helper import (
        ensure_trend_data,
        ensure_fibonacci_levels,
        get_redis_connection
    )
    # Import the correct function from monitor_market_trends_fixed
    from omega_ai.monitor.monitor_market_trends_fixed import monitor_market_trends
    logger.info("Successfully imported required modules")
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    logger.error("Make sure you're running this from the project root directory")
    sys.exit(1)

def ensure_market_data():
    """
    Ensures all required market data is available in Redis
    """
    logger.info("Ensuring all required market data is available...")
    
    # Get Redis connection
    redis_conn = get_redis_connection()
    
    # Verify Redis connection
    if redis_conn is None:
        logger.error("Failed to connect to Redis")
        return False
    
    # Check for current BTC price
    btc_price_json = redis_conn.get("btc_price")
    if btc_price_json:
        btc_price_data = json.loads(btc_price_json)
        current_price = btc_price_data.get("price", 50000.0)
        logger.info(f"Current BTC price: ${current_price:,.2f}")
    else:
        current_price = 50000.0
        btc_price_data = {
            "price": current_price,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        redis_conn.set("btc_price", json.dumps(btc_price_data))
        logger.warning(f"No BTC price found, using default: ${current_price:,.2f}")
    
    # Ensure Fibonacci levels
    fib_levels = ensure_fibonacci_levels(current_price)
    logger.info(f"Fibonacci levels ensured with high: ${fib_levels['high']:,.2f}, low: ${fib_levels['low']:,.2f}")

    # Ensure trend data for all timeframes
    timeframes = [1, 5, 15, 30, 60, 240, 720, 1440]
    for tf in timeframes:
        trend, change_pct = ensure_trend_data(tf)
        logger.info(f"{tf}min trend: {trend} ({change_pct:.2f}%)")

    # Check for volatility data
    volatility_json = redis_conn.get("btc_volatility")
    if not volatility_json:
        volatility_data = {
            "volatility": 0.015,  # 1.5%
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        redis_conn.set("btc_volatility", json.dumps(volatility_data))
        logger.warning("No volatility data found, using default: 1.5%")
    
    # Check for 24h volume data
    volume_json = redis_conn.get("btc_24h_volume")
    if not volume_json:
        volume_data = {
            "volume": 20000.0,  # 20,000 BTC
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        redis_conn.set("btc_24h_volume", json.dumps(volume_data))
        logger.warning("No 24h volume data found, using default: 20,000 BTC")
    
    # Check for Schumann resonance data
    schumann_json = redis_conn.get("schumann_resonance")
    if not schumann_json:
        schumann_data = {
            "frequency": 7.83,  # Hz
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        redis_conn.set("schumann_resonance", json.dumps(schumann_data))
        logger.warning("No Schumann resonance data found, using default: 7.83 Hz")
    
    logger.info("All required market data is now available")
    return True

def run_enhanced_monitor(fixed_display=True, refresh_rate=5):
    """
    Runs the market trends monitor with enhanced fallback capabilities
    
    Args:
        fixed_display (bool): Whether to use fixed display mode
        refresh_rate (int): Refresh rate in seconds
    """
    logger.info(f"Starting enhanced market trends monitor (fixed_display={fixed_display}, refresh_rate={refresh_rate}s)")
    
    # Ensure all required market data is available
    if not ensure_market_data():
        logger.error("Failed to ensure market data. Exiting.")
        return
    
    # Set environment variable for fixed display if needed
    if fixed_display:
        os.environ["FIXED_DISPLAY"] = "true"
    
    # Run the market trends monitor
    try:
        monitor_market_trends()
    except KeyboardInterrupt:
        logger.info("Market trends monitor stopped by user")
    except Exception as e:
        logger.error(f"Error running market trends monitor: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced Market Trends Monitor")
    parser.add_argument(
        "--dynamic", 
        action="store_true", 
        help="Use dynamic display mode instead of fixed"
    )
    parser.add_argument(
        "--refresh", 
        type=int, 
        default=5,
        help="Refresh rate in seconds (only for dynamic mode)"
    )
    args = parser.parse_args()
    
    run_enhanced_monitor(
        fixed_display=not args.dynamic,
        refresh_rate=args.refresh
    ) 