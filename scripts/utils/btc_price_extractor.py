#!/usr/bin/env python3
"""
BTC Price Extractor - Retrieves recent BTC price data from Redis and saves to JSON

This script connects to a local Redis instance, extracts the BTC price history
for the last 15 minutes, and saves it to a JSON file with timestamp data.
"""

import os
import sys
import json
import time
import redis
from datetime import datetime, timedelta
import argparse

# ANSI color codes for pretty terminal output
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"

def log_message(message, color=BLUE):
    """Print a colorful log message to the console."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {message}{RESET}")

def connect_to_redis(host='localhost', port=6379):
    """Connect to Redis with error handling."""
    log_message(f"Connecting to Redis at {host}:{port}...", BLUE)
    try:
        redis_client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
            socket_timeout=3
        )
        
        # Test connection with ping
        if redis_client.ping():
            log_message("Successfully connected to Redis", GREEN)
            return redis_client
        else:
            log_message("Failed to ping Redis server", RED)
            return None
    except Exception as e:
        log_message(f"Error connecting to Redis: {str(e)}", RED)
        return None

def extract_btc_price_history(redis_client, minutes=15):
    """
    Extract BTC price history for the specified number of minutes.
    Returns structured data with timestamps.
    """
    log_message(f"Extracting BTC price history for the last {minutes} minutes...", BLUE)
    
    price_history = []
    current_time = datetime.now()
    
    try:
        # Get current BTC price
        current_price = redis_client.get("last_btc_price")
        if current_price:
            price_history.append({
                "timestamp": current_time.isoformat(),
                "price": float(current_price),
                "type": "current"
            })
            log_message(f"Current BTC price: ${float(current_price):,.2f}", GREEN)
        
        # Get historical data from btc_movement_history list
        raw_history = redis_client.lrange("btc_movement_history", 0, minutes*10)  # Get extra data to ensure we have enough
        
        if raw_history:
            log_message(f"Found {len(raw_history)} historical price entries", GREEN)
            
            entries_processed = 0
            for i, item in enumerate(raw_history):
                try:
                    # Based on our actual Redis data inspection, it's just the price as a string
                    price = float(item)
                    
                    # Calculate approximate timestamp based on position in list
                    # Newest entries are first in the list (about 6 seconds apart)
                    approx_time = current_time - timedelta(seconds=(i+1)*6)
                    
                    price_history.append({
                        "timestamp": approx_time.isoformat(),
                        "price": price,
                        "type": "historical"
                    })
                    entries_processed += 1
                except Exception as e:
                    log_message(f"Error parsing entry {i}: {str(e)}", YELLOW)
                    continue
                
                # Stop if we have enough entries to cover our time window
                if entries_processed >= minutes * 10:  # Assuming ~10 price updates per minute
                    break
        else:
            log_message("No historical price data found in Redis", YELLOW)
        
        # Sort by timestamp (newest first)
        price_history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Trim to the specified time window
        cutoff_time = (current_time - timedelta(minutes=minutes)).isoformat()
        price_history = [entry for entry in price_history if entry["timestamp"] >= cutoff_time]
        
        # Add metadata
        result = {
            "metadata": {
                "extracted_at": current_time.isoformat(),
                "time_window_minutes": minutes,
                "total_entries": len(price_history)
            },
            "prices": price_history
        }
        
        log_message(f"Successfully extracted {len(price_history)} price entries", GREEN)
        return result
    
    except Exception as e:
        log_message(f"Error extracting price history: {str(e)}", RED)
        return None

def save_to_json(data, filename=None):
    """Save data to a JSON file with error handling."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"btc_price_history_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        log_message(f"Successfully saved data to {filename}", GREEN)
        return filename
    except Exception as e:
        log_message(f"Error saving data to JSON: {str(e)}", RED)
        return None

def main():
    """Main function to extract BTC price history and save to JSON."""
    parser = argparse.ArgumentParser(description="Extract BTC price history from Redis and save to JSON")
    parser.add_argument("-m", "--minutes", type=int, default=15, help="Number of minutes of price history to extract")
    parser.add_argument("-o", "--output", type=str, help="Output filename (default: btc_price_history_<timestamp>.json)")
    parser.add_argument("--host", type=str, default="localhost", help="Redis host (default: localhost)")
    parser.add_argument("--port", type=int, default=6379, help="Redis port (default: 6379)")
    args = parser.parse_args()
    
    log_message(f"BTC Price Extractor - Retrieving {args.minutes} minutes of price data", CYAN)
    
    # Connect to Redis
    redis_client = connect_to_redis(host=args.host, port=args.port)
    if not redis_client:
        return 1
    
    # Extract price history
    price_history = extract_btc_price_history(redis_client, minutes=args.minutes)
    if not price_history:
        return 1
    
    # Save to JSON
    saved_filename = save_to_json(price_history, args.output)
    if not saved_filename:
        return 1
    
    log_message(f"Process completed successfully. Data saved to {saved_filename}", CYAN)
    
    # Print a summary of the extracted data
    current_price = None
    oldest_price = None
    
    for entry in price_history["prices"]:
        if entry["type"] == "current":
            current_price = entry["price"]
        
    if price_history["prices"]:
        oldest_price = price_history["prices"][-1]["price"]
    
    if current_price and oldest_price:
        price_diff = current_price - oldest_price
        price_pct = (price_diff / oldest_price) * 100
        direction = "UP" if price_diff >= 0 else "DOWN"
        color = GREEN if price_diff >= 0 else RED
        
        log_message(f"Price movement over last {args.minutes} min: {direction} ${abs(price_diff):,.2f} ({abs(price_pct):.2f}%)", color)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 