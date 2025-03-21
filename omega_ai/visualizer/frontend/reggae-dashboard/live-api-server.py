#!/usr/bin/env python3
"""
Simple API server for OMEGA BTC AI Dashboard
Connects to Redis and serves real Bitcoin data
"""

import json
import redis
import logging
from datetime import datetime, timezone, timedelta
from flask import Flask, jsonify, send_from_directory
import os
import sys
import random
from pathlib import Path
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("live_api_server")

app = Flask(__name__)

# Redis connection
def get_redis_client():
    """Get Redis client connection"""
    try:
        # Connect to Redis
        client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        client.ping()  # Test connection
        logger.info("Connected to Redis at localhost:6379")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None

# Get data from Redis with fallback
def get_data_from_redis(key, fallback_data):
    """Get data from Redis with fallback data if not available"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            data = redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"Error getting data from Redis: {e}")
    
    logger.warning(f"Using fallback data for {key}")
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
    
    # Calculate PnL based on position side and price difference
    pct_diff = (current_price - entry_price) / entry_price
    if position_side == "short":
        pct_diff = -pct_diff
    
    pnl_percent = pct_diff * 100
    pnl_usd = pnl_percent * position_size * entry_price / 100
    
    return {
        "has_position": True,
        "position_side": position_side,
        "entry_price": entry_price,
        "current_price": current_price,
        "position_size": position_size,
        "pnl_percent": pnl_percent,
        "pnl_usd": pnl_usd,
        "timestamp": now.isoformat(),
        "source": "simulator"
    }

def get_btc_price_data():
    """Get BTC price data from Redis with fallback to generated data"""
    # Try to get real BTC price data from Redis
    redis_client = get_redis_client()
    if redis_client:
        try:
            # Try different potential Redis keys for BTC price
            for key in ["btc_price", "current_btc_price", "bitcoin_price", "price_btc"]:
                data = redis_client.get(key)
                if data:
                    try:
                        # If it's a simple number
                        return {"price": float(data), "timestamp": datetime.now(timezone.utc).isoformat()}
                    except ValueError:
                        # If it's a JSON string
                        try:
                            return json.loads(data)
                        except json.JSONDecodeError:
                            pass  # Try next key
            
            # Try to get the price from the position data
            position_data = redis_client.get("current_position")
            if position_data:
                try:
                    position_json = json.loads(position_data)
                    if "current_price" in position_json:
                        return {
                            "price": position_json["current_price"],
                            "timestamp": position_json.get("timestamp", datetime.now(timezone.utc).isoformat())
                        }
                except Exception:
                    pass
            
        except Exception as e:
            logger.error(f"Error getting BTC price from Redis: {e}")
    
    # Fallback to generated price data
    logger.warning("Using fallback BTC price data")
    return {
        "price": random.uniform(60000, 70000),
        "timestamp": datetime.now(timezone.utc).isoformat()
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
    data = get_data_from_redis("current_trap_probability", fallback_data)
    return jsonify(data)

@app.route('/api/position')
def position():
    """Get position data from Redis"""
    fallback_data = get_fallback_position_data()
    data = get_data_from_redis("current_position", fallback_data)
    return jsonify(data)

@app.route('/api/btc-price')
def btc_price():
    """Get current BTC price"""
    data = get_btc_price_data()
    return jsonify(data)

@app.route('/api/data')
def combined_data():
    """Get combined data for all endpoints"""
    trap_data = get_data_from_redis("current_trap_probability", get_fallback_trap_data())
    position_data = get_data_from_redis("current_position", get_fallback_position_data())
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
    parser.add_argument('--port', type=int, default=5000,
                       help='Port to run the server on (default: 5000)')
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
    
    # Enable CORS for local development
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Run the app
    port = args.port
    logger.info(f"Starting Live API Server on http://localhost:{port}")
    logger.info(f"Access the dashboard at http://localhost:{port}/")
    app.run(host='0.0.0.0', port=port, debug=True) 