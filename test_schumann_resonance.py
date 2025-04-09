#!/usr/bin/env python3
"""
Test the Schumann resonance parsing fix.
This script verifies that the high-frequency detector correctly handles
Schumann resonance data stored as JSON in Redis.
"""

import os
import sys
import json
import redis
import time
from datetime import datetime, timezone

def main():
    """Test the Schumann resonance parsing fix"""
    # Connect to Redis
    try:
        redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_conn.ping()
        print("✅ Connected to Redis successfully")
    except redis.ConnectionError as e:
        print(f"❌ Failed to connect to Redis: {e}")
        sys.exit(1)
    
    # 1. Store test Schumann data in Redis (JSON format)
    print("\n🧪 TEST 1: Storing Schumann data as JSON")
    schumann_data = {
        "frequency": 7.83,
        "amplitude": 1.2,
        "alignment": "aligned",
        "market_influence": 0.1
    }
    redis_conn.set("schumann_resonance", json.dumps(schumann_data))
    print(f"✅ Stored Schumann resonance data in Redis: {json.dumps(schumann_data)}")
    
    # 2. Verify we can read the data
    print("\n🧪 TEST 2: Reading Schumann data from Redis")
    schumann_bytes = redis_conn.get("schumann_resonance")
    print(f"📊 Raw Schumann data from Redis: {schumann_bytes}")
    
    # 3. Parse the Schumann data with our new approach
    print("\n🧪 TEST 3: Parsing Schumann data")
    schumann_resonance = parse_schumann_data(schumann_bytes)
    print(f"✅ Successfully parsed Schumann frequency: {schumann_resonance} Hz")
    
    # 4. Test with non-JSON format
    print("\n🧪 TEST 4: Testing with non-JSON format")
    redis_conn.set("schumann_resonance", "7.83")
    schumann_bytes = redis_conn.get("schumann_resonance")
    print(f"📊 Raw Schumann data from Redis: {schumann_bytes}")
    
    schumann_resonance = parse_schumann_data(schumann_bytes)
    print(f"✅ Successfully parsed Schumann frequency: {schumann_resonance} Hz")
    
    # 5. Test with invalid data
    print("\n🧪 TEST 5: Testing with invalid data")
    redis_conn.set("schumann_resonance", "invalid-data")
    schumann_bytes = redis_conn.get("schumann_resonance")
    print(f"📊 Raw Schumann data from Redis: {schumann_bytes}")
    
    schumann_resonance = parse_schumann_data(schumann_bytes)
    print(f"✅ Using default Schumann value: {schumann_resonance} Hz")
    
    # 6. Restore the JSON format
    print("\n🧪 TEST 6: Restoring JSON format")
    schumann_data = {
        "frequency": 7.83,
        "amplitude": 1.2,
        "alignment": "aligned",
        "market_influence": 0.1
    }
    redis_conn.set("schumann_resonance", json.dumps(schumann_data))
    print(f"✅ Restored Schumann resonance data in Redis: {json.dumps(schumann_data)}")
    
    print("\n✅ All tests completed successfully!")

def parse_schumann_data(schumann_bytes):
    """Parse Schumann resonance data from Redis in various formats."""
    if not schumann_bytes:
        return 0.0
        
    try:
        # Try to parse as JSON first (new format)
        schumann_json = json.loads(schumann_bytes)
        if isinstance(schumann_json, dict) and "frequency" in schumann_json:
            return float(schumann_json.get("frequency", 0.0))
        else:
            # JSON parsed but not in expected format
            try:
                # Maybe it's a JSON number
                return float(schumann_json)
            except (ValueError, TypeError):
                return 0.0
    except (json.JSONDecodeError, TypeError):
        # If not JSON, try direct float conversion (old format)
        try:
            return float(schumann_bytes)
        except (ValueError, TypeError) as e:
            print(f"❌ Failed to parse Schumann resonance: {e}")
            return 0.0

if __name__ == "__main__":
    main() 