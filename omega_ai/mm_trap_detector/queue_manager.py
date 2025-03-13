#!/usr/bin/env python3

"""
Trap Queue Manager: Ensures trap queues remain at manageable sizes
with intelligent sampling and rate limiting.
"""

import redis
import json
import random
import time
import datetime

class TrapQueueManager:
    """Manages market maker trap queues with intelligent sampling"""
    
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost', 
            port=6379, 
            db=0, 
            socket_connect_timeout=2,
            socket_keepalive=True
        )
        
        # Queue configuration
        self.queue_name = "mm_trap_queue:zset"
        self.max_queue_size = 50000
        self.cleanup_threshold = 60000
        self.sampling_rate = 1.0  # 1.0 = keep all, 0.5 = keep 50%
        
        # Rate limiting
        self.last_add_time = time.time()
        self.min_interval = 0.01  # seconds between adds
    
    def add_trap(self, trap_data):
        """Add a trap to the queue with rate limiting and sampling"""
        # Apply rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_add_time
        if time_since_last < self.min_interval:
            # Too many adds, sleep briefly
            time.sleep(self.min_interval - time_since_last)
        
        # Check queue size and adjust sampling if needed
        queue_size = self.redis.zcard(self.queue_name)
        
        # Update last add time
        self.last_add_time = time.time()
        
        # Dynamic sampling based on queue size
        if queue_size > 10000:
            # Reduce sampling rate as queue grows
            self.sampling_rate = min(1.0, 10000 / queue_size)
        else:
            self.sampling_rate = 1.0
        
        # Apply sampling (randomly skip some items when queue is large)
        if random.random() > self.sampling_rate:
            return False
        
        # Serialize trap data
        if isinstance(trap_data, dict):
            # Add timestamp if not present
            if "timestamp" not in trap_data:
                trap_data["timestamp"] = datetime.datetime.now().isoformat()
            json_data = json.dumps(trap_data)
        else:
            json_data = trap_data
        
        # Add to queue with current time as score
        self.redis.zadd(self.queue_name, {json_data: time.time()})
        
        # Check if cleanup needed
        if queue_size > self.cleanup_threshold:
            self._cleanup_queue()
        
        return True
    
    def _cleanup_queue(self):
        """Clean up the queue to keep it at manageable size"""
        queue_size = self.redis.zcard(self.queue_name)
        if queue_size > self.max_queue_size:
            # Remove oldest entries
            to_remove = queue_size - self.max_queue_size
            self.redis.zremrangebyrank(self.queue_name, 0, to_remove - 1)
    
    def get_queue_stats(self):
        """Get statistics about the queue"""
        queue_size = self.redis.zcard(self.queue_name)
        
        stats = {
            "queue_size": queue_size,
            "sampling_rate": self.sampling_rate,
            "max_size": self.max_queue_size,
            "cleanup_threshold": self.cleanup_threshold
        }
        
        # Get age of oldest and newest items
        if queue_size > 0:
            oldest = self.redis.zrange(self.queue_name, 0, 0, withscores=True)
            newest = self.redis.zrange(self.queue_name, -1, -1, withscores=True)
            
            if oldest and newest:
                oldest_time = oldest[0][1]
                newest_time = newest[0][1]
                stats["oldest_item_age"] = time.time() - oldest_time
                stats["newest_item_age"] = time.time() - newest_time
        
        return stats

# Create singleton instance
trap_queue_manager = TrapQueueManager()

# Exposed function for other modules to use
def add_trap_to_queue(trap_type, confidence, price, data=None):
    """Add a trap detection event to the queue using the manager"""
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
    
    # Use the queue manager to add with rate limiting
    return trap_queue_manager.add_trap(trap_data)