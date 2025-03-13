import redis
import sys
import json
import argparse
from datetime import datetime
from omega_ai.utils.redis_connection import RedisConnectionManager

def connect_to_redis():
    """Connect to Redis using RedisConnectionManager."""
    try:
        redis_manager = RedisConnectionManager()
        redis_manager.client.ping()
        return redis_manager
    except redis.ConnectionError:
        print("Error: Could not connect to Redis. Make sure Redis is running and accessible.")
        sys.exit(1)

def check_json_structure(data, expected_keys):
    if not isinstance(data, dict):
        return False, "Data is not a dictionary"
    missing_keys = [key for key in expected_keys if key not in data]
    if missing_keys:
        return False, f"Missing keys: {', '.join(missing_keys)}"
    return True, "Valid structure"

def check_trader_data(data):
    if not isinstance(data, dict):
        return False, "Data is not a dictionary"
    
    expected_profiles = ["strategic", "aggressive", "newbie", "scalper"]
    missing_profiles = [profile for profile in expected_profiles if profile not in data]
    if missing_profiles:
        return False, f"Missing trader profiles: {', '.join(missing_profiles)}"
    
    expected_keys = ["name", "capital", "pnl", "win_rate", "trades", "winning_trades", "losing_trades",
                     "emotional_state", "confidence", "risk_level", "positions", "trade_history", "achievements"]
    
    for profile, profile_data in data.items():
        if not isinstance(profile_data, dict):
            return False, f"Profile data for {profile} is not a dictionary"
        
        missing_keys = [key for key in expected_keys if key not in profile_data]
        if missing_keys:
            return False, f"Missing keys in {profile} profile: {', '.join(missing_keys)}"
    
    return True, "Valid trader data structure"

def check_battle_state(data):
    expected_keys = ["day", "session", "btc_price", "btc_history", "battle_active", "start_time", "timeline_events"]
    structure_valid, message = check_json_structure(data, expected_keys)
    if not structure_valid:
        return structure_valid, message
    
    if not isinstance(data["btc_history"], list):
        return False, "btc_history is not a list"
    
    if not all(isinstance(price, (int, float)) for price in data["btc_history"]):
        return False, "btc_history contains non-numeric values"
    
    return True, "Valid battle state structure"

def check_battle_state(data):
    expected_keys = ["day", "session", "btc_price", "btc_history", "battle_active", "start_time", "timeline_events"]
    return check_json_structure(data, expected_keys)

def check_redis_data(show_content=False, fix_issues=False):
    redis_manager = connect_to_redis()
    
    keys_to_check = {
        "omega:live_trader_data": {"type": "string", "structure": "json", "checker": check_trader_data},
        "omega:live_battle_state": {"type": "string", "structure": "json", "checker": check_battle_state},
        "omega:start_trading": {"type": "string", "structure": "simple"}
    }
    
    results = {}
    issues_found = False

    print("Performing comprehensive Redis health check:")
    for key, expected in keys_to_check.items():
        print(f"\nChecking {key}:")
        if redis_manager.client.exists(key):
            value = redis_manager.get(key)
            results[key] = {"status": "present", "issues": []}
            
            # Check type
            if expected["type"] == "string" and isinstance(value, str):
                print(f"  ✅ Type: Correct (string)")
            else:
                print(f"  ❌ Type: Incorrect (expected string, got {type(value)})")
                results[key]["issues"].append("Incorrect type")
            
            # Check structure
            if expected["structure"] == "json":
                try:
                    json_data = json.loads(value)
                    print(f"  ✅ Structure: Valid JSON")
                    if "checker" in expected:
                        is_valid, message = expected["checker"](json_data)
                        if is_valid:
                            print(f"  ✅ Content: {message}")
                        else:
                            print(f"  ❌ Content: {message}")
                            results[key]["issues"].append(f"Invalid content: {message}")
                    if show_content:
                        print(f"  Content: {json.dumps(json_data, indent=2)}")
                except json.JSONDecodeError:
                    print(f"  ❌ Structure: Invalid JSON")
                    results[key]["issues"].append("Invalid JSON")
            elif expected["structure"] == "simple":
                print(f"  ✅ Structure: Simple string")
                if show_content:
                    print(f"  Content: {value}")
            
            if results[key]["issues"]:
                issues_found = True
        else:
            print(f"  ❌ Key is missing")
            results[key] = {"status": "missing", "issues": ["Key not found"]}
            issues_found = True
        
        if fix_issues and results[key]["issues"]:
            print(f"  🔧 Attempting to fix issues for {key}")
            print(f"  ⚠️ Automatic fixing not implemented for {key}")
    
    print("\nHealth Check Summary:")
    for key, result in results.items():
        status = "✅ Healthy" if not result["issues"] else f"❌ Issues found: {', '.join(result['issues'])}"
        print(f"{key}: {status}")
    
    if issues_found:
        print("\n⚠️ Some issues were found. Please review and address them.")
    else:
        print("\n✅ All checks passed. Redis data is healthy.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform a health check on Redis data for Omega BTC AI")
    parser.add_argument("--show-content", action="store_true", help="Display the content of the keys")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues automatically")
    args = parser.parse_args()
    
    check_redis_data(args.show_content, args.fix)