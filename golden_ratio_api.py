#!/usr/bin/env python3
"""
OMEGA BTC AI - Golden Ratio Visualization API
==================================================

A Flask API that connects the HTML UI to the golden ratio visualization functionality.
"""

import os
import sys
import asyncio
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template
import threading
import time
import requests
import math
import json
from typing import Dict, Any, List, Optional

# Import the visualization functions from position_flow_tracker
from scripts.position_flow_tracker import visualize_golden_ratio_overlay, connect_to_redis

# Add new imports for live price tracking
import ccxt
from datetime import timedelta

# Constants for golden ratio tracking
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2  # ~1.618033988749895
FIBONACCI_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618]

# Global variables to cache data
current_btc_price = None
golden_price = None
last_price_update = None
price_history = []
golden_history = []
golden_state = "INITIALIZING"
last_fib_level_crossed = None

# Add trading data cache
trading_data_cache = {
    "positions": [],
    "elite_strategy": {
        "name": "OMEGA Elite Exit Strategy",
        "active_signals": [],
        "fibonacci_levels": [],
        "last_update": None
    },
    "take_profits": [],
    "last_update": None
}

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    """Serve the HTML UI."""
    return send_file('btc_golden_ratio_ui.html')

@app.route('/divine')
def divine_dashboard():
    """Serve the Divine Alignment Dashboard."""
    return send_file('divine_alignment_dashboard.html')

@app.route('/api/generate', methods=['POST'])
def generate_visualization():
    """Generate a new golden ratio visualization with the given parameters."""
    try:
        # Get parameters from request
        data = request.json or {}
        years = int(data.get('years', 7))
        use_redis = data.get('dataSource', 'redis') == 'redis'
        use_3d = data.get('mode', '2d') == '3d'
        
        # Create a timestamp for the output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"btc_golden_ratio_{years}yr_{timestamp}.png"
        
        # This part is tricky since we need to run an async function
        # We'll use a subprocess to run the CLI script instead
        cmd = [
            sys.executable,
            'scripts/position_flow_tracker.py',
            f'--years={years}'
        ]
        
        # Add appropriate flag based on visualization mode
        if use_3d:
            cmd.append('--golden-ratio-3d')
        else:
            cmd.append('--golden-ratio')
        
        if not use_redis:
            cmd.append('--no-redis')
            
        # Run the subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({
                'success': False,
                'error': f"Error generating visualization: {result.stderr}"
            }), 500
        
        # Find the latest generated file matching our pattern
        files = [f for f in os.listdir('.') if f.startswith(f'btc_golden_ratio_{years}yr_')]
        if not files:
            return jsonify({
                'success': False,
                'error': "No visualization file generated"
            }), 500
            
        # Get the most recent file
        latest_file = max(files, key=lambda f: os.path.getctime(f))
        
        return jsonify({
            'success': True,
            'file': f'/api/images/{latest_file}',
            'message': f"Visualization generated with {years} years of {'historical' if use_redis else 'simulated'} data."
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/images/<filename>')
def serve_image(filename):
    """Serve a generated image."""
    if os.path.exists(filename):
        return send_file(filename)
    else:
        return "Image not found", 404

@app.route('/api/generate/fallback')
def fallback_chart():
    """Provide a fallback golden ratio chart when real generation fails."""
    # Look for any existing golden ratio chart
    files = [f for f in os.listdir('.') if f.startswith('btc_golden_ratio_')]
    
    if files:
        # Use the most recent file
        latest_file = max(files, key=lambda f: os.path.getctime(f))
        return send_file(latest_file)
    
    # If no existing files, try to generate a new one with minimal parameters
    try:
        cmd = [
            sys.executable,
            'scripts/position_flow_tracker.py',
            '--golden-ratio',
            '--years=7',
            '--no-redis'
        ]
        
        subprocess.run(cmd, capture_output=True, timeout=30)
        
        # Check if we now have files
        files = [f for f in os.listdir('.') if f.startswith('btc_golden_ratio_')]
        if files:
            latest_file = max(files, key=lambda f: os.path.getctime(f))
            return send_file(latest_file)
    except Exception as e:
        print(f"Error generating fallback chart: {e}")
    
    # Ultimate fallback: return a 404 that the frontend will handle
    return "Fallback chart not available", 404

@app.route('/api/images/btc_golden_ratio_7yr_latest.png')
def serve_latest_chart():
    """Serve the most recent 7-year BTC golden ratio chart."""
    # Find the most recent btc_golden_ratio_7yr file
    files = [f for f in os.listdir('.') if f.startswith('btc_golden_ratio_7yr_')]
    
    if files:
        # Get the most recent file
        latest_file = max(files, key=lambda f: os.path.getctime(f))
        return send_file(latest_file)
    
    # If no existing file, try to generate a new one
    try:
        cmd = [
            sys.executable,
            'scripts/position_flow_tracker.py',
            '--golden-ratio',
            '--years=7'
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        
        if result.returncode == 0:
            # Find the newly generated file
            files = [f for f in os.listdir('.') if f.startswith('btc_golden_ratio_7yr_')]
            if files:
                latest_file = max(files, key=lambda f: os.path.getctime(f))
                return send_file(latest_file)
    except Exception as e:
        print(f"Error generating latest chart: {e}")
    
    # If we couldn't generate a new chart, return a 404
    return "Latest golden ratio chart not available", 404

def fetch_btc_price():
    """Fetch current BTC price from an exchange API with fallbacks."""
    # Try multiple API endpoints for redundancy
    
    # Attempt 1: CoinGecko API with proper error handling
    try:
        # Add a user-agent header to avoid getting blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        response = requests.get(
            'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd',
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'bitcoin' in data and 'usd' in data['bitcoin']:
                price = data['bitcoin']['usd']
                print(f"Successfully fetched BTC price from CoinGecko: ${price}")
                return float(price)
            else:
                print(f"Unexpected CoinGecko response format: {data}")
        else:
            print(f"CoinGecko API error: {response.status_code}")
    except Exception as e:
        print(f"Error with CoinGecko API: {e}")
    
    # Attempt 2: Try Binance API
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'price' in data:
                price = float(data['price'])
                print(f"Successfully fetched BTC price from Binance: ${price}")
                return price
            else:
                print(f"Unexpected Binance response format: {data}")
        else:
            print(f"Binance API error: {response.status_code}")
    except Exception as e:
        print(f"Error with Binance API: {e}")
    
    # Attempt 3: Alternative free API
    try:
        response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'amount' in data['data']:
                price = float(data['data']['amount'])
                print(f"Successfully fetched BTC price from Coinbase: ${price}")
                return price
            else:
                print(f"Unexpected Coinbase response format: {data}")
        else:
            print(f"Coinbase API error: {response.status_code}")
    except Exception as e:
        print(f"Error with Coinbase API: {e}")
    
    # Final fallback: Use a simulated price
    # Calculate a realistic simulated price based on time (varies by ±5% each day)
    days_since_halving = (datetime.now() - datetime(2024, 4, 20)).days
    base_price = 84000.0
    daily_factor = math.sin(days_since_halving * 0.3) * 0.05  # ±5% variation
    simulated_price = base_price * (1 + daily_factor)
    
    print(f"Using simulated BTC price: ${simulated_price:.2f}")
    return simulated_price

def calculate_golden_price():
    """Calculate the golden ratio price projection based on historical patterns."""
    global price_history, golden_history
    
    # If we don't have enough price history, use a simplified model
    if len(price_history) < 10:
        base_price = 84000  # Starting from approximate post-halving 2024 level
        days_since_halving = (datetime.now() - datetime(2024, 4, 20)).days
        
        # Apply golden ratio-based growth model
        # Using a simplified version of the golden ratio simulation
        growth_factor = 1 + ((GOLDEN_RATIO - 1) * 0.01)  # ~0.618% daily compounded growth
        current_golden = base_price * (growth_factor ** days_since_halving)
        return current_golden
    
    # For a more sophisticated model using actual price history
    # This would implement the golden ratio simulation from our main script
    # For now using a simplified version
    return price_history[-1] * GOLDEN_RATIO / 1.5  # Simplified projection

def determine_golden_state(price, golden_price):
    """Calculate if price is in positive vibration (GREEN_DIVINE) or trapped state (RED_TRAPPED)."""
    if price > golden_price:
        state = "GREEN_DIVINE"  # Above golden ratio line
        deviation = (price / golden_price - 1) * 100  # % above
    else:
        state = "RED_TRAPPED"  # Below golden ratio line
        deviation = (1 - price / golden_price) * 100  # % below
        
    return {
        "state": state,
        "deviation": deviation,
        "price": price,
        "golden_price": golden_price
    }

def check_fibonacci_crossings(current_price, previous_price, base_price=20000):
    """Check if price crossed any key fibonacci levels."""
    if previous_price is None:
        return None
    
    # Calculate Fibonacci levels from base price
    price_range = 100000 - base_price  # Approximate range from bottom to projected top
    fib_levels = {level: base_price + (level * price_range) for level in FIBONACCI_LEVELS}
    
    # Check for crossings
    for level_name, level_price in fib_levels.items():
        if (previous_price < level_price and current_price >= level_price) or \
           (previous_price > level_price and current_price <= level_price):
            direction = "UP" if current_price > previous_price else "DOWN"
            return {
                "level": level_name,
                "price": level_price,
                "direction": direction
            }
    
    return None

def update_price_data():
    """Background thread function to regularly update price data."""
    global current_btc_price, golden_price, last_price_update, price_history, golden_history, golden_state, last_fib_level_crossed
    
    while True:
        try:
            # Fetch current price
            previous_price = current_btc_price
            current_btc_price = fetch_btc_price()
            
            # Calculate golden price
            golden_price = calculate_golden_price()
            
            # Update tracking data
            now = datetime.now()
            last_price_update = now
            
            # Add to history (limit to 1000 points)
            price_history.append(current_btc_price)
            golden_history.append(golden_price)
            if len(price_history) > 1000:
                price_history.pop(0)
                golden_history.pop(0)
            
            # Calculate current state
            state_data = determine_golden_state(current_btc_price, golden_price)
            golden_state = state_data["state"]
            
            # Check for Fibonacci crossings
            crossing = check_fibonacci_crossings(current_btc_price, previous_price)
            if crossing:
                last_fib_level_crossed = crossing
                print(f"🔥 FIBONACCI CROSSING: Level {crossing['level']} ({crossing['price']}) crossed {crossing['direction']}")
            
            # Wait for next update (every 60 seconds)
            time.sleep(60)
            
        except Exception as e:
            print(f"Error in price update thread: {e}")
            time.sleep(60)  # Wait and try again

@app.route('/api/golden_status')
def golden_status():
    """Return current golden ratio status."""
    global current_btc_price, golden_price, last_price_update, golden_state, last_fib_level_crossed
    
    # If we haven't initialized price data yet
    if current_btc_price is None:
        current_btc_price = fetch_btc_price()
        golden_price = calculate_golden_price()
        last_price_update = datetime.now()
        state_data = determine_golden_state(current_btc_price, golden_price)
        golden_state = state_data["state"]
    
    # Calculate deviation (ensure golden_price is not None)
    if golden_price and current_btc_price:
        deviation = abs((current_btc_price / golden_price - 1) * 100)
    else:
        deviation = 0
    
    # Format the response
    response = {
        "price": current_btc_price,
        "golden_price": golden_price,
        "state": golden_state,
        "deviation": deviation,
        "last_update": last_price_update.isoformat() if last_price_update else None,
        "last_fib_crossing": last_fib_level_crossed,
        "fibonacci_levels": {
            "0.236": "First Awakening (~$19,885)",
            "0.382": "Manipulation Zone (~$30,193)",
            "0.5": "Balance Point (~$39,252)",
            "0.618": "Golden Reconnection (~$48,310)",
            "0.786": "Return to Light (~$61,207)",
            "1.0": "Crown Zone (~$77,635)",
            "1.618": "Divine Extension (~$97,000)"
        }
    }
    
    return jsonify(response)

@app.route('/api/trading_data')
def get_trading_data():
    """Return current trading data including positions and elite strategy info."""
    global trading_data_cache
    
    # If we need to refresh the data (30 second cache)
    current_time = datetime.now()
    if (trading_data_cache["last_update"] is None or 
        (current_time - trading_data_cache["last_update"]).total_seconds() > 30):
        
        # This would normally fetch from your trading system
        # For now, we'll simulate some data
        trading_data_cache = generate_trading_data(current_btc_price)
        trading_data_cache["last_update"] = current_time
    
    return jsonify(trading_data_cache)

def generate_trading_data(current_price: Optional[float] = None) -> Dict[str, Any]:
    """Generate or fetch current trading data."""
    if current_price is None:
        current_price = fetch_btc_price()
        
    # Calculate golden ratio-based take profit levels
    fib_levels = [0.618, 1.0, 1.618, 2.618]
    take_profit_base = current_price * 0.98  # Simulate entry slightly below current price
    
    # Generate simulated positions
    positions = [
        {
            "id": "omega-long-1",
            "symbol": "BTCUSDT",
            "side": "long",
            "entry_price": take_profit_base,
            "current_price": current_price,
            "size": 0.01,
            "leverage": 11,
            "pnl": (current_price - take_profit_base) * 0.01 * 11,
            "pnl_percent": ((current_price / take_profit_base) - 1) * 100 * 11,
            "status": "open",
            "open_time": (datetime.now() - timedelta(hours=4)).isoformat(),
            "take_profits": [
                {"level": "0.618", "price": take_profit_base * 1.02, "filled": False, "percentage": 33},
                {"level": "1.0", "price": take_profit_base * 1.035, "filled": False, "percentage": 33},
                {"level": "1.618", "price": take_profit_base * 1.055, "filled": False, "percentage": 34}
            ],
            "stop_loss": take_profit_base * 0.99,
            "type": "elite_fib"
        },
        {
            "id": "omega-short-1",
            "symbol": "BTCUSDT",
            "side": "short",
            "entry_price": take_profit_base * 1.01,
            "current_price": current_price,
            "size": 0.008,
            "leverage": 11,
            "pnl": (take_profit_base * 1.01 - current_price) * 0.008 * 11,
            "pnl_percent": ((take_profit_base * 1.01 / current_price) - 1) * 100 * 11,
            "status": "open",
            "open_time": (datetime.now() - timedelta(hours=2)).isoformat(),
            "take_profits": [
                {"level": "0.618", "price": take_profit_base * 0.992, "filled": False, "percentage": 50},
                {"level": "1.0", "price": take_profit_base * 0.985, "filled": False, "percentage": 50}
            ],
            "stop_loss": take_profit_base * 1.015,
            "type": "elite_trap"
        }
    ]
    
    # Calculate distance to take profit for each position
    for position in positions:
        for tp in position["take_profits"]:
            if position["side"] == "long":
                tp["distance_percent"] = ((tp["price"] / current_price) - 1) * 100
                tp["distance_price"] = tp["price"] - current_price
            else:
                tp["distance_percent"] = ((current_price / tp["price"]) - 1) * 100
                tp["distance_price"] = current_price - tp["price"]
                
            # Determine if this TP would be filled
            if position["side"] == "long":
                tp["filled"] = current_price >= tp["price"]
            else:
                tp["filled"] = current_price <= tp["price"]
    
    # Generate elite strategy info
    elite_strategy = {
        "name": "OMEGA Elite Exit Strategy",
        "mode": "Adaptive Fibonacci",
        "current_pattern": "Continuation",
        "trap_probability": 0.42,
        "active_signals": [
            {
                "name": "Fibonacci Expansion",
                "confidence": 0.89,
                "description": "Price approaching key 0.618 expansion level",
                "recommendation": "Partial take profit at $" + str(round(current_price * 1.02, 2))
            },
            {
                "name": "Golden Harmonic",
                "confidence": 0.76,
                "description": "Harmonic resonance between price and time",
                "recommendation": "Hold for continued alignment with divine pattern"
            }
        ],
        "fibonacci_levels": [
            {"name": "0.618", "price": current_price * 1.02, "significance": "Golden Ratio"},
            {"name": "1.0", "price": current_price * 1.035, "significance": "Full Extension"},
            {"name": "1.618", "price": current_price * 1.055, "significance": "Golden Ratio Extension"}
        ],
        "last_update": datetime.now().isoformat()
    }
    
    # Create fake trading history
    history = []
    for i in range(5):
        entry_price = current_price * (0.95 + (i * 0.01))
        exit_price = current_price * (0.96 + (i * 0.012))
        
        history.append({
            "id": f"omega-trade-{i+1}",
            "symbol": "BTCUSDT",
            "side": "long" if i % 2 == 0 else "short",
            "entry_price": entry_price if i % 2 == 0 else exit_price,
            "exit_price": exit_price if i % 2 == 0 else entry_price,
            "size": 0.01 - (i * 0.001),
            "pnl": (exit_price - entry_price) * (0.01 - (i * 0.001)) * 11 if i % 2 == 0 else (entry_price - exit_price) * (0.01 - (i * 0.001)) * 11,
            "open_time": (datetime.now() - timedelta(days=i, hours=i)).isoformat(),
            "close_time": (datetime.now() - timedelta(days=i, hours=i-2)).isoformat(),
            "exit_reason": "tp_hit" if i % 3 == 0 else ("stop_loss" if i % 3 == 1 else "manual")
        })
    
    return {
        "positions": positions,
        "elite_strategy": elite_strategy,
        "history": history,
        "total_pnl": sum(p["pnl"] for p in positions),
        "total_positions": len(positions),
        "current_price": current_price,
        "last_update": datetime.now().isoformat()
    }

@app.route('/assets/css/<filename>')
def serve_css(filename):
    """Serve CSS files from the assets directory."""
    # Try multiple possible paths
    possible_paths = [
        # Direct path relative to the script
        os.path.join(os.path.dirname(__file__), 'omega_ai/visualizer/frontend/assets/css', filename),
        # Path from project root
        os.path.join('omega_ai/visualizer/frontend/assets/css', filename),
        # Absolute path from project root
        os.path.abspath(os.path.join('omega_ai/visualizer/frontend/assets/css', filename))
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return send_file(path)
    
    # If we got here, the file wasn't found
    print(f"CSS file '{filename}' not found in any of these paths: {possible_paths}")
    return "CSS file not found", 404

if __name__ == '__main__':
    # Start background thread for price updates
    price_thread = threading.Thread(target=update_price_data, daemon=True)
    price_thread.start()
    
    print("Starting OMEGA BTC AI Golden Ratio Visualization API...")
    app.run(debug=True, host='0.0.0.0', port=5051) 