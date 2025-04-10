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
Test data generator for OMEGA BTC AI Reggae Dashboard
Populates Redis with sample trap and position data for testing
"""

import argparse
import json
import random
import redis
import time
from datetime import datetime, timedelta


def generate_trap_data(probability=None):
    """Generate random trap probability data"""
    if probability is None:
        probability = random.uniform(0.2, 0.9)
    
    trap_types = [
        "bull_trap", "bear_trap", "liquidity_grab",
        "stop_hunt", "fake_pump", "fake_dump"
    ]
    
    # Only assign trap type if probability is high enough
    trap_type = random.choice(trap_types) if probability > 0.6 else None
    confidence = random.uniform(0.7, 0.95) if trap_type else 0.0
    
    # Generate component data
    volume_spike = random.uniform(0.2, 0.9)
    price_pattern = random.uniform(0.4, 0.95)
    market_sentiment = random.uniform(0.3, 0.8)
    fibonacci_level = random.uniform(0.3, 0.9)
    liquidity_concentration = random.uniform(0.3, 0.9)
    order_book_imbalance = random.uniform(0.3, 0.85)
    
    # Trend can be increasing, decreasing, or stable
    trends = ["increasing", "decreasing", "stable"]
    trend = random.choice(trends)
    
    return {
        "probability": probability,
        "trap_type": trap_type,
        "confidence": confidence,
        "components": {
            "volume_spike": {"value": volume_spike, "description": "Abnormal trading volume detected"},
            "price_pattern": {"value": price_pattern, "description": "Price pattern analysis"},
            "market_sentiment": {"value": market_sentiment, "description": "Crowd sentiment indicator"},
            "fibonacci_match": {"value": fibonacci_level, "description": "Fibonacci retracement correlation"},
            "liquidity_concentration": {"value": liquidity_concentration, "description": "Order book liquidity analysis"},
            "order_imbalance": {"value": order_book_imbalance, "description": "Bid/ask imbalance detection"}
        },
        "trend": trend
    }


def generate_position_data(has_position=None):
    """Generate random position data"""
    if has_position is None:
        has_position = random.choice([True, False])
    
    if not has_position:
        return {"has_position": False}
    
    # Generate random position data
    position_side = random.choice(["long", "short"])
    
    # Base price around $65k for BTC
    base_price = 65000
    entry_price = base_price + random.uniform(-2000, 2000)
    
    # Current price with some variation from entry
    price_change_pct = random.uniform(-0.05, 0.05)
    current_price = entry_price * (1 + price_change_pct)
    
    # Take profit and stop loss based on position side
    if position_side == "long":
        take_profit = entry_price * 1.05  # 5% profit target
        stop_loss = entry_price * 0.98    # 2% stop loss
    else:
        take_profit = entry_price * 0.95  # 5% profit target
        stop_loss = entry_price * 1.02    # 2% stop loss
    
    # Entry time in the last 24 hours
    hours_ago = random.randint(1, 24)
    entry_time = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
    
    # Position size between 0.1 and 2 BTC
    position_size = random.uniform(0.1, 2.0)
    
    # Leverage between 1x and 20x
    leverage = random.randint(1, 20)
    
    return {
        "has_position": True,
        "position_side": position_side,
        "entry_price": entry_price,
        "current_price": current_price,
        "take_profit": take_profit,
        "stop_loss": stop_loss,
        "position_size": position_size,
        "leverage": leverage,
        "entry_time": entry_time
    }


def populate_redis(redis_client, cycle_count=None, interval=1.0):
    """Populate Redis with test data"""
    count = 0
    
    try:
        while cycle_count is None or count < cycle_count:
            # Generate and store trap data
            trap_data = generate_trap_data()
            redis_client.set("current_trap_probability", json.dumps(trap_data))
            
            # Generate and store position data
            position_data = generate_position_data()
            redis_client.set("current_position", json.dumps(position_data))
            
            # Store current BTC price
            if position_data.get("current_price"):
                redis_client.set("last_btc_price", str(position_data["current_price"]))
            
            print(f"[{datetime.now().isoformat()}] Updated Redis with test data")
            print(f"  Trap probability: {trap_data['probability']:.2f}")
            if trap_data.get("trap_type"):
                print(f"  Trap type: {trap_data['trap_type']}")
            print(f"  Has position: {position_data['has_position']}")
            
            # Increment count and sleep
            count += 1
            if cycle_count is None or count < cycle_count:
                time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nStopping data generator")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate test data for Reggae Dashboard")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", type=int, default=6379, help="Redis port")
    parser.add_argument("--password", help="Redis password")
    parser.add_argument("--cycles", type=int, help="Number of update cycles (default: infinite)")
    parser.add_argument("--interval", type=float, default=1.0, help="Update interval in seconds")
    
    args = parser.parse_args()
    
    # Connect to Redis
    r = redis.Redis(
        host=args.host,
        port=args.port,
        password=args.password,
        decode_responses=True
    )
    
    # Test connection
    try:
        r.ping()
        print(f"Connected to Redis at {args.host}:{args.port}")
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
        exit(1)
    
    # Run the data generator
    populate_redis(r, args.cycles, args.interval) 