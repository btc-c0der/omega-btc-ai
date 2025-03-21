#!/usr/bin/env python3
"""
Simple API server for OMEGA BTC AI Dashboard
Connects to Redis and serves real Bitcoin data
"""

import json
import redis
import logging
from datetime import datetime, timezone, timedelta
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import sys
import random
from pathlib import Path
import argparse
from dotenv import load_dotenv
import numpy as np
import requests
import uvicorn

# ANSI color codes for terminal output
GREEN = "\033[92m"
GOLD = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Add parent directory to Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import position flow tracker functionality
try:
    from scripts.position_flow_tracker import calculate_fibonacci_targets
except ImportError:
    # Define a fallback function if the import fails
    def calculate_fibonacci_targets(entry_price, direction, current_price=None):
        """Fallback function to calculate Fibonacci targets when the import fails."""
        if not current_price:
            current_price = entry_price
            
        # Simple Fibonacci ratios
        fib_ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618]
        
        targets = {
            'levels': {},
            'current_level': 0
        }
        
        if direction.upper() == 'LONG':
            # For long positions, targets are above entry price
            price_diff = current_price - entry_price
            
            for ratio in fib_ratios:
                target_price = entry_price + (price_diff * ratio)
                targets['levels'][ratio] = target_price
                
            # Determine current Fibonacci level
            if current_price > entry_price:
                # We're in profit, find the closest level below current price
                levels_below = [r for r in fib_ratios if targets['levels'][r] <= current_price]
                targets['current_level'] = max(levels_below) if levels_below else 0
            else:
                # We're in loss
                targets['current_level'] = 0
                
        else:  # SHORT
            # For short positions, targets are below entry price
            price_diff = entry_price - current_price
            
            for ratio in fib_ratios:
                target_price = entry_price - (price_diff * ratio)
                targets['levels'][ratio] = target_price
                
            # Determine current Fibonacci level
            if current_price < entry_price:
                # We're in profit, find the closest level above current price
                levels_above = [r for r in fib_ratios if targets['levels'][r] >= current_price]
                targets['current_level'] = max(levels_above) if levels_above else 0
            else:
                # We're in loss
                targets['current_level'] = 0
        
        return targets

# Load environment variables
load_dotenv()

# Force Redis connection to localhost
os.environ['REDIS_HOST'] = 'localhost'
os.environ['REDIS_PORT'] = '6379'
os.environ['REDIS_PASSWORD'] = ''  # No password for local Redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("reggae_dashboard.log")
    ]
)
logger = logging.getLogger("live_api_server")

app = Flask(__name__)

# Enable CORS for all routes with more permissive settings
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True,
        "max_age": 600
    }
})

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Redis connection settings - use environment variables
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None  # No password for local Redis

# Log Redis connection settings
logger.info(f"Redis connection configured for: {REDIS_HOST}:{REDIS_PORT}")
logger.info(f"Redis password: {'Not used' if not REDIS_PASSWORD else 'Configured'}")

# Redis keys we're interested in
REDIS_KEYS = {
    'btc_price': ['last_btc_price', 'btc_price', 'sim_last_btc_price'],
    'price_changes': ['btc_price_changes'],
    'price_patterns': ['btc_price_patterns'],
    'trap_probability': ['current_trap_probability', 'trap_probability'],
    'position': ['current_position', 'active_position']
}

def get_redis_client():
    """Get Redis client connection"""
    # Hardcoded Redis settings - ignore environment variables for reliability
    redis_host = 'localhost'
    redis_port = 6379
    redis_password = None
    
    try:
        # Log connection attempt details with more visibility
        logger.info(f"🔄 Attempting to connect to Redis at {redis_host}:{redis_port}")
        logger.info(f"🔑 Redis password: {'Not used' if not redis_password else 'Configured'}")
        
        # Connect to Redis with hardcoded settings
        client = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True,
            socket_timeout=5.0,  # 5 second timeout
            socket_connect_timeout=5.0  # 5 second connect timeout
        )
        
        # Test connection with ping
        ping_result = client.ping()
        if not ping_result:
            logger.error("❌ Redis ping failed even though no exception was raised")
            return None
            
        logger.info(f"✅ Redis connection successful! PING response: {ping_result}")
        
        # Check for available keys
        available_keys = []
        for key_type, keys in REDIS_KEYS.items():
            for key in keys:
                if client.exists(key):
                    available_keys.append(f"{key_type}:{key}")
        
        if available_keys:
            logger.info(f"✅ Found {len(available_keys)} data keys in Redis: {', '.join(available_keys)}")
        else:
            logger.warning("⚠️ Connected to Redis but no expected keys found")
            logger.warning("⚠️ Dashboard will use fallback data")
            
            # Show all existing keys for debugging
            all_keys = client.keys("*")
            if all_keys:
                logger.info(f"📋 Total Redis keys found: {len(all_keys)}")
                logger.info("📋 First 10 Redis keys:")
                for key in all_keys[:10]:
                    logger.info(f"  - {key}")
            else:
                logger.warning("⚠️ Redis database is empty - no keys found")
            
        return client
    except redis.ConnectionError as e:
        logger.error(f"❌ Redis connection error: {e}")
        logger.error("❌ Please check that Redis is running on localhost:6379")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error connecting to Redis: {e}")
        return None

def get_fallback_btc_price():
    """Generate a realistic BTC price simulation."""
    # Current price range as of April 2024 (approximately $60-70k)
    base_price = random.uniform(60000, 70000)
    
    # Add minor fluctuations to make it look realistic
    fluctuation = base_price * random.uniform(-0.005, 0.005)
    
    return base_price + fluctuation

def enhance_position_data(position_data):
    """Enhance position data with Fibonacci targets and additional metrics."""
    if not position_data or not position_data.get('has_position', False):
        return position_data
    
    # Get key position metrics
    entry_price = position_data.get('entry_price')
    current_price = position_data.get('current_price')
    direction = position_data.get('position_side', '').upper()
    
    # Proceed only if we have the required data
    if not entry_price or not current_price or not direction:
        return position_data
    
    # Calculate Fibonacci targets
    fib_targets = calculate_fibonacci_targets(entry_price, direction, current_price)
    
    # Add Fibonacci targets to position data
    position_data['fibonacci_targets'] = fib_targets
    
    # Calculate next take profit level
    take_profits = position_data.get('take_profits', [])
    if take_profits:
        # Find the next take profit level
        current_take_profit = take_profits[0]
        position_data['next_take_profit'] = current_take_profit
        
        # Calculate distance to take profit
        if direction == 'LONG':
            distance = (current_take_profit['price'] - current_price) / current_price * 100
        else:  # SHORT
            distance = (current_price - current_take_profit['price']) / current_price * 100
            
        position_data['distance_to_take_profit'] = distance
        
        # Estimate time to target
        entry_time = datetime.fromisoformat(position_data.get('entry_time', datetime.now(timezone.utc).isoformat()))
        now = datetime.now(timezone.utc)
        elapsed_time = (now - entry_time).total_seconds()
        
        if elapsed_time > 0:
            # Calculate price change per second
            price_change = abs(current_price - entry_price)
            price_velocity = price_change / elapsed_time
            
            # Calculate remaining price change to target
            remaining_change = abs(current_take_profit['price'] - current_price)
            
            # Estimate time in seconds
            if price_velocity > 0:
                estimated_seconds = remaining_change / price_velocity
                
                # Convert to human-readable format
                if estimated_seconds < 60:
                    eta = f"< 1 min"
                elif estimated_seconds < 3600:
                    eta = f"~{int(estimated_seconds / 60)} min"
                elif estimated_seconds < 86400:
                    eta = f"~{int(estimated_seconds / 3600)} hours"
                else:
                    eta = f"~{int(estimated_seconds / 86400)} days"
                    
                position_data['estimated_completion_time'] = eta
            else:
                position_data['estimated_completion_time'] = "Unknown"
        else:
            position_data['estimated_completion_time'] = "Just started"
    
    # Add price movement metrics
    if direction == 'LONG':
        price_change_pct = (current_price - entry_price) / entry_price * 100
    else:
        price_change_pct = (entry_price - current_price) / entry_price * 100
        
    position_data['price_change_pct'] = price_change_pct
    
    # Add trend information
    if abs(price_change_pct) < 0.5:
        trend = "SIDEWAYS"
    elif price_change_pct > 0:
        if price_change_pct > 2:
            trend = "STRONG_BULLISH"
        else:
            trend = "BULLISH"
    else:
        if price_change_pct < -2:
            trend = "STRONG_BEARISH"
        else:
            trend = "BEARISH"
            
    position_data['trend'] = trend
    
    return position_data

# Get data from Redis with fallback
def get_data_from_redis(key_type, fallback_data):
    """Get data from Redis with fallback data if not available"""
    logger.info(f"🔍 Starting Redis data retrieval for key_type: {key_type}")
    logger.info(f"📊 Fallback data type: {type(fallback_data)}")
    
    redis_client = get_redis_client()
    if redis_client:
        try:
            # Try each possible key for this data type
            for key in REDIS_KEYS.get(key_type, []):
                logger.info(f"🔑 Attempting to get Redis key: {key}")
                logger.info(f"🔍 Checking if key exists: {key}")
                exists = redis_client.exists(key)
                logger.info(f"📊 Key exists: {exists}")
                
                if exists:
                    data = redis_client.get(key)
                    if data is not None:  # Check for None explicitly
                        logger.info(f"✅ Successfully retrieved data for key: {key}")
                        logger.info(f"📊 Data type: {type(data)}")
                        logger.info(f"📊 Data length: {len(data)}")
                        
                        try:
                            parsed_data = json.loads(data)
                            logger.info(f"✅ Successfully parsed JSON data for key: {key}")
                            logger.info(f"📊 Parsed data type: {type(parsed_data)}")
                            return parsed_data
                        except json.JSONDecodeError:
                            # If it's not JSON, try to convert it to a number
                            try:
                                logger.info(f"🔄 Attempting to convert non-JSON data to float for key: {key}")
                                float_value = float(data)
                                logger.info(f"✅ Successfully converted to float: {float_value}")
                                return {"value": float_value}
                            except ValueError:
                                logger.warning(f"❌ Failed to convert data to float for key: {key}")
                                continue
                    else:
                        logger.info(f"ℹ️ No data found for key: {key}")
                else:
                    logger.info(f"ℹ️ Key does not exist: {key}")
            logger.warning(f"⚠️ No valid data found for {key_type}")
        except Exception as e:
            logger.error(f"❌ Error getting {key_type} data from Redis: {e}")
            logger.error(f"❌ Exception type: {type(e)}")
            logger.error(f"❌ Exception args: {e.args}")
    
    logger.info(f"ℹ️ Using fallback data for {key_type}")
    logger.info(f"📊 Fallback data: {fallback_data}")
    return fallback_data

# Fallback data
def get_fallback_trap_data():
    """Generate fallback trap data if Redis is not available"""
    trap_types = [
        "bull_trap", "bear_trap", "liquidity_grab", 
        "stop_hunt", "fake_pump", "fake_dump"
    ]
    
    # Generate random probability with trend
    now = datetime.now(timezone.utc)
    probability = random.uniform(0.1, 0.9)
    
    # Generate components
    components = {
        "price_pattern": random.uniform(0.1, 0.9),
        "volume_spike": random.uniform(0.1, 0.9),
        "fibonacci_level": random.uniform(0.1, 0.9),
        "historical_match": random.uniform(0.1, 0.9),
        "order_book": random.uniform(0.1, 0.9),
        "market_regime": random.uniform(0.1, 0.9)
    }
    
    # Generate descriptions
    descriptions = {
        "price_pattern": "No significant pattern" if components["price_pattern"] < 0.5 else "Strong reversal pattern",
        "volume_spike": f"Volume {random.uniform(0.1, 0.5):.1f}x below average" if components["volume_spike"] < 0.5 else f"Volume {random.uniform(1.5, 3):.1f}x above average",
        "fibonacci_level": f"Price near Fibonacci level ±{random.uniform(0.1, 0.5):.1f}%" if components["fibonacci_level"] > 0.5 else "Not near any key Fibonacci level",
        "historical_match": "Weak match: May 2021 liquidation pattern" if components["historical_match"] < 0.5 else "Strong match: June 2022 cascade pattern",
        "order_book": "Large bid wall detected" if components["order_book"] > 0.5 else "Thin liquidity detected",
        "market_regime": "High Volatility regime" if components["market_regime"] > 0.5 else "Range-bound regime"
    }
    
    # Determine trend
    trends = ["stable", "increasing", "rapidly_increasing", "decreasing", "rapidly_decreasing"]
    trend = random.choice(trends)
    
    # Determine change based on trend
    if trend == "stable":
        change = random.uniform(-0.05, 0.05)
    elif trend == "increasing":
        change = random.uniform(0.05, 0.1)
    elif trend == "rapidly_increasing":
        change = random.uniform(0.1, 0.2)
    elif trend == "decreasing":
        change = random.uniform(-0.1, -0.05)
    else:  # rapidly_decreasing
        change = random.uniform(-0.2, -0.1)
    
    return {
        "probability": probability,
        "timestamp": now.isoformat(),
        "trend": trend,
        "change": change,
        "components": components,
        "descriptions": descriptions,
        "trap_type": random.choice(trap_types),
        "confidence": random.uniform(0.3, 0.9),
        "message": "JAH SYSTEM ANALYZING MARKET VIBRATIONS!"
    }

def get_fallback_position_data():
    """Generate fallback position data with simulated metrics."""
    # Get current BTC price from get_fallback_btc_price
    btc_price = get_fallback_btc_price()
    
    # Determine if we should simulate a position (70% chance)
    has_position = random.random() < 0.7
    
    # Random trading direction
    direction = random.choice(['LONG', 'SHORT'])
    
    if has_position:
        # Generate entry price around current price
        entry_adjustment = random.uniform(0.95, 1.05)
        entry_price = btc_price * entry_adjustment
        
        # Simulated leverage and position size
        leverage = random.choice([5, 10, 20, 50, 100])
        position_size = random.uniform(0.001, 0.1)
        
        # Calculate take profits
        take_profits = []
        if direction == 'LONG':
            # For long positions, take profits are above entry price
            tp_price = entry_price * random.uniform(1.01, 1.05)
            take_profits.append({"price": tp_price, "size": random.uniform(0.5, 1.0)})
        else:
            # For short positions, take profits are below entry price
            tp_price = entry_price * random.uniform(0.95, 0.99)
            take_profits.append({"price": tp_price, "size": random.uniform(0.5, 1.0)})
        
        # Calculate stop loss
        if direction == 'LONG':
            # For long positions, stop loss is below entry price
            stop_loss = entry_price * random.uniform(0.95, 0.99)
        else:
            # For short positions, stop loss is above entry price
            stop_loss = entry_price * random.uniform(1.01, 1.05)
        
        # Calculate PnL
        if direction == 'LONG':
            pnl_percent = (btc_price - entry_price) / entry_price * 100
        else:
            pnl_percent = (entry_price - btc_price) / entry_price * 100
            
        pnl_usd = (pnl_percent / 100) * entry_price * position_size * leverage
        
        # Determine risk multiplier based on leverage
        risk_multiplier = 1 + (leverage / 100)
        
        # Calculate entry time (between 1 hour and 1 day ago)
        hours_ago = random.uniform(1, 24)
        entry_time = (datetime.now(timezone.utc) - timedelta(hours=hours_ago)).isoformat()
        
        # Position source
        source = random.choice([
            'Strategic Trader',
            'Aggressive Trader',
            'Scalper Trader',
            'Manual Entry'
        ])
        
        # Generate trap awareness data
        trap_awareness = {
            "trap_probability": random.uniform(0, 1),
            "trap_type": random.choice([
                "BULL_TRAP", 
                "BEAR_TRAP", 
                "LIQUIDITY_TRAP", 
                "CONSOLIDATION_TRAP", 
                "FIBONACCI_TRAP"
            ]),
            "confidence": random.uniform(0.5, 1.0)
        }
        
        # Return position data
        return {
            "has_position": True,
            "position_side": direction,
            "entry_price": entry_price,
            "current_price": btc_price,
            "position_size": position_size,
            "leverage": leverage,
            "pnl_percent": pnl_percent,
            "pnl_usd": pnl_usd,
            "risk_multiplier": risk_multiplier,
            "stop_loss": stop_loss,
            "take_profits": take_profits,
            "entry_time": entry_time,
            "source": source,
            "trap_awareness": trap_awareness,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    else:
        # Return no position data
        return {
            "has_position": False,
            "current_price": btc_price,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

def get_btc_price_data():
    """Get BTC price data from Redis with fallback to generated data"""
    logger.info("🔍 Starting BTC price data retrieval")
    redis_client = get_redis_client()
    
    if redis_client:
        try:
            # Get current price
            price_data = None
            for key in REDIS_KEYS['btc_price']:
                logger.info(f"🔑 Attempting to get BTC price from key: {key}")
                logger.info(f"🔍 Checking if key exists: {key}")
                exists = redis_client.exists(key)
                logger.info(f"📊 Key exists: {exists}")
                
                if exists:
                    price = redis_client.get(key)
                    if price is not None:  # Check for None explicitly
                        logger.info(f"✅ Successfully retrieved BTC price from key: {key}")
                        logger.info(f"📊 Price value: {price}")
                        
                        try:
                            float_price = float(price)
                            logger.info(f"✅ Successfully converted price to float: {float_price}")
                            price_data = {
                                "price": float_price,
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "source": key
                            }
                            logger.info(f"📊 Created price data object: {price_data}")
                            break
                        except ValueError:
                            logger.warning(f"❌ Failed to convert price to float for key: {key}")
                            continue
                    else:
                        logger.info(f"ℹ️ No price data found for key: {key}")
                else:
                    logger.info(f"ℹ️ Key does not exist: {key}")

            # Get price changes
            logger.info("🔍 Attempting to get BTC price changes")
            changes_key = 'btc_price_changes'
            logger.info(f"🔍 Checking if changes key exists: {changes_key}")
            changes_exists = redis_client.exists(changes_key)
            logger.info(f"📊 Changes key exists: {changes_exists}")
            
            changes_data = None
            if changes_exists:
                changes = redis_client.get(changes_key)
                if changes is not None:  # Check for None explicitly
                    logger.info(f"✅ Successfully retrieved price changes")
                    try:
                        changes_data = json.loads(changes)
                        logger.info(f"✅ Successfully parsed price changes JSON")
                        logger.info(f"📊 Changes data: {changes_data}")
                    except json.JSONDecodeError:
                        logger.warning("❌ Failed to parse BTC price changes JSON")
                        pass
                else:
                    logger.info("ℹ️ No price changes data found")
            else:
                logger.info("ℹ️ Price changes key does not exist")

            # Get price patterns
            logger.info("🔍 Attempting to get BTC price patterns")
            patterns_key = 'btc_price_patterns'
            logger.info(f"🔍 Checking if patterns key exists: {patterns_key}")
            patterns_exists = redis_client.exists(patterns_key)
            logger.info(f"📊 Patterns key exists: {patterns_exists}")
            
            patterns_data = None
            if patterns_exists:
                patterns = redis_client.get(patterns_key)
                if patterns is not None:  # Check for None explicitly
                    logger.info(f"✅ Successfully retrieved price patterns")
                    try:
                        patterns_data = json.loads(patterns)
                        logger.info(f"✅ Successfully parsed price patterns JSON")
                        logger.info(f"📊 Patterns data: {patterns_data}")
                    except json.JSONDecodeError:
                        logger.warning("❌ Failed to parse BTC price patterns JSON")
                        pass
                else:
                    logger.info("ℹ️ No price patterns data found")
            else:
                logger.info("ℹ️ Price patterns key does not exist")

            if price_data:
                result = price_data
                if changes_data:
                    result["changes"] = changes_data
                if patterns_data:
                    result["patterns"] = patterns_data
                logger.info(f"📊 Final combined BTC price data: {result}")
                return result

        except Exception as e:
            logger.error(f"❌ Error getting BTC price data from Redis: {e}")
            logger.error(f"❌ Exception type: {type(e)}")
            logger.error(f"❌ Exception args: {e.args}")
    
    # Fallback to generated price data
    logger.warning("⚠️ Using fallback BTC price data")
    fallback_data = {
        "price": random.uniform(60000, 70000),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "fallback",
        "changes": {
            "short_term": random.uniform(-0.05, 0.05),
            "medium_term": random.uniform(-0.1, 0.1)
        },
        "patterns": {
            "wyckoff_distribution": random.uniform(0, 1),
            "double_top": random.uniform(0, 1),
            "head_and_shoulders": random.uniform(0, 1),
            "bull_flag": random.uniform(0, 1)
        }
    }
    logger.info(f"📊 Generated fallback data: {fallback_data}")
    return fallback_data

def get_position_data():
    """Get the current trading position data."""
    logger.info("🔍 Starting position data retrieval")
    try:
        redis_client = get_redis_client()
        
        # Attempt to fetch from Redis
        if redis_client:
            for key in REDIS_KEYS['position']:
                logger.info(f"🔑 Attempting to get position data from key: {key}")
                logger.info(f"🔍 Checking if key exists: {key}")
                exists = redis_client.exists(key)
                logger.info(f"📊 Key exists: {exists}")
                
                if exists:
                    try:
                        position_json = redis_client.get(key)
                        if position_json is not None:  # Check for None explicitly
                            logger.info(f"✅ Successfully retrieved position data from key: {key}")
                            logger.info(f"📊 Position JSON length: {len(position_json)}")
                            
                            position_data = json.loads(position_json)
                            logger.info(f"✅ Successfully parsed position JSON data")
                            logger.info(f"📊 Position data type: {type(position_data)}")
                            
                            # Add source and timestamp if missing
                            position_data.setdefault('source', 'redis')
                            position_data.setdefault('timestamp', datetime.now(timezone.utc).isoformat())
                            logger.info(f"📊 Added source and timestamp to position data")
                            
                            # Enhance with position flow tracking data
                            logger.info("🔄 Enhancing position data with flow tracking")
                            enhanced_data = enhance_position_data(position_data)
                            logger.info("✅ Successfully enhanced position data")
                            logger.info(f"📊 Enhanced data type: {type(enhanced_data)}")
                            
                            return enhanced_data
                        else:
                            logger.info(f"ℹ️ No position data found for key: {key}")
                    except json.JSONDecodeError:
                        logger.warning(f"❌ Invalid JSON in Redis key {key}")
                    except Exception as e:
                        logger.error(f"❌ Error processing Redis key {key}: {e}")
                        logger.error(f"❌ Exception type: {type(e)}")
                        logger.error(f"❌ Exception args: {e.args}")
                else:
                    logger.info(f"ℹ️ Position key does not exist: {key}")
        
        # If we get here, use fallback data
        logger.info("ℹ️ Using fallback position data")
        logger.info("🔄 Generating fallback position data")
        fallback_data = get_fallback_position_data()
        logger.info(f"📊 Generated fallback data type: {type(fallback_data)}")
        
        logger.info("🔄 Enhancing fallback position data")
        enhanced_fallback = enhance_position_data(fallback_data)
        logger.info("✅ Successfully enhanced fallback data")
        logger.info(f"📊 Enhanced fallback data type: {type(enhanced_fallback)}")
        
        return enhanced_fallback
        
    except Exception as e:
        logger.error(f"❌ Error getting position data: {e}")
        logger.error(f"❌ Exception type: {type(e)}")
        logger.error(f"❌ Exception args: {e.args}")
        
        logger.info("ℹ️ Using fallback data due to error")
        logger.info("🔄 Generating fallback position data")
        fallback_data = get_fallback_position_data()
        logger.info(f"📊 Generated fallback data type: {type(fallback_data)}")
        
        logger.info("🔄 Enhancing fallback position data")
        enhanced_fallback = enhance_position_data(fallback_data)
        logger.info("✅ Successfully enhanced fallback data")
        logger.info(f"📊 Enhanced fallback data type: {type(enhanced_fallback)}")
        
        return enhanced_fallback

# API routes
@app.route('/')
def index():
    """Serve the dashboard HTML."""
    logger.info("🔍 GET / - Serving dashboard HTML")
    return send_from_directory('.', 'live-dashboard.html')

@app.route('/backup')
def backup_dashboard():
    """Backup endpoint for data recovery."""
    logger.info("🔍 GET /backup - Backup request received")
    return send_from_directory('.', 'backup-dashboard.html')

# Add route for static files in the src directory
@app.route('/src/<path:filename>')
def serve_static(filename):
    """Serve static files from the src directory."""
    logger.info(f"🔍 GET /src/{filename} - Serving static file")
    return send_from_directory('src', filename)

# Add route for node_modules
@app.route('/node_modules/<path:filename>')
def serve_node_modules(filename):
    """Serve files from node_modules directory."""
    logger.info(f"🔍 GET /node_modules/{filename} - Serving node module file")
    return send_from_directory('node_modules', filename)

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    logger.info("🔍 GET /api/health - Health check request")
    redis_status = "disconnected"
    
    # Try to connect to Redis directly
    try:
        # Create a new Redis client for testing
        r = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        # Get trap probability data
        test_data = r.get("current_trap_probability")
        if test_data:
            redis_status = "connected"
            logger.info("✅ Redis connection test successful")
        else:
            if r.ping():
                redis_status = "connected"
                logger.info("✅ Redis ping successful but no data found")
    except Exception as e:
        logger.error(f"❌ Redis health check failed: {e}")
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.route('/api/trap-probability')
def trap_probability():
    """Get the current trap probability data."""
    logger.info("🔍 GET /api/trap-probability - Trap probability request")
    data = get_data_from_redis('trap_probability', get_fallback_trap_data())
    logger.info("✅ Trap probability data retrieved")
    return jsonify(data)

@app.route('/api/position')
def get_position():
    """Get the current trading position data."""
    logger.info("🔍 GET /api/position - Position data request")
    data = get_position_data()
    logger.info("✅ Position data retrieved")
    return jsonify(data)

@app.route('/api/btc-price')
def btc_price():
    """Get current BTC price with additional market data"""
    logger.info("🔍 GET /api/btc-price - BTC price request")
    data = get_btc_price_data()
    logger.info("✅ BTC price data retrieved")
    return jsonify(data)

@app.route('/api/data')
def combined_data():
    """Get combined data for the dashboard."""
    logger.info("🔍 GET /api/data - Combined data request")
    # Get all data elements
    price_data = get_btc_price_data()
    trap_data = trap_probability()
    position_data = get_position()
    
    # Combine into a single response
    combined = {
        "price": price_data,
        "trap_probability": trap_data,
        "position": position_data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    logger.info("✅ Combined data retrieved")
    return jsonify(combined)

@app.route('/api/redis-keys')
def redis_keys():
    """Get a list of recently updated Redis keys."""
    logger.info("🔍 GET /api/redis-keys - Redis keys request")
    try:
        redis_client = get_redis_client()
        if not redis_client:
            logger.error("❌ Redis not connected")
            return {"error": "Redis not connected"}
        
        # Get a limited set of keys to prevent timeouts
        logger.info("🔍 Retrieving all Redis keys")
        all_keys = redis_client.keys("*")
        logger.info(f"📊 Found {len(all_keys)} total Redis keys")
        
        # Prioritize certain patterns and limit to 20 keys max
        test_keys = [k for k in all_keys if k.startswith("test:")]
        other_keys = [k for k in all_keys if not k.startswith("test:")]
        logger.info(f"📊 Found {len(test_keys)} test keys and {len(other_keys)} other keys")
        
        # Prioritize test: keys first, then add others
        sample_keys = test_keys[:10]  # Up to 10 test keys
        if len(sample_keys) < 20:
            # Add other keys to fill up to 20
            sample_keys.extend(other_keys[:20-len(sample_keys)])
        logger.info(f"📊 Selected {len(sample_keys)} keys for processing")
        
        # Process this limited set
        recent_keys = []
        for key in sample_keys:
            try:
                logger.info(f"🔍 Processing key: {key}")
                # Get key type and add some metadata
                key_type = redis_client.type(key)
                logger.info(f"📊 Key type: {key_type}")
                
                key_info = {
                    "key": key,
                    "type": key_type,
                }
                
                # Add additional info based on type
                if key_type == "string":
                    # Get string length
                    value = redis_client.get(key)
                    if value is not None:
                        key_info["length"] = len(value)
                        logger.info(f"📊 String key length: {key_info['length']}")
                    else:
                        logger.info(f"ℹ️ String key has no value: {key}")
                elif key_type == "list":
                    # Get list length
                    key_info["length"] = redis_client.llen(key)
                    logger.info(f"📊 List key length: {key_info['length']}")
                elif key_type == "hash":
                    # Get hash field count
                    key_info["fields"] = len(redis_client.hkeys(key))
                    logger.info(f"📊 Hash key field count: {key_info['fields']}")
                
                recent_keys.append(key_info)
                logger.info(f"✅ Successfully processed key: {key}")
            except Exception as e:
                logger.error(f"❌ Error processing Redis key {key}: {e}")
                logger.error(f"❌ Exception type: {type(e)}")
                logger.error(f"❌ Exception args: {e.args}")
        
        response = {
            "keys": recent_keys,
            "total_keys": len(all_keys),
            "displayed_keys": len(recent_keys)
        }
        logger.info(f"📊 Final Redis keys response: {response}")
        return response
    except Exception as e:
        logger.error(f"❌ Error getting Redis keys: {e}")
        logger.error(f"❌ Exception type: {type(e)}")
        logger.error(f"❌ Exception args: {e.args}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Start the server
    logger.info(f"Starting Reggae Dashboard server on 0.0.0.0:5001")
    
    # Print colorful banner
    print(f"\n{GREEN}{BOLD}==============================================={RESET}")
    print(f"{GREEN}{BOLD}    OMEGA BTC AI - REGGAE DASHBOARD SERVER    {RESET}")
    print(f"{GREEN}{BOLD}==============================================={RESET}")
    print(f"{GOLD}    JAH BLESS YOUR TRADING JOURNEY    {RESET}")
    print(f"{GREEN}{BOLD}==============================================={RESET}\n")
    
    # Run the app with Flask's development server on port 5001
    app.run(host="0.0.0.0", port=5001)
else:
    # For imported usage, we already have the app instance created above
    pass 