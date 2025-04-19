
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

import redis
import json
import time
from datetime import datetime, timedelta

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Get current BTC price
current_price = float(r.get('last_btc_price') or 0)
if current_price == 0:
    current_price = 88000  # Default if no price is available

# Create test candle data for different timeframes
timeframes = ['1min', '5min', '15min', '30min', '60min', '240min']

for tf in timeframes:
    # Create random but realistic candle data
    open_price = current_price * 0.98  # 2% lower than current price
    close_price = current_price
    high_price = current_price * 1.03  # 3% higher than current price
    low_price = current_price * 0.97   # 3% lower than current price
    volume = 1000  # Random volume
    
    # Create candle data
    candle = {
        'o': open_price,
        'c': close_price,
        'h': high_price,
        'l': low_price,
        'v': volume,
        't': int(time.time() * 1000)  # Current timestamp in milliseconds
    }
    
    # Store in Redis
    r.set(f'btc_candle_{tf}', json.dumps(candle))
    print(f'Created candle data for {tf}: {candle}')

# Create trend data
for tf in timeframes:
    trend_data = {
        "trend": "Bullish",
        "change": 2.0,  # 2% change
        "timestamp": datetime.now().isoformat()
    }
    
    # Store in Redis
    r.set(f'btc_trend_{tf}', json.dumps(trend_data))
    print(f'Created trend data for {tf}: {trend_data}')

print("Test data creation completed successfully!") 