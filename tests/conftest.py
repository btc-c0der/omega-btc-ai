import os
import sys
import pytest
import redis
import fakeredis
import json
from datetime import datetime, timedelta
import random
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_redis():
    """Fixture to provide a fake Redis server for testing"""
    server = fakeredis.FakeServer()
    redis_client = fakeredis.FakeRedis(server=server, decode_responses=True)
    yield redis_client

@pytest.fixture
def mock_redis_with_data(mock_redis):
    """Fixture to provide a fake Redis server with sample BTC price data"""
    # Add current BTC price
    mock_redis.set("last_btc_price", "85000")
    mock_redis.set("last_btc_volume", "120.5")
    mock_redis.set("last_btc_update_time", str(datetime.now().timestamp()))
    
    # Add BTC price history
    base_price = 85000
    for i in range(50):
        # Add some random variation
        price_change = random.uniform(-200, 200)
        price = base_price + price_change
        # Add to history
        mock_redis.rpush("btc_movement_history", price)
        mock_redis.rpush("btc_volume_history", random.uniform(50, 150))
    
    # Add some fake traps
    trap_types = ["Bull Trap", "Bear Trap", "Liquidity Grab", "Stop Hunt", "Fake Pump"]
    for i in range(5):
        trap = {
            "type": random.choice(trap_types),
            "confidence": random.uniform(0.6, 0.9),
            "price": random.uniform(84000, 86000),
            "timestamp": (datetime.now() - timedelta(minutes=i*5)).isoformat()
        }
        mock_redis.lpush("recent_mm_traps", json.dumps(trap))
    
    yield mock_redis

@pytest.fixture
def sample_price_data():
    """Fixture to provide sample BTC price data"""
    base_price = 85000
    timestamps = []
    prices = []
    volumes = []
    
    now = datetime.now()
    
    for i in range(100):
        price_change = random.uniform(-500, 500) if i % 10 == 0 else random.uniform(-100, 100)
        price = base_price + price_change
        volume = random.uniform(50, 150)
        timestamp = now - timedelta(minutes=i*5)
        
        timestamps.append(timestamp)
        prices.append(price)
        volumes.append(volume)
    
    return {
        "timestamps": timestamps,
        "prices": prices,
        "volumes": volumes
    }

@pytest.fixture
def mock_btc_live_feed_data():
    """Fixture for mocking data produced by btc_live_feed.py"""
    prices = []
    volumes = []
    timestamps = []
    
    now = datetime.now()
    
    for i in range(100):
        timestamp = now - timedelta(minutes=i)
        price = 85000 * (1 + random.uniform(-0.01, 0.01))
        volume = random.uniform(1, 10)
        
        prices.append(price)
        volumes.append(volume)
        timestamps.append(timestamp)
    
    return {
        "prices": prices,
        "volumes": volumes,
        "timestamps": timestamps
    }

@pytest.fixture
def mock_trap_data():
    """Fixture for providing sample market maker trap data"""
    trap_types = ["Bull Trap", "Bear Trap", "Liquidity Grab", "Stop Hunt", "Fake Pump", "Fake Dump"]
    traps = []
    
    now = datetime.now()
    
    for i in range(10):
        trap = {
            "type": random.choice(trap_types),
            "confidence": random.uniform(0.5, 0.95),
            "price_level": 85000 * (1 + random.uniform(-0.03, 0.03)),
            "direction": random.choice(["up", "down"]),
            "timestamp": (now - timedelta(hours=random.randint(0, 48))).isoformat(),
            "volume_spike": random.uniform(1.2, 3.0),
            "timeframe": random.choice(["1m", "5m", "15m", "1h"]),
            "description": f"Test trap {i}"
        }
        traps.append(trap)
    
    return traps 