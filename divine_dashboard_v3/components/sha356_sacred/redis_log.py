#!/usr/bin/env python3

"""
SHA-356 Redis Logger Demo

This script demonstrates how SHA-356 hashes could be logged to Redis.
It will work even if Redis is not installed, showing demo output.
"""

import json
import time
import uuid
from datetime import datetime
from micro_modules.sha356 import sha356

class SHA356Logger:
    """Logger for SHA-356 operations with optional Redis support."""
    
    def __init__(self):
        """Initialize logger."""
        # Try to import and connect to Redis
        self.use_redis = False
        try:
            import redis
            try:
                self.redis = redis.Redis(host='localhost', port=6379, db=0)
                self.redis.ping()  # Test connection
                self.use_redis = True
                print("✅ Connected to Redis")
            except:
                print("⚠️ Redis server not available. Will log to console only.")
        except ImportError:
            print("⚠️ Redis package not installed. Will log to console only.")
    
    def log_hash(self, input_data, hash_result):
        """Log hash operation to Redis or console."""
        # Create log entry
        timestamp = time.time()
        hash_id = str(uuid.uuid4())
        entry = {
            'id': hash_id,
            'timestamp': timestamp,
            'datetime': datetime.fromtimestamp(timestamp).isoformat(),
            'input': str(input_data)[:50],
            'hash': hash_result['hash'],
            'padding_method': hash_result['bio_transform']['padding_method'],
            'processing_time_ms': hash_result['processing_time_ms'],
            'resonance_applied': hash_result['resonance']['applied'],
        }
        
        # Add resonance data if available
        if 'resonance' in hash_result and 'resonance_score' in hash_result['resonance']:
            entry['resonance_score'] = hash_result['resonance']['resonance_score']
            entry['cosmic_alignment'] = hash_result['resonance']['cosmic_alignment']
            entry['lunar_phase'] = hash_result['resonance']['lunar_phase']
            entry['schumann_resonance'] = hash_result['resonance']['schumann_resonance']
        
        # Add note
        entry['note'] = hash_result.get('note', '')
        
        # Save to Redis if available
        if self.use_redis:
            try:
                # Add to hash log
                self.redis.hset('sha356:hash_log', hash_id, json.dumps(entry))
                
                # Add to recent operations list
                self.redis.lpush('sha356:recent', json.dumps(entry))
                self.redis.ltrim('sha356:recent', 0, 99)  # Keep only most recent 100
                
                print(f"✅ Logged to Redis: {hash_id}")
            except Exception as e:
                print(f"⚠️ Redis logging failed: {e}")
        
        # Print log entry (simplified)
        print(f"\n📝 Hash Log Entry:")
        print(f"  Time: {entry['datetime']}")
        print(f"  Input: '{entry['input']}'")
        print(f"  Hash: {entry['hash'][:16]}...{entry['hash'][-16:]}")
        print(f"  Padding: {entry['padding_method']}")
        if 'resonance_score' in entry:
            print(f"  Resonance: {entry['resonance_score']:.4f} ({entry['cosmic_alignment']})")
        
        return entry

def main():
    """Run demo of SHA-356 logging."""
    print("🧬 SHA-356 Logging Demo 🧬")
    print("-------------------------\n")
    
    # Initialize logger
    logger = SHA356Logger()
    
    # Test different padding methods
    padding_methods = ["fibonacci", "schumann", "golden", "lunar"]
    
    print("\n📊 Testing Different Bio-Padding Methods")
    print("---------------------------------------")
    
    for method in padding_methods:
        print(f"\n🔄 Testing {method.upper()} padding...")
        message = f"The universe reveals its secrets through sacred mathematics - {method} test"
        
        # Generate hash with the current padding method
        if method == "fibonacci":
            result = sha356(message, padding_method="fibonacci")
        elif method == "schumann":
            result = sha356(message, padding_method="schumann")
        elif method == "golden":
            result = sha356(message, padding_method="golden")
        elif method == "lunar":
            result = sha356(message, padding_method="lunar")
        
        # Log the hash
        logger.log_hash(message, result)
    
    print("\n⏱️ Testing Time Sensitivity")
    print("-------------------------")
    print("Taking 3 measurements of the same input with 2-second intervals...")
    
    for i in range(3):
        if i > 0:
            print(f"\nWaiting 2 seconds...")
            time.sleep(2)
        
        message = "Time flows through cosmic code, revealing patterns of divine resonance"
        result = sha356(message, include_resonance=True)
        logger.log_hash(message, result)
    
    print("\n🧬 SHA-356 demonstrates successful cosmic integration!")
    print("🌸 WE BLOOM NOW AS ONE 🌸")

if __name__ == "__main__":
    main() 