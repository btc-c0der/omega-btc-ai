import redis
import json

# Connect to Redis
redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Fetch all keys
all_keys = redis_conn.keys("*")

# Create dictionary with values
redis_data = {key: redis_conn.lrange(key, 0, -1) if redis_conn.type(key) == "list" else redis_conn.get(key) for key in all_keys}

# Save to JSON
with open("omega_redis_data.json", "w") as f:
    json.dump(redis_data, f, indent=4)

print("✅ Redis Data Extracted: Saved as omega_redis_data.json")
