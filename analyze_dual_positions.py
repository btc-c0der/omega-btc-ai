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
BitGet Dual Position Trader Performance Analyzer

This script analyzes the performance of the BitGet dual position traders,
including position history, PnL, and correlation with market maker trap events.
"""

import os
import asyncio
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dotenv import load_dotenv
from datetime import datetime, timedelta
from influxdb_client.client.influxdb_client import InfluxDBClient

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
                
            # Ensure time column is datetime
            result['_time'] = pd.to_datetime(result['_time'])
            
            # Sort by time for better analysis
            result = result.sort_values('_time')
            
            return result
        else:
            print("No position data found")
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error querying position data: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def query_trade_data(client):
    """Query trade execution data from InfluxDB."""
    query_api = client.query_api()
    
    query = f'''
    from(bucket: "{BUCKET}")
        |> range(start: {TIME_RANGE})
        |> filter(fn: (r) => r._measurement == "trades")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    
    try:
        result = query_api.query_data_frame(query)
        if isinstance(result, list) and len(result) > 0:
            result = pd.concat(result)
        
        # Print summary of trades
        if not result.empty:
            print(f"\n🔄 Found {len(result)} trade execution records")
            
            if 'side' in result.columns:
                print(f"Trade sides: {result['side'].value_counts().to_dict()}")
                
            if 'realized_pnl' in result.columns:
                print(f"Total realized PnL: {result['realized_pnl'].sum():.2f} USDT")
                
            # Ensure time column is datetime
            result['_time'] = pd.to_datetime(result['_time'])
            
            # Sort by time for better analysis
            result = result.sort_values('_time')
            
            return result
        else:
            print("No trade data found")
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error querying trade data: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def plot_cumulative_pnl(position_data, trade_data):
    """Create visualization of cumulative PnL over time."""
    # Check if we have the necessary data
    if (position_data.empty and trade_data.empty) or \
       ('realizedPnl' not in position_data.columns and 'realized_pnl' not in trade_data.columns):
        print("Cannot create PnL visualization: missing required data")
        return
    
    # Create figure with two subplots
    fig = make_subplots(
        rows=2, 
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Cumulative PnL', 'Daily PnL')
    )
    
    # Prepare PnL data
    df = None
    
    if not position_data.empty and 'realizedPnl' in position_data.columns:
        df = position_data.copy()
        df['date'] = df['_time'].dt.date
        df['pnl'] = df['realizedPnl']
    elif not trade_data.empty and 'realized_pnl' in trade_data.columns:
        df = trade_data.copy()
        df['date'] = df['_time'].dt.date
        df['pnl'] = df['realized_pnl']
    
    if df is not None:
        # Calculate cumulative PnL
        df['cumulative_pnl'] = df['pnl'].cumsum()
        
        # Add cumulative PnL line
        fig.add_trace(
            go.Scatter(
                x=df['_time'],
                y=df['cumulative_pnl'],
                mode='lines',
                name='Cumulative PnL',
                line=dict(color='green', width=2)
            ),
            row=1, col=1
        )
        
        # Calculate daily PnL
        daily_pnl = df.groupby('date')['pnl'].sum().reset_index()
        
        # Add daily PnL bars
        fig.add_trace(
            go.Bar(
                x=daily_pnl['date'],
                y=daily_pnl['pnl'],
                name='Daily PnL',
                marker_color=daily_pnl['pnl'].apply(lambda x: 'green' if x > 0 else 'red')
            ),
            row=2, col=1
        )
        
        # Add horizontal line at 0
        fig.add_shape(
            type="line",
            x0=df['_time'].min(),
            x1=df['_time'].max(),
            y0=0,
            y1=0,
            line=dict(color="black", width=1, dash="dash"),
            row=1, col=1
        )
        
        fig.add_shape(
            type="line",
            x0=daily_pnl['date'].min(),
            x1=daily_pnl['date'].max(),
            y0=0,
            y1=0,
            line=dict(color="black", width=1, dash="dash"),
            row=2, col=1
        )
        
        # Improve layout
        fig.update_layout(
            title="BitGet Dual Position Trader Performance",
            xaxis_title="Date",
            height=800,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Update y-axis titles
        fig.update_yaxes(title_text="Cumulative PnL (USDT)", row=1, col=1)
        fig.update_yaxes(title_text="Daily PnL (USDT)", row=2, col=1)
        
        # Save figure
        fig.write_html('dual_trader_pnl.html')
        print("📈 Dual trader PnL visualization saved to dual_trader_pnl.html")

def plot_position_size_history(position_data):
    """Create visualization of position size history."""
    if position_data.empty or 'positionAmt' not in position_data.columns:
        print("Cannot create position size visualization: missing required data")
        return
    
    # Create figure
    fig = go.Figure()
    
    # If we have account data, split by account
    if 'account' in position_data.columns:
        for account in position_data['account'].unique():
            account_data = position_data[position_data['account'] == account]
            fig.add_trace(
                go.Scatter(
                    x=account_data['_time'],
                    y=account_data['positionAmt'],
                    mode='lines',
                    name=f"Account: {account}"
                )
            )
    else:
        # Add position size line
        fig.add_trace(
            go.Scatter(
                x=position_data['_time'],
                y=position_data['positionAmt'],
                mode='lines',
                name='Position Size'
            )
        )
    
    # Add horizontal line at 0
    fig.add_shape(
        type="line",
        x0=position_data['_time'].min(),
        x1=position_data['_time'].max(),
        y0=0,
        y1=0,
        line=dict(color="black", width=1, dash="dash")
    )
    
    # Improve layout
    fig.update_layout(
        title="BitGet Position Size History",
        xaxis_title="Date",
        yaxis_title="Position Size (BTC)",
        height=600
    )
    
    # Save figure
    fig.write_html('position_size_history.html')
    print("📊 Position size history visualization saved to position_size_history.html")

def calculate_performance_metrics(trade_data):
    """Calculate performance metrics for the trading strategy."""
    if trade_data.empty or 'realized_pnl' not in trade_data.columns:
        print("Cannot calculate performance metrics: missing required data")
        return
    
    # Calculate basic metrics
    total_trades = len(trade_data)
    winning_trades = len(trade_data[trade_data['realized_pnl'] > 0])
    losing_trades = len(trade_data[trade_data['realized_pnl'] <= 0])
    
    win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
    
    total_pnl = trade_data['realized_pnl'].sum()
    avg_win = trade_data[trade_data['realized_pnl'] > 0]['realized_pnl'].mean() if winning_trades > 0 else 0
    avg_loss = trade_data[trade_data['realized_pnl'] <= 0]['realized_pnl'].mean() if losing_trades > 0 else 0
    
    profit_factor = -1 * trade_data[trade_data['realized_pnl'] > 0]['realized_pnl'].sum() / trade_data[trade_data['realized_pnl'] < 0]['realized_pnl'].sum() if trade_data[trade_data['realized_pnl'] < 0].sum() != 0 else float('inf')
    
    # Print metrics
    print("\n📊 Trading Performance Metrics")
    print("=" * 50)
    print(f"Total trades: {total_trades}")
    print(f"Winning trades: {winning_trades} ({win_rate:.1f}%)")
    print(f"Losing trades: {losing_trades} ({100 - win_rate:.1f}%)")
    print(f"Total PnL: {total_pnl:.2f} USDT")
    print(f"Average win: {avg_win:.2f} USDT")
    print(f"Average loss: {avg_loss:.2f} USDT")
    print(f"Profit factor: {profit_factor:.2f}")
    print("-" * 50)
    
    # Create a summary dataframe for visualization
    metrics_df = pd.DataFrame({
        'Metric': ['Win Rate', 'Profit Factor', 'Avg Win', 'Avg Loss'],
        'Value': [win_rate, profit_factor, avg_win, -1 * avg_loss if avg_loss < 0 else avg_loss]
    })
    
    # Create bar chart
    fig = px.bar(
        metrics_df,
        x='Metric',
        y='Value',
        title='Trading Performance Metrics',
        color='Metric',
        text='Value'
    )
    
    # Format text
    fig.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside'
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_title="Metrics",
        yaxis_title="Value",
        height=500
    )
    
    # Save figure
    fig.write_html('performance_metrics.html')
    print("📊 Performance metrics visualization saved to performance_metrics.html")

async def check_current_positions():
    """Check current open positions using the BitGetDualPositionTraders class."""
    try:
        # Only import if we're actually running this function
        from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders
        
        # Initialize dual traders
        dual_traders = BitGetDualPositionTraders(
            use_testnet=False,
            long_capital=float(os.getenv('INITIAL_CAPITAL', '24.0')),
            short_capital=float(os.getenv('INITIAL_CAPITAL', '24.0')),
            symbol=os.getenv('TRADING_SYMBOL', 'BTCUSDT'),
            long_leverage=int(os.getenv('MAX_LEVERAGE', '20')),
            short_leverage=int(os.getenv('MAX_LEVERAGE', '20')),
            long_sub_account=os.getenv('STRATEGIC_SUB_ACCOUNT_NAME', ''),
            short_sub_account="fst_short"
        )
        
        # Initialize traders
        await dual_traders.initialize()
        
        # Get positions
        long_positions, long_pnl = await dual_traders._get_trader_metrics(dual_traders.long_trader)
        short_positions, short_pnl = await dual_traders._get_trader_metrics(dual_traders.short_trader)
        
        # Print summary
        print("\n====== CURRENT POSITION SUMMARY ======")
        print(f"Long positions: {len(long_positions)}")
        print(f"Short positions: {len(short_positions)}")
        print(f"Long PnL: {long_pnl:.2f} USDT")
        print(f"Short PnL: {short_pnl:.2f} USDT")
        print(f"Total PnL: {(long_pnl + short_pnl):.2f} USDT")
        
        # Close connections
        if hasattr(dual_traders, 'long_trader') and dual_traders.long_trader:
            for name, trader in dual_traders.long_trader.traders.items():
                if hasattr(trader, 'exchange') and hasattr(trader.exchange, 'close'):
                    await trader.exchange.close()
        
        if hasattr(dual_traders, 'short_trader') and dual_traders.short_trader:
            for name, trader in dual_traders.short_trader.traders.items():
                if hasattr(trader, 'exchange') and hasattr(trader.exchange, 'close'):
                    await trader.exchange.close()
                    
    except Exception as e:
        print(f"❌ Error checking current positions: {e}")
        import traceback
        traceback.print_exc()

async def main_async():
    """Async main function for handling both InfluxDB and API operations."""
    # Connect to InfluxDB
    client = connect_to_influxdb()
    if not client:
        return
    
    try:
        # Query data
        position_data = query_position_data(client)
        trade_data = query_trade_data(client)
        
        # Generate visualizations
        plot_cumulative_pnl(position_data, trade_data)
        plot_position_size_history(position_data)
        
        # Calculate performance metrics
        calculate_performance_metrics(trade_data)
        
        # Check current positions 
        # This uses the actual BitGet API via the BitGetDualPositionTraders class
        await check_current_positions()
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close client
        client.close()
        print("\n✅ Dual position analysis complete!")

def main():
    """Main function to analyze dual position trader performance."""
    asyncio.run(main_async())

if __name__ == "__main__":
    main() 