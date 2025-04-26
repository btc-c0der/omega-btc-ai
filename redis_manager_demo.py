#!/usr/bin/env python3

import os
import sys
import asyncio
import json
from datetime import datetime
from omega_ai.mm_trap_detector.redis_manager_v2 import RedisManagerV2, RedisConfig

# Set environment variables for the local Redis container
os.environ['REDIS_HOST'] = 'localhost'
os.environ['REDIS_PORT'] = '6379'
os.environ['REDIS_PASSWORD'] = ''
os.environ['REDIS_SSL'] = 'false'

async def run_redis_operations():
    """Run various Redis operations using RedisManagerV2."""
    print("Initializing Redis Manager V2...")
    
    # Create custom config for the local Docker Redis
    config = RedisConfig(
        host='localhost',
        port=6379,
        password=None,
        ssl=False,
        decode_responses=True
    )
    
    # Initialize the manager with our config
    redis_manager = RedisManagerV2(config)
    print("Redis Manager V2 initialized")
    
    # Perform health check
    print("\nPerforming health check...")
    health_status = await redis_manager.health_check()
    print(f"Health check result: {json.dumps(health_status, indent=2)}")
    
    # Store trap probability data
    print("\nStoring trap probability data...")
    trap_data = {
        "probability": 0.78,
        "trap_type": "Bull Trap",
        "confidence": 0.85,
        "components": {
            "price_pattern": {
                "value": 0.82,
                "description": "Strong upward reversal"
            },
            "volume_spike": {
                "value": 0.73,
                "description": "Volume 2.2x above average"
            },
            "fib_level": {
                "value": 0.90,
                "description": "Price at key Fibonacci level (±0.1%)"
            },
            "historical_match": {
                "value": 0.65,
                "description": "Similar to April 2023 pattern"
            },
            "order_book": {
                "value": 0.76,
                "description": "Order book ask weighted (3.2x)"
            },
            "market_regime": {
                "value": 0.82,
                "description": "Distribution regime"
            }
        },
        "timestamp": datetime.now().isoformat(),
        "trend": "rapidly_increasing",
        "market_data": {
            "btc_price": 48751.25,
            "volume_24h": 3500000000,
            "rsi": 68,
            "macd": "bullish"
        }
    }
    success = await redis_manager.set_data("trap_prediction_v2", trap_data, expire=3600)
    print(f"Data stored successfully: {success}")
    
    # Retrieve the stored data
    print("\nRetrieving trap probability data...")
    retrieved_data = await redis_manager.get_data("trap_prediction_v2")
    print(f"Retrieved trap type: {retrieved_data.get('trap_type')}")
    print(f"Retrieved probability: {retrieved_data.get('probability')}")
    print(f"Component count: {len(retrieved_data.get('components', {}))}")
    
    # Publish a message to a channel
    print("\nPublishing message to channel...")
    message = {
        "event": "trap_detected",
        "trap_type": "Bull Trap",
        "probability": 0.78,
        "timestamp": datetime.now().isoformat()
    }
    await redis_manager.publish_message("trap_alerts", message)
    print("Message published")
    
    # Demonstrate memory optimization
    print("\nOptimizing Redis memory...")
    optimization_result = await redis_manager.optimize_memory()
    print(f"Memory optimization result: {json.dumps(optimization_result, indent=2)}")
    
    # Close connection
    print("\nClosing Redis connections...")
    await redis_manager.close()
    print("All connections closed")

if __name__ == "__main__":
    asyncio.run(run_redis_operations())