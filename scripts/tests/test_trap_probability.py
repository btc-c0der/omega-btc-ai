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
OMEGA BTC AI - Trap Probability Meter Test
==========================================

This script tests the Trap Probability Meter functionality by:
1. Generating mock trap probability data
2. Storing it in Redis for the meter to access
3. Running the trap probability meter to visualize the data

Usage:
    python scripts/test_trap_probability.py
"""

import json
import random
import redis
import subprocess
import sys
import time
from datetime import datetime, timedelta

# Redis connection parameters
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Mock data generation parameters
MOCK_DURATION_MINUTES = 60  # Generate 60 minutes of mock data
MOCK_INTERVAL_SECONDS = 10  # Generate a data point every 10 seconds
TREND_CHANGES = 3  # Number of trend changes in the mock data
TRAP_TYPES = ["liquidity_grab", "stop_hunt", "bull_trap", "bear_trap", "fake_pump", "fake_dump"]


def is_redis_running():
    """Check if Redis server is running."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        return r.ping()
    except redis.ConnectionError:
        return False


def generate_mock_price_data():
    """Generate mock BTC price data."""
    # Start with a realistic BTC price
    base_price = 85000.0
    
    # Add some randomness to create a realistic price curve
    now = datetime.now()
    prices = []
    
    # Generate data for the last hour with 10-second intervals
    for i in range(MOCK_DURATION_MINUTES * 60 // MOCK_INTERVAL_SECONDS):
        timestamp = now - timedelta(seconds=i * MOCK_INTERVAL_SECONDS)
        
        # Add some randomness to the price
        random_factor = random.uniform(-0.002, 0.002)  # 0.2% max change
        trend_factor = math.sin(i / 180 * math.pi) * 0.01  # Adds a sinusoidal trend
        
        # Calculate price with randomness and trend
        price = base_price * (1 + random_factor + trend_factor)
        
        prices.append({
            "timestamp": timestamp.isoformat(),
            "price": price
        })
    
    # Sort by timestamp (oldest first)
    prices.sort(key=lambda x: x["timestamp"])
    
    return prices


def generate_mock_volume_data(price_data):
    """Generate mock volume data based on price data."""
    volumes = []
    
    # Base volume
    base_volume = 100.0  # BTC
    
    for i, price_point in enumerate(price_data):
        timestamp = price_point["timestamp"]
        price = price_point["price"]
        
        # Add randomness to volume
        random_factor = random.uniform(0.5, 1.5)
        
        # Add spikes at certain points
        spike = 1.0
        if i % 60 == 0:  # Every ~10 minutes
            spike = random.uniform(2.0, 4.0)
        
        volume = base_volume * random_factor * spike
        
        volumes.append({
            "timestamp": timestamp,
            "volume": volume
        })
        
    return volumes


def generate_mock_trap_signals(price_data, volume_data):
    """Generate mock trap signals at certain points."""
    signals = []
    
    # Determine points for trap signals (approximately 3 traps in the dataset)
    trap_indices = random.sample(range(len(price_data)), 3)
    
    for idx in trap_indices:
        trap_type = random.choice(TRAP_TYPES)
        confidence = random.uniform(0.6, 0.95)
        timestamp = price_data[idx]["timestamp"]
        price = price_data[idx]["price"]
        
        signals.append({
            "timestamp": timestamp,
            "trap_type": trap_type,
            "confidence": confidence,
            "price": price
        })
    
    return signals


def generate_mock_fibonacci_levels(price_data):
    """Generate mock Fibonacci levels based on price data."""
    # Find max and min price in the data
    prices = [p["price"] for p in price_data]
    max_price = max(prices)
    min_price = min(prices)
    
    # Calculate the range
    price_range = max_price - min_price
    
    # Generate Fibonacci levels
    fib_levels = {
        "high": max_price,
        "low": min_price,
        "levels": {
            "0.0": max_price,
            "0.236": max_price - 0.236 * price_range,
            "0.382": max_price - 0.382 * price_range,
            "0.5": max_price - 0.5 * price_range,
            "0.618": max_price - 0.618 * price_range,
            "0.786": max_price - 0.786 * price_range,
            "1.0": min_price
        }
    }
    
    return fib_levels


def generate_mock_probability_data():
    """Generate mock trap probability data over time."""
    probabilities = []
    
    # Start with a moderate probability
    base_probability = 0.4
    
    # Define trend changes
    trend_points = [i * (MOCK_DURATION_MINUTES // TREND_CHANGES) for i in range(TREND_CHANGES)]
    trends = [random.uniform(-0.3, 0.3) for _ in range(TREND_CHANGES)]
    
    # Current timestamp
    now = datetime.now()
    
    # Generate data
    for i in range(MOCK_DURATION_MINUTES):
        timestamp = now - timedelta(minutes=MOCK_DURATION_MINUTES - i)
        
        # Determine current trend
        trend_idx = 0
        for j, point in enumerate(trend_points):
            if i >= point:
                trend_idx = j
        
        # Apply trend and randomness
        trend_effect = trends[trend_idx] * (i % (MOCK_DURATION_MINUTES // TREND_CHANGES)) / (MOCK_DURATION_MINUTES // TREND_CHANGES)
        random_effect = random.uniform(-0.05, 0.05)
        
        # Calculate probability
        probability = base_probability + trend_effect + random_effect
        
        # Ensure probability is between 0 and 1
        probability = max(0.05, min(0.95, probability))
        
        # Generate component probabilities
        components = {
            "price_pattern": random.uniform(0.2, 0.9),
            "volume_spike": random.uniform(0.2, 0.9),
            "fib_level": random.uniform(0.1, 0.8),
            "historical_match": random.uniform(0.2, 0.7),
            "order_book": random.uniform(0.3, 0.8),
            "market_regime": random.uniform(0.3, 0.7)
        }
        
        # Optionally add a detected trap
        trap_type = None
        confidence = 0.0
        
        # If probability is high, maybe detect a trap
        if probability > 0.7 and random.random() > 0.3:
            trap_type = random.choice(TRAP_TYPES)
            confidence = random.uniform(0.6, 0.9)
        
        # Create data point
        data_point = {
            "timestamp": timestamp.isoformat(),
            "probability": probability,
            "components": components
        }
        
        if trap_type:
            data_point["trap_type"] = trap_type
            data_point["confidence"] = confidence
        
        probabilities.append(data_point)
    
    return probabilities


def populate_redis_with_mock_data():
    """Populate Redis with mock data for testing."""
    try:
        # Connect to Redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        
        # Check connection
        if not r.ping():
            print("Error: Could not connect to Redis")
            return False
        
        # Generate price data
        price_data = generate_mock_price_data()
        
        # Store current price
        current_price = price_data[-1]["price"]
        r.set("btc_price", json.dumps({"price": current_price}))
        
        # Generate volume data
        volume_data = generate_mock_volume_data(price_data)
        
        # Store current volume and average
        volumes = [v["volume"] for v in volume_data]
        current_volume = volumes[-1]
        avg_volume = sum(volumes) / len(volumes)
        
        r.set("btc_volume_data", json.dumps({
            "current": current_volume,
            "average": avg_volume
        }))
        
        # Generate Fibonacci levels
        fib_levels = generate_mock_fibonacci_levels(price_data)
        r.set("btc_recent_high_low", json.dumps({
            "high": fib_levels["high"],
            "low": fib_levels["low"]
        }))
        
        # Generate mock price patterns
        patterns = {
            "wyckoff_distribution": random.uniform(0.3, 0.8),
            "double_top": random.uniform(0.2, 0.7),
            "head_and_shoulders": random.uniform(0.1, 0.6),
            "bull_flag": random.uniform(0.2, 0.7)
        }
        r.set("btc_price_patterns", json.dumps(patterns))
        
        # Generate mock historical matches
        r.set("btc_historical_matches", json.dumps({
            "match_score": random.uniform(0.4, 0.9),
            "match_type": "May 2021 liquidation"
        }))
        
        # Generate mock order book
        r.set("btc_order_book_summary", json.dumps({
            "largest_bid_wall": random.uniform(50, 150),
            "largest_ask_wall": random.uniform(50, 150),
            "total_bids": random.uniform(500, 1500),
            "total_asks": random.uniform(500, 1500)
        }))
        
        # Generate mock market regime
        regimes = ["high_volatility", "distribution", "bullish_trend", "sideways"]
        r.set("btc_market_regime", json.dumps({
            "regime": random.choice(regimes)
        }))
        
        # Generate mock price changes
        r.set("btc_price_changes", json.dumps({
            "short_term": random.uniform(-0.05, 0.05),
            "medium_term": random.uniform(-0.07, 0.07)
        }))
        
        # Generate trap probability history
        trap_probabilities = generate_mock_probability_data()
        
        # Store history
        for prob in trap_probabilities:
            r.lpush("trap_probability_history", json.dumps(prob))
        
        # Trim to keep a reasonable size
        r.ltrim("trap_probability_history", 0, 999)
        
        print(f"Successfully populated Redis with mock data")
        return True
        
    except Exception as e:
        print(f"Error populating Redis: {e}")
        return False


def run_trap_probability_meter():
    """Run the trap probability meter."""
    try:
        # Run the meter with a short interval and verbose mode
        cmd = [
            sys.executable,
            "-m", "omega_ai.tools.trap_probability_meter",
            "--interval", "3",
            "--verbose"
        ]
        
        print("Starting Trap Probability Meter...")
        print("Press Ctrl+C to stop")
        
        # Run the command
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\nStopped Trap Probability Meter")
    except Exception as e:
        print(f"Error running Trap Probability Meter: {e}")


def main():
    """Main function."""
    print("OMEGA BTC AI - Trap Probability Meter Test")
    print("==========================================")
    
    # Check if Redis is running
    print("Checking if Redis is running...")
    if not is_redis_running():
        print("Error: Redis server is not running!")
        print("Please start Redis server before running this script.")
        return 1
    
    print("Redis server is running.")
    
    # Populate Redis with mock data
    print("\nPopulating Redis with mock data...")
    if not populate_redis_with_mock_data():
        print("Failed to populate Redis with mock data.")
        return 1
    
    # Run the trap probability meter
    run_trap_probability_meter()
    
    return 0


if __name__ == "__main__":
    # Import math here to avoid issues when imported elsewhere
    import math
    sys.exit(main()) 