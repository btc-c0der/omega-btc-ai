import redis
from datetime import timedelta
import json

# Create a connection pool
pool = redis.ConnectionPool(
    host='redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com',
    port=19332,
    decode_responses=True,
    username="default",
    password="Gbzlwv6BgNK1oT2B9AvH8MuwAZ0JmQkj"
)

# Create Redis client using the connection pool
r = redis.Redis(connection_pool=pool)

try:
    print("\nChecking for live BTC data in Redis Labs:")
    
    # Check for BTC price keys
    btc_keys = [
        'last_btc_price',
        'prev_btc_price',
        'btc_movement_history',
        'fibonacci_levels',
        'last_btc_update_time'
    ]
    
    print("\n1. Checking BTC price keys:")
    for key in btc_keys:
        value = r.get(key)
        if value:
            print(f"{key}: {value}")
        else:
            list_value = r.lrange(key, 0, -1) if r.type(key) == 'list' else None
            if list_value:
                print(f"{key} (list): {list_value[:5]} ... (showing first 5 entries)")
            else:
                print(f"{key}: Not found")
    
    # Check all keys matching BTC patterns
    print("\n2. All BTC-related keys:")
    btc_pattern_keys = r.keys('*btc*')
    print(f"Found {len(btc_pattern_keys)} BTC-related keys:")
    for key in btc_pattern_keys:
        print(f"Key: {key}")
    
    # Check recent updates
    print("\n3. Checking for recent updates:")
    last_update = r.get('last_btc_update_time')
    if last_update:
        from datetime import datetime
        last_update_time = datetime.fromtimestamp(float(last_update))
        print(f"Last BTC price update: {last_update_time}")
    
    # Check movement history
    print("\n4. Recent price movements:")
    history = r.lrange('btc_movement_history', 0, 4)  # Get last 5 entries
    if history:
        print("Last 5 price movements:")
        for entry in history:
            print(entry)
    else:
        print("No price movement history found")

except Exception as e:
    print(f"Error checking Redis data: {str(e)}")

# Test basic operations
print("\n1. Testing basic operations:")
success = r.set('foo', 'bar')
print(f"Set operation successful: {success}")
result = r.get('foo')
print(f"Retrieved value: {result}")

# Test connection
response = r.ping()
print(f"Connection successful! Ping response: {response}")

# Test key expiration
print("\n2. Testing key expiration:")
r.set('temp_key', 'will expire', ex=10)  # Expires in 10 seconds
ttl = r.ttl('temp_key')
print(f"TTL for temp_key: {ttl} seconds")

# Test lists
print("\n3. Testing Redis lists:")
r.rpush('btc_prices', '85000')
r.rpush('btc_prices', '86000')
prices = r.lrange('btc_prices', 0, -1)
print(f"BTC prices in list: {prices}")

# Test hashes
print("\n4. Testing Redis hashes:")
r.hset('trade_position', mapping={
    'symbol': 'BTCUSDT',
    'side': 'long',
    'entry_price': '85000',
    'size': '0.001'
})
position = r.hgetall('trade_position')
print(f"Trade position: {position}")

# Test sets
print("\n5. Testing Redis sets:")
r.sadd('active_traders', 'trader1', 'trader2', 'trader3')
traders = r.smembers('active_traders')
print(f"Active traders: {traders}")

# Test key patterns
print("\n6. Testing key patterns:")
keys = r.keys('*')
print(f"Found {len(keys)} keys")
print("First 5 keys:")
for key in keys[:5]:
    print(f"Key: {key}")

# Clean up test keys
r.delete('foo', 'temp_key', 'btc_prices', 'trade_position', 'active_traders') 