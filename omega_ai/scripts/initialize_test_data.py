def initialize_test_price_data():
    """Initialize test price data in Redis"""
    import redis
    import datetime
    import json
    import random
    
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    # Generate some test price data
    base_price = 83000.0
    current_time = datetime.datetime.now(datetime.UTC)
    
    for i in range(1500):  # Enough data for all timeframes
        # Generate slightly varying price
        price = base_price * (1 + (random.random() - 0.5) * 0.01)
        
        # Create movement data
        movement = {
            "timestamp": (current_time - datetime.timedelta(minutes=i)).isoformat(),
            "price": price,
            "volume": random.uniform(1, 100),
            "high": price * 1.001,
            "low": price * 0.999
        }
        
        # Store in Redis
        r.lpush("btc_movement_history", json.dumps(movement))
    
    print("✅ Test price data initialized")

if __name__ == "__main__":
    initialize_test_price_data()