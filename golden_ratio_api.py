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
    import math
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

if __name__ == '__main__':
    # Start background thread for price updates
    price_thread = threading.Thread(target=update_price_data, daemon=True)
    price_thread.start()
    
    print("Starting OMEGA BTC AI Golden Ratio Visualization API...")
    app.run(debug=True, host='0.0.0.0', port=5051) 