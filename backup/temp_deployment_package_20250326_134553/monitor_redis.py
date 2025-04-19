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
monitor_redis.py - Live monitoring of Redis data from the BTC Live Feed
Part of the OMEGA BTC AI DIVINE COLLECTIVE

This script displays real-time data from Redis in a formatted console display.
"""

import os
import json
import time
import argparse
import logging
from typing import Any, Dict, Optional
from datetime import datetime

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

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

def format_price(price: float) -> str:
    """Format price with commas and 2 decimal places."""
    return f"${price:,.2f}"

def format_time(timestamp: int) -> str:
    """Format Unix timestamp to readable time."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_json(data: Optional[str]) -> Dict[str, Any]:
    """Format and parse JSON data."""
    try:
        if data is None:
            return {}
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return {}

def get_latest_price(redis_mgr: RedisManager) -> tuple:
    """Get the latest BTC price and update time."""
    price = redis_mgr.get('btc:latest_price')
    update_time = redis_mgr.get('btc:latest_update')
    
    try:
        price = float(price) if price else 0.0
        update_time = int(update_time) if update_time else 0
        return price, update_time
    except (ValueError, TypeError):
        return 0.0, 0

def get_stats(redis_mgr: RedisManager) -> Dict[str, Any]:
    """Get BTC statistics."""
    stats_json = redis_mgr.get('btc:stats')
    return format_json(stats_json)

def get_fib_levels(redis_mgr: RedisManager) -> Dict[str, Any]:
    """Get Fibonacci levels."""
    fib_json = redis_mgr.get('btc:fibonacci_levels')
    return format_json(fib_json)

def get_traps(redis_mgr: RedisManager) -> Dict[str, Any]:
    """Get market maker trap data."""
    traps_json = redis_mgr.get('btc:market_traps')
    return format_json(traps_json)

def get_prediction(redis_mgr: RedisManager) -> Dict[str, Any]:
    """Get price prediction data."""
    prediction_json = redis_mgr.get('btc:price_prediction')
    return format_json(prediction_json)

def get_price_history(redis_mgr: RedisManager, count: int = 5) -> list:
    """Get recent price history."""
    history_json = redis_mgr.lrange('btc:price_history', -count, -1)
    history = []
    for item in history_json:
        try:
            history.append(json.loads(item))
        except (json.JSONDecodeError, TypeError):
            pass
    return history

def display_header(price: float, update_time: int) -> None:
    """Display the header with current price."""
    print(f"{BOLD}{BLUE}=== OMEGA BTC LIVE FEED MONITOR ==={RESET}")
    print(f"{BOLD}Current BTC Price: {YELLOW}{format_price(price)}{RESET}")
    print(f"Last Updated: {format_time(update_time)}")
    print(f"{BLUE}{'-' * 40}{RESET}")

def display_stats(stats: Dict[str, Any]) -> None:
    """Display BTC statistics."""
    if not stats:
        print(f"{RED}No statistics available{RESET}")
        return
    
    change_color = GREEN if stats.get('change_pct', 0) >= 0 else RED
    change_symbol = "▲" if stats.get('change_pct', 0) >= 0 else "▼"
    
    print(f"{BOLD}{BLUE}BTC STATISTICS:{RESET}")
    print(f"  High: {format_price(stats.get('high', 0))}")
    print(f"  Low: {format_price(stats.get('low', 0))}")
    print(f"  Open: {format_price(stats.get('open', 0))}")
    print(f"  Change: {change_color}{change_symbol} {format_price(abs(stats.get('change', 0)))} ({stats.get('change_pct', 0)}%){RESET}")
    print(f"{BLUE}{'-' * 40}{RESET}")

def display_fibonacci(fib: Dict[str, Any]) -> None:
    """Display Fibonacci levels."""
    if not fib:
        print(f"{RED}No Fibonacci levels available{RESET}")
        return
    
    print(f"{BOLD}{BLUE}FIBONACCI LEVELS:{RESET}")
    print(f"  High: {format_price(fib.get('high', 0))}")
    print(f"  Low: {format_price(fib.get('low', 0))}")
    print(f"  0.236: {format_price(fib.get('fib_0.236', 0))}")
    print(f"  0.382: {format_price(fib.get('fib_0.382', 0))}")
    print(f"  0.500: {format_price(fib.get('fib_0.5', 0))}")
    print(f"  0.618: {format_price(fib.get('fib_0.618', 0))}")
    print(f"  0.786: {format_price(fib.get('fib_0.786', 0))}")
    print(f"  1.272: {format_price(fib.get('fib_1.272', 0))}")
    print(f"  1.618: {format_price(fib.get('fib_1.618', 0))}")
    print(f"{BLUE}{'-' * 40}{RESET}")

def display_traps(traps: Dict[str, Any]) -> None:
    """Display market maker traps."""
    if not traps:
        print(f"{RED}No trap data available{RESET}")
        return
    
    print(f"{BOLD}{BLUE}MARKET MAKER TRAPS:{RESET}")
    
    bull_traps = traps.get('bull_traps', [])
    if bull_traps:
        print(f"  {RED}Bull Traps:{RESET}")
        for trap in bull_traps:
            print(f"    Price: {format_price(trap.get('price', 0))}")
            print(f"    Confidence: {trap.get('confidence', 0)}%")
            print(f"    Description: {trap.get('description', 'N/A')}")
    else:
        print(f"  {GREEN}No Bull Traps Detected{RESET}")
        
    bear_traps = traps.get('bear_traps', [])
    if bear_traps:
        print(f"  {GREEN}Bear Traps:{RESET}")
        for trap in bear_traps:
            print(f"    Price: {format_price(trap.get('price', 0))}")
            print(f"    Confidence: {trap.get('confidence', 0)}%")
            print(f"    Description: {trap.get('description', 'N/A')}")
    else:
        print(f"  {RED}No Bear Traps Detected{RESET}")
        
    print(f"{BLUE}{'-' * 40}{RESET}")

def display_prediction(prediction: Dict[str, Any]) -> None:
    """Display price prediction."""
    if not prediction:
        print(f"{RED}No prediction available{RESET}")
        return
    
    direction = prediction.get('direction', '')
    direction_color = GREEN if direction == 'up' else RED
    direction_symbol = "▲" if direction == 'up' else "▼"
    accelerated = prediction.get('accelerated', False)
    
    print(f"{BOLD}{BLUE}PRICE PREDICTION:{RESET}")
    print(f"  Current: {format_price(prediction.get('current_price', 0))}")
    print(f"  Prediction: {direction_color}{direction_symbol} {format_price(prediction.get('prediction', 0))}{RESET}")
    print(f"  Direction: {direction_color}{direction.upper()}{RESET}")
    print(f"  Confidence: {prediction.get('confidence', 0) * 100:.1f}%")
    print(f"  GPU Accelerated: {GREEN if accelerated else RED}{accelerated}{RESET}")
    print(f"{BLUE}{'-' * 40}{RESET}")

def display_price_history(history: list) -> None:
    """Display recent price history."""
    if not history:
        print(f"{RED}No price history available{RESET}")
        return
    
    print(f"{BOLD}{BLUE}RECENT PRICE HISTORY:{RESET}")
    for entry in history:
        price = entry.get('price', 0)
        timestamp = entry.get('timestamp', 0)
        print(f"  {format_time(timestamp)}: {format_price(price)}")
    print(f"{BLUE}{'-' * 40}{RESET}")

def monitor_redis(redis_mgr: RedisManager, refresh_interval: int = 5, continuous: bool = True) -> None:
    """
    Monitor Redis data with real-time updates.
    
    Args:
        redis_mgr: Connected RedisManager instance
        refresh_interval: Seconds between updates
        continuous: Whether to run continuously or once
    """
    try:
        while True:
            # Get all data
            price, update_time = get_latest_price(redis_mgr)
            stats = get_stats(redis_mgr)
            fib_levels = get_fib_levels(redis_mgr)
            traps = get_traps(redis_mgr)
            prediction = get_prediction(redis_mgr)
            history = get_price_history(redis_mgr)
            
            # Clear screen and display data
            clear_screen()
            display_header(price, update_time)
            display_stats(stats)
            display_fibonacci(fib_levels)
            display_traps(traps)
            display_prediction(prediction)
            display_price_history(history)
            
            if not continuous:
                break
                
            print(f"{YELLOW}Next update in {refresh_interval} seconds. Press Ctrl+C to exit.{RESET}")
            time.sleep(refresh_interval)
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Monitoring stopped by user.{RESET}")
    except Exception as e:
        logger.error(f"Error monitoring Redis: {e}")
        print(f"\n{RED}Error monitoring Redis: {e}{RESET}")

def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Monitor BTC Live Feed Redis data in real-time")
    parser.add_argument("--host", default=os.environ.get('REDIS_HOST', 'localhost'), help="Redis host")
    parser.add_argument("--port", type=int, default=int(os.environ.get('REDIS_PORT', '6379')), help="Redis port")
    parser.add_argument("--password", default=os.environ.get('REDIS_PASSWORD', 'omegaredispass'), help="Redis password")
    parser.add_argument("--ssl", action="store_true", default=os.environ.get('REDIS_USE_TLS', 'false').lower() == 'true', help="Use SSL/TLS")
    parser.add_argument("--cert", default=os.environ.get('REDIS_CERT'), help="Redis CA certificate path")
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval in seconds")
    parser.add_argument("--once", action="store_true", help="Display data once and exit")
    args = parser.parse_args()
    
    print(f"{BLUE}Connecting to Redis at {args.host}:{args.port}...{RESET}")
    
    try:
        # Create Redis manager
        redis_mgr = RedisManager(
            host=args.host,
            port=args.port,
            username=os.environ.get('REDIS_USERNAME'),
            password=args.password,
            ssl=args.ssl,
            ssl_ca_certs=args.cert if args.ssl else None
        )
        
        # Test connection
        if redis_mgr.ping():
            print(f"{GREEN}Redis connection successful!{RESET}")
            monitor_redis(redis_mgr, args.interval, not args.once)
        else:
            print(f"{RED}Failed to connect to Redis. Check your connection settings.{RESET}")
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"{RED}Error connecting to Redis: {e}{RESET}")

if __name__ == "__main__":
    main() 