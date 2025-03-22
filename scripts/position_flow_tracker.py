#!/usr/bin/env python3
"""
OMEGA BTC AI - Position Flow Tracker (3D Enhanced)
===================================================

This script visualizes the price flow of a BTC position from entry to current price,
showing how the price moved relative to take profit and stop loss targets.
Now with 3D visualization capabilities and Redis data support!
"""

import os
import sys
import json
import asyncio
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta
import redis
from dotenv import load_dotenv
import ccxt.async_support as ccxt

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

# Get API credentials from environment variables
BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_SECRET_KEY = os.getenv('BITGET_SECRET_KEY')
BITGET_PASSPHRASE = os.getenv('BITGET_PASSPHRASE')

# Fibonacci levels from .env or default
FIBONACCI_LEVELS_STR = os.getenv('FIBONACCI_LEVELS', '0,0.236,0.382,0.5,0.618,0.786,1,1.618,2.618,4.236')
FIBONACCI_LEVELS = [float(level) for level in FIBONACCI_LEVELS_STR.split(',')]

# Redis connection details (from .env or defaults)
REDIS_HOST = 'localhost'  # Overriding to use localhost since that's working
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = None  # No password needed for localhost

# Redis keys for BTC price data
BTC_PRICE_KEY = "btc_price"
BTC_PRICES_HISTORY_KEY = "btc_prices_history"
PRICE_HISTORY_PREFIX = "price_history:"

def connect_to_redis():
    """Connect to Redis trying different auth methods."""
    log_color(f"Trying to connect to Redis on {REDIS_HOST}:{REDIS_PORT} without password...", BLUE)
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            socket_timeout=2
        )
        
        if client.ping():
            log_color("Successfully connected to Redis (no password)", GREEN)
            return client
    except Exception as e:
        log_color(f"Could not connect to Redis: {e}", RED)
    
    log_color("Failed to connect to Redis", RED)
    return None

def fetch_price_data_from_redis(redis_client, since_time, until_time):
    """Fetch historical BTC price data from Redis."""
    if not redis_client:
        return None
    
    log_color(f"Fetching BTC price data from Redis for period {since_time} to {until_time}", BLUE)
    
    try:
        # We found these specific keys in Redis
        key_to_check = "btc_movement_history"
        
        if redis_client.exists(key_to_check):
            log_color(f"Found price data in Redis at key: {key_to_check}", GREEN)
            
            # Get the data type
            key_type = redis_client.type(key_to_check)
            log_color(f"Key '{key_to_check}' is of type: {key_type}", BLUE)
            
            # Handle list type (confirmed by our redis-cli check)
            if key_type == "list":
                # Get length
                list_length = redis_client.llen(key_to_check)
                log_color(f"Found {list_length} entries in {key_to_check}", GREEN)
                
                # Get all entries
                entries = redis_client.lrange(key_to_check, 0, -1)
                
                # Process entries (format is "price,volume" like "84329.9,0.0005")
                current_time = datetime.now()
                records = []
                
                # Each entry seems to be a simple price,volume pair without timestamp
                # We'll create timestamps by working backwards from now
                for i, entry in enumerate(entries):
                    try:
                        # Timestamps go from newest to oldest (index 0 = newest)
                        # So reverse the timestamps to match that order
                        timestamp = current_time - timedelta(minutes=i)
                        
                        # Parse the price,volume format
                        price_str, volume_str = entry.split(',')
                        price = float(price_str)
                        volume = float(volume_str)
                        
                        records.append({
                            'timestamp': timestamp,
                            'close': price,
                            'volume': volume
                        })
                    except Exception as e:
                        log_color(f"Error parsing entry {entry}: {e}", RED)
                
                if records:
                    # Create DataFrame and sort by timestamp
                    df = pd.DataFrame(records)
                    df = df.sort_values('timestamp')
                    
                    # Add any missing fields needed for visualization
                    if 'open' not in df.columns:
                        df['open'] = df['close'].shift(1)
                    if 'high' not in df.columns:
                        df['high'] = df['close']
                    if 'low' not in df.columns:
                        df['low'] = df['close']
                    
                    log_color(f"Converted {len(df)} price points from Redis {key_to_check}", GREEN)
                    return df
            
            # If we couldn't process the data, continue to check other keys
            log_color(f"Could not process data from {key_to_check} key", YELLOW)
        
        # Check all other BTC-related keys
        possible_keys = [
            "btc_price",
            "btc_movements_1min",
            "btc_movements_5min",
            "btc_movements_15min",
            "btc_movements_60min",
            "btc_price_changes"
        ]
        
        # If one key didn't work, try others
        for key in possible_keys:
            if key != key_to_check and redis_client.exists(key):
                log_color(f"Checking alternative key: {key}", BLUE)
                key_type = redis_client.type(key)
                
                # Handle based on key type
                if key_type == "string":
                    # Simple string value (current price)
                    try:
                        value = redis_client.get(key)
                        price = float(value)
                        timestamp = datetime.now()
                        
                        # Create a single-point dataset
                        df = pd.DataFrame([{
                            'timestamp': timestamp,
                            'open': price, 
                            'high': price,
                            'low': price,
                            'close': price,
                            'volume': 1.0
                        }])
                        
                        log_color(f"Created single-point dataset from {key}", YELLOW)
                        return df
                    except Exception as e:
                        log_color(f"Could not use {key}: {e}", RED)
                
                elif key_type == "list":
                    # Try to interpret list data
                    try:
                        entries = redis_client.lrange(key, 0, -1)
                        log_color(f"Found {len(entries)} entries in {key}", GREEN)
                        
                        # Sample first entry to determine format
                        if entries:
                            log_color(f"Sample entry from {key}: {entries[0]}", CYAN)
                    except Exception as e:
                        log_color(f"Error accessing {key}: {e}", RED)
        
        log_color("No usable BTC price data found in Redis", YELLOW)
        return None
        
    except Exception as e:
        log_color(f"Error processing Redis price data: {e}", RED)
        return None

async def fetch_historical_prices(symbol, since_time, until_time, timeframe='1m', redis_client=None):
    """Fetch historical prices, trying Redis first then falling back to BitGet API."""
    # Try Redis first
    if redis_client:
        redis_df = fetch_price_data_from_redis(redis_client, since_time, until_time)
        if redis_df is not None and not redis_df.empty:
            log_color(f"Using Redis data with {len(redis_df)} price points", GREEN)
            return redis_df
    
    # Fall back to BitGet API if Redis data is not available
    log_color("Redis data not available, falling back to BitGet API", YELLOW)
    
    exchange = ccxt.bitget({
        'apiKey': BITGET_API_KEY,
        'secret': BITGET_SECRET_KEY,
        'password': BITGET_PASSPHRASE,
        'enableRateLimit': True
    })
    
    try:
        # Convert timestamps to milliseconds if needed
        if isinstance(since_time, datetime):
            since = int(since_time.timestamp() * 1000)
        else:
            since = since_time
            
        if isinstance(until_time, datetime):
            until = int(until_time.timestamp() * 1000)
        else:
            until = until_time
            
        log_color(f"Fetching historical prices from BitGet API for period {datetime.fromtimestamp(since/1000)} to {datetime.fromtimestamp(until/1000)}", BLUE)
        
        # Fetch OHLCV data
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
        
        # Fetch more data if needed
        while ohlcv and ohlcv[-1][0] < until:
            since = ohlcv[-1][0] + 1
            batch = await exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
            if not batch:
                break
            ohlcv.extend(batch)
            
        # Filter by time range and convert to DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[(df['timestamp'] >= pd.to_datetime(since, unit='ms')) & 
                (df['timestamp'] <= pd.to_datetime(until, unit='ms'))]
        
        if not df.empty:
            log_color(f"Successfully fetched {len(df)} price points from BitGet API", GREEN)
        else:
            log_color("No price data available from BitGet API for this time range", YELLOW)
            
        return df
        
    finally:
        await exchange.close()

async def get_current_position():
    """Get the current BitGet position using the API."""
    exchange = ccxt.bitget({
        'apiKey': BITGET_API_KEY,
        'secret': BITGET_SECRET_KEY,
        'password': BITGET_PASSPHRASE,
        'enableRateLimit': True
    })
    
    try:
        log_color("Fetching current positions from BitGet...", BLUE)
        positions = await exchange.fetch_positions()
        
        # Filter for active positions
        active_positions = [p for p in positions if p.get('contracts', 0) and float(str(p.get('contracts', 0))) > 0]
        
        if not active_positions:
            log_color("No active positions found.", YELLOW)
            return None
        
        # Get the BTC position (assuming there's only one)
        for position in active_positions:
            symbol = position.get('symbol', '')
            # Check if 'BTC' is in the symbol string
            if symbol and 'BTC' in symbol:
                # Format position for visualization
                # Assume position was opened 24 hours ago if entry time not available
                entry_time = datetime.now() - timedelta(days=1)  
                
                # Safely extract and convert values
                entry_price_raw = position.get('entryPrice', 0)
                entry_price = float(str(entry_price_raw)) if entry_price_raw is not None else 0
                
                side_raw = position.get('side', 'LONG')
                direction = side_raw.upper() if side_raw is not None else 'LONG'
                
                leverage_raw = position.get('leverage', 11)
                leverage = float(str(leverage_raw)) if leverage_raw is not None else 11
                
                # Default risk parameters
                stop_loss_pct = 1.0
                take_profit_1_pct = 1.0
                take_profit_2_pct = 2.0
                
                # Calculate TP and SL levels
                if direction == 'LONG':
                    take_profit_1 = entry_price * (1 + take_profit_1_pct / 100)
                    take_profit_2 = entry_price * (1 + take_profit_2_pct / 100)
                    stop_loss = entry_price * (1 - stop_loss_pct / 100)
                else:  # SHORT
                    take_profit_1 = entry_price * (1 - take_profit_1_pct / 100)
                    take_profit_2 = entry_price * (1 - take_profit_2_pct / 100)
                    stop_loss = entry_price * (1 + stop_loss_pct / 100)
                
                # Safely handle position size
                contracts_raw = position.get('contracts', 0)
                size = float(str(contracts_raw)) if contracts_raw is not None else 0
                
                # Safely handle unrealized PnL
                pnl_raw = position.get('unrealizedPnl', 0)
                unrealized_pnl = float(str(pnl_raw)) if pnl_raw is not None else 0
                
                # Create position object with relevant data
                position_data = {
                    'id': position.get('id', 'current'),
                    'symbol': symbol,
                    'direction': direction,
                    'entry_price': entry_price,
                    'entry_time': entry_time.isoformat(),
                    'size': size,
                    'leverage': leverage,
                    'status': 'OPEN',
                    'unrealized_pnl': unrealized_pnl,
                    'take_profits': [
                        {'percentage': 50, 'price': take_profit_1},
                        {'percentage': 100, 'price': take_profit_2}
                    ],
                    'stop_loss': stop_loss
                }
                
                log_color(f"Found {direction} position with entry price {entry_price} and current PnL {unrealized_pnl}", GREEN)
                return position_data
                
        return None
            
    finally:
        await exchange.close()

def get_simulated_position():
    """Create a simulated position for testing."""
    log_color("Creating simulated position...", BLUE)
    
    # Current BTC price (this would be fetched in a real implementation)
    # For now, let's use a hard-coded price
    current_price = 84300.0  # Example price
    
    # Create a simulated position with timestamp in the past
    # Use a timestamp that's far enough in the past to have historical data
    entry_time = datetime.now() - timedelta(hours=24)  # Use 24 hours (1 day) ago
    entry_price = 84100.0  # Fixed price for simulation
    
    # Default risk parameters
    leverage = 11.0
    direction = 'LONG'
    
    # Default risk parameters
    stop_loss_pct = 1.0
    take_profit_1_pct = 1.0
    take_profit_2_pct = 2.0
    
    # Calculate TP and SL levels
    if direction == 'LONG':
        take_profit_1 = entry_price * (1 + take_profit_1_pct / 100)
        take_profit_2 = entry_price * (1 + take_profit_2_pct / 100)
        stop_loss = entry_price * (1 - stop_loss_pct / 100)
    else:  # SHORT
        take_profit_1 = entry_price * (1 - take_profit_1_pct / 100)
        take_profit_2 = entry_price * (1 - take_profit_2_pct / 100)
        stop_loss = entry_price * (1 + stop_loss_pct / 100)
    
    # Calculate rough PnL
    pnl = (current_price - entry_price) * 0.003 * leverage
    
    # Create position object
    position_data = {
        'id': 'simulated-1',
        'symbol': 'BTC/USDT:USDT',
        'direction': direction,
        'entry_price': entry_price,
        'entry_time': entry_time.isoformat(),
        'size': 0.003,
        'leverage': leverage,
        'status': 'OPEN',
        'unrealized_pnl': pnl,
        'take_profits': [
            {'percentage': 50, 'price': take_profit_1},
            {'percentage': 100, 'price': take_profit_2}
        ],
        'stop_loss': stop_loss
    }
    
    log_color(f"Created simulated {direction} position with entry price {entry_price}", GREEN)
    log_color(f"Entry time: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}", GREEN)
    return position_data

def calculate_fibonacci_targets(entry_price, direction, current_price=None):
    """
    Calculate Fibonacci take profit targets based on the entry price.
    
    Args:
        entry_price: The position entry price
        direction: 'long' or 'short'
        current_price: Current price (optional) to highlight the closest level
    
    Returns:
        Dictionary of Fibonacci levels and their price values
    """
    targets = {}
    
    # Long targets are above entry price, short targets are below
    if direction.lower() == 'long':
        # For longs, we primarily use extension levels (1.0+)
        extension_levels = [level for level in FIBONACCI_LEVELS if level >= 1.0]
        
        # Calculate the base move using average historical volatility
        # For simplicity, using a fixed percentage of the entry price
        base_move = entry_price * 0.03  # 3% of entry price
        
        for level in extension_levels:
            target_price = entry_price + (base_move * level)
            targets[str(level)] = target_price
            
    else:  # Short
        # For shorts, we primarily use extension levels (1.0+) but in reverse
        extension_levels = [level for level in FIBONACCI_LEVELS if level >= 1.0]
        
        # Calculate the base move
        base_move = entry_price * 0.03  # 3% of entry price
        
        for level in extension_levels:
            target_price = entry_price - (base_move * level)
            targets[str(level)] = target_price
    
    # Add the closest level to current price indicator
    if current_price:
        min_diff = float('inf')
        closest_level = None
        
        for level, price in targets.items():
            diff = abs(price - current_price)
            if diff < min_diff:
                min_diff = diff
                closest_level = level
                
        if closest_level:
            targets['closest_level'] = closest_level
    
    return targets

async def track_position_flow_2d(position=None, hours_back=24, redis_client=None):
    """Track and visualize the price flow of a position in traditional 2D."""
    # Get position data from API if not provided
    if position is None:
        position = await get_current_position()
        
    if not position:
        log_color("No active position found on BitGet.", YELLOW)
        return
    
    # Extract position details
    entry_price = position['entry_price']
    entry_time = datetime.fromisoformat(position['entry_time'])
    direction = position['direction']
    take_profits = position.get('take_profits', [])
    stop_loss = position.get('stop_loss')
    
    # Set time range
    until_time = datetime.now()
    since_time = until_time - timedelta(hours=hours_back)
    
    # Ensure entry_time is within our range
    if entry_time < since_time:
        log_color(f"Entry time {entry_time} is before our time range, adjusting...", YELLOW)
        entry_time = since_time + timedelta(minutes=10)
    
    # Fetch historical prices
    df = await fetch_historical_prices(
        position['symbol'],
        since_time,
        until_time,
        redis_client=redis_client
    )
    
    if df is None or df.empty:
        log_color("No price data available for this time range.", RED)
        return
    
    # Calculate Fibonacci targets
    fib_targets = calculate_fibonacci_targets(
        entry_price, 
        direction,
        df['close'].iloc[-1]
    )
    
    # Create the plot
    plt.figure(figsize=(14, 8), facecolor='#121212')
    ax = plt.axes()
    
    # Plot price movement
    plt.plot(df['timestamp'], df['close'], label='BTC Price', color='#f0f0f0', linewidth=2)
    
    # Mark entry point
    plt.axhline(y=entry_price, color='yellow', linestyle='--', alpha=0.5, label='Entry Price')
    
    # Convert datetime to matplotlib format
    entry_time_num = mdates.date2num(entry_time)
    plt.scatter([entry_time_num], [entry_price], color='yellow', s=100, marker='^' if direction == 'LONG' else 'v', 
                label=f"{direction} Entry at ${entry_price:.2f}")
    
    # Mark take profit levels
    for idx, tp in enumerate(take_profits):
        tp_price = tp.get('price')
        if tp_price:
            plt.axhline(y=tp_price, color='green', linestyle='--', alpha=0.3)
            # Create a safe timestamp for text positioning - use a float explicitly
            safe_date_num = float(mdates.date2num(df['timestamp'].iloc[0])) if not df.empty else float(mdates.date2num(entry_time))
            plt.text(safe_date_num, float(tp_price), f"TP{idx+1}: ${tp_price:.2f}", 
                     color='green', verticalalignment='bottom')
    
    # Mark stop loss level
    if stop_loss:
        plt.axhline(y=stop_loss, color='red', linestyle='--', alpha=0.5, label=f"Stop Loss: ${stop_loss:.2f}")
    
    # Highlight max profit and max loss points
    price_during_position = df[(df['timestamp'] >= entry_time)]['close']
    
    if not price_during_position.empty:
        max_price = price_during_position.max()
        min_price = price_during_position.min()
        max_price_idx = price_during_position.idxmax()
        min_price_idx = price_during_position.idxmin()
        max_price_time = df.loc[max_price_idx, 'timestamp']
        min_price_time = df.loc[min_price_idx, 'timestamp']
        
        max_price_time_num = mdates.date2num(max_price_time)
        min_price_time_num = mdates.date2num(min_price_time)
        
        # For long positions, max price is max profit, min price is max loss
        if direction == 'LONG':
            plt.scatter([max_price_time_num], [max_price], color='lime', s=80, marker='*', 
                       label=f"Max Potential Profit: ${max_price:.2f}")
            plt.scatter([min_price_time_num], [min_price], color='orangered', s=80, marker='*', 
                       label=f"Max Potential Loss: ${min_price:.2f}")
        # For short positions, min price is max profit, max price is max loss
        else:
            plt.scatter([min_price_time_num], [min_price], color='lime', s=80, marker='*', 
                       label=f"Max Potential Profit: ${min_price:.2f}")
            plt.scatter([max_price_time_num], [max_price], color='orangered', s=80, marker='*', 
                       label=f"Max Potential Loss: ${max_price:.2f}")
    
    # Calculate current PnL
    current_price = df['close'].iloc[-1] if not df.empty else entry_price
    if direction == 'LONG':
        pnl_pct = ((current_price - entry_price) / entry_price * 100) * position.get('leverage', 1)
    else:
        pnl_pct = ((entry_price - current_price) / entry_price * 100) * position.get('leverage', 1)
        
    color = 'green' if pnl_pct >= 0 else 'red'
    plt.figtext(0.5, 0.01, f"Current PnL: {pnl_pct:.2f}% ({position.get('unrealized_pnl', 0):.2f} USD)", 
                ha='center', color=color, fontsize=12)
    
    # Calculate distance from price to TP and SL targets
    if take_profits and len(take_profits) > 0:
        nearest_tp = min(take_profits, key=lambda x: abs(x.get('price', 0) - entry_price))
        tp_distance = abs((nearest_tp.get('price', 0) - entry_price) / entry_price * 100)
        plt.figtext(0.25, 0.01, f"TP Distance: {tp_distance:.2f}%", ha='center', color='green', fontsize=12)
    
    if stop_loss:
        sl_distance = abs((stop_loss - entry_price) / entry_price * 100)
        plt.figtext(0.75, 0.01, f"SL Distance: {sl_distance:.2f}%", ha='center', color='red', fontsize=12)
    
    # Add data source info
    data_source = "Redis" if redis_client else "BitGet API"
    plt.figtext(0.5, 0.96, f"Data Source: {data_source} | Points: {len(df)}", ha='center', color='white', fontsize=10)
    
    # Format the plot
    title_prefix = "[BitGet]" if position.get('id') != 'simulated-1' else "[Simulated]"
    plt.title(f"{title_prefix} BTC Price Flow During {direction} Position", color='white', fontsize=16)
    plt.xlabel('Time', color='white')
    plt.ylabel('Price (USD)', color='white')
    plt.grid(True, alpha=0.2)
    plt.legend(loc='upper left')
    
    # Format time axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=45)
    
    # Adjust layout
    plt.tight_layout(rect=(0, 0.03, 1, 0.97))
    
    # Add Fibonacci take profit targets
    for level, target_price in fib_targets.items():
        if level == 'closest_level':
            continue
            
        # Skip levels that are outside the chart range
        if target_price < min(df['close']) or target_price > max(df['close']):
            continue
            
        # Different colors for different Fibonacci levels
        fib_color = CYAN
        if float(level) >= 2.618:
            fib_color = MAGENTA
        elif float(level) >= 1.618:
            fib_color = YELLOW
        elif float(level) >= 1.0:
            fib_color = GREEN
            
        # Draw the Fibonacci level line
        plt.axhline(
            y=target_price, 
            color=fib_color, 
            linestyle='--', 
            alpha=0.8,
            linewidth=1.5
        )
        
        # Add a label for the Fibonacci level
        plt.text(
            x=df.index[0], 
            y=target_price * 1.0005, 
            s=f"TP {level}x: {target_price:.2f}", 
            color=fib_color, 
            fontsize=10, 
            ha='left', 
            va='bottom'
        )
    
    # Save the figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"position_flow_2d_{timestamp}.png"
    plt.savefig(filename)
    
    log_color(f"2D position flow visualization saved as {filename}", GREEN)
    plt.show()

async def track_position_flow_3d(position=None, hours_back=24, redis_client=None):
    """Track and visualize the price flow of a position in 3D with momentum/velocity on z-axis."""
    # Get position data from API if not provided
    if position is None:
        position = await get_current_position()
        
    if not position:
        log_color("No active position found on BitGet.", YELLOW)
        return
    
    # Extract position details
    entry_price = position['entry_price']
    entry_time = datetime.fromisoformat(position['entry_time'])
    direction = position['direction']
    take_profits = position.get('take_profits', [])
    stop_loss = position.get('stop_loss')
    
    # Set time range
    until_time = datetime.now()
    since_time = until_time - timedelta(hours=hours_back)
    
    # Ensure entry_time is within our range
    if entry_time < since_time:
        log_color(f"Entry time {entry_time} is before our time range, adjusting...", YELLOW)
        entry_time = since_time + timedelta(minutes=10)
    
    # Fetch historical prices
    df = await fetch_historical_prices(
        position['symbol'],
        since_time,
        until_time,
        redis_client=redis_client
    )
    
    if df is None or df.empty:
        log_color("No price data available for this time range.", RED)
        return
    
    # Calculate price momentum/velocity
    df['price_change'] = df['close'].diff()
    df['momentum'] = df['price_change'].rolling(window=5).mean().fillna(0)
    
    # Normalize momentum for better visualization
    max_momentum = max(abs(df['momentum'].max()), abs(df['momentum'].min()))
    if max_momentum > 0:
        df['momentum_norm'] = df['momentum'] / max_momentum
    else:
        df['momentum_norm'] = df['momentum']
    
    # Normalize volume for visualization
    max_volume = df['volume'].max()
    if max_volume > 0:
        df['volume_norm'] = df['volume'] / max_volume
    else:
        df['volume_norm'] = df['volume']
    
    # Set up plotting style
    plt.style.use('dark_background')
    
    # Create figure for 3D plot
    fig = plt.figure(figsize=(14, 10))
    # Make sure to specify that we want a 3D Axes specifically
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('#121212')
    
    # Create a colormap based on price direction
    colors = []
    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['close'].iloc[i-1]:
            colors.append('green')
        else:
            colors.append('red')
    
    # Add first point color based on initial direction
    colors.insert(0, 'blue')
    
    # Create arrays for plotting
    x = np.arange(len(df))  # Time index
    y = df['close'].values   # Price
    z = df['momentum_norm'].values  # Momentum on z-axis
    
    # Plot 3D price path with colors based on price direction
    for i in range(1, len(df)):
        ax.plot([x[i-1], x[i]], [y[i-1], y[i]], [z[i-1], z[i]], 
                color=colors[i-1], linewidth=2)
        
        # Add points with size based on volume (with a size scaling value)
        point_volume = 30 * (df['volume_norm'].iloc[i] + 0.1)  # Add 0.1 to ensure min size
        ax.scatter(x[i], y[i], z[i], color=colors[i], s=point_volume, alpha=0.7)
    
    # Mark entry point on 3D plot
    entry_idx = np.abs((df['timestamp'] - entry_time).dt.total_seconds()).argmin()
    entry_x = x[entry_idx]
    entry_y = entry_price
    entry_z = z[entry_idx]
    
    # Use size parameter explicitly
    ax.scatter([entry_x], [entry_y], [entry_z], color='yellow', 
              s=200,  # Explicit size parameter
              marker='^' if direction == 'LONG' else 'v', 
              label=f"{direction} Entry at ${entry_price:.2f}")
    
    # Create horizontal surfaces for important price levels using meshgrid
    x_min, x_max = 0, len(df) - 1
    z_min, z_max = min(z), max(z)
    xx, zz = np.meshgrid([x_min, x_max], [z_min, z_max])
    
    # Entry price plane - using plot_wireframe instead of plot_surface
    yy = np.ones_like(xx) * entry_price
    ax.plot_wireframe(xx, yy, zz, color='yellow', alpha=0.2, linewidths=0.5)
    
    # Take profit planes
    for idx, tp in enumerate(take_profits):
        tp_price = tp.get('price')
        if tp_price:
            yy_tp = np.ones_like(xx) * tp_price
            ax.plot_wireframe(xx, yy_tp, zz, color='green', alpha=0.2, linewidths=0.5)
            
            # Add a label for the TP level - fix text parameters
            tp_label_x = x_max * 0.95
            tp_label_z = z_max * 0.8
            ax.text(tp_label_x, tp_price, tp_label_z, 
                   s=f"TP {idx+1}: ${tp_price:.2f}",  # Use s parameter for text
                   color='green', fontsize=9)
    
    # Stop loss plane
    if stop_loss:
        yy_sl = np.ones_like(xx) * stop_loss
        ax.plot_wireframe(xx, yy_sl, zz, color='red', alpha=0.2, linewidths=0.5)
        
        # Add a label for the SL level - fix text parameters
        sl_label_x = x_max * 0.95
        sl_label_z = z_min * 0.8
        ax.text(sl_label_x, stop_loss, sl_label_z, 
               s=f"SL: ${stop_loss:.2f}",  # Use s parameter for text
               color='red', fontsize=9)
    
    # Mark current price point
    current_price = df['close'].iloc[-1]
    current_x = x[-1]
    current_z = z[-1]
    
    ax.scatter([current_x], [current_price], [current_z], color='cyan', 
              s=150,  # Explicit size parameter
              marker='o', label=f"Current: ${current_price:.2f}")
    
    # Calculate PnL
    if direction == 'LONG':
        pnl_pct = ((current_price - entry_price) / entry_price * 100) * position.get('leverage', 1)
    else:
        pnl_pct = ((entry_price - current_price) / entry_price * 100) * position.get('leverage', 1)
    
    # Add informative text on figure
    pnl_color = 'green' if pnl_pct >= 0 else 'red'
    fig.text(0.5, 0.01, f"Current PnL: {pnl_pct:.2f}% ({position.get('unrealized_pnl', 0):.2f} USD)",
            ha='center', color=pnl_color, fontsize=11)
    
    # Add explanation of axes
    fig.text(0.02, 0.02, "X-axis: Time sequence\nY-axis: Price\nZ-axis: Price momentum\nPoint size: Volume",
            ha='left', color='white', fontsize=9)
    
    # Add data source info
    data_source = "Redis" if redis_client else "BitGet API"
    fig.text(0.5, 0.96, f"Data Source: {data_source} | Points: {len(df)}", ha='center', color='white', fontsize=9)
    
    # Set labels and title
    title_prefix = "[BitGet 3D]" if position.get('id') != 'simulated-1' else "[Simulated 3D]"
    ax.set_title(f"{title_prefix} BTC Price Flow with Momentum", color='white', fontsize=16)
    
    # Format axes
    time_ticks = np.linspace(0, len(df)-1, min(6, len(df)), dtype=int)
    time_labels = [df['timestamp'].iloc[i].strftime('%H:%M') for i in time_ticks]
    
    ax.set_xticks(time_ticks)
    ax.set_xticklabels(time_labels)
    ax.set_xlabel('Time', labelpad=10)
    ax.set_ylabel('Price (USD)', labelpad=10)
    # Make sure the 3D axis has the zlabel attribute
    ax.set_zlabel('Price Momentum', labelpad=10)
    
    # Text color
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    # Handle z-axis with proper check
    if hasattr(ax, 'zaxis'):
        ax.zaxis.label.set_color('white')
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    # Handle z-axis ticks with proper check
    if hasattr(ax, 'zaxis'):
        ax.tick_params(axis='z', colors='white')
    
    # Add grid for better depth perception
    ax.grid(True, alpha=0.2)
    
    # Calculate Fibonacci targets
    fib_targets = calculate_fibonacci_targets(
        entry_price, 
        direction,
        current_price
    )
    
    # Add Fibonacci targets as horizontal planes in 3D space
    for level, target_price in fib_targets.items():
        if level == 'closest_level':
            continue
            
        # Skip levels that are outside the chart range
        if target_price < min(df['close']) or target_price > max(df['close']):
            continue
            
        # Different colors for different Fibonacci levels
        fib_color = 'cyan'
        if float(level) >= 2.618:
            fib_color = 'magenta'
        elif float(level) >= 1.618:
            fib_color = 'yellow'
        elif float(level) >= 1.0:
            fib_color = 'green'
            
        # Create a plane at the Fibonacci level
        x_range = np.array([0, len(df.index) - 1])
        y_range = np.array([min(z), max(z)])
        X, Y = np.meshgrid(x_range, y_range)
        Z = np.ones(X.shape) * target_price
        
        # Plot the semi-transparent plane
        ax.plot_surface(
            X, Y, Z, 
            color=fib_color, 
            alpha=0.2, 
            linewidth=0,
            antialiased=True
        )
        
        # Add a line at the edge of the plane for better visibility
        ax.plot(
            x_range, 
            [min(z)] * 2, 
            [target_price] * 2, 
            color=fib_color, 
            linewidth=2, 
            linestyle='--',
            label=f"TP {level}x: {target_price:.2f}"
        )
    
    # Adjust viewing angle if the method exists
    if hasattr(ax, 'view_init'):
        ax.view_init(elev=30, azim=45)
    
    # Set legend
    ax.legend(loc='upper left')
    
    # Save the figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"position_flow_3d_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='#121212')
    
    log_color(f"3D position flow visualization saved as {filename}", GREEN)
    plt.show()

async def fetch_long_term_price_data(years=7, redis_client=None):
    """
    Fetch long-term (multi-year) BTC price data from Redis or API.
    
    Args:
        years: Number of years to fetch
        redis_client: Redis client connection (optional)
        
    Returns:
        DataFrame with long-term price data
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=365 * years)
    
    log_color(f"Fetching {years}-year BTC price data from {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}", BLUE)
    
    # Try to get data from Redis first
    if redis_client:
        try:
            log_color("Checking for long-term BTC data in Redis...", BLUE)
            
            # Check for historical keys that might contain our data
            historical_keys = redis_client.keys("btc_historical_*")
            if historical_keys:
                log_color(f"Found historical data keys: {historical_keys}", GREEN)
                
                # Try each key
                for key in historical_keys:
                    try:
                        key_type = redis_client.type(key)
                        if key_type == "hash":
                            # For hash data structure
                            data = redis_client.hgetall(key)
                            if data:
                                log_color(f"Found {len(data)} data points in {key}", GREEN)
                                records = []
                                for timestamp_str, price_str in data.items():
                                    try:
                                        timestamp = datetime.fromtimestamp(float(timestamp_str))
                                        price = float(price_str)
                                        records.append({
                                            'timestamp': timestamp,
                                            'close': price
                                        })
                                    except Exception as e:
                                        log_color(f"Error parsing entry {timestamp_str}, {price_str}: {e}", RED)
                                
                                if records:
                                    df = pd.DataFrame(records)
                                    df = df.sort_values('timestamp')
                                    log_color(f"Successfully loaded {len(df)} historical data points from Redis", GREEN)
                                    return df
                                
                        elif key_type == "list":
                            # For list data structure
                            data = redis_client.lrange(key, 0, -1)
                            if data:
                                log_color(f"Found {len(data)} data points in list {key}", GREEN)
                                # Process based on expected format
                                # You might need to adjust this parsing logic based on actual data format
                                records = []
                                for i, item in enumerate(data):
                                    try:
                                        # Try parsing as JSON
                                        entry = json.loads(item)
                                        timestamp = datetime.fromtimestamp(entry.get('timestamp', 0) / 1000)
                                        price = float(entry.get('close', 0))
                                        records.append({
                                            'timestamp': timestamp,
                                            'close': price
                                        })
                                    except json.JSONDecodeError:
                                        # Try parsing as string
                                        parts = item.split(',')
                                        if len(parts) >= 2:
                                            try:
                                                # Assuming format: timestamp,price
                                                timestamp = datetime.fromtimestamp(float(parts[0]))
                                                price = float(parts[1])
                                                records.append({
                                                    'timestamp': timestamp,
                                                    'close': price
                                                })
                                            except Exception as e:
                                                log_color(f"Error parsing list item: {e}", RED)
                                
                                if records:
                                    df = pd.DataFrame(records)
                                    df = df.sort_values('timestamp')
                                    log_color(f"Successfully loaded {len(df)} historical data points from Redis list", GREEN)
                                    return df
                    except Exception as e:
                        log_color(f"Error processing Redis key {key}: {e}", RED)
                        continue
            
            log_color("No suitable historical BTC data found in Redis", YELLOW)
        except Exception as e:
            log_color(f"Error processing Redis historical data: {e}", RED)
    
    # If Redis data is not available or failed to load, generate simulated data
    log_color("Generating simulated 7-year price data for demonstration", YELLOW)
    
    # Create date range for 7 years
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    
    # Initialize price series with realistic starting point
    np.random.seed(42)  # For reproducibility
    base_price = 1200  # Starting price (around 2014 levels)
    
    # Generate simulated prices
    prices = [base_price]
    for i in range(1, len(dates)):
        # Use a random walk with upward bias
        daily_return = np.random.normal(0.001, 0.03)  # Mean daily return ~0.1%, std dev 3%
        
        # Add some cyclical patterns
        cycle1 = 0.0002 * np.sin(2 * np.pi * i / 365)  # Annual cycle
        cycle2 = 0.0001 * np.sin(2 * np.pi * i / (365 * 4))  # 4-year cycle (halving)
        
        daily_return += cycle1 + cycle2
        
        # Calculate next price
        next_price = prices[-1] * (1 + daily_return)
        prices.append(next_price)
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': dates,
        'close': prices
    })
    
    log_color(f"Generated simulated data with {len(df)} price points", GREEN)
    return df

async def create_golden_ratio_simulation(actual_data):
    """
    Create a golden ratio price simulation based on actual data's starting point.
    
    Args:
        actual_data: DataFrame with actual BTC price data
        
    Returns:
        DataFrame with simulated golden ratio price data
    """
    log_color("Creating golden ratio price simulation...", BLUE)
    
    # Get the starting price from actual data
    start_price = actual_data['close'].iloc[0]
    
    # Calculate golden ratio (φ = 1.618033988749895)
    golden_ratio = (1 + np.sqrt(5)) / 2
    
    # Create simulated prices based on golden ratio growth
    dates = actual_data['timestamp']
    num_periods = len(dates)
    
    # Initialize price array
    golden_prices = np.zeros(num_periods)
    golden_prices[0] = start_price
    
    # Create Fibonacci-based growth pattern
    for i in range(1, num_periods):
        # Calculate period (using modulo to create cycles)
        period = i % 144  # 144-day cycle (roughly 5 months)
        
        if period < 89:  # Growth phase (Fibonacci number 89)
            # Growth rate based on golden ratio
            growth = (golden_ratio - 1) * 0.01 * (1 + 0.5 * np.sin(i / 21))  # Add sine wave for variability
        else:
            # Correction phase
            growth = -0.005 * (1 + 0.3 * np.sin(i / 13))
            
        # Apply growth rate
        golden_prices[i] = golden_prices[i-1] * (1 + growth)
    
    # Create DataFrame for golden ratio simulation
    golden_df = pd.DataFrame({
        'timestamp': dates,
        'golden_price': golden_prices
    })
    
    log_color(f"Generated golden ratio simulation with {len(golden_df)} price points", GREEN)
    return golden_df

async def visualize_golden_ratio_overlay(years=7, redis_client=None):
    """
    Create a visualization that overlays actual BTC price with a golden ratio simulation
    and shows Fibonacci levels for a 7-year period.
    
    Args:
        years: Number of years to analyze
        redis_client: Redis client connection (optional)
    """
    # Fetch long-term BTC price data
    price_data = await fetch_long_term_price_data(years, redis_client)
    
    if price_data is None or price_data.empty:
        log_color("No price data available for visualization.", RED)
        return
    
    # Generate golden ratio simulation
    golden_simulation = await create_golden_ratio_simulation(price_data)
    
    # Merge actual and simulated data
    combined_data = pd.merge(price_data, golden_simulation, on='timestamp')
    
    # Calculate Fibonacci levels based on price range
    max_price = combined_data['close'].max()
    min_price = combined_data['close'].min()
    price_range = max_price - min_price
    
    # Standard Fibonacci levels
    fibo_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618, 4.236]
    level_prices = [min_price + (level * price_range) for level in fibo_levels]
    
    # Create the plot
    plt.figure(figsize=(16, 9), facecolor='#121212')
    ax = plt.axes()
    
    # Plot actual BTC price
    plt.plot(combined_data['timestamp'], combined_data['close'], 
             label='BTC Actual Price', color='#f0f0f0', linewidth=2)
    
    # Plot golden ratio simulation
    plt.plot(combined_data['timestamp'], combined_data['golden_price'], 
             label='Golden Ratio Simulation', color='gold', linewidth=2, alpha=0.7)
    
    # Calculate and plot the difference
    combined_data['difference'] = combined_data['close'] - combined_data['golden_price']
    
    # Plot Fibonacci levels
    for level, price, fib in zip(level_prices, level_prices, fibo_levels):
        if min_price <= price <= max_price * 1.5:  # Show levels within reasonable range
            color = 'cyan'
            if fib == 0.618:  # Highlight golden ratio
                color = 'gold'
                linewidth = 2.0
                alpha = 0.8
            elif fib == 1.0:
                color = 'white'
                linewidth = 1.5
                alpha = 0.6
            else:
                linewidth = 1.0
                alpha = 0.4
                
            plt.axhline(y=price, color=color, linestyle='--', 
                       alpha=alpha, linewidth=linewidth,
                       label=f'Fibo {fib:.3f}: ${price:.2f}')
    
    # Mark halving events (approximate dates)
    halving_dates = [
        datetime(2016, 7, 9),
        datetime(2020, 5, 11),
        datetime(2024, 4, 20)
    ]
    
    for halving_date in halving_dates:
        if halving_date >= combined_data['timestamp'].min() and halving_date <= combined_data['timestamp'].max():
            plt.axvline(x=halving_date, color='magenta', linestyle='-', alpha=0.5, linewidth=1.5)
            
            # Get price at halving date
            closest_idx = (combined_data['timestamp'] - halving_date).abs().idxmin()
            price_at_halving = combined_data.loc[closest_idx, 'close']
            
            plt.text(halving_date, price_at_halving * 1.1, 
                    f"Halving\n{halving_date.strftime('%Y-%m-%d')}", 
                    color='magenta', fontsize=9, ha='center')
    
    # Calculate correlation between actual and golden ratio prices
    correlation = combined_data['close'].corr(combined_data['golden_price'])
    plt.figtext(0.5, 0.01, f"Correlation between actual price and golden ratio simulation: {correlation:.4f}", 
               ha='center', color='white', fontsize=11)
    
    # Add title and labels
    plt.title(f"{years}-Year BTC Price with Golden Ratio Overlay and Fibonacci Levels", 
             color='white', fontsize=16)
    plt.xlabel('Date', color='white', fontsize=12)
    plt.ylabel('Price (USD)', color='white', fontsize=12)
    
    # Format the plot
    plt.grid(True, alpha=0.2)
    plt.legend(loc='upper left', framealpha=0.7)
    
    # Format time axis
    years_fmt = mdates.DateFormatter('%Y')
    plt.gca().xaxis.set_major_formatter(years_fmt)
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    
    # Format price axis (log scale)
    plt.yscale('log')
    plt.grid(True, alpha=0.2, which='both')
    
    # Style the graph
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    # Add secondary y-axis for difference
    ax2 = ax.twinx()
    ax2.fill_between(combined_data['timestamp'], combined_data['difference'], 
                    alpha=0.2, color='green', where=(combined_data['difference'] > 0))
    ax2.fill_between(combined_data['timestamp'], combined_data['difference'], 
                    alpha=0.2, color='red', where=(combined_data['difference'] < 0))
    ax2.set_ylabel('Difference (Actual - Golden)', color='white', fontsize=12)
    ax2.tick_params(colors='white')
    
    # Save the figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"btc_golden_ratio_{years}yr_{timestamp}.png"
    plt.tight_layout(rect=(0, 0.03, 1, 0.97))
    plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='#121212')
    
    log_color(f"{years}-year BTC golden ratio visualization saved as {filename}", GREEN)
    plt.show()

async def main():
    parser = argparse.ArgumentParser(description='Visualize BTC position price flow using Redis or BitGet API')
    parser.add_argument('--hours', type=int, default=24, help='Number of hours to look back for analysis')
    parser.add_argument('--use-bitget', action='store_true', help='Use actual BitGet positions (default)')
    parser.add_argument('--use-simulated', action='store_true', help='Use simulated position for testing')
    parser.add_argument('--2d', dest='use_2d', action='store_true', help='Use 2D visualization')
    parser.add_argument('--3d', dest='use_3d', action='store_true', help='Use 3D visualization')
    parser.add_argument('--no-redis', action='store_true', help='Skip Redis and use BitGet API directly')
    parser.add_argument('--check-redis', action='store_true', help='Only check Redis connection and available keys')
    parser.add_argument('--golden-ratio', action='store_true', help='Generate 7-year BTC chart with golden ratio overlay')
    parser.add_argument('--years', type=int, default=7, help='Number of years for golden ratio analysis')
    
    args = parser.parse_args()
    
    # Connect to Redis
    redis_client = None
    if not args.no_redis:
        redis_client = connect_to_redis()
    
    # If --check-redis flag is set, just check Redis and exit
    if args.check_redis:
        if redis_client:
            log_color("Redis connection successful. Run without --check-redis to continue.", GREEN)
        else:
            log_color("Redis connection failed. Use --no-redis flag to skip Redis.", RED)
        return
    
    # If golden ratio flag is set, run that visualization
    if args.golden_ratio:
        await visualize_golden_ratio_overlay(years=args.years, redis_client=redis_client)
        return
        
    position = None
    if args.use_simulated:
        position = get_simulated_position()
    
    # Choose visualization mode
    if args.use_3d:
        await track_position_flow_3d(position=position, hours_back=args.hours, redis_client=redis_client)
    else:  # Default to 2D
        await track_position_flow_2d(position=position, hours_back=args.hours, redis_client=redis_client)

if __name__ == "__main__":
    asyncio.run(main()) 