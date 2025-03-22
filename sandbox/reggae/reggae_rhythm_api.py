#!/usr/bin/env python3
"""
OMEGA BTC AI - REGGAE RHYTHM API with WebSocket Integration
==========================================================

A Flask API that connects the HTML UI to the rhythm pattern analysis
functionality with real-time WebSocket updates.

Usage:
    python reggae_rhythm_api.py [--port PORT]

Options:
    --port PORT     Port to run the API on (default: 5053)

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import asyncio
import subprocess
import argparse
import json
import websockets
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_file, render_template
import random
import math
from pathlib import Path
import requests

# Try to import matplotlib for visualization
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    print("Warning: matplotlib not available, visualization will be limited")
    HAS_MATPLOTLIB = False

# WebSocket integration with Big Brother
MM_WS_PORT = 8765
MM_WS_PATH = "/ws"
MM_WS_URL = f"ws://localhost:{MM_WS_PORT}{MM_WS_PATH}"

# Constants for reggae rhythm patterns
RHYTHM_PATTERNS = {
    "one_drop": [1, 0, 0, 0],  # Classic one drop pattern
    "rockers": [1, 0, 1, 0],  # Rockers rhythm
    "steppers": [1, 1, 1, 1],  # Four-to-the-floor steppers rhythm
    "nyabinghi": [1, 0, 1, 1],  # Nyabinghi rhythm
    "dub": [1, 0, 0, 1, 0, 1, 0, 0]  # Dub rhythm pattern
}

# Market state colors (Rastafarian)
MARKET_COLORS = {
    "uptrend": "#009900",  # Green for bullish trends
    "downtrend": "#CC0000",  # Red for bearish trends
    "consolidation": "#FFCC00",  # Yellow/Gold for sideways/consolidation
    "breakout": "#FF9900",  # Orange for breakouts
    "reversal": "#660099"  # Purple for reversals
}

# Initialize Flask application
app = Flask(__name__)

# Global variables for state tracking
current_btc_price = None
last_price_check = 0
price_history = []
detected_patterns = []
market_state = "consolidation"
babylon_alerts = []
reggae_signals = []
websocket_connected = False
ws_client = None

# Setup a cache directory for generated images
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def connect_to_websocket():
    """Set up WebSocket connection in a background thread."""
    global websocket_connected, ws_client
    
    async def websocket_client_loop():
        global websocket_connected, ws_client
        
        while True:
            try:
                async with websockets.connect(MM_WS_URL) as websocket:
                    ws_client = websocket
                    websocket_connected = True
                    print(f"✅ Connected to WebSocket server at {MM_WS_URL}")
                    
                    # Send initial message
                    await websocket.send(json.dumps({
                        "type": "reggae_dashboard_connected",
                        "timestamp": datetime.now().isoformat(),
                        "message": "REGGAE DASHBOARD connected and listening for the rhythm"
                    }))
                    
                    # Listen for messages
                    async for message in websocket:
                        try:
                            data = json.loads(message)
                            process_websocket_message(data)
                        except json.JSONDecodeError:
                            print(f"❌ Received invalid JSON: {message}")
                        except Exception as e:
                            print(f"❌ Error processing WebSocket message: {str(e)}")
            
            except websockets.exceptions.ConnectionClosedError:
                print(f"❌ WebSocket connection closed with error. Reconnecting...")
                websocket_connected = False
                ws_client = None
            except Exception as e:
                print(f"❌ WebSocket error: {str(e)}. Reconnecting...")
                websocket_connected = False
                ws_client = None
            
            # Wait before trying to reconnect
            await asyncio.sleep(5)
    
    def run_websocket_client():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websocket_client_loop())
    
    # Start WebSocket client in a background thread
    ws_thread = threading.Thread(target=run_websocket_client, daemon=True)
    ws_thread.start()

def process_websocket_message(data):
    """Process incoming WebSocket messages."""
    global current_btc_price, price_history, detected_patterns
    
    # Check message type
    msg_type = data.get('type', '')
    
    if msg_type == 'price_update' and 'price' in data:
        # Update price
        current_btc_price = float(data['price'])
        timestamp = datetime.now().isoformat()
        
        # Add to price history
        price_history.append({
            'price': current_btc_price,
            'timestamp': timestamp
        })
        
        # Keep only recent price history (last 1000 points)
        if len(price_history) > 1000:
            price_history = price_history[-1000:]
        
        # Check for rhythm patterns
        new_patterns = check_rhythm_patterns()
        if new_patterns:
            detected_patterns.extend(new_patterns)
            # Keep only the last 50 patterns
            if len(detected_patterns) > 50:
                detected_patterns = detected_patterns[-50:]
    
    elif msg_type == 'trader_update' and 'message' in data:
        # Process trader updates
        process_trader_message(data)

def process_trader_message(data):
    """Process trader messages for rhythm patterns."""
    message = data.get('message', '')
    
    # Check for Babylon system mentions
    babylon_keywords = ['central bank', 'fed', 'federal reserve', 'inflation', 'crash']
    if any(keyword in message.lower() for keyword in babylon_keywords):
        babylon_alerts.append({
            'message': f"Babylon System Alert: {message}",
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent alerts
        if len(babylon_alerts) > 20:
            babylon_alerts.pop(0)

def check_rhythm_patterns():
    """Analyze recent price movements for reggae rhythm patterns."""
    if len(price_history) < 16:
        return []  # Not enough data
    
    new_patterns = []
    
    # Get the last 16 price points
    recent_prices = [p['price'] for p in price_history[-16:]]
    
    # Convert to price movements (up=1, down=0)
    movements = []
    for i in range(1, len(recent_prices)):
        if recent_prices[i] > recent_prices[i-1]:
            movements.append(1)  # Price went up
        else:
            movements.append(0)  # Price went down or stayed the same
    
    # Check each pattern
    for pattern_name, pattern in RHYTHM_PATTERNS.items():
        pattern_len = len(pattern)
        
        # Sliding window over the movements to find matches
        for i in range(len(movements) - pattern_len + 1):
            window = movements[i:i+pattern_len]
            
            # Calculate match percentage
            matches = sum(1 for a, b in zip(window, pattern) if a == b)
            match_pct = (matches / pattern_len) * 100
            
            # If 75% match or better, consider it a pattern
            if match_pct >= 75:
                # Calculate strength based on price movement amplitude
                amplitude = max(recent_prices) - min(recent_prices)
                strength = min(100, (amplitude / recent_prices[-1]) * 100 * 2)
                
                new_patterns.append({
                    'pattern': pattern_name,
                    'strength': strength,
                    'match_pct': match_pct,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Generate reggae signal if strong pattern detected
                if match_pct >= 90 and strength >= 50:
                    generate_reggae_signal(pattern_name, strength)
                
                break  # Found a match, move to next pattern
    
    return new_patterns

def generate_reggae_signal(pattern_name, strength):
    """Generate trading signal based on reggae rhythm pattern."""
    global reggae_signals, market_state
    
    # Determine signal type based on pattern
    signal_type = ""
    if pattern_name == "one_drop":
        signal_type = "buy"  # One drop often signals good buying opportunity
        market_state = "uptrend"
    elif pattern_name == "rockers":
        signal_type = "hold"  # Rockers pattern suggests holding positions
        market_state = "consolidation"
    elif pattern_name == "steppers":
        signal_type = "bullish"  # Steppers pattern is highly bullish
        market_state = "uptrend"
    elif pattern_name == "nyabinghi":
        signal_type = "alert"  # Nyabinghi suggests paying attention
        market_state = "breakout"
    elif pattern_name == "dub":
        signal_type = "reversal"  # Dub patterns often precede reversals
        market_state = "reversal"
    
    # Create a signal message with Rastafarian flavor
    messages = {
        "buy": [
            "JAH BLESS! ONE DROP RHYTHM SAYS BUY NOW, SEEN?",
            "BABYLON SYSTEM FALLING, BUY DE BITCOIN MON!",
            "I AND I DETECTA STRONG BUY SIGNAL!"
        ],
        "hold": [
            "HODL STRONG, ROCKERS RHYTHM SAYS WAIT AND SEE",
            "NAH SELL YET MON, ROCKERS PATTERN HOLDS STEADY",
            "HOLD DE BITCOIN, JAH PROVIDES PATIENCE!"
        ],
        "bullish": [
            "STEPPERS RHYTHM STRONG! HIGHER HEIGHTS COMING!",
            "FORWARD EVER, BACKWARD NEVER! BITCOIN RISING!",
            "JAH LION ROARING! BTC READY TO JUMP UP!"
        ],
        "alert": [
            "NYABINGHI DRUMS BEATING! WATCH DE CHARTS MON!",
            "MARKET TENSION BUILDING, PREPARE FOR MOVEMENT",
            "BIG MOVES SOON COME! NYABINGHI RHYTHM DETECTED!"
        ],
        "reversal": [
            "DUB ECHO WARNING! PREPARE FOR DIRECTION CHANGE",
            "REVERB PATTERN SEEN, MARKET TURNING AROUND",
            "DUB MASTER SAYS: BE READY FOR SHIFT!"
        ]
    }
    
    # Select a random message for variety
    message = random.choice(messages[signal_type])
    
    # Add signal to list
    reggae_signals.append({
        'type': signal_type,
        'pattern': pattern_name,
        'strength': strength,
        'message': message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Keep only recent signals
    if len(reggae_signals) > 20:
        reggae_signals.pop(0)

def update_price_data():
    """Update price data periodically in a background thread."""
    global current_btc_price, last_price_check
    
    while True:
        try:
            # If we're connected to WebSocket, it will update prices
            if not websocket_connected:
                # Fallback: fetch price from API
                price = fetch_btc_price()
                if price:
                    current_btc_price = price
            
            # Run pattern detection
            if len(price_history) >= 16:
                check_rhythm_patterns()
            
            # Sleep for a while
            time.sleep(30)
        
        except Exception as e:
            print(f"Error in update_price_data: {str(e)}")
            time.sleep(30)

def fetch_btc_price():
    """Fetch the current BTC price from an exchange API."""
    try:
        # Try CoinGecko API
        response = requests.get(
            'https://api.coingecko.com/api/v3/simple/price',
            params={'ids': 'bitcoin', 'vs_currencies': 'usd'},
            timeout=10
        )
        data = response.json()
        if data and 'bitcoin' in data and 'usd' in data['bitcoin']:
            return float(data['bitcoin']['usd'])
    except Exception as e:
        print(f"Error fetching BTC price: {str(e)}")
        
        # Return simulated price for testing
        if current_btc_price:
            # Random walk from current price
            return current_btc_price * (1 + random.uniform(-0.005, 0.005))
        else:
            # Start with a reasonable BTC price
            return random.uniform(50000, 60000)
    
    return None

def generate_rhythm_visualization(pattern_name=None):
    """Generate visualization of detected rhythm patterns."""
    if not HAS_MATPLOTLIB:
        return None
    
    try:
        plt.figure(figsize=(12, 8))
        
        # Plot price history
        if len(price_history) > 0:
            prices = [p['price'] for p in price_history[-100:]]
            timestamps = [p['timestamp'] for p in price_history[-100:]]
            
            plt.plot(range(len(prices)), prices, 'b-', linewidth=2)
            
            # Add rhythm pattern highlights
            for pattern in detected_patterns[-10:]:
                pattern_time = datetime.fromisoformat(pattern['timestamp'])
                
                # Find closest data point
                closest_idx = 0
                for i, ts in enumerate(timestamps):
                    if datetime.fromisoformat(ts) >= pattern_time:
                        closest_idx = i
                        break
                
                # Highlight pattern region
                pattern_len = len(RHYTHM_PATTERNS[pattern['pattern']])
                if closest_idx - pattern_len >= 0:
                    start_idx = closest_idx - pattern_len
                    color = "green" if pattern['pattern'] in ['one_drop', 'steppers'] else "gold"
                    if pattern['pattern'] == 'dub':
                        color = "red"
                    
                    # Draw rectangle for pattern
                    min_price = min(prices[start_idx:closest_idx+1])
                    max_price = max(prices[start_idx:closest_idx+1])
                    plt.axvspan(start_idx, closest_idx, 
                               alpha=0.2, color=color)
                    
                    # Add pattern label
                    plt.text(start_idx, max_price, 
                            f"{pattern['pattern']} ({pattern['match_pct']:.0f}%)", 
                            fontsize=8, color=color)
            
            # Show current market state
            plt.title(f"BTC REGGAE RHYTHM ANALYSIS - Market State: {market_state.upper()}", 
                     color=MARKET_COLORS.get(market_state, 'blue'))
            
            # Add red/gold/green horizontal lines (Rastafarian colors)
            min_price = min(prices)
            max_price = max(prices)
            range_price = max_price - min_price
            
            plt.axhline(y=min_price + range_price * 0.236, color='red', linestyle='--', alpha=0.5)
            plt.axhline(y=min_price + range_price * 0.618, color='gold', linestyle='--', alpha=0.5)
            plt.axhline(y=min_price + range_price * 0.786, color='green', linestyle='--', alpha=0.5)
            
            # Add Rasta-style labels
            plt.text(len(prices) - 1, min_price + range_price * 0.236, 
                   "Red Support (0.236)", color='red', fontsize=8, ha='right')
            plt.text(len(prices) - 1, min_price + range_price * 0.618, 
                   "Gold Level (0.618)", color='goldenrod', fontsize=8, ha='right')
            plt.text(len(prices) - 1, min_price + range_price * 0.786, 
                   "Green Resistance (0.786)", color='green', fontsize=8, ha='right')
            
            # If specific pattern requested, show its rhythm
            if pattern_name and pattern_name in RHYTHM_PATTERNS:
                pattern = RHYTHM_PATTERNS[pattern_name]
                
                # Create small rhythm visualization in corner
                ax2 = plt.axes([0.75, 0.05, 0.2, 0.1])
                ax2.set_title(f"{pattern_name.capitalize()} Rhythm", fontsize=8)
                ax2.bar(range(len(pattern)), pattern, color='red')
                ax2.set_xlim(-0.5, len(pattern) - 0.5)
                ax2.set_ylim(0, 1.2)
                ax2.set_xticks([])
                ax2.set_yticks([])
        
        else:
            plt.text(0.5, 0.5, "Insufficient price data for visualization", 
                   ha='center', va='center', fontsize=12)
        
        # Save the visualization
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if pattern_name:
            filename = f"btc_reggae_rhythm_{pattern_name}_{timestamp}.png"
        else:
            filename = f"btc_reggae_rhythm_{timestamp}.png"
        
        filepath = os.path.join(CACHE_DIR, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    except Exception as e:
        print(f"Error generating visualization: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


# API Routes
@app.route('/')
def index():
    """Serve the main page."""
    return redirect('/reggae')

@app.route('/reggae')
def reggae_dashboard():
    """Serve the REGGAE DASHBOARD."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # We'll create this HTML file later
    return send_file(os.path.join(script_dir, 'reggae_dashboard.html'))

@app.route('/favicon.ico')
def favicon():
    """Serve favicon."""
    return "", 204  # No content

@app.route('/api/status')
def get_status():
    """Get the current status of the REGGAE DASHBOARD."""
    return jsonify({
        'current_price': current_btc_price,
        'market_state': market_state,
        'patterns_detected': len(detected_patterns),
        'signals_generated': len(reggae_signals),
        'babylon_alerts': len(babylon_alerts),
        'websocket_connected': websocket_connected,
        'last_updated': datetime.now().isoformat()
    })

@app.route('/api/patterns')
def get_patterns():
    """Get detected rhythm patterns."""
    return jsonify({
        'patterns': detected_patterns,
        'count': len(detected_patterns)
    })

@app.route('/api/signals')
def get_signals():
    """Get reggae trading signals."""
    return jsonify({
        'signals': reggae_signals,
        'count': len(reggae_signals)
    })

@app.route('/api/babylon_alerts')
def get_babylon_alerts():
    """Get Babylon system alerts."""
    return jsonify({
        'alerts': babylon_alerts,
        'count': len(babylon_alerts)
    })

@app.route('/api/price_history')
def get_price_history():
    """Get price history data."""
    # Determine how many points to return
    try:
        limit = int(request.args.get('limit', 100))
    except ValueError:
        limit = 100
    
    data = price_history[-limit:] if len(price_history) > limit else price_history
    
    return jsonify({
        'history': data,
        'count': len(data)
    })

@app.route('/api/visualization', methods=['GET'])
def get_visualization():
    """Generate and return a rhythm visualization."""
    pattern = request.args.get('pattern', None)
    
    # Generate visualization
    filepath = generate_rhythm_visualization(pattern)
    
    if filepath and os.path.exists(filepath):
        return send_file(filepath, mimetype='image/png')
    else:
        return "Error generating visualization", 500

@app.route('/api/pattern_info')
def get_pattern_info():
    """Get information about reggae rhythm patterns."""
    return jsonify({
        'patterns': {
            name: {
                'rhythm': pattern,
                'description': get_pattern_description(name)
            }
            for name, pattern in RHYTHM_PATTERNS.items()
        }
    })

def get_pattern_description(pattern_name):
    """Get a description of a reggae rhythm pattern."""
    descriptions = {
        'one_drop': "The classic 'one drop' rhythm with emphasis on the third beat, suggesting patient accumulation before sudden price rise.",
        'rockers': "The 'rockers' rhythm alternates strong beats, indicating regular oscillation between buying and selling pressure.",
        'steppers': "Four-to-the-floor 'steppers' rhythm represents steady upward momentum with regular buying volume.",
        'nyabinghi': "Ancient 'Nyabinghi' rhythm signals approaching market enlightenment or significant events.",
        'dub': "The spacious 'dub' pattern with heavy echo effects suggests price reversals and trend changes."
    }
    
    return descriptions.get(pattern_name, "No description available")

# Initialize WebSocket connection
connect_to_websocket()

# Start the price update thread
price_update_thread = threading.Thread(target=update_price_data, daemon=True)
price_update_thread.start()

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='OMEGA BTC AI - REGGAE RHYTHM API')
    parser.add_argument('--port', type=int, default=5053, help='Port to run the API on (default: 5053)')
    args = parser.parse_args()
    
    from flask import redirect
    
    # Run the Flask app
    print(f"Starting REGGAE RHYTHM API on port {args.port}")
    app.run(host='0.0.0.0', port=args.port, debug=True) 