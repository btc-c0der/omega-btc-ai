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
def get_position():
    """Return current position data with enhanced position flow tracking."""
    try:
        redis_client = get_redis_client()
        
        # Attempt to fetch from Redis
        if redis_client:
            for key in REDIS_KEYS['position']:
                if redis_client.exists(key):
                    try:
                        position_json = redis_client.get(key)
                        if position_json:  # Check that it's not None
                            position_data = json.loads(position_json)
                            
                            # Add source and timestamp if missing
                            position_data.setdefault('source', 'redis')
                            position_data.setdefault('timestamp', datetime.now(timezone.utc).isoformat())
                            
                            # Enhance with position flow tracking data
                            enhanced_data = enhance_position_data(position_data)
                            
                            return jsonify(enhanced_data)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in Redis key {key}")
                    except Exception as e:
                        logger.error(f"Error processing Redis key {key}: {e}")
        
        # If we get here, use fallback data
        logger.info("Using fallback position data")
        fallback_data = get_fallback_position_data()
        enhanced_fallback = enhance_position_data(fallback_data)
        return jsonify(enhanced_fallback)
        
    except Exception as e:
        logger.error(f"Error getting position data: {e}")
        fallback_data = get_fallback_position_data()
        enhanced_fallback = enhance_position_data(fallback_data)
        return jsonify(enhanced_fallback)

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

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Live API Server for OMEGA BTC AI Dashboard")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    parser.add_argument("--no-reload", action="store_true", help="Disable Flask auto-reloader")
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
    logger.info(f"Starting Live API Server on http://localhost:{args.port}")
    logger.info(f"Access the dashboard at http://localhost:{args.port}/")
    
    app.run(
        host="0.0.0.0",
        port=args.port,
        debug=True,
        use_reloader=not args.no_reload
    ) 