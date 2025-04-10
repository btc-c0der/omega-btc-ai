
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
from datetime import datetime
import sys
from typing import Dict, Any, List, Union

# ANSI colors for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def connect_redis() -> redis.Redis:
    """Establish connection to Redis."""
    try:
        r = redis.StrictRedis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )
        r.ping()  # Test connection
        print(f"{GREEN}✓ Connected to Redis successfully{RESET}")
        return r
    except redis.ConnectionError as e:
        print(f"{RED}✗ Failed to connect to Redis: {e}{RESET}")
        sys.exit(1)

def safe_get_value(r: redis.Redis, key: str) -> Any:
    """Safely get value from Redis handling different data types."""
    try:
        # Try to get the type of the key
        key_type = r.type(key)
        
        if key_type == "string":
            return r.get(key)
        elif key_type == "list":
            return r.lrange(key, 0, -1)
        elif key_type == "hash":
            return r.hgetall(key)
        elif key_type == "set":
            return list(r.smembers(key))
        elif key_type == "zset":
            return r.zrange(key, 0, -1, withscores=True)
        else:
            print(f"{YELLOW}⚠️ Unsupported Redis type {key_type} for key {key}{RESET}")
            return None
    except redis.RedisError as e:
        print(f"{YELLOW}⚠️ Error getting value for key {key}: {e}{RESET}")
        return None

def extract_mm_traps(r: redis.Redis) -> Dict[str, Any]:
    """Extract all MM trap related data from Redis."""
    trap_data = {
        "mm_traps": [],
        "trap_detections": [],
        "trap_metrics": {},
        "timeframe_detections": {},
        "raw_data": {}  # Store raw data for unknown formats
    }
    
    try:
        # Get all keys that might contain trap data
        all_keys = list(r.scan_iter("*"))
        trap_keys = [k for k in all_keys if any(x in k.lower() for x in ["trap", "manipulation", "mm_"])]
        
        print(f"\n{CYAN}Found {len(trap_keys)} potential MM trap related keys{RESET}")
        
        for key in trap_keys:
            try:
                value = safe_get_value(r, key)
                if value is None:
                    continue
                    
                # Store raw data for analysis
                trap_data["raw_data"][key] = value
                
                # Try to parse known formats
                if key.startswith("mm_trap:"):
                    if isinstance(value, str):
                        try:
                            trap_data["mm_traps"].append({
                                "key": key,
                                "data": json.loads(value)
                            })
                        except json.JSONDecodeError:
                            trap_data["mm_traps"].append({
                                "key": key,
                                "data": value
                            })
                
                elif key == "mm_trap_detections":
                    if isinstance(value, list):
                        parsed_detections = []
                        for d in value:
                            try:
                                parsed_detections.append(json.loads(str(d)))
                            except json.JSONDecodeError:
                                parsed_detections.append(d)
                        trap_data["trap_detections"].extend(parsed_detections)
                
                elif key.startswith("mm_trap_detections:"):
                    timeframe = str(key).split(":")[-1]
                    if isinstance(value, list):
                        parsed_detections = []
                        for d in value:
                            try:
                                parsed_detections.append(json.loads(str(d)))
                            except json.JSONDecodeError:
                                parsed_detections.append(d)
                        trap_data["timeframe_detections"][timeframe] = parsed_detections
                
                elif "trap" in key.lower():
                    # Store metrics as is
                    trap_data["trap_metrics"][key] = value
                        
            except Exception as e:
                print(f"{YELLOW}⚠️ Error processing key {key}: {e}{RESET}")
                continue
                
        # Print summary
        print(f"\n{GREEN}✓ Extracted MM trap data summary:{RESET}")
        print(f"  • Individual traps: {len(trap_data['mm_traps'])}")
        print(f"  • Detection events: {len(trap_data['trap_detections'])}")
        print(f"  • Timeframe detections: {len(trap_data['timeframe_detections'])} timeframes")
        print(f"  • Additional metrics: {len(trap_data['trap_metrics'])} entries")
        print(f"  • Raw data entries: {len(trap_data['raw_data'])} keys")
        
        return trap_data
        
    except Exception as e:
        print(f"{RED}✗ Error extracting MM trap data: {e}{RESET}")
        return trap_data

def save_trap_data(data: Dict[str, Any]) -> None:
    """Save the extracted trap data to a JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"mm_trap_data_{timestamp}.json"
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n{GREEN}✓ MM trap data saved to {output_file}{RESET}")
    except Exception as e:
        print(f"{RED}✗ Error saving data to file: {e}{RESET}")

def main():
    """Main execution function."""
    print(f"\n{CYAN}🔍 Starting MM Trap Data Extraction...{RESET}")
    
    # Connect to Redis
    redis_conn = connect_redis()
    
    # Extract trap data
    trap_data = extract_mm_traps(redis_conn)
    
    # Save to file
    save_trap_data(trap_data)

if __name__ == "__main__":
    main()
