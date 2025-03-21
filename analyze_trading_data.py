#!/usr/bin/env python3
"""
Bitcoin Trading Data Analyzer

This script connects to InfluxDB and analyzes trading data, including:
- Position history
- Market maker trap events
- Balance history
- PnL performance

It generates visualizations to help understand trading patterns and performance.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# InfluxDB configuration
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "w4JzUNsut5GjPBB72ts_U3D5r6ojYkWGUTTHZdMOjVXmJqX8Wnuyp3EYLRzi9H5BLwM9hAEltSFdEF-ZDwSjOg==")
ORG = os.getenv("INFLUX_ORG", "omega")
BUCKET = os.getenv("INFLUX_BUCKET", "mm_traps")

# Time range for data analysis
TIME_RANGE = "-30d"  # Last 30 days

def connect_to_influxdb():
    """Connect to InfluxDB and return client."""
    try:
        client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=ORG
        )
        health = client.health()
        if health.status == "pass":
            print("✅ Connected to InfluxDB")
            return client
        else:
            print(f"❌ InfluxDB health check failed: {health.message}")
            return None
    except Exception as e:
        print(f"❌ Error connecting to InfluxDB: {e}")
        return None

def query_mm_trap_events(client):
    """Query market maker trap events from InfluxDB."""
    query_api = client.query_api()
    
    query = f'''
    from(bucket: "{BUCKET}")
        |> range(start: {TIME_RANGE})
        |> filter(fn: (r) => r._measurement == "mm_traps" or r._measurement == "trap_events")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    
    try:
        result = query_api.query_data_frame(query)
        if isinstance(result, list) and len(result) > 0:
            result = pd.concat(result)
        
        # Print summary of trap events
        if not result.empty:
            print(f"\n📊 Found {len(result)} market maker trap events")
            print(f"Trap types: {result['type'].value_counts().to_dict()}")
            
            # Calculate confidence statistics
            if 'confidence' in result.columns:
                print(f"Average confidence: {result['confidence'].mean():.2f}")
                print(f"High confidence events (>0.7): {len(result[result['confidence'] > 0.7])}")
        else:
            print("No market maker trap events found")
            
        return result
    except Exception as e:
        print(f"❌ Error querying trap events: {e}")
        return pd.DataFrame()

def query_position_data(client):
    """Query position data from InfluxDB."""
    query_api = client.query_api()
    
    query = f'''
    from(bucket: "{BUCKET}")
        |> range(start: {TIME_RANGE})
        |> filter(fn: (r) => r._measurement == "positions")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    
    try:
        result = query_api.query_data_frame(query)
        if isinstance(result, list) and len(result) > 0:
            result = pd.concat(result)
        
        # Print summary of positions
        if not result.empty:
            print(f"\n📈 Found {len(result)} position records")
            if 'side' in result.columns:
                print(f"Position sides: {result['side'].value_counts().to_dict()}")
            if 'unrealizedPnl' in result.columns:
                print(f"Total unrealized PnL: {result['unrealizedPnl'].sum():.2f} USDT")
        else:
            print("No position data found")
            
        return result
    except Exception as e:
        print(f"❌ Error querying position data: {e}")
        return pd.DataFrame()

def query_balance_history(client):
    """Query balance history from InfluxDB."""
    query_api = client.query_api()
    
    query = f'''
    from(bucket: "{BUCKET}")
        |> range(start: {TIME_RANGE})
        |> filter(fn: (r) => r._measurement == "balance" or r._measurement == "account_balance")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    
    try:
        result = query_api.query_data_frame(query)
        if isinstance(result, list) and len(result) > 0:
            result = pd.concat(result)
        
        # Print summary of balance data
        if not result.empty:
            print(f"\n💰 Found {len(result)} balance records")
            if 'total' in result.columns:
                latest = result.sort_values('_time').iloc[-1]
                earliest = result.sort_values('_time').iloc[0]
                print(f"Latest total balance: {latest['total']:.2f} USDT")
                print(f"Change over period: {latest['total'] - earliest['total']:.2f} USDT")
        else:
            print("No balance data found")
            
        return result
    except Exception as e:
        print(f"❌ Error querying balance history: {e}")
        return pd.DataFrame()

def plot_trap_events(trap_data):
    """Plot market maker trap events."""
    if trap_data.empty:
        return
    
    # Ensure _time column is datetime
    trap_data['_time'] = pd.to_datetime(trap_data['_time'])
    
    # Create figure with price and trap events
    if 'btc_price' in trap_data.columns:
        fig = px.line(trap_data, x='_time', y='btc_price', title='BTC Price with Market Maker Trap Events')
        
        # Add trap events as markers, colored by type
        if 'type' in trap_data.columns:
            for trap_type in trap_data['type'].unique():
                trap_subset = trap_data[trap_data['type'] == trap_type]
                fig.add_trace(
                    go.Scatter(
                        x=trap_subset['_time'],
                        y=trap_subset['btc_price'],
                        mode='markers',
                        name=trap_type,
                        marker=dict(size=10)
                    )
                )
        
        # Improve layout
        fig.update_layout(
            xaxis_title='Time',
            yaxis_title='BTC Price (USDT)',
            legend_title='Trap Type',
            height=600
        )
        
        # Save figure
        fig.write_html('trap_events.html')
        print("📊 Trap events visualization saved to trap_events.html")
    else:
        print("Cannot plot trap events: missing btc_price column")

def plot_balance_history(balance_data):
    """Plot balance history."""
    if balance_data.empty or 'total' not in balance_data.columns:
        return
    
    # Ensure _time column is datetime
    balance_data['_time'] = pd.to_datetime(balance_data['_time'])
    
    # Create figure
    fig = px.line(
        balance_data.sort_values('_time'), 
        x='_time', 
        y='total', 
        title='Account Balance History'
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Total Balance (USDT)',
        height=500
    )
    
    # Add annotations for significant changes
    balance_data['change'] = balance_data['total'].diff()
    significant_changes = balance_data[abs(balance_data['change']) > 10].sort_values('_time')
    
    for _, row in significant_changes.iterrows():
        fig.add_annotation(
            x=row['_time'],
            y=row['total'],
            text=f"{row['change']:.2f}",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40
        )
    
    # Save figure
    fig.write_html('balance_history.html')
    print("📈 Balance history visualization saved to balance_history.html")

def analyze_pnl_by_trap_type(trap_data, position_data):
    """Analyze PnL by trap type to see effectiveness of signals."""
    if trap_data.empty or position_data.empty:
        return
    
    # Ensure time columns are datetime
    trap_data['_time'] = pd.to_datetime(trap_data['_time'])
    position_data['_time'] = pd.to_datetime(position_data['_time'])
    
    # Check if we have the necessary columns
    if 'type' not in trap_data.columns or 'realizedPnl' not in position_data.columns:
        print("Cannot analyze PnL by trap type: missing required columns")
        return
    
    trap_types = trap_data['type'].unique()
    results = {}
    
    # Find positions that follow trap events (within 30 minutes)
    for trap_type in trap_types:
        trap_events = trap_data[trap_data['type'] == trap_type]
        total_pnl = 0
        winning_trades = 0
        total_trades = 0
        
        for _, trap in trap_events.iterrows():
            # Find positions opened after this trap (within 30 min)
            next_positions = position_data[
                (position_data['_time'] > trap['_time']) & 
                (position_data['_time'] <= trap['_time'] + pd.Timedelta(minutes=30))
            ]
            
            if not next_positions.empty:
                total_trades += len(next_positions)
                pnl = next_positions['realizedPnl'].sum()
                total_pnl += pnl
                winning_trades += len(next_positions[next_positions['realizedPnl'] > 0])
        
        if total_trades > 0:
            win_rate = winning_trades / total_trades * 100
            results[trap_type] = {
                'trades': total_trades,
                'pnl': total_pnl,
                'win_rate': win_rate
            }
    
    # Print results
    if results:
        print("\n📊 PnL Analysis by Trap Type")
        print("=" * 50)
        for trap_type, stats in results.items():
            print(f"Trap Type: {trap_type}")
            print(f"  Trades: {stats['trades']}")
            print(f"  Total PnL: {stats['pnl']:.2f} USDT")
            print(f"  Win Rate: {stats['win_rate']:.1f}%")
            print("-" * 50)

def main():
    """Main function to analyze trading data."""
    client = connect_to_influxdb()
    if not client:
        return
    
    # Query data
    trap_data = query_mm_trap_events(client)
    position_data = query_position_data(client)
    balance_data = query_balance_history(client)
    
    # Generate visualizations
    plot_trap_events(trap_data)
    plot_balance_history(balance_data)
    
    # Analyze performance
    analyze_pnl_by_trap_type(trap_data, position_data)
    
    # Close client
    client.close()
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main() 