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
Producer for Market Maker Trap events, using sorted sets for better performance
"""

import redis
import json
import time
import datetime

# Connect to Redis
r = redis.Redis(
    host='localhost', 
    port=6379, 
    db=0,
    socket_timeout=2,
    socket_connect_timeout=2,
    health_check_interval=30
)

def add_trap_to_queue(trap_type, confidence, price, data=None):
    """Add a trap detection event to the queue using sorted sets"""
    queue_name = "mm_trap_queue:zset"  # Use the optimized sorted set queue
    
    # Create trap data
    trap_data = {
        "type": trap_type,
        "confidence": confidence,
        "price": price,
        "timestamp": datetime.datetime.now().isoformat(),
    }
    
    # Add any additional data
    if data:
        trap_data.update(data)
    
    # Convert to JSON
    json_data = json.dumps(trap_data)
    
    # Add to sorted set with current timestamp as score for ordering
    score = time.time()
    r.zadd(queue_name, {json_data: score})
    
    # Keep the queue size manageable - remove old items if too many
    queue_size = r.zcard(queue_name)
    if queue_size > 500000:  # Limit to 500K entries
        # Remove oldest entries (lowest scores)
        r.zremrangebyrank(queue_name, 0, queue_size - 500000)
    
    return True

# Example: To be called from your high_frequency_detector.py
def register_trap_detection(trap_type, confidence, price_change):
    """Register a trap detection event."""
    # Get current BTC price
    price = float(r.get("last_btc_price") or 0)
    
    # Add to queue
    add_trap_to_queue(
        trap_type=trap_type, 
        confidence=confidence,
        price=price,
        data={
            "price_change": price_change,
            "detected_by": "high_frequency_detector"
        }
    )
    
    # Also log directly to Redis (for immediate access by other components)
    r.set("last_trap_detection", json.dumps({
        "type": trap_type,
        "confidence": confidence,
        "price": price,
        "timestamp": datetime.datetime.now().isoformat(),
    }))
    
    # Increment the trap counter
    r.incr("trap_detection_count")
    
    # For high confidence traps, add to a special set
    if confidence > 0.8:
        r.incr("high_confidence_trap_count")