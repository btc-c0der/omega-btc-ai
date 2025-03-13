import redis
import json
import time

def get_redis_metrics_for_grafana_all_keys_info(redis_host='localhost', redis_port=6379, redis_password=None):
    """
    Connects to Redis, extracts all keys, all server info (from INFO command),
    and formats the data into a JSON structure suitable for Grafana.

    This version retrieves *all* keys in the Redis database and all server info
    from the INFO command, as requested, for use with Grafana, especially
    the Redis plugin.

    Args:
        redis_host (str): Redis server hostname or IP address.
        redis_port (int): Redis server port.
        redis_password (str, optional): Redis server password if authentication is required.

    Returns:
        str: JSON string containing Redis metrics (all keys and all info) for Grafana.
             Returns None if there's an error connecting to Redis.
    """

    try:
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        r.ping()  # Check connection
    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        return None

    metrics = {}
    timestamp = int(time.time())  # Unix timestamp for Grafana

    # 1. All Server Info (from INFO command)
    info = r.info()
    metrics['redis_full_info'] = info  # Include the entire info dictionary

    # 2. All Keys
    all_keys = []
    for key in r.scan_iter(match='*'):  # Retrieve all keys using SCAN
        all_keys.append(key)
    metrics['redis_keys'] = all_keys
    metrics['redis_key_count_all'] = len(all_keys) # Add a count of all keys for convenience

    # 3. Redis Version
    metrics['redis_version'] = info.get('redis_version')

    # 4. Role (Master/Slave/Sentinel - if applicable)
    metrics['redis_role'] = info.get('role', 'standalone')

    # Structure the data for Grafana
    grafana_data = {
        "metrics": metrics,
        "timestamp": timestamp
    }

    return json.dumps(grafana_data, indent=2) # Indent for readability


if __name__ == "__main__":
    # Configuration - Customize these values
    redis_host = 'localhost'  # Or your Redis server IP/hostname
    redis_port = 6379
    redis_password = None  # Set your Redis password if needed

    grafana_json_output = get_redis_metrics_for_grafana_all_keys_info(
        redis_host=redis_host,
        redis_port=redis_port,
        redis_password=redis_password
    )

    if grafana_json_output:
        print(grafana_json_output)
    else:
        print("Failed to retrieve Redis metrics.")


# --- How to use this with Grafana ---

# 1. Install required library:
#    pip install redis

# 2. Run this script:
#    python your_script_name.py

#    This will print a JSON output to your console.

# 3. Integrate with Grafana Redis Plugin (or other methods):

#    a) **Using the JSON output directly (less common for Redis Plugin):**
#       - You *could* potentially use a "JSON API" or "Simple JSON" data source in Grafana and
#         serve this JSON output (e.g., via a web server, or write to a file). However, the Grafana
#         Redis plugin is designed to directly query Redis.  Direct JSON ingestion of this kind
#         is less typical for the Redis plugin itself, but possible for generic Grafana JSON data sources.

#    b) **Understanding the Output for Redis Plugin Configuration:**
#       - The primary benefit of this script for the *Redis Plugin* is to *discover* keys and understand
#         the overall Redis server state.
#       - **Run the script and examine the JSON output.**
#       - You will find:
#         - `"redis_full_info"`:  This contains *all* the output from the Redis `INFO` command. You can
#           explore these metrics and decide which ones to visualize in Grafana using the Redis plugin.
#         - `"redis_keys"`: This is a *list of all keys* in your Redis instance. You can use these keys
#           as a starting point to decide which keys to monitor or query in your Grafana Redis panels.
#         - `"redis_key_count_all"`:  A simple count of all keys, which might be a useful overview metric.
#         - `"redis_version"`, `"redis_role"`: Basic server information.

#    c) **Using the Redis Plugin with Discovered Keys and Info:**
#       - In Grafana, add a "Redis" data source, configuring it to connect to your Redis server.
#       - When creating panels in Grafana with the Redis data source:
#         - For server-level metrics: Explore the available metrics provided by the Redis plugin,
#           which often mirrors or builds upon the `INFO` output. You now have the *full `INFO` output*
#           in the JSON from this script to see what's available.
#         - For key-level metrics: Use the *`redis_keys` list from the script's output* as a guide.  The
#           Redis plugin lets you query values for specific keys. You can copy keys from the `redis_keys`
#           list and use them in your Grafana panel queries with the Redis plugin to visualize key values,
#           lengths, types, etc.

# In essence, this script now acts as a *discovery and information gathering tool* to help you effectively
# use the Grafana Redis plugin. It provides you with the raw data (all keys and full INFO) that you can
# then leverage to build targeted and informative dashboards in Grafana using the Redis plugin.