#!/usr/bin/env python3
"""
OMEGA BTC AI - Position Flow Tracker
==============================

This script visualizes the price flow of a BTC position from entry to current price,
showing how the price moved relative to take profit and stop loss targets.
"""

import os
import sys
import json
import asyncio
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from dotenv import load_dotenv
import ccxt.async_support as ccxt

# Load environment variables
load_dotenv()

# Get API credentials from environment variables
BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_SECRET_KEY = os.getenv('BITGET_SECRET_KEY')
BITGET_PASSPHRASE = os.getenv('BITGET_PASSPHRASE')

async def fetch_historical_prices(symbol, since, until, timeframe='1m'):
    """Fetch historical prices from BitGet exchange."""
    exchange = ccxt.bitget({
        'apiKey': BITGET_API_KEY,
        'secret': BITGET_SECRET_KEY,
        'password': BITGET_PASSPHRASE,
        'enableRateLimit': True
    })
    
    try:
        # Convert timestamps to milliseconds if needed
        if isinstance(since, datetime):
            since = int(since.timestamp() * 1000)
        if isinstance(until, datetime):
            until = int(until.timestamp() * 1000)
            
        print(f"Fetching historical prices from {datetime.fromtimestamp(since/1000)} to {datetime.fromtimestamp(until/1000)}")
        
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
        print("Fetching current positions from BitGet...")
        positions = await exchange.fetch_positions()
        
        # Filter for active positions
        active_positions = [p for p in positions if p.get('contracts', 0) and float(str(p.get('contracts', 0))) > 0]
        
        if not active_positions:
            print("No active positions found.")
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
                
                print(f"Found {direction} position with entry price {entry_price} and current PnL {unrealized_pnl}")
                return position_data
                
        return None
            
    finally:
        await exchange.close()

def get_simulated_position():
    """Create a simulated position for testing."""
    print("Creating simulated position...")
    
    # Current BTC price (this would be fetched in a real implementation)
    # For now, let's use a hard-coded price
    current_price = 84300.0  # Example price
    
    # Create a simulated position
    entry_time = datetime.now() - timedelta(hours=12)
    entry_price = current_price - 200  # Entry 200 below current
    
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
    
    print(f"Created simulated {direction} position with entry price {entry_price}")
    return position_data

async def track_position_flow(position=None, hours_back=24, symbol="BTC/USDT:USDT"):
    """Track and visualize the price flow of a position."""
    # Get position data from API if not provided
    if position is None:
        position = await get_current_position()
        
    if not position:
        print("No active position found on BitGet.")
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
        entry_time = since_time + timedelta(minutes=10)
    
    # Fetch historical prices
    df = await fetch_historical_prices(
        symbol,
        since_time,
        until_time
    )
    
    if df.empty:
        print("No price data available for this time range.")
        return
    
    # Create plot
    plt.figure(figsize=(12, 8))
    plt.style.use('dark_background')
    
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
            # Safely convert timestamp to matplotlib date format
            first_timestamp_num = mdates.date2num(df['timestamp'].iloc[0]) if not df.empty else mdates.date2num(entry_time)
            plt.text(first_timestamp_num, tp_price, f"TP{idx+1}: ${tp_price:.2f}", 
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
    
    # Save the figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"position_flow_{timestamp}.png"
    plt.savefig(filename)
    
    print(f"Position flow visualization saved as {filename}")
    plt.show()

async def main():
    parser = argparse.ArgumentParser(description='Visualize BTC position price flow')
    parser.add_argument('--hours', type=int, default=24, help='Number of hours to look back for analysis')
    parser.add_argument('--use-bitget', action='store_true', help='Use actual BitGet positions (default)')
    parser.add_argument('--use-simulated', action='store_true', help='Use simulated position for testing')
    
    args = parser.parse_args()
    
    if args.use_simulated:
        simulated_position = get_simulated_position()
        await track_position_flow(position=simulated_position, hours_back=args.hours)
    else:
        # Default: use BitGet position
        await track_position_flow(hours_back=args.hours)

if __name__ == "__main__":
    asyncio.run(main()) 