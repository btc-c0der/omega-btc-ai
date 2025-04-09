#!/usr/bin/env python3

"""
Diagnostic script to test trend analysis for different timeframes
"""

import redis
import json
import logging
import time
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timezone

# Configure logger
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("trend-analysis-test")

# Initialize Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Terminal colors for enhanced visibility
BLUE = "\033[94m"           # Price up
YELLOW = "\033[93m"         # Price down
GREEN = "\033[92m"          # Strongly positive
RED = "\033[91m"            # Strongly negative
CYAN = "\033[96m"           # Info highlight
MAGENTA = "\033[95m"        # Special emphasis
RESET = "\033[0m"           # Reset color

def get_btc_price_history(limit=100):
    """Get BTC price history from Redis with error handling."""
    try:
        history = []
        raw_data = redis_conn.lrange("btc_movement_history", 0, limit-1)
        
        logger.info(f"Raw data length from Redis: {len(raw_data)}")
        
        if raw_data:
            for item in raw_data:
                try:
                    if "," in item:
                        price_str, volume_str = item.split(",")
                        price = float(price_str)
                        volume = float(volume_str)
                        history.append({"price": price, "volume": volume})
                    else:
                        price = float(item)
                        history.append({"price": price, "volume": 0})
                except Exception as e:
                    logger.warning(f"Error parsing price history item: {e}")
                    continue
            
            return history
        return []
    except Exception as e:
        logger.error(f"Error fetching BTC price history: {e}")
        return []

def analyze_price_trend(minutes=15):
    """Analyze price trend for specified timeframe."""
    try:
        # Get price history with limit that's 2x the requested minutes to ensure enough data
        history = get_btc_price_history(limit=minutes*3)
        logger.info(f"For {minutes}min trend, received {len(history)} historical data points")
        
        if not history or len(history) < minutes:
            logger.warning(f"Insufficient data for {minutes}min trend analysis. Need at least {minutes} data points, got {len(history)}")
            return "No Data", 0.0
        
        # Calculate relevant price points
        current_price = history[0]["price"]
        past_price = history[min(minutes, len(history)-1)]["price"]
        
        logger.info(f"Current price: ${current_price:.2f}, Past price ({minutes}min ago): ${past_price:.2f}")
        
        # Calculate percentage change
        change_pct = ((current_price - past_price) / past_price) * 100
        
        # Determine trend
        if change_pct > 2.0:
            trend = "Strongly Bullish"
        elif change_pct > 0.5:
            trend = "Bullish"
        elif change_pct < -2.0:
            trend = "Strongly Bearish"
        elif change_pct < -0.5:
            trend = "Bearish"
        else:
            trend = "Neutral"
            
        return trend, change_pct
        
    except Exception as e:
        logger.error(f"Error analyzing price trend: {e}")
        return "Error", 0.0

def describe_movement(change_pct, abs_change):
    """Describe the price movement characteristics with Fibonacci wisdom."""
    # Determine intensity of movement
    if abs(change_pct) > 3.618:  # PHI^3
        intensity = f"{RED}COSMIC SHIFT{RESET}"
    elif abs(change_pct) > 2.618:  # PHI^2
        intensity = f"{RED}EXTREMELY AGGRESSIVE{RESET}"
    elif abs(change_pct) > 1.618:  # PHI
        intensity = f"{YELLOW}VERY AGGRESSIVE{RESET}"
    elif abs(change_pct) > 1.0:
        intensity = f"{YELLOW}AGGRESSIVE{RESET}"
    elif abs(change_pct) > 0.618:  # 1/PHI
        intensity = f"{CYAN}MODERATE{RESET}"
    elif abs(change_pct) > 0.382:  # 1/PHI^2
        intensity = f"{BLUE}MILD{RESET}"
    else:
        intensity = f"{RESET}SUBTLE{RESET}"
        
    # Determine direction with arrow
    if change_pct > 0:
        direction = f"{GREEN}↑ UP{RESET}"
    elif change_pct < 0:
        direction = f"{RED}↓ DOWN{RESET}"
    else:
        direction = f"{RESET}→ FLAT{RESET}"
        
    return f"{direction} | {intensity} | ${abs_change:.2f} absolute"

def format_trend_output(interval, trend, change_pct):
    """Format trend output with colors based on direction and intensity."""
    if "Bullish" in trend:
        if "Strongly" in trend:
            color_trend = f"{GREEN}{trend}{RESET}"
        else:
            color_trend = f"{BLUE}{trend}{RESET}"
        sign = "+"
        color_pct = GREEN
    elif "Bearish" in trend:
        if "Strongly" in trend:
            color_trend = f"{RED}{trend}{RESET}"
        else:
            color_trend = f"{YELLOW}{trend}{RESET}"
        sign = ""
        color_pct = RED
    else:
        color_trend = f"{CYAN}{trend}{RESET}"
        sign = "" if change_pct < 0 else "+"
        color_pct = BLUE if change_pct > 0 else YELLOW if change_pct < 0 else RESET
        
    return f"📈 {MAGENTA}{interval}min{RESET} Trend: {color_trend} ({color_pct}{sign}{change_pct:.2f}%{RESET})"

def display_redis_keys():
    """Display relevant Redis keys and their counts for diagnostics."""
    print(f"\n{CYAN}Redis Key Analysis:{RESET}")
    print("-" * 40)
    
    try:
        # Check btc_movement_history
        movement_history_len = redis_conn.llen("btc_movement_history")
        print(f"btc_movement_history: {movement_history_len} entries")
        
        # Check other potentially relevant keys
        for key_pattern in ["*price*", "*btc*", "*candle*", "*trend*", "*movement*"]:
            keys = redis_conn.keys(key_pattern)
            print(f"\nKeys matching '{key_pattern}':")
            for key in keys:
                key_type = redis_conn.type(key).decode('utf-8')
                if key_type == 'list':
                    count = redis_conn.llen(key)
                    print(f"  {key} ({key_type}): {count} entries")
                    # Show sample data for lists
                    if count > 0:
                        sample = redis_conn.lrange(key, 0, 2)
                        print(f"    Sample: {sample}")
                elif key_type == 'string':
                    value = redis_conn.get(key)
                    print(f"  {key} ({key_type}): {value}")
                elif key_type == 'hash':
                    count = redis_conn.hlen(key)
                    print(f"  {key} ({key_type}): {count} fields")
                    # Show sample data for hashes
                    if count > 0:
                        sample = redis_conn.hgetall(key)
                        print(f"    Sample: {list(sample.items())[:2]}")
                else:
                    print(f"  {key} ({key_type})")
    
    except Exception as e:
        print(f"{RED}Error analyzing Redis keys: {e}{RESET}")

def test_all_timeframes():
    """Test trend analysis for all timeframes."""
    timeframes = [1, 5, 15, 30, 60, 240, 720, 1444]
    
    print(f"\n{YELLOW}══════════════ {GREEN}MARKET TREND ANALYSIS TEST{YELLOW} ══════════════{RESET}")
    
    # Get data availability info
    total_history = get_btc_price_history(limit=2000)  # Get as much as possible
    print(f"{CYAN}Total available data points: {len(total_history)}{RESET}")
    
    # Report earliest available data point
    if total_history:
        print(f"{CYAN}Most recent price: ${total_history[0]['price']:.2f}{RESET}")
        if len(total_history) > 1:
            print(f"{CYAN}Oldest available price: ${total_history[-1]['price']:.2f}{RESET}")
            data_span_minutes = len(total_history)
            print(f"{CYAN}Data spans approximately {data_span_minutes} minutes / {data_span_minutes/60:.1f} hours{RESET}")
    
    # Test all timeframes
    for minutes in timeframes:
        trend, change = analyze_price_trend(minutes)
        output = format_trend_output(minutes, trend, change)
        movement = describe_movement(change, abs(change))
        print(f"\n{output}")
        print(f"   {movement}")

if __name__ == "__main__":
    print(f"{MAGENTA}🔍 BTC Trend Analysis Diagnostic Tool{RESET}")
    print(f"{CYAN}Testing connection to Redis...{RESET}")
    
    try:
        redis_conn.ping()
        print(f"{GREEN}✓ Successfully connected to Redis{RESET}")
        
        # Display Redis key diagnostics
        display_redis_keys()
        
        # Test all timeframes
        test_all_timeframes()
        
    except redis.ConnectionError as e:
        print(f"{RED}✗ Failed to connect to Redis: {e}{RESET}")
    except Exception as e:
        print(f"{RED}Error during testing: {e}{RESET}") 