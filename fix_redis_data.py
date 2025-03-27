#!/usr/bin/env python3
"""
Fix Redis data format for btc_movement_history.
This script ensures price,volume data format is correctly stored.
"""

import redis
import os
from omega_ai.utils.redis_manager import RedisManager

# Rasta color constants
GREEN_RASTA = "\033[92m"
YELLOW_RASTA = "\033[93m"
RED_RASTA = "\033[91m"
BLUE_RASTA = "\033[94m"
RESET = "\033[0m"

def log_rasta(message, color=GREEN_RASTA, level="info"):
    """Log with Rasta style and colors."""
    if level == "error":
        print(f"{RED_RASTA}❌ {message}{RESET}")
    elif level == "warning":
        print(f"{YELLOW_RASTA}⚠️  {message}{RESET}")
    elif level == "success":
        print(f"{GREEN_RASTA}✅ {message}{RESET}")
    else:
        print(f"{color}ℹ️  {message}{RESET}")

def fix_btc_movement_history():
    """Check and fix the format of data in btc_movement_history."""
    # Connect to Redis with localhost
    redis_host = 'localhost'
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_manager = RedisManager(host=redis_host, port=redis_port)
    
    try:
        # Get all entries from btc_movement_history
        entries = redis_manager.lrange("btc_movement_history", 0, -1)
        if not entries:
            log_rasta("No entries found in btc_movement_history", YELLOW_RASTA, "warning")
            return
        
        log_rasta(f"Found {len(entries)} entries in btc_movement_history", BLUE_RASTA)
        
        # Check if entries need fixing (some entries might not have volume)
        needs_fixing = False
        for entry in entries:
            if "," not in entry:
                needs_fixing = True
                log_rasta(f"Found entry without volume information: {entry}", YELLOW_RASTA, "warning")
                break
                
        if not needs_fixing:
            log_rasta("All entries have the correct price,volume format", GREEN_RASTA, "success")
            # Print a sample of the data
            sample_entries = entries[:5]
            for i, entry in enumerate(sample_entries):
                parts = entry.split(",")
                price = float(parts[0])
                volume = float(parts[1]) if len(parts) > 1 else 0.0
                log_rasta(f"Entry {i+1}: Price=${price:.2f}, Volume={volume}", BLUE_RASTA)
            return
            
        # Create a new temporary key to fix the data
        temp_key = "btc_movement_history_fixed"
        
        # Process each entry and push to temporary key
        fixed_count = 0
        for entry in entries:
            try:
                # If the entry contains a comma, it's already in the format "price,volume"
                if "," in entry:
                    # Validate the format
                    parts = entry.split(",")
                    price = float(parts[0])
                    volume = float(parts[1])
                    redis_manager.lpush(temp_key, entry)
                else:
                    # Add a default volume of 0.1 if missing
                    price = float(entry)
                    volume = 0.1  # Default volume 
                    redis_manager.lpush(temp_key, f"{price},{volume}")
                fixed_count += 1
            except Exception as e:
                log_rasta(f"Error processing entry {entry}: {e}", RED_RASTA, "error")
        
        # Rename the temporary key to replace the original
        redis_conn = redis.Redis(host=redis_host, port=redis_port)
        redis_conn.rename(temp_key, "btc_movement_history")
        
        log_rasta(f"Successfully fixed {fixed_count} entries", GREEN_RASTA, "success")
        
    except Exception as e:
        log_rasta(f"Error fixing btc_movement_history: {e}", RED_RASTA, "error")

if __name__ == "__main__":
    fix_btc_movement_history() 