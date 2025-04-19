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
OMEGA BTC AI - Redis Data Checker
================================

This script checks Redis for BTC price history data and other stored information.
"""

import os
import sys
import json
import redis
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ANSI color codes for prettier output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def log_color(message, color=GREEN):
    """Print a colorized message."""
    print(f"{color}{message}{RESET}")

def check_redis_connection():
    """Check Redis connection and return client if successful."""
    try:
        # Try to connect to Redis
        # First with explicit host/port, then localhost fallback
        for host, port in [
            (os.getenv('REDIS_HOST', 'redis'), int(os.getenv('REDIS_PORT', 6379))),
            ('localhost', 6379),
            ('127.0.0.1', 6379)
        ]:
            try:
                log_color(f"Trying to connect to Redis at {host}:{port}...", BLUE)
                
                # Try without authentication first
                redis_client = redis.Redis(
                    host=host,
                    port=port,
                    password=None,  # No password
                    decode_responses=True
                )
                
                if redis_client.ping():
                    log_color(f"✅ Connected to Redis at {host}:{port} (no auth)", GREEN)
                    return redis_client
            except Exception as e:
                log_color(f"❌ Failed to connect to Redis at {host}:{port} without auth: {e}", RED)
                
                # Try with authentication as fallback
                try:
                    log_color(f"Trying to connect to Redis at {host}:{port} with auth...", BLUE)
                    redis_client = redis.Redis(
                        host=host,
                        port=port,
                        password=os.getenv('REDIS_PASSWORD'),
                        decode_responses=True
                    )
                    
                    if redis_client.ping():
                        log_color(f"✅ Connected to Redis at {host}:{port} with auth", GREEN)
                        return redis_client
                except Exception as auth_e:
                    log_color(f"❌ Failed to connect to Redis at {host}:{port} with auth: {auth_e}", RED)
        
        log_color("Could not connect to Redis on any host/port combination", RED)
        return None
    except Exception as e:
        log_color(f"Error checking Redis connection: {e}", RED)
        return None

def get_btc_price_data(redis_client):
    """Get BTC price data from Redis."""
    try:
        # Get current and previous prices
        last_price = redis_client.get("last_btc_price")
        prev_price = redis_client.get("prev_btc_price")
        last_update = redis_client.get("last_btc_update_time")
        
        if last_update:
            last_update_time = datetime.fromtimestamp(float(last_update))
            time_ago = datetime.now() - last_update_time
            time_ago_str = f"{time_ago.seconds // 60} minutes, {time_ago.seconds % 60} seconds ago"
        else:
            time_ago_str = "unknown"
            
        log_color("\n==== CURRENT BTC PRICE DATA ====", CYAN)
        log_color(f"Current Price: ${float(last_price) if last_price else 'N/A'}", GREEN)
        log_color(f"Previous Price: ${float(prev_price) if prev_price else 'N/A'}", YELLOW)
        log_color(f"Last Updated: {time_ago_str}", BLUE)
        
        # Get price history - checking different formats
        history = []
        raw_history = redis_client.lrange("btc_movement_history", 0, -1)
        
        log_color(f"\n==== BTC PRICE HISTORY ====", CYAN)
        log_color(f"Total raw history items: {len(raw_history)}", BLUE)
        
        if raw_history:
            # Check first item to determine format
            sample = raw_history[0]
            log_color(f"Sample history item: {sample}", YELLOW)
            
            # Try different formats
            if ',' in sample:  # Format: "price,volume"
                log_color("Detected 'price,volume' format", BLUE)
                for item in raw_history:
                    try:
                        price_str = item.split(',')[0]
                        history.append(float(price_str))
                    except (ValueError, IndexError) as e:
                        log_color(f"Error parsing item {item}: {e}", RED)
            else:
                # Try direct conversion
                for item in raw_history:
                    try:
                        history.append(float(item))
                    except ValueError as e:
                        log_color(f"Error parsing item {item}: {e}", RED)
            
            history.reverse()  # Most recent first, reverse to get chronological order
            
            log_color(f"Successfully parsed {len(history)} price points", GREEN)
            
            if history:
                log_color(f"First price: ${history[0]}", YELLOW)
                log_color(f"Latest price: ${history[-1]}", GREEN)
                log_color(f"Price change: ${history[-1] - history[0]} ({((history[-1] / history[0]) - 1) * 100:.2f}%)", 
                         GREEN if history[-1] >= history[0] else RED)
            
        return history
    except Exception as e:
        log_color(f"Error getting BTC price data: {e}", RED)
        return []

def plot_price_history(history, save_path=None):
    """Plot BTC price history."""
    if not history:
        log_color("No price history to plot", RED)
        return
    
    # Create time axis assuming consistent intervals
    # Since we don't have timestamps in the raw data, we'll create synthetic ones
    # Most recent price point is now, and work backwards
    end_time = datetime.now()
    # Assuming each price point is ~1 minute apart
    times = [end_time - timedelta(minutes=i) for i in range(len(history)-1, -1, -1)]
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': times,
        'price': history
    })
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.style.use('dark_background')
    plt.plot(df['timestamp'], df['price'], label='BTC Price', color='#f0f0f0', linewidth=2)
    
    # Add grid
    plt.grid(True, alpha=0.2)
    
    # Format axes
    plt.title('BTC Price History', color='white', fontsize=16)
    plt.xlabel('Time', color='white')
    plt.ylabel('Price (USD)', color='white')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=45)
    
    # Show min/max points
    max_price = max(history)
    min_price = min(history)
    max_idx = history.index(max_price)
    min_idx = history.index(min_price)
    
    plt.scatter([times[max_idx]], [max_price], color='lime', s=80, marker='*', 
               label=f"Max: ${max_price:.2f}")
    plt.scatter([times[min_idx]], [min_price], color='orangered', s=80, marker='*', 
               label=f"Min: ${min_price:.2f}")
    
    # Add legend
    plt.legend(loc='best')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path)
        log_color(f"Price history plot saved to {save_path}", GREEN)
    else:
        plt.show()
    
    return df

def get_position_entry_time(redis_client, position_id=None):
    """Try to find position entry time in Redis."""
    try:
        # Get profiles to search
        profiles = ["strategic", "aggressive", "scalping"]
        
        for profile in profiles:
            # Get list of positions for this profile
            positions_key = f"trader:positions:{profile}"
            positions = redis_client.lrange(positions_key, 0, -1)
            
            if positions:
                log_color(f"\n==== POSITIONS FOR {profile.upper()} PROFILE ====", CYAN)
                log_color(f"Found {len(positions)} positions", BLUE)
                
                for i, position_json in enumerate(positions):
                    try:
                        position = json.loads(position_json)
                        
                        # If position_id provided, filter for it
                        if position_id and position.get('id') != position_id:
                            continue
                            
                        entry_time = position.get('entry_time')
                        entry_price = position.get('entry_price')
                        direction = position.get('direction')
                        leverage = position.get('leverage', 'N/A')
                        status = position.get('status', 'N/A')
                        
                        log_color(f"Position #{i+1}:", BLUE)
                        log_color(f"  ID: {position.get('id', 'N/A')}", YELLOW)
                        log_color(f"  Direction: {direction}", GREEN if direction == 'LONG' else RED)
                        log_color(f"  Entry Time: {entry_time}", BLUE)
                        log_color(f"  Entry Price: ${entry_price}", YELLOW)
                        log_color(f"  Leverage: {leverage}x", MAGENTA)
                        log_color(f"  Status: {status}", GREEN if status == 'OPEN' else RED)
                        
                        # Return the first position or the one matching position_id
                        return position
                    except json.JSONDecodeError:
                        log_color(f"Error parsing position data: {position_json[:50]}...", RED)
        
        log_color("No positions found in Redis", YELLOW)
        return None
    except Exception as e:
        log_color(f"Error getting position entry time: {e}", RED)
        return None

def main():
    """Main function."""
    log_color("\n====== OMEGA BTC AI - REDIS DATA CHECKER ======", CYAN)
    
    # Check Redis connection
    redis_client = check_redis_connection()
    if not redis_client:
        sys.exit(1)
    
    # Get BTC price data
    history = get_btc_price_data(redis_client)
    
    # Get position entry time
    position = get_position_entry_time(redis_client)
    
    # Plot price history if we have data
    if history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_df = plot_price_history(history, save_path=f"btc_price_history_{timestamp}.png")
        
        # If we have position data, check the price at entry time
        if position and position.get('entry_time'):
            try:
                entry_time = datetime.fromisoformat(position['entry_time'])
                entry_price = position['entry_price']
                
                log_color(f"\n==== POSITION ANALYSIS ====", CYAN)
                log_color(f"Entry Time: {entry_time}", BLUE)
                log_color(f"Entry Price: ${entry_price}", YELLOW)
                
                # Check current price
                current_price = float(redis_client.get("last_btc_price") or 0)
                if current_price > 0:
                    price_change = ((current_price / entry_price) - 1) * 100
                    log_color(f"Current Price: ${current_price}", GREEN)
                    log_color(f"Price Change: {price_change:.2f}%", 
                             GREEN if price_change >= 0 else RED)
                    
                    # Calculate PnL with leverage
                    leverage = position.get('leverage', 1)
                    if position['direction'] == 'LONG':
                        pnl = price_change * leverage
                    else:  # SHORT
                        pnl = -price_change * leverage
                        
                    log_color(f"Current PnL (with {leverage}x leverage): {pnl:.2f}%", 
                             GREEN if pnl >= 0 else RED)
            except Exception as e:
                log_color(f"Error analyzing position: {e}", RED)

if __name__ == "__main__":
    main()