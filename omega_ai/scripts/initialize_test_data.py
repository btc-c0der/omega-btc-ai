
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

import logging
import datetime

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def generate_test_btc_data():
    """Generate test BTC price data in Redis for Fibonacci analysis."""
    try:
        logger.info("Generating test BTC price movement data")
        import json
        
        # Initialize Redis connection
        redis_conn = redis.Redis(host='localhost', port=6379, db=0)
        
        # Base price and timestamp
        base_price = 50000.0
        now = datetime.now()
        
        # Generate price movements for different timeframes
        for timeframe in [1, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1440]:
            key = f"btc_movements_{timeframe}min"
            
            # Clear existing data
            redis_conn.delete(key)
            
            # Generate movements - create a wave pattern 
            for i in range(100):
                # Add some randomness and a wave pattern
                change = (i % 20) * 100 + ((i % 5) * 50) - ((i % 3) * 30)
                price = base_price + change
                
                timestamp = (now - timedelta(minutes=timeframe*(100-i))).isoformat()
                
                # Create movement data
                movement = {
                    "timestamp": timestamp,
                    "price": price,
                    "volume": 10 + (i % 10)
                }
                
                # Store in Redis
                redis_conn.lpush(key, json.dumps(movement))
            
            logger.info(f"Generated {100} test movements for {timeframe}min timeframe")
        
        # Set current price
        redis_conn.set("last_btc_price", base_price)
        
        return True
    except Exception as e:
        logger.error(f"Error generating test data: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    initialize_test_price_data()