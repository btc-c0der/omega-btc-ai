#!/usr/bin/env python3

"""
Update Fibonacci Levels for BTC Price Analysis

This script calculates and updates Fibonacci retracement levels based on recent price movements,
storing them in Redis for the dashboard to display.
"""

import os
import sys
import redis
import json
import time
import signal
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.utils.redis_connection import RedisConnectionManager
from omega_ai.config import REDIS_HOST, REDIS_PORT

# ANSI escape codes for colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Global flag for graceful shutdown
running = True

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global running
    print(f"\n{YELLOW}Received shutdown signal. Completing final update...{RESET}")
    running = False

def calculate_fibonacci_levels(high: float, low: float) -> Dict[str, float]:
    """Calculate Fibonacci retracement and extension levels."""
    diff = high - low
    
    # Standard Fibonacci retracement levels
    retracements = {
        "0.0": low,
        "0.236": low + diff * 0.236,
        "0.382": low + diff * 0.382,
        "0.5": low + diff * 0.5,
        "0.618": low + diff * 0.618,
        "0.786": low + diff * 0.786,
        "1.0": high
    }
    
    # Fibonacci extension levels
    extensions = {
        "1.272": high + diff * 0.272,  # 127.2% extension
        "1.414": high + diff * 0.414,  # Square root of 2
        "1.618": high + diff * 0.618,  # Golden Ratio extension
        "2.0": high + diff * 1.0,      # 200% extension
        "2.414": high + diff * 1.414,  # Square root of 2 (doubled)
        "2.618": high + diff * 1.618   # Golden Ratio (doubled)
    }
    
    # Combine retracements and extensions
    return {**retracements, **extensions}

def get_recent_price_data(redis_conn: redis.Redis, timeframe: str = "1min") -> Optional[Tuple[float, float]]:
    """Get recent high and low prices for Fibonacci calculations."""
    try:
        # Get price history from Redis
        movements_key = f"btc_movements_{timeframe}"
        movements_data = redis_conn.lrange(movements_key, -100, -1)  # Get last 100 prices
        
        if not movements_data:
            print(f"{YELLOW}No price data found for {timeframe} timeframe{RESET}")
            return None
            
        # Extract prices from list items
        prices = []
        for item in movements_data:
            try:
                if isinstance(item, bytes):
                    item = item.decode('utf-8')
                data = json.loads(item)
                if isinstance(data, dict) and "price" in data:
                    prices.append(float(data["price"]))
                elif isinstance(data, (int, float)):
                    prices.append(float(data))
            except (json.JSONDecodeError, ValueError) as e:
                print(f"{YELLOW}Error parsing price data: {e}{RESET}")
                continue
        
        if not prices:
            print(f"{YELLOW}No valid prices found in movements data{RESET}")
            return None
            
        return max(prices), min(prices)
        
    except Exception as e:
        print(f"{RED}Error getting price data: {e}{RESET}")
        return None

def update_fibonacci_levels() -> bool:
    """Update Fibonacci levels in Redis. Returns True if successful."""
    try:
        # Initialize Redis connection
        redis_conn = RedisConnectionManager().client
        
        # Get price data for different timeframes
        timeframes = ["1min", "5min", "15min", "60min"]  # Updated timeframes to match Redis keys
        all_levels = []
        
        for timeframe in timeframes:
            price_data = get_recent_price_data(redis_conn, timeframe)
            if price_data:
                high, low = price_data
                levels = calculate_fibonacci_levels(high, low)
                all_levels.append((timeframe, levels))
                print(f"{GREEN}Calculated Fibonacci levels for {timeframe}:{RESET}")
                for level, price in levels.items():
                    print(f"  {level}: ${price:.2f}")
        
        if not all_levels:
            print(f"{RED}No valid Fibonacci levels calculated{RESET}")
            return False
            
        # Find confluence zones (levels that are close to each other across timeframes)
        confluence_zones = []
        tolerance = 100  # $100 tolerance for confluence
        
        for i, (tf1, levels1) in enumerate(all_levels):
            for j, (tf2, levels2) in enumerate(all_levels[i+1:], i+1):
                for level1, price1 in levels1.items():
                    for level2, price2 in levels2.items():
                        if abs(price1 - price2) < tolerance:
                            confluence_zones.append({
                                "level": f"{level1}/{level2}",
                                "price": (price1 + price2) / 2,
                                "timeframes": [tf1, tf2],
                                "strength": 2
                            })
        
        # Store Fibonacci levels in Redis
        redis_conn.hset("realtime_fibonacci_levels", mapping={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **{k: str(v) for k, v in all_levels[0][1].items()}  # Use 1min timeframe as primary
        })
        
        # Store confluence zones
        if confluence_zones:
            redis_conn.set("latest_fibonacci_confluence", json.dumps(confluence_zones))
            print(f"\n{MAGENTA}Found {len(confluence_zones)} confluence zones:{RESET}")
            for zone in confluence_zones:
                print(f"  Level {zone['level']} at ${zone['price']:.2f} across {', '.join(zone['timeframes'])}")
        
        print(f"\n{GREEN}✅ Fibonacci levels updated successfully{RESET}")
        return True
        
    except Exception as e:
        print(f"{RED}Error updating Fibonacci levels: {e}{RESET}")
        return False

def run_continuous_updates(update_interval: int = 300):
    """Run continuous Fibonacci level updates.
    
    Args:
        update_interval: Update interval in seconds (default: 300 seconds / 5 minutes)
    """
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"{CYAN}Starting continuous Fibonacci level updates every {update_interval} seconds{RESET}")
    print(f"{CYAN}Press Ctrl+C to stop{RESET}")
    
    last_update = 0
    failures = 0
    max_failures = 3
    
    while running:
        current_time = time.time()
        
        if current_time - last_update >= update_interval:
            print(f"\n{CYAN}Running Fibonacci level update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
            
            if update_fibonacci_levels():
                last_update = current_time
                failures = 0
            else:
                failures += 1
                if failures >= max_failures:
                    print(f"{RED}Too many consecutive failures ({failures}). Stopping updates.{RESET}")
                    break
                    
        time.sleep(1)  # Sleep for 1 second to prevent CPU overuse
    
    print(f"{YELLOW}Fibonacci level updates stopped{RESET}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Update Fibonacci levels continuously')
    parser.add_argument('--interval', type=int, default=300,
                      help='Update interval in seconds (default: 300)')
    parser.add_argument('--once', action='store_true',
                      help='Run once and exit')
    args = parser.parse_args()
    
    if args.once:
        update_fibonacci_levels()
    else:
        run_continuous_updates(args.interval) 