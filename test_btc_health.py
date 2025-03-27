#!/usr/bin/env python3
"""
Test BTC health check with corrected Redis parameters
"""

import os
import redis
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

def check_redis_health():
    """Perform a health check on Redis connection and data integrity."""
    try:
        # Check Redis connection using localhost
        redis_host = 'localhost'
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_manager = RedisManager(host=redis_host, port=redis_port)
        redis_manager.ping()
        log_rasta(f"Redis connection: OK (Host: {redis_host}, Port: {redis_port})", GREEN_RASTA, "success")

        # Check if essential keys exist
        essential_keys = ["last_btc_price", "prev_btc_price", "btc_movement_history"]
        for key in essential_keys:
            if not redis_manager.get_cached(key) and key != "btc_movement_history":
                log_rasta(f"Essential key missing: {key}", YELLOW_RASTA, "warning")
            elif key == "btc_movement_history":
                # For list type, we need to check differently
                history = redis_manager.lrange(key, 0, 0)
                if not history:
                    log_rasta(f"Essential key missing: {key}", YELLOW_RASTA, "warning")
                else:
                    log_rasta(f"Essential key present: {key}", GREEN_RASTA, "success")
            else:
                log_rasta(f"Essential key present: {key}", GREEN_RASTA, "success")

        # Check data integrity
        btc_movement_history = redis_manager.lrange("btc_movement_history", 0, -1)
        log_rasta(f"BTC movement history length: {len(btc_movement_history) if btc_movement_history else 0}", BLUE_RASTA)
        
        # Check data format
        if btc_movement_history:
            sample = btc_movement_history[0]
            if "," in sample:
                try:
                    price_str, volume_str = sample.split(",")
                    price = float(price_str)
                    volume = float(volume_str)
                    log_rasta(f"Data format OK - Sample: Price=${price:.2f}, Volume={volume}", GREEN_RASTA, "success")
                except Exception as e:
                    log_rasta(f"Invalid data format in btc_movement_history: {e}", YELLOW_RASTA, "warning")
            else:
                log_rasta("Data format missing volume information", YELLOW_RASTA, "warning")

        return True
    except Exception as e:
        log_rasta(f"Redis health check failed: {e}", RED_RASTA, "error")
        return False

if __name__ == "__main__":
    print(f"{BLUE_RASTA}=== BTC Health Check ==={RESET}")
    check_redis_health() 