#!/usr/bin/env python3
"""
OMEGA BTC AI - Golden Ratio Visualization API with Trader Personas
==================================================================

A Flask API that connects the HTML UI to the golden ratio visualization functionality.
This version includes trader personas integration for the Divine Alignment Dashboard.

Usage:
    python golden_ratio_api.py [--port PORT]

Options:
    --port PORT     Port to run the API on (default: 5051)

Changelog:
- Added port selection via command line argument
- Added trader personas endpoint
- Added a new footer section with trader information
- Modified server to run on port 5051
- Created as a sandbox version for development
"""

import os
import sys
import asyncio
import subprocess
import argparse
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template
import threading
import time
import requests
import math
import json
from typing import Dict, Any, List, Optional
import random

# Import the visualization functions from position_flow_tracker
# Comment out the problematic import
# from scripts.position_flow_tracker import visualize_golden_ratio_overlay, connect_to_redis

# Add new imports for visualization
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Add new imports for live price tracking
import ccxt
from datetime import timedelta

# Constants for golden ratio tracking
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2  # ~1.618033988749895
FIBONACCI_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618]

# Initialize Flask application
app = Flask(__name__)

# Global variables for state tracking
last_generated_image = None
last_price_check = 0
current_btc_price = None
golden_state = None
most_recent_crossing = None
price_history = []
last_saved_timestamp = None
most_recent_ratio_level = None
# Add trader persona state
trader_personas = {}

# Configure startup parameters
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')

# API roots for multiple services
TRADER_API_ROOT = os.environ.get('TRADER_API_ROOT', 'http://localhost:5000')
MONITOR_API_ROOT = os.environ.get('MONITOR_API_ROOT', 'http://localhost:5001')
VISUALIZATION_API_ROOT = os.environ.get('VISUALIZATION_API_ROOT', 'http://localhost:5002')

# Cache directory
CACHE_DIR = os.environ.get('CACHE_DIR', '/tmp/omega_btc_ai_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Create a mock visualization function to replace the imported one
async def visualize_golden_ratio_overlay(
    years=7, 
    output_path=None, 
    view_type="2d", 
    current_price=None, 
    **kwargs
):
    """
    Mock implementation of the golden ratio visualization function.
    Creates a simple chart showing BTC price with golden ratio levels.
    
    Args:
        years: Number of years to simulate in the chart
        output_path: Where to save the output image
        view_type: Type of visualization (2d or 3d)
        current_price: Current BTC price to highlight
    
    Returns:
        Path to generated image
    """
    try:
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Generate some mock data
        days = int(years * 365)  # Ensure days is an integer
        x = np.linspace(0, days, days)
        
        # Create a sine wave with upward trend and some noise to simulate BTC price
        noise = np.random.normal(0, 0.5, days)
        trend = np.linspace(0, 5, days)
        # Ensure price is a float
        price_value = float(current_price) if current_price is not None and current_price > 0 else 50000.0
        y = np.exp(0.7 * np.sin(x / 100) + trend) * 1000 + noise * 1000
        
        # If current price provided, make sure the last data point matches
        if price_value > 0:
            y[-1] = price_value
        
        # Calculate golden ratio levels
        GOLDEN_RATIO = (1 + 5 ** 0.5) / 2  # ~1.618033988749895
        base = float(min(y))
        max_val = float(max(y))
        range_val = max_val - base
        
        fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
        fib_lines = [base + (range_val * level) for level in fib_levels]
        
        # Plot the price curve
        plt.plot(x, y, 'b-', label='BTC Price')
        
        # Plot golden ratio levels
        for i, (level, price) in enumerate(zip(fib_levels, fib_lines)):
            color = f'C{i}'
            plt.axhline(y=float(price), color=color, linestyle='--', alpha=0.7, 
                        label=f'Fib {level} - ${float(price):,.0f}')
        
        # Mark current price if provided
        if price_value > 0:
            plt.scatter([float(days-1)], [price_value], color='red', s=100, zorder=5)
            plt.text(float(days-50), price_value, f'${price_value:,.0f}', 
                    fontsize=12, color='red')
        
        # Set labels and title
        plt.title(f'BTC Golden Ratio Analysis - {years} Year View', fontsize=16)
        plt.xlabel('Days', fontsize=12)
        plt.ylabel('Price (USD)', fontsize=12)
        
        # Use log scale for y-axis
        plt.yscale('log')
        
        # Add legend
        plt.legend(loc='upper left')
        
        # Add grid
        plt.grid(True, alpha=0.3)
        
        # Add golden ratio watermark
        plt.figtext(0.5, 0.02, 'OMEGA BTC AI - Divine Alignment', 
                   ha='center', fontsize=12, alpha=0.7)
        
        # Save the figure
        if output_path:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return output_path
        
        # Close the plot to free memory
        plt.close()
        return True
        
    except Exception as e:
        print(f"Error in visualization: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# Mock connection function
async def connect_to_redis(*args, **kwargs):
    """Mock implementation of the redis connection function."""
    return {"success": True, "message": "Mock Redis connection (not actually connected)"}


@app.route('/')
def index():
    """Serve the main dashboard."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return send_file(os.path.join(script_dir, 'divine_alignment_dashboard.html'))


@app.route('/divine')
def divine_dashboard():
    """Serve the Divine Alignment Dashboard."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return send_file(os.path.join(script_dir, 'divine_alignment_dashboard.html'))


@app.route('/favicon.ico')
def favicon():
    """Serve the favicon."""
    return "", 204  # Return No Content response for favicon requests


@app.route('/api/generate', methods=['POST'])
def generate_visualization():
    """Generate a new golden ratio visualization based on form parameters."""
    global last_generated_image, last_saved_timestamp
    
    try:
        # Get form data
        data = request.get_json() or {}
        timeframe = data.get('timeframe', '1d')
        years = int(data.get('years', '7'))
        view_type = data.get('view_type', '2d')
        
        # Try to get current price, defaulting to fetched price if not provided
        try:
            current_price = float(data.get('current_price', '0'))
            if current_price <= 0:
                current_price = fetch_btc_price() or 50000.0
        except (ValueError, TypeError):
            current_price = fetch_btc_price() or 50000.0
        
        # Use the script directory for file operations
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"btc_golden_ratio_{view_type}_{years}yr_{timestamp}.png"
        full_path = os.path.join(script_dir, filename)
        
        # Run the visualization function (async wrapper needed)
        async def run_visualization():
            return await visualize_golden_ratio_overlay(
                years=years,
                output_path=full_path,
                view_type=view_type,
                current_price=current_price
            )
        
        # Run in asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_visualization())
        loop.close()
        
        if os.path.exists(full_path):
            last_generated_image = filename
            last_saved_timestamp = timestamp
            return jsonify({
                "success": True,
                "filename": filename,
                "url": f"/api/images/{filename}"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to generate image"
            }), 500
    
    except Exception as e:
        print(f"Error generating visualization: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/images/<filename>')
def serve_image(filename):
    """Serve a generated image by filename."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, filename)
    
    # Check if file exists
    if not os.path.exists(image_path):
        # Generate a fallback image if requested file doesn't exist
        if 'btc_golden_ratio_7yr_latest.png' in filename:
            # Generate a new image with current timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"btc_golden_ratio_7yr_{timestamp}.png"
            full_path = os.path.join(script_dir, new_filename)
            
            try:
                async def run_visualization():
                    return await visualize_golden_ratio_overlay(
                        years=7,
                        output_path=full_path,
                        view_type="2d",
                        current_price=fetch_btc_price()
                    )
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(run_visualization())
                loop.close()
                
                if os.path.exists(full_path):
                    return send_file(full_path, mimetype='image/png')
            except Exception as e:
                print(f"Error generating image: {str(e)}")
                return f"Error generating image: {str(e)}", 500
        
        return f"Image not found: {filename}", 404
    
    return send_file(image_path, mimetype='image/png')


@app.route('/api/generate/fallback')
def fallback_chart():
    """Generate a fallback chart when no custom parameters are provided."""
    global last_generated_image
    
    # Look for existing recent charts
    if last_generated_image and os.path.exists(last_generated_image):
        return jsonify({
            "success": True,
            "filename": last_generated_image,
            "url": f"/api/images/{last_generated_image}"
        })
    
    # Find the most recent golden ratio file
    png_files = [f for f in os.listdir('.') if f.startswith('btc_golden_ratio_') and f.endswith('.png')]
    if png_files:
        # Sort by modification time, newest first
        png_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        last_generated_image = png_files[0]
        return jsonify({
            "success": True,
            "filename": last_generated_image,
            "url": f"/api/images/{last_generated_image}"
        })
    
    # If no files found, generate a new one with default parameters
    try:
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"btc_golden_ratio_7yr_{timestamp}.png"
        full_path = os.path.join(os.getcwd(), filename)
        
        # Run with default parameters
        async def run_visualization():
            return await visualize_golden_ratio_overlay(
                symbol="BTCUSDT",
                timeframe="1d",
                years=7,
                output_path=full_path
            )
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_visualization())
        loop.close()
        
        last_generated_image = filename
        return jsonify({
            "success": True,
            "filename": filename,
            "url": f"/api/images/{filename}"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/images/btc_golden_ratio_7yr_latest.png')
def serve_latest_chart():
    """Serve the most recent 7-year golden ratio chart."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find the most recent 7yr chart
    png_files = [f for f in os.listdir(script_dir) if 'btc_golden_ratio_7yr_' in f and f.endswith('.png')]
    
    if not png_files:
        # Generate a new one if none exists
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"btc_golden_ratio_7yr_{timestamp}.png"
        full_path = os.path.join(script_dir, filename)
        
        try:
            async def run_visualization():
                return await visualize_golden_ratio_overlay(
                    years=7,
                    output_path=full_path,
                    view_type="2d",
                    current_price=fetch_btc_price()
                )
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_visualization())
            loop.close()
            
            if os.path.exists(full_path):
                return send_file(full_path, mimetype='image/png')
            else:
                return "Failed to generate chart image", 500
        except Exception as e:
            error_msg = f"Error generating chart: {str(e)}"
            print(error_msg)
            return error_msg, 500
    
    # Sort by modification time, newest first
    png_files.sort(key=lambda x: os.path.getmtime(os.path.join(script_dir, x)), reverse=True)
    return send_file(os.path.join(script_dir, png_files[0]), mimetype='image/png')


def fetch_btc_price():
    """Fetch the current BTC price from an exchange."""
    global current_btc_price, last_price_check
    
    # Only check price every 60 seconds
    current_time = time.time()
    if current_btc_price is not None and current_time - last_price_check < 60:
        return current_btc_price
    
    try:
        # First try CCXT with Binance
        exchange = ccxt.binance()
        ticker = exchange.fetch_ticker('BTC/USDT')
        price = float(ticker['last']) if ticker and 'last' in ticker else None
        
        if price is not None:
            current_btc_price = price
            
            # Track price history with timestamps
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            price_history.append({
                'price': price,
                'timestamp': timestamp
            })
            
            # Keep only the last 1000 price points
            if len(price_history) > 1000:
                price_history.pop(0)
            
            # Check for Fibonacci crossings
            if len(price_history) >= 2:
                previous_price = price_history[-2]['price']
                crossings = check_fibonacci_crossings(price, previous_price)
                
                global most_recent_crossing, most_recent_ratio_level
                if crossings:
                    most_recent_crossing = {
                        'level': crossings[0]['level'],
                        'direction': crossings[0]['direction'],
                        'timestamp': timestamp
                    }
                    most_recent_ratio_level = most_recent_crossing['level']
            
            # Get golden state
            golden_price = calculate_golden_price()
            global golden_state
            if golden_price is not None:
                golden_state = determine_golden_state(price, golden_price)
            
            last_price_check = current_time
            print(f"Updated BTC price: ${price:,.2f}")
            
        return price
    
    except Exception as e:
        print(f"Error fetching BTC price from Binance: {str(e)}")
        try:
            # Fallback to CoinGecko API
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={'ids': 'bitcoin', 'vs_currencies': 'usd'},
                timeout=10
            )
            data = response.json()
            if data and 'bitcoin' in data and 'usd' in data['bitcoin']:
                price = float(data['bitcoin']['usd'])
                current_btc_price = price
                
                # Track price history
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                price_history.append({
                    'price': price,
                    'timestamp': timestamp
                })
                
                # Keep only the last 1000 price points
                if len(price_history) > 1000:
                    price_history.pop(0)
                
                last_price_check = current_time
                return price
        
        except Exception as e2:
            print(f"Error fetching BTC price from CoinGecko: {str(e2)}")
            # Return the last known price or None
            return current_btc_price


def calculate_golden_price():
    """Calculate the golden ratio price based on historical data."""
    try:
        # This is a simplified implementation
        # You might want to implement more sophisticated logic
        # For now, we'll use a base price and the golden ratio
        
        # Use the all-time low as the base
        base_price = 3122  # Dec 2018 low
        
        # Calculate golden ratio extensions
        # Level 1 - base price * golden ratio
        # Level 2 - base price * golden ratio^2
        # Level 3 - base price * golden ratio^3
        
        golden_price = base_price * (GOLDEN_RATIO ** 3)
        return golden_price
    
    except Exception as e:
        print(f"Error calculating golden price: {str(e)}")
        return None


def determine_golden_state(price, golden_price):
    """Determine if BTC is in golden ratio alignment."""
    if price is None or golden_price is None:
        return "unknown"
    
    # Calculate percentage difference
    diff_percent = abs((price - golden_price) / golden_price) * 100
    
    if diff_percent <= 3:
        return "aligned"
    elif diff_percent <= 10:
        return "approaching"
    else:
        return "distant"


def check_fibonacci_crossings(current_price, previous_price, base_price=20000):
    """Check if price crossed any Fibonacci levels."""
    crossings = []
    
    # Calculate Fibonacci levels based on a chosen range
    # This is simplistic - you would use actual market highs/lows
    range_low = base_price  # Example base price
    range_high = 69000      # Example high price (Nov 2021 ATH)
    range_diff = range_high - range_low
    
    for level in FIBONACCI_LEVELS:
        fib_price = range_low + (range_diff * level)
        
        # Check if price crossed this level
        if (previous_price < fib_price and current_price >= fib_price):
            crossings.append({
                'level': level,
                'price': fib_price,
                'direction': 'up'
            })
        elif (previous_price > fib_price and current_price <= fib_price):
            crossings.append({
                'level': level,
                'price': fib_price,
                'direction': 'down'
            })
    
    return crossings


def update_price_data():
    """Update price data periodically in a background thread."""
    while True:
        try:
            price = fetch_btc_price()
            if price is None:
                # If we couldn't fetch price, generate a random one for testing
                price = current_btc_price or random.uniform(40000, 80000)
                print(f"Using simulated price: ${price:,.2f}")
            time.sleep(60)  # Update every minute
        except Exception as e:
            print(f"Error in update_price_data: {str(e)}")
            time.sleep(60)  # Still wait before retry


@app.route('/api/golden_status')
def golden_status():
    """API endpoint to get the current golden ratio status."""
    try:
        # Ensure we have the latest price
        price = fetch_btc_price()
        
        # Calculate the golden price
        golden_price = calculate_golden_price()
        
        # Determine alignment status
        status = determine_golden_state(price, golden_price)
        
        # Get historical prices for chart
        recent_prices = price_history[-100:] if len(price_history) > 100 else price_history
        price_data = [p['price'] for p in recent_prices]
        timestamps = [p['timestamp'] for p in recent_prices]
        
        # Format crossing info
        crossing_info = "None detected"
        if most_recent_crossing:
            level_name = f"Fibonacci {most_recent_crossing['level']}"
            direction = "upward" if most_recent_crossing['direction'] == 'up' else "downward"
            crossing_info = f"{level_name} ({direction} cross at {most_recent_crossing['timestamp']})"
        
        # Get the active Fibonacci level if any
        active_level = most_recent_ratio_level if most_recent_ratio_level else "None"
        
        # Make sure we never return null/None values that could cause frontend issues
        if price is None:
            price = 50000.0  # Default fallback
        if golden_price is None:
            golden_price = 61800.0  # Default fallback
            
        return jsonify({
            "current_price": price,
            "golden_price": golden_price,
            "alignment_status": status,
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "price_history": {
                "prices": price_data if price_data else [price],
                "timestamps": timestamps if timestamps else [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            },
            "most_recent_crossing": crossing_info,
            "active_fibonacci_level": active_level
        })
    except Exception as e:
        print(f"Error in golden_status endpoint: {str(e)}")
        # Return minimal valid data to avoid frontend errors
        return jsonify({
            "current_price": 50000.0,
            "golden_price": 61800.0,
            "alignment_status": "unknown",
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "price_history": {
                "prices": [50000.0],
                "timestamps": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            },
            "most_recent_crossing": "None detected",
            "active_fibonacci_level": "None"
        })


@app.route('/api/trading_data')
def get_trading_data():
    """Get combined trading data including price and alignment."""
    # Get current price
    price = fetch_btc_price()
    
    # Generate trading data
    trading_data = generate_trading_data(price)
    
    return jsonify(trading_data)


def generate_trading_data(current_price: Optional[float] = None) -> Dict[str, Any]:
    """Generate trading data for display."""
    # Fetch price if not provided
    if current_price is None:
        current_price = fetch_btc_price()
    
    # Handle case where price could not be fetched
    if current_price is None:
        current_price = 50000.0  # Default fallback price
    
    # Calculate golden price and state
    golden_price = calculate_golden_price()
    
    # Handle case where golden price could not be calculated
    if golden_price is None:
        golden_price = 61800.0  # Default fallback golden price
    
    alignment = determine_golden_state(current_price, golden_price)
    
    # Calculate percentage difference
    diff_percent = ((current_price - golden_price) / golden_price) * 100
    
    # Generate a trade recommendation (simplified)
    signal, confidence = generate_trade_signal(current_price, golden_price, alignment)
    
    # Get price momentum (simplified)
    momentum = calculate_momentum()
    
    # Calculate trend strength
    trend_strength = calculate_trend_strength()
    
    # Get key support/resistance levels (simplified)
    levels = generate_key_levels(current_price)
    
    # Get risk assessment
    risk = assess_risk(current_price, golden_price, alignment, momentum)
    
    # Generate a trade description
    description = generate_trade_description(signal, alignment, momentum, risk)
    
    # Return combined data
    return {
        "price": {
            "current": current_price,
            "golden": golden_price,
            "difference_percent": diff_percent,
            "alignment": alignment,
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        "trade": {
            "signal": signal,
            "confidence": confidence,
            "description": description,
            "momentum": momentum,
            "trend_strength": trend_strength,
            "risk_level": risk
        },
        "levels": levels
    }


def generate_trade_signal(price, golden_price, alignment):
    """Generate a trade signal based on golden ratio alignment."""
    if not price or not golden_price:
        return "NEUTRAL", 0
    
    # Calculate percentage difference
    diff_percent = ((price - golden_price) / golden_price) * 100
    
    # Simplified signal logic
    signal = "NEUTRAL"
    confidence = 0
    
    if alignment == "aligned":
        if diff_percent > 0:
            signal = "SELL"
            confidence = min(abs(diff_percent) / 2, 95)  # Cap at 95%
        else:
            signal = "BUY"
            confidence = min(abs(diff_percent) / 2, 95)
    elif alignment == "approaching":
        if diff_percent > 0:
            signal = "HOLD"
            confidence = 70
        else:
            signal = "ACCUMULATE"
            confidence = 60
    else:  # distant
        if diff_percent > 20:
            signal = "STRONG SELL"
            confidence = 80
        elif diff_percent < -20:
            signal = "STRONG BUY"
            confidence = 80
        else:
            signal = "NEUTRAL"
            confidence = 50
    
    return signal, confidence


def calculate_momentum():
    """Calculate price momentum."""
    if len(price_history) < 24:
        return "NEUTRAL"
    
    # Get prices from 24 hours ago and now
    price_24h_ago = price_history[-24]['price']
    current_price = price_history[-1]['price']
    
    # Calculate change
    change_percent = ((current_price - price_24h_ago) / price_24h_ago) * 100
    
    if change_percent > 5:
        return "STRONG BULLISH"
    elif change_percent > 2:
        return "BULLISH"
    elif change_percent < -5:
        return "STRONG BEARISH"
    elif change_percent < -2:
        return "BEARISH"
    else:
        return "NEUTRAL"


def calculate_trend_strength():
    """Calculate trend strength (simplified)."""
    if len(price_history) < 48:
        return 50  # Neutral
    
    # Simple trend strength metric
    # More sophisticated metrics would use indicators like ADX
    price_48h_ago = price_history[-48]['price']
    price_24h_ago = price_history[-24]['price']
    current_price = price_history[-1]['price']
    
    # Check consistency of direction
    first_change = ((price_24h_ago - price_48h_ago) / price_48h_ago) * 100
    second_change = ((current_price - price_24h_ago) / price_24h_ago) * 100
    
    # If consistent direction, stronger trend
    if (first_change > 0 and second_change > 0) or (first_change < 0 and second_change < 0):
        # Magnitude also affects strength
        strength = 50 + min(abs(first_change + second_change) * 2, 45)
    else:
        # Inconsistent direction, weaker trend
        strength = max(50 - abs(first_change + second_change) * 2, 5)
    
    return strength


def generate_key_levels(current_price):
    """Generate key support and resistance levels."""
    # This is a simplified implementation
    # Real implementation would use actual market data
    
    # Example: generate levels as percentage offsets from current price
    return {
        "support": [
            round(current_price * 0.95, 2),
            round(current_price * 0.9, 2),
            round(current_price * 0.85, 2)
        ],
        "resistance": [
            round(current_price * 1.05, 2),
            round(current_price * 1.1, 2),
            round(current_price * 1.15, 2)
        ]
    }


def assess_risk(price, golden_price, alignment, momentum):
    """Assess trading risk level."""
    if not price or not golden_price:
        return "MEDIUM"
    
    # Calculate percentage difference
    diff_percent = abs((price - golden_price) / golden_price) * 100
    
    # Basic risk assessment
    if alignment == "aligned":
        if momentum == "NEUTRAL":
            return "LOW"
        elif "BULLISH" in momentum and diff_percent > 0:
            return "MEDIUM"
        elif "BEARISH" in momentum and diff_percent < 0:
            return "MEDIUM"
        else:
            return "LOW"
    elif alignment == "approaching":
        return "MEDIUM"
    else:  # distant
        if "STRONG" in momentum:
            return "HIGH"
        else:
            return "MEDIUM"


def generate_trade_description(signal, alignment, momentum, risk):
    """Generate a human-readable trade description."""
    descriptions = {
        "BUY": f"Favorable buying opportunity with {alignment} golden ratio alignment. " +
               f"Price momentum is {momentum.lower()} with {risk.lower()} risk.",
        
        "ACCUMULATE": f"Consider gradual accumulation with {alignment} golden ratio alignment. " +
                      f"Price momentum is {momentum.lower()} with {risk.lower()} risk.",
        
        "HOLD": f"Hold current positions with {alignment} golden ratio alignment. " +
                f"Price momentum is {momentum.lower()} with {risk.lower()} risk.",
        
        "SELL": f"Consider taking profits with {alignment} golden ratio alignment. " +
                f"Price momentum is {momentum.lower()} with {risk.lower()} risk.",
        
        "STRONG BUY": f"Strong buying opportunity despite {alignment} golden ratio alignment. " +
                      f"Price momentum is {momentum.lower()} with {risk.lower()} risk.",
        
        "STRONG SELL": f"Consider significant profit-taking despite {alignment} golden ratio alignment. " +
                       f"Price momentum is {momentum.lower()} with {risk.lower()} risk.",
        
        "NEUTRAL": f"No clear signal with {alignment} golden ratio alignment. " +
                   f"Price momentum is {momentum.lower()} with {risk.lower()} risk."
    }
    
    return descriptions.get(signal, descriptions["NEUTRAL"])


@app.route('/assets/css/<filename>')
def serve_css(filename):
    """Serve CSS files."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return send_file(os.path.join(script_dir, 'assets', 'css', filename))


@app.route('/api/trader_personas')
def get_trader_personas():
    """Get trader personas data."""
    personas = {
        "strategic": {
            "name": "Strategic Trader",
            "personality": "Methodical and disciplined with a focus on Fibonacci levels",
            "style": "Position trading based on golden ratio alignments",
            "risk_level": "Medium",
            "favorite_pattern": "Golden Ratio Retracements",
            "current_position": "Long BTC with defined exit at key resistance",
            "performance": {
                "win_rate": 68,
                "avg_profit": 12.4,
                "max_drawdown": 15.2
            }
        },
        "aggressive": {
            "name": "Aggressive Trader",
            "personality": "Bold and decisive, seeking high-leverage opportunities",
            "style": "Momentum trading with aggressive entries on breakouts",
            "risk_level": "High",
            "favorite_pattern": "Golden Ratio Extensions",
            "current_position": "Leveraged long targeting next Fibonacci extension",
            "performance": {
                "win_rate": 52,
                "avg_profit": 22.8,
                "max_drawdown": 28.5
            }
        },
        "scalper": {
            "name": "Scalper Trader",
            "personality": "Quick and nimble, exploiting small golden ratio divergences",
            "style": "High-frequency trading on micro Fibonacci patterns",
            "risk_level": "Medium-High",
            "favorite_pattern": "Intraday Golden Spirals",
            "current_position": "Multiple small positions with tight stops",
            "performance": {
                "win_rate": 74,
                "avg_profit": 4.2,
                "max_drawdown": 9.8
            }
        },
        "divine": {
            "name": "Divine Harmonizer",
            "personality": "Intuitive and balanced, seeking universal alignment",
            "style": "Holistic trading based on divine proportions across markets",
            "risk_level": "Low-Medium",
            "favorite_pattern": "Multi-market Golden Harmony",
            "current_position": "Balanced portfolio aligned with cosmic proportions",
            "performance": {
                "win_rate": 82,
                "avg_profit": 8.6,
                "max_drawdown": 6.4
            }
        }
    }
    
    return jsonify(personas)


# Start the price update thread
price_update_thread = threading.Thread(target=update_price_data, daemon=True)
price_update_thread.start()

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='OMEGA BTC AI - Divine Alignment Dashboard API')
    parser.add_argument('--port', type=int, default=5051, help='Port to run the server on (default: 5051)')
    args = parser.parse_args()
    
    # Run the Flask app on specified port
    print(f"Starting Divine Alignment Dashboard API on port {args.port}...")
    app.run(host='0.0.0.0', port=args.port, debug=True) 