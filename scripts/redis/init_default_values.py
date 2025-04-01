#!/usr/bin/env python3
"""
Redis Default Values Initialization Script for OMEGA BTC AI

This script initializes default values for important Redis keys
that the dashboard needs to function properly.
"""

import os
import sys
import json
import redis
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=f"{GREEN}[%(asctime)s]{RESET} {BLUE}%(levelname)s{RESET}: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("redis_init")

# Redis configuration (from environment or defaults)
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

def connect_to_redis():
    """Connect to Redis server using different auth methods."""
    # First try without password
    try:
        logger.info(f"Trying to connect to Redis on {REDIS_HOST}:{REDIS_PORT} without password...")
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            socket_timeout=2
        )
        
        if client.ping():
            logger.info(f"{GREEN}Successfully connected to Redis (no password){RESET}")
            return client
    except Exception as e:
        logger.warning(f"{YELLOW}Could not connect without password: {e}{RESET}")
    
    # If that fails, try with password if provided
    if REDIS_PASSWORD:
        try:
            logger.info(f"Trying to connect to Redis with password...")
            client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True,
                socket_timeout=2
            )
            
            if client.ping():
                logger.info(f"{GREEN}Successfully connected to Redis (with password){RESET}")
                return client
        except Exception as e:
            logger.error(f"{RED}Could not connect with password: {e}{RESET}")
    
    logger.error(f"{RED}Failed to connect to Redis{RESET}")
    return None

def set_default_values(redis_client):
    """Set default values for important Redis keys if they don't exist."""
    if not redis_client:
        logger.error(f"{RED}Cannot set default values - no Redis connection{RESET}")
        return False
    
    # Define default values
    default_values = {
        # Trader configuration
        "trader_config": {
            "trap_protection": True,
            "trap_threshold": 70,
            "long_risk_multiplier": 1.0,
            "short_risk_multiplier": 1.0,
            "auto_tp_sl": True,
            "default_leverage": 10,
            "updated_at": datetime.now().isoformat()
        },
        
        # Position targets
        "position_targets": {
            "long": [],
            "short": []
        },
        
        # Default BTC price (just for testing)
        "last_btc_price": "84500.0",
        "sim_last_btc_price": "84500.0",
        
        # MM trap data
        "current_trap_probability": {
            "probability": 0.15,
            "type": "none",
            "description": "No significant trap patterns detected",
            "timestamp": datetime.now().isoformat()
        },
        
        # Market regime
        "market_regime": {
            "regime": "bullish",
            "confidence": 0.75,
            "timestamp": datetime.now().isoformat()
        }
    }
    
    # Set values in Redis only if they don't exist
    success_count = 0
    for key, value in default_values.items():
        try:
            # Check if key already exists
            if not redis_client.exists(key):
                # Convert dictionaries to JSON strings
                if isinstance(value, dict):
                    value = json.dumps(value)
                
                # Set the value
                redis_client.set(key, value)
                logger.info(f"{GREEN}Set default value for {key}{RESET}")
                success_count += 1
            else:
                logger.info(f"{YELLOW}Key {key} already exists, skipping{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error setting default value for {key}: {e}{RESET}")
    
    logger.info(f"{GREEN}Set {success_count} default values in Redis{RESET}")
    return True

def main():
    """Main function."""
    print(f"\n{BOLD}{GREEN}====== OMEGA BTC AI - Redis Default Values Initialization ======{RESET}\n")
    
    # Connect to Redis
    redis_client = connect_to_redis()
    if not redis_client:
        sys.exit(1)
    
    # Set default values
    if set_default_values(redis_client):
        print(f"\n{BOLD}{GREEN}✓ Successfully initialized default Redis values{RESET}\n")
    else:
        print(f"\n{BOLD}{RED}✗ Failed to initialize default Redis values{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main() 