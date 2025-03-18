#!/usr/bin/env python3
"""Check Redis data for BTC price movements."""

import json
import logging
from datetime import datetime
from omega_ai.utils.redis_connection import RedisConnectionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Check Redis data for BTC price movements."""
    redis_manager = RedisConnectionManager()
    timeframes = ["1min", "5min", "15min", "60min"]
    
    for timeframe in timeframes:
        key = f"btc_movements_{timeframe}"
        try:
            # Get all data for the timeframe
            data = redis_manager.lrange(key, 0, -1)
            logging.info(f"\nChecking {timeframe} data:")
            logging.info(f"Total entries: {len(data)}")
            
            if data:
                # Check first entry
                first = json.loads(data[0])
                first_time = datetime.fromisoformat(first['timestamp'])
                logging.info(f"First entry: {first_time} - {first['price']}")
                
                # Check last entry
                last = json.loads(data[-1])
                last_time = datetime.fromisoformat(last['timestamp'])
                logging.info(f"Last entry: {last_time} - {last['price']}")
                
                # Calculate time span
                time_diff = last_time - first_time
                logging.info(f"Time span: {time_diff}")
                
                # Check for unique prices
                prices = set()
                for entry in data:
                    entry_data = json.loads(entry)
                    prices.add(float(entry_data['price']))
                logging.info(f"Unique prices: {len(prices)}")
                logging.info(f"Price range: {min(prices)} - {max(prices)}")
            else:
                logging.warning(f"No data found for {timeframe}")
                
        except Exception as e:
            logging.error(f"Error checking {timeframe}: {e}")

if __name__ == "__main__":
    main() 