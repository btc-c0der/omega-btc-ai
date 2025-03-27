#!/usr/bin/env python3
"""
Initialize MM Trap Detector with current BTC price data
This script loads data from Redis and feeds it to the MM Trap Detector
"""

import os
import time
import redis
from datetime import datetime, UTC, timedelta

# Set Redis host environment variable
os.environ['REDIS_HOST'] = 'localhost'

from omega_ai.utils.redis_manager import RedisManager
from omega_ai.mm_trap_detector.high_frequency_detector import hf_detector

# Rasta color constants
GREEN_RASTA = "\033[92m"
YELLOW_RASTA = "\033[93m"
RED_RASTA = "\033[91m"
BLUE_RASTA = "\033[94m"
RESET = "\033[0m"

def log_message(message, color=GREEN_RASTA, level="info"):
    """Log with color coding."""
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    if level == "error":
        print(f"{RED_RASTA}[{timestamp}] ❌ {message}{RESET}")
    elif level == "warning":
        print(f"{YELLOW_RASTA}[{timestamp}] ⚠️  {message}{RESET}")
    elif level == "success":
        print(f"{GREEN_RASTA}[{timestamp}] ✅ {message}{RESET}")
    else:
        print(f"{color}[{timestamp}] ℹ️  {message}{RESET}")

def initialize_trap_detector():
    """Initialize the MM Trap Detector with Redis data"""
    print(f"{BLUE_RASTA}=== Initializing MM Trap Detector with BTC Price Data ==={RESET}")
    
    # Connect to Redis
    redis_host = 'localhost'
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_manager = RedisManager(host=redis_host, port=redis_port)
    
    try:
        # Get current BTC price
        current_price_str = redis_manager.get_cached("last_btc_price")
        if not current_price_str:
            log_message("No BTC price data available in Redis", RED_RASTA, "error")
            return False
            
        current_price = float(current_price_str)
        log_message(f"Current BTC price: ${current_price:.2f}", BLUE_RASTA)
        
        # Get historical price data
        history = redis_manager.lrange("btc_movement_history", 0, 20)
        if not history:
            log_message("No BTC price history available", YELLOW_RASTA, "warning")
            history = []  # Use empty list instead of None
        else:
            log_message(f"Found {len(history)} historical price entries", GREEN_RASTA, "success")
        
        # Feed historical data to the detector in reverse order (oldest first)
        timestamp = datetime.now(UTC) - timedelta(minutes=len(history))
        for i, entry in enumerate(reversed(history)):
            try:
                if "," in entry:
                    price_str, _ = entry.split(",")
                    price = float(price_str)
                else:
                    price = float(entry)
                
                # Update detector with this price
                hf_detector.update_price_data(price, timestamp)
                log_message(f"Processed historical price ${price:.2f}", BLUE_RASTA)
                
                # Increment timestamp for next entry
                timestamp += timedelta(minutes=1)
                
                # Sleep a bit to avoid overloading
                time.sleep(0.1)
            except Exception as e:
                log_message(f"Error processing history entry {entry}: {e}", RED_RASTA, "error")
        
        # Finally, add the current price
        hf_detector.update_price_data(current_price, datetime.now(UTC))
        log_message(f"Added current price: ${current_price:.2f}", GREEN_RASTA, "success")
        
        # Check for high frequency mode activation
        hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(current_price)
        if hf_active:
            log_message(f"HIGH FREQUENCY TRAP MODE ACTIVATED! Multiplier: {multiplier}", RED_RASTA, "warning")
        else:
            log_message(f"Regular market mode. Multiplier: {multiplier}", GREEN_RASTA, "success")
        
        log_message("MM Trap Detector successfully initialized", GREEN_RASTA, "success")
        return True
    
    except Exception as e:
        log_message(f"Error initializing MM Trap Detector: {e}", RED_RASTA, "error")
        return False

if __name__ == "__main__":
    initialize_trap_detector() 