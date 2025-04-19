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
OMEGA BTC AI - Redis Health Check Script
=======================================

Tests Redis connectivity and checks for expected keys
"""

import redis
import argparse
import sys
import time
import logging
import json
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("redis_health_check")

# Redis keys we're interested in
REDIS_KEYS = {
    'btc_price': ['last_btc_price', 'btc_price', 'sim_last_btc_price'],
    'price_changes': ['btc_price_changes'],
    'price_patterns': ['btc_price_patterns'],
    'trap_probability': ['current_trap_probability', 'trap_probability'],
    'position': ['current_position', 'active_position']
}

def test_redis_connection(host='localhost', port=6379, password=None, inject_sample_data=False):
    """Test connection to Redis server"""
    try:
        # Connect to Redis
        logger.info(f"Attempting to connect to Redis at {host}:{port}")
        if password:
            logger.info("Using password authentication")
        
        client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )
        
        # Test connection
        ping_result = client.ping()
        if ping_result:
            logger.info(f"✅ Redis connection successful! PING response: {ping_result}")
        else:
            logger.error("❌ Redis ping failed")
            return False
        
        # Try to set a test key
        test_key = "omega_ai_health_check"
        test_value = f"Health check at {datetime.now(timezone.utc).isoformat()}"
        
        client.set(test_key, test_value)
        logger.info(f"✅ Successfully set test key: {test_key}")
        
        # Read the test key back
        read_value = client.get(test_key)
        logger.info(f"✅ Successfully read test key: {read_value}")
        
        # Verify the value matches
        if read_value == test_value:
            logger.info("✅ Test key value matches expected value")
        else:
            logger.error(f"❌ Test key value mismatch! Expected: {test_value}, Got: {read_value}")
        
        # Check for existing keys
        found_keys = []
        missing_keys = []
        
        for key_type, keys in REDIS_KEYS.items():
            for key in keys:
                if client.exists(key):
                    found_keys.append(f"{key_type}:{key}")
                else:
                    missing_keys.append(f"{key_type}:{key}")
        
        if found_keys:
            logger.info(f"Found {len(found_keys)} expected keys in Redis:")
            for key in found_keys:
                logger.info(f"  - {key}")
        else:
            logger.warning("No expected keys found in Redis")
            
        if missing_keys:
            logger.warning(f"Missing {len(missing_keys)} expected keys in Redis:")
            for key in missing_keys:
                logger.warning(f"  - {key}")
        
        # Show all Redis keys
        all_keys = client.keys("*")
        logger.info(f"Total Redis keys found: {len(all_keys)}")
        if all_keys:
            logger.info("First 10 Redis keys:")
            for key in all_keys[:10]:
                logger.info(f"  - {key}")
                
        # Inject sample data if requested
        if inject_sample_data:
            logger.info("Injecting sample data into Redis...")
            inject_test_data(client)
            logger.info("✅ Sample data injected")
            
        return True
        
    except redis.ConnectionError as e:
        logger.error(f"❌ Redis connection error: {e}")
        logger.error("Please check that Redis is running and accessible at the specified host/port")
        return False
    except Exception as e:
        logger.error(f"❌ Error testing Redis connection: {e}")
        return False

def inject_test_data(client):
    """Inject test data into Redis for dashboard testing"""
    # Sample BTC price
    client.set("last_btc_price", "65789.42")
    
    # Sample trap probability
    trap_data = {
        "probability": 0.72,
        "trap_type": "bear_trap",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "JAH WARNS OF TRAP VIBRATIONS! STAY CONSCIOUS OF FALSE MOVEMENTS!"
    }
    client.set("current_trap_probability", json.dumps(trap_data))
    
    # Sample position
    position_data = {
        "has_position": True,
        "symbol": "BTCUSDT",
        "entry_price": 63500.00,
        "current_price": 65789.42,
        "direction": "LONG",
        "size": 0.1,
        "pnl": 228.94,
        "pnl_percent": 3.61,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "take_profit_target": 67500.00,
        "stop_loss": 61500.00
    }
    client.set("current_position", json.dumps(position_data))

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="OMEGA BTC AI Redis Health Check")
    parser.add_argument("--host", default="localhost", help="Redis host (default: localhost)")
    parser.add_argument("--port", type=int, default=6379, help="Redis port (default: 6379)")
    parser.add_argument("--password", help="Redis password (default: None)")
    parser.add_argument("--inject-data", action="store_true", help="Inject sample data for testing")
    
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print("               OMEGA BTC AI REDIS HEALTH CHECK                ")
    print("=" * 80 + "\n")
    
    success = test_redis_connection(
        host=args.host,
        port=args.port,
        password=args.password,
        inject_sample_data=args.inject_data
    )
    
    print("\n" + "=" * 80)
    if success:
        print("               REDIS HEALTH CHECK PASSED ✅                ")
    else:
        print("               REDIS HEALTH CHECK FAILED ❌                ")
    print("=" * 80 + "\n")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 