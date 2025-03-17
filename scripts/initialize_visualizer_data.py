#!/usr/bin/env python3

"""
Initialize visualization data for the OmegaBTC AI Visualizer

This script creates the omega:latest_dump key in Redis with test data
for the visualizer to display.
"""

import redis
import json
import datetime
import random
import hashlib
import time

# Initialize Redis connection
redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def create_test_trap_data():
    """Generate test trap detection data"""
    trap_types = ["Bull Trap", "Bear Trap", "Liquidity Grab", "Fake Pump", "Fake Dump"]
    
    traps = []
    
    # Current time for timestamps
    now = datetime.datetime.now()
    
    # Generate 20 trap events
    for i in range(20):
        # Random trap properties
        trap_type = random.choice(trap_types)
        confidence = round(random.uniform(0.6, 0.95), 2)
        price = round(40000 + random.uniform(-2000, 2000), 2)
        
        # Create a timestamp within the last 2 days
        hours_ago = random.randint(1, 48)
        timestamp = (now - datetime.timedelta(hours=hours_ago)).isoformat()
        
        # Create trap data
        trap = {
            "id": f"trap_{i}",
            "type": trap_type,
            "confidence": confidence,
            "price": price,
            "timestamp": timestamp,
            "detected_by": "test_initializer"
        }
        
        traps.append(trap)
    
    return traps

def create_test_price_movements():
    """Generate test BTC price movement data"""
    movements = []
    
    # Base price and timestamp
    base_price = 41200
    now = datetime.datetime.now()
    
    # Generate 100 price movements
    for i in range(100):
        # Create realistic price movement with some volatility
        if i > 0:
            change = random.uniform(-200, 200)
            if random.random() < 0.1:  # 10% chance of larger movement
                change *= 2
            price = round(movements[-1]["price"] + change, 2)
        else:
            price = base_price
        
        # Create a timestamp with appropriate intervals
        minutes_ago = (100 - i) * 5  # 5-minute intervals
        timestamp = (now - datetime.timedelta(minutes=minutes_ago)).isoformat()
        
        # Create movement data
        movement = {
            "timestamp": timestamp,
            "price": price,
            "volume": round(random.uniform(10, 100), 2)
        }
        
        movements.append(movement)
    
    return movements

def create_test_fibonacci_levels():
    """Generate test Fibonacci retracement levels"""
    # Get the last price from movements
    last_price = 41200
    
    # Create price range for Fibonacci
    high = last_price + 1000
    low = last_price - 800
    range_size = high - low
    
    # Calculate Fibonacci levels
    levels = {
        "timeframe": "5min",
        "high": high,
        "low": low,
        "levels": {
            "0.236": round(low + (range_size * 0.236), 2),
            "0.382": round(low + (range_size * 0.382), 2),
            "0.500": round(low + (range_size * 0.500), 2),
            "0.618": round(low + (range_size * 0.618), 2),
            "0.786": round(low + (range_size * 0.786), 2)
        }
    }
    
    return levels

def create_dump_data():
    """Create the main dump data structure"""
    dump_data = {
        "version": "1.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "trap_data": create_test_trap_data(),
        "price_movements": create_test_price_movements(),
        "fibonacci_levels": create_test_fibonacci_levels(),
        "market_state": {
            "last_price": 41200,
            "24h_change": 1.25,
            "24h_volume": 28563.45,
            "market_sentiment": "Bullish",
            "volatility_index": 68.3
        }
    }
    
    # Add data hash for integrity verification
    data_hash = hashlib.sha256(json.dumps(dump_data).encode()).hexdigest()
    dump_data["data_hash"] = data_hash
    
    return dump_data

def initialize_visualizer_data():
    """Initialize all visualizer data in Redis"""
    try:
        print("🔄 Generating visualizer data...")
        
        # Create and store main dump data
        dump_data = create_dump_data()
        dump_json = json.dumps(dump_data)
        redis_conn.set("omega:latest_dump", dump_json)
        
        # Store last BTC price
        redis_conn.set("last_btc_price", dump_data["market_state"]["last_price"])
        
        # Store recent trap detections separately
        for trap in dump_data["trap_data"]:
            key = f"trap:{int(time.time())}"
            redis_conn.hset(key, mapping=trap)
        
        print("✅ Visualizer data initialized successfully!")
        print(f"  - Created omega:latest_dump ({len(dump_json)} bytes)")
        print(f"  - Added {len(dump_data['trap_data'])} trap detection events")
        print(f"  - Added {len(dump_data['price_movements'])} price movements")
        
        return True
    except Exception as e:
        print(f"❌ Error initializing visualizer data: {e}")
        return False

if __name__ == "__main__":
    initialize_visualizer_data() 