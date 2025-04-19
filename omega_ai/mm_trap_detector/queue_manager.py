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
Trap Queue Manager: Ensures trap queues remain at manageable sizes
with intelligent sampling and rate limiting.
"""

from typing import Dict, List, Any, Optional, Union, cast
import json
import random
import time
import logging
from datetime import datetime
from collections import defaultdict
from omega_ai.utils.redis_manager import RedisManager

logger = logging.getLogger(__name__)

class TrapQueueManager:
    """Manages market maker trap queues with intelligent sampling"""
    
    def __init__(self, redis_manager: Optional[RedisManager] = None):
        """Initialize the trap queue manager.
        
        Args:
            redis_manager: Optional RedisManager instance. If not provided,
                         a new instance will be created.
        """
        self.redis = redis_manager or RedisManager()
        
        # Queue configuration
        self.queue_name = "mm_trap_queue:zset"
        self.max_queue_size = 50000
        self.cleanup_threshold = 60000
        self.sampling_rate = 1.0  # 1.0 = keep all, 0.5 = keep 50%
        
        # Rate limiting
        self.last_add_time = time.time()
        self.min_interval = 0.01  # seconds between adds
    
    def add_trap(self, trap_data: Dict[str, Any]) -> bool:
        """Add a trap to the queue with rate limiting and sampling.
        
        Args:
            trap_data: Dictionary containing trap detection data
            
        Returns:
            bool: True if trap was added, False if skipped due to rate limiting
                 or sampling
        """
        # Apply rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_add_time
        if time_since_last < self.min_interval:
            return False
        
        # Check queue size and adjust sampling if needed
        queue_size = self.get_queue_size()
        
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
        
        # Add timestamp if not present
        if "timestamp" not in trap_data:
            trap_data["timestamp"] = datetime.now().isoformat()
            
        # Add to queue with current time as score
        try:
            result = self.redis.zadd(
                self.queue_name,
                {json.dumps(trap_data): time.time()}
            )
            
            # Redis zadd returns the number of new elements added
            # So if result > 0, it means the trap was added successfully
            success = result > 0
            
            # Check if cleanup needed
            if success and queue_size > self.cleanup_threshold:
                self.cleanup_queue()
            
            return success
            
        except Exception as e:
            logger.error(f"Error adding trap to queue: {e}")
            return False
    
    def get_recent_traps(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent traps from the queue.
        
        Args:
            limit: Maximum number of traps to return
            
        Returns:
            List of trap data dictionaries, ordered by most recent first
        """
        traps = self.redis.zrange(
            self.queue_name,
            0,
            limit - 1,
            desc=True
        )
        return [json.loads(cast(str, trap)) for trap in traps] if traps else []
    
    def cleanup_queue(self) -> bool:
        """Clean up the queue to keep it at manageable size.
        
        Returns:
            bool: True if cleanup was successful
        """
        queue_size = self.get_queue_size()
        if queue_size > self.max_queue_size:
            # Remove oldest entries
            return bool(self.redis.zremrangebyrank(
                self.queue_name,
                0,
                -self.max_queue_size
            ))
        return True
    
    def get_queue_size(self) -> int:
        """Get the current size of the queue.
        
        Returns:
            int: Number of items in queue
        """
        return self.redis.zcard(self.queue_name) or 0
    
    def clear_queue(self) -> bool:
        """Clear all traps from the queue.
        
        Returns:
            bool: True if queue was cleared successfully
        """
        return bool(self.redis.delete(self.queue_name))
    
    def get_trap_distribution(self) -> Dict[str, int]:
        """Get distribution of trap types in the queue.
        
        Returns:
            Dict mapping trap types to their counts
        """
        distribution = defaultdict(int)
        traps = self.redis.zrange(self.queue_name, 0, -1, desc=True)
        
        for trap_json in traps:
            try:
                trap = json.loads(cast(str, trap_json))
                if "type" in trap:
                    distribution[trap["type"]] += 1
            except json.JSONDecodeError:
                continue
                
        return dict(distribution)
    
    def get_queue_stats(self) -> Dict[str, Union[int, float]]:
        """Get statistics about the queue.
        
        Returns:
            Dict containing queue statistics
        """
        queue_size = self.get_queue_size()
        
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
                oldest_time = float(oldest[0][1])
                newest_time = float(newest[0][1])
                stats["oldest_item_age"] = time.time() - oldest_time
                stats["newest_item_age"] = time.time() - newest_time
        
        return stats


# Create singleton instance
trap_queue_manager = TrapQueueManager()

def add_trap_to_queue(
    trap_type: str,
    confidence: float,
    price: float,
    data: Optional[Dict[str, Any]] = None
) -> bool:
    """Add a trap detection event to the queue using the manager.
    
    Args:
        trap_type: Type of trap detected (e.g. "bullish", "bearish")
        confidence: Confidence score of the detection (0.0-1.0)
        price: Price level where trap was detected
        data: Optional additional data to include
        
    Returns:
        bool: True if trap was added successfully
    """
    # Create trap data
    trap_data = {
        "type": trap_type,
        "confidence": confidence,
        "price": price,
        "timestamp": datetime.now().isoformat(),
    }
    
    # Add any additional data
    if data:
        trap_data.update(data)
    
    # Use the queue manager to add with rate limiting
    return trap_queue_manager.add_trap(trap_data)