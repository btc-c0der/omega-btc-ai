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
Simple script to insert test data into Redis for the dashboard
"""

import redis
import json
import time
from datetime import datetime, timezone

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Check connection
if r.ping():
    print("✅ Connected to Redis")
else:
    print("❌ Failed to connect to Redis")
    exit(1)

# Sample data to insert
test_data = {
    # Trap probability
    "current_trap_probability": json.dumps({
        "probability": 0.75,
        "trap_type": "liquidity_grab",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "JAH WARNS OF TRAP VIBRATIONS! STAY CONSCIOUS OF FALSE MOVEMENTS!"
    }),
    
    # Position data
    "current_position": json.dumps({
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
    }),
    
    # BTC price
    "last_btc_price": "65789.42",
    
    # Custom test key
    "test:redis_monitor": "Testing the Redis Monitor UI",
    
    # List example
    "test:list_example": ["item1", "item2", "item3"],
    
    # Hash example
    "test:hash_example": {
        "field1": "value1",
        "field2": "value2",
        "field3": "value3"
    }
}

# Insert data into Redis
print("\nInserting test data into Redis:")
for key, value in test_data.items():
    try:
        if isinstance(value, str):
            r.set(key, value)
        elif isinstance(value, list):
            r.delete(key)  # Clear existing list
            for item in value:
                r.rpush(key, item)
        elif isinstance(value, dict) and not key.startswith("current_"):
            r.delete(key)  # Clear existing hash
            r.hset(key, mapping=value)
        else:
            # Ensure it's a string for other types (like JSON)
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            r.set(key, value)
        
        print(f"✅ Inserted: {key}")
    except Exception as e:
        print(f"❌ Error inserting {key}: {e}")

# Confirm data was inserted
print("\nVerifying data in Redis:")
all_keys = r.keys("*")
print(f"Total keys in Redis: {len(all_keys)}")
print("Keys: " + ", ".join(all_keys[:10]) + ("..." if len(all_keys) > 10 else ""))

print("\nRedis monitor data should now appear in the dashboard!") 