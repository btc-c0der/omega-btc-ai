# Test script to check if data exists in Redis
import redis
import json

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Check if movement data exists
keys = r.keys("btc_movements_*")
print(f"Found {len(keys)} movement timeframe keys: {keys}")

# Check general movement history
movement_history = r.lrange("btc_movement_history", 0, -1)
print(f"Found {len(movement_history)} items in btc_movement_history")

# Generate test data if none exists
if not movement_history:
    print("No movement data found. Generating test data...")
    import time
    from datetime import datetime
    
    # Generate sample data for testing
    base_price = 50000.0
    for i in range(100):
        # Simple price movement simulation
        price = base_price + (i % 10) * 100
        timestamp = datetime.now().isoformat()
        
        # Create movement data
        movement_data = json.dumps({
            "timestamp": timestamp,
            "price": price,
            "volume": 10.0 + i,
            "high": price + 50,
            "low": price - 50
        })
        
        # Store in Redis
        r.rpush("btc_movement_history", movement_data)
        
        # Also store in timeframe-specific keys
        for timeframe in [1, 5, 15, 30, 60]:
            key = f"btc_movements_{timeframe}min"
            r.rpush(key, movement_data)
            
    print("Test data generated!")