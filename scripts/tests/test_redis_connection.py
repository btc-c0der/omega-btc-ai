#!/usr/bin/env python3

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


"""
Test Redis connections for the OmegaBTC AI system

This script tests connections to both local and cloud Redis instances.
"""

import os
import sys
import argparse
import redis
import time
import json
from datetime import datetime

def test_local_redis():
    """Test connection to local Redis instance"""
    print("\n🏠 Testing LOCAL Redis connection...")
    
    connection_params = {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "decode_responses": True
    }
    
    try:
        # Create Redis connection
        r = redis.Redis(**connection_params)
        
        # Test ping
        start_time = time.time()
        r.ping()
        ping_time = time.time() - start_time
        
        print(f"✅ Successfully connected to local Redis")
        print(f"  • Ping time: {ping_time*1000:.2f}ms")
        
        # Test write/read
        key = f"test:local:{int(time.time())}"
        test_data = {
            "timestamp": datetime.now().isoformat(),
            "system": "local_test",
            "status": "active"
        }
        
        # Write test
        start_time = time.time()
        r.set(key, json.dumps(test_data))
        write_time = time.time() - start_time
        
        # Read test
        start_time = time.time()
        retrieved = r.get(key)
        read_time = time.time() - start_time
        
        # Clean up
        r.delete(key)
        
        print(f"✅ Successfully wrote and read test data")
        print(f"  • Write time: {write_time*1000:.2f}ms")
        print(f"  • Read time: {read_time*1000:.2f}ms")
        
        return True
    except redis.RedisError as e:
        print(f"❌ Error connecting to local Redis: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_cloud_redis(username='btc-omega-redis', password=None, ssl_cert=None):
    """Test connection to cloud Redis instance"""
    print("\n☁️ Testing CLOUD Redis connection...")
    
    if not password:
        password = os.environ.get('REDIS_PASSWORD', '')
        if not password:
            print("❌ No password provided for cloud Redis")
            print("   Please set REDIS_PASSWORD environment variable or provide with --password")
            return False
    
    # Set certificate file
    if not ssl_cert:
        ssl_cert = os.environ.get('REDIS_CA_CERT', 'SSL_redis-btc-omega-redis.pem')
    
    # Check if certificate file exists
    if not os.path.isfile(ssl_cert):
        print(f"⚠️ SSL certificate file not found: {ssl_cert}")
        print("  Continuing without certificate validation (not recommended for production)")
        ssl_cert = False
    
    connection_params = {
        "host": "172.16.8.2",
        "port": 6379,
        "username": username,
        "password": password,
        "decode_responses": True,
        "ssl": True
    }
    
    # Add certificate if available
    if ssl_cert:
        connection_params["ssl_ca_certs"] = ssl_cert
    
    try:
        # Create Redis connection
        r = redis.Redis(**connection_params)
        
        # Test ping
        start_time = time.time()
        r.ping()
        ping_time = time.time() - start_time
        
        print(f"✅ Successfully connected to cloud Redis")
        print(f"  • Ping time: {ping_time*1000:.2f}ms")
        print(f"  • SSL: {'Enabled with certificate' if ssl_cert else 'Enabled without certificate'}")
        
        # Test write/read
        key = f"test:cloud:{int(time.time())}"
        test_data = {
            "timestamp": datetime.now().isoformat(),
            "system": "cloud_test",
            "status": "active"
        }
        
        # Write test
        start_time = time.time()
        r.set(key, json.dumps(test_data))
        write_time = time.time() - start_time
        
        # Read test
        start_time = time.time()
        retrieved = r.get(key)
        read_time = time.time() - start_time
        
        # Clean up
        r.delete(key)
        
        print(f"✅ Successfully wrote and read test data")
        print(f"  • Write time: {write_time*1000:.2f}ms")
        print(f"  • Read time: {read_time*1000:.2f}ms")
        
        return True
    except redis.RedisError as e:
        print(f"❌ Error connecting to cloud Redis: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function to run the tests"""
    parser = argparse.ArgumentParser(description='Test Redis connections')
    parser.add_argument('--local', action='store_true', help='Test local Redis only')
    parser.add_argument('--cloud', action='store_true', help='Test cloud Redis only')
    parser.add_argument('--password', help='Password for cloud Redis')
    parser.add_argument('--cert', help='Path to SSL certificate file')
    
    args = parser.parse_args()
    
    # If no specific test is requested, run both
    run_local = args.local or not args.cloud
    run_cloud = args.cloud or not args.local
    
    # Track test results
    results = {}
    
    if run_local:
        results['local'] = test_local_redis()
    
    if run_cloud:
        results['cloud'] = test_cloud_redis(password=args.password, ssl_cert=args.cert)
    
    # Print summary
    print("\n📊 Test Summary:")
    for test, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  • {test.upper()} Redis: {status}")
    
    # Return exit code based on test results
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main()) 