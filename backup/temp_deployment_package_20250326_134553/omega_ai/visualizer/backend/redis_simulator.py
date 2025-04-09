#!/usr/bin/env python3

"""
Redis Simulator for Reggae Dashboard

This script simulates Redis data for testing the Reggae Dashboard
without requiring an actual Redis server.
"""

import redis
import json
import time
import random
import os
from datetime import datetime, timezone
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("redis_simulator")

# Trap types
TRAP_TYPES = [
    "bull_trap", "bear_trap", "liquidity_grab", 
    "stop_hunt", "fake_pump", "fake_dump"
]

class RedisSimulator:
    """Simulates Redis data for the Reggae Dashboard"""
    
    def __init__(self):
        """Initialize the Redis simulator"""
        # Connect to Redis - use localhost explicitly
        self.redis_host = "localhost"
        self.redis_port = int(os.environ.get("REDIS_PORT", 6379))
        
        # Try to connect without password
        try:
            self.redis = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True
            )
            self.redis.ping()
            logger.info(f"Connected to Redis at {self.redis_host}:{self.redis_port}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            logger.info("Operating in simulation-only mode")
            self.redis = None
    
    def generate_trap_probability(self):
        """Generate a random trap probability and store in Redis"""
        # Generate random data
        probability = random.random()
        trap_type = random.choice(TRAP_TYPES)
        
        # Create data object
        data = {
            "probability": probability,
            "trap_type": trap_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "simulator"
        }
        
        # Store in Redis if connected
        if self.redis:
            try:
                self.redis.set("current_trap_probability", json.dumps(data))
                logger.info(f"Updated trap probability: {probability:.2f} ({trap_type})")
            except Exception as e:
                logger.error(f"Failed to update Redis: {e}")
        
        return data
    
    def generate_position_data(self):
        """Generate random position data and store in Redis"""
        # 20% chance of no position
        if random.random() < 0.2:
            data = {
                "has_position": False,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "simulator"
            }
        else:
            # Generate random position
            position_side = random.choice(["long", "short"])
            entry_price = random.uniform(50000, 70000)
            current_price = entry_price * random.uniform(0.95, 1.05)
            position_size = random.uniform(0.1, 2.0)
            
            # Calculate PnL
            if position_side == "long":
                pnl_percent = (current_price - entry_price) / entry_price * 100
            else:
                pnl_percent = (entry_price - current_price) / entry_price * 100
            
            pnl_usd = position_size * pnl_percent / 100
            
            data = {
                "has_position": True,
                "position_side": position_side,
                "entry_price": entry_price,
                "current_price": current_price,
                "position_size": position_size,
                "pnl_percent": pnl_percent,
                "pnl_usd": pnl_usd,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "simulator"
            }
        
        # Store in Redis if connected
        if self.redis:
            try:
                self.redis.set("current_position", json.dumps(data))
                status = f"{'⬆️' if data.get('position_side') == 'long' else '⬇️'}" if data.get("has_position") else "No position"
                logger.info(f"Updated position: {status}")
            except Exception as e:
                logger.error(f"Failed to update Redis: {e}")
        
        return data
    
    def run(self, interval=5):
        """Run the simulator continuously"""
        logger.info(f"Starting Redis simulator with {interval}s interval")
        
        try:
            while True:
                # Generate new data
                self.generate_trap_probability()
                self.generate_position_data()
                
                # Wait for the next update
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Simulator stopped by user")

if __name__ == "__main__":
    simulator = RedisSimulator()
    simulator.run() 