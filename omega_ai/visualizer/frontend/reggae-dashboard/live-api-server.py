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

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

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
    try:
        # Connect to Redis with environment settings
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
        
        # Test connection
        client.ping()
        
        # Check for available keys
        available_keys = []
        for key_type, keys in REDIS_KEYS.items():
            for key in keys:
                if client.exists(key):
                    available_keys.append(f"{key_type}:{key}")
        
        if available_keys:
            logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            logger.info(f"Found data keys: {', '.join(available_keys)}")
        else:
            logger.warning("Connected to Redis but no relevant data keys found")
            
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        logger.info("Using fallback data simulation")
        return None

# Get data from Redis with fallback
def get_data_from_redis(key_type, fallback_data):
    """Get data from Redis with fallback data if not available"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            # Try each possible key for this data type
            for key in REDIS_KEYS.get(key_type, []):
                data = redis_client.get(key)
                if data:
                    try:
                        return json.loads(data)
                    except json.JSONDecodeError:
                        # If it's not JSON, try to convert it to a number
                        try:
                            return {"value": float(data)}
                        except ValueError:
                            continue
            logger.warning(f"No valid data found for {key_type}")
        except Exception as e:
            logger.error(f"Error getting {key_type} data from Redis: {e}")
    
    logger.info(f"Using fallback data for {key_type}")
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
    """Generate fallback position data if Redis is not available"""
    now = datetime.now(timezone.utc)
    has_position = random.choice([True, False])
    
    if not has_position:
        return {
            "has_position": False,
            "timestamp": now.isoformat(),
            "source": "simulator"
        }
    
    position_side = random.choice(["long", "short"])
    entry_price = random.uniform(60000, 70000)
    current_price = entry_price * random.uniform(0.98, 1.02)
    position_size = random.uniform(0.1, 0.5)
    leverage = random.randint(1, 20)
    
    # Calculate PnL based on position side and price difference
    pct_diff = (current_price - entry_price) / entry_price
    if position_side == "short":
        pct_diff = -pct_diff
    
    pnl_percent = pct_diff * 100
    pnl_usd = pnl_percent * position_size * entry_price / 100
    
    # Generate take profit and stop loss levels
    take_profits = [
        {"price": entry_price * (1.02 if position_side == "long" else 0.98), "size": 0.5},
        {"price": entry_price * (1.05 if position_side == "long" else 0.95), "size": 0.3},
        {"price": entry_price * (1.08 if position_side == "long" else 0.92), "size": 0.2}
    ]
    
    stop_loss = entry_price * (0.98 if position_side == "long" else 1.02)
    
    return {
        "has_position": True,
        "position_side": position_side,
        "entry_price": entry_price,
        "current_price": current_price,
        "position_size": position_size,
        "leverage": leverage,
        "pnl_percent": pnl_percent,
        "pnl_usd": pnl_usd,
        "take_profits": take_profits,
        "stop_loss": stop_loss,
        "entry_time": (now - timedelta(hours=random.randint(1, 24))).isoformat(),
        "timestamp": now.isoformat(),
        "source": "simulator",
        "risk_multiplier": random.uniform(0.5, 1.5),
        "trap_awareness": {
            "trap_probability": random.uniform(0, 1),
            "trap_type": random.choice(["bull_trap", "bear_trap", "liquidity_grab", "stop_hunt", "fake_pump", "fake_dump"]),
            "confidence": random.uniform(0.3, 0.9)
        }
    }

def get_btc_price_data():
    """Get BTC price data from Redis with fallback to generated data"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            # Get current price
            price_data = None
            for key in REDIS_KEYS['btc_price']:
                price = redis_client.get(key)
                if price:
                    try:
                        price_data = {
                            "price": float(price),
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "source": key
                        }
                        break
                    except ValueError:
                        continue

            # Get price changes
            changes_data = None
            changes = redis_client.get('btc_price_changes')
            if changes:
                try:
                    changes_data = json.loads(changes)
                except json.JSONDecodeError:
                    pass

            # Get price patterns
            patterns_data = None
            patterns = redis_client.get('btc_price_patterns')
            if patterns:
                try:
                    patterns_data = json.loads(patterns)
                except json.JSONDecodeError:
                    pass

            if price_data:
                result = price_data
                if changes_data:
                    result["changes"] = changes_data
                if patterns_data:
                    result["patterns"] = patterns_data
                return result

        except Exception as e:
            logger.error(f"Error getting BTC price data from Redis: {e}")
    
    # Fallback to generated price data
    logger.warning("Using fallback BTC price data")
    return {
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

# API routes
@app.route('/')
def index():
    """Serve the live dashboard HTML file"""
    return send_from_directory('.', 'live-dashboard.html')

@app.route('/backup')
def backup_dashboard():
    """Serve the backup dashboard HTML file"""
    return send_from_directory('.', 'backup-dashboard.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    redis_client = get_redis_client()
    return jsonify({
        "status": "healthy",
        "redis": "connected" if redis_client else "disconnected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route('/api/trap-probability')
def trap_probability():
    """Get trap probability data from Redis"""
    fallback_data = get_fallback_trap_data()
    data = get_data_from_redis("trap_probability", fallback_data)
    return jsonify(data)

@app.route('/api/position')
def position():
    """Get position data from Redis"""
    fallback_data = get_fallback_position_data()
    data = get_data_from_redis("position", fallback_data)
    
    # Add trap probability data if available
    trap_data = get_data_from_redis("trap_probability", None)
    if trap_data and isinstance(data, dict) and data.get("has_position"):
        data["trap_awareness"] = {
            "trap_probability": trap_data.get("probability", 0),
            "trap_type": trap_data.get("trap_type"),
            "confidence": trap_data.get("confidence", 0),
            "components": trap_data.get("components", {}),
            "descriptions": trap_data.get("descriptions", {})
        }
    
    return jsonify(data)

@app.route('/api/btc-price')
def btc_price():
    """Get current BTC price with additional market data"""
    data = get_btc_price_data()
    return jsonify(data)

@app.route('/api/data')
def combined_data():
    """Get combined data for all endpoints"""
    trap_data = get_data_from_redis("trap_probability", get_fallback_trap_data())
    position_data = get_data_from_redis("position", get_fallback_position_data())
    price_data = get_btc_price_data()
    
    return jsonify({
        "trap_probability": trap_data,
        "position": position_data,
        "btc_price": price_data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Reggae Dashboard Server')
    parser.add_argument('--port', type=int, default=8080,
                       help='Port to run the server on (default: 8080)')
    args = parser.parse_args()
    
    # Determine directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if necessary HTML files exist
    if not os.path.exists("live-dashboard.html"):
        logger.warning("live-dashboard.html not found, will use backup if available")
        if not os.path.exists("backup-dashboard.html"):
            logger.error("No dashboard HTML files found in the current directory")
            sys.exit(1)
    
    # Log found dashboard files
    available_dashboards = []
    if os.path.exists("live-dashboard.html"):
        available_dashboards.append("live-dashboard.html")
    if os.path.exists("backup-dashboard.html"):
        available_dashboards.append("backup-dashboard.html")
    
    logger.info(f"Found dashboard files: {', '.join(available_dashboards)}")
    
    # Run the app
    port = args.port
    logger.info(f"Starting Live API Server on http://localhost:{port}")
    logger.info(f"Access the dashboard at http://localhost:{port}/")
    app.run(host='0.0.0.0', port=port, debug=True) 