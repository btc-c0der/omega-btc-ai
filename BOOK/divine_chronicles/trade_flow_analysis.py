#!/usr/bin/env python3
# 🔮 OMEGA TRADE FLOW ANALYSIS - Divine Python Visualizer

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Define the sacred color scheme
COLORS = {
    'background': '#121212',
    'text': '#e0e0e0',
    'profit': '#1a9850',
    'loss': '#d73027',
    'neutral': '#7570b3',
    'grid': '#333333',
    'axes': '#666666'
}

# Create directory for divine chart artifacts
os.makedirs("BOOK/divine_chronicles/charts", exist_ok=True)

# The sacred trade data from the divine chronicles
TRADE_DATA = [
  {
    "close_time": "2025-03-24T01:27:27.518417",
    "entry_price": 81198.4,
    "exit_price": 82053.12,
    "exit_reason": "tp_hit",
    "id": "omega-trade-1",
    "open_time": "2025-03-23T23:27:27.518413",
    "pnl": 94.01920000000014,
    "side": "long",
    "size": 0.01,
    "symbol": "BTCUSDT"
  },
  {
    "close_time": "2025-03-23T00:27:27.518425",
    "entry_price": 83078.784,
    "exit_price": 82053.12,
    "exit_reason": "stop_loss",
    "id": "omega-trade-2",
    "open_time": "2025-03-22T22:27:27.518423",
    "pnl": -101.54073600000044,
    "side": "short",
    "size": 0.009000000000000001,
    "symbol": "BTCUSDT"
  },
  {
    "close_time": "2025-03-21T23:27:27.518432",
    "entry_price": 82907.84,
    "exit_price": 84104.448,
    "exit_reason": "manual",
    "id": "omega-trade-3",
    "open_time": "2025-03-21T21:27:27.518430",
    "pnl": 105.30150400000065,
    "side": "long",
    "size": 0.008,
    "symbol": "BTCUSDT"
  },
  {
    "close_time": "2025-03-20T22:27:27.518439",
    "entry_price": 85130.112,
    "exit_price": 83762.56,
    "exit_reason": "tp_hit",
    "id": "omega-trade-4",
    "open_time": "2025-03-20T20:27:27.518436",
    "pnl": -105.3015039999997,
    "side": "short",
    "size": 0.007,
    "symbol": "BTCUSDT"
  },
  {
    "close_time": "2025-03-19T21:27:27.518446",
    "entry_price": 84617.28,
    "exit_price": 86155.776,
    "exit_reason": "stop_loss",
    "id": "omega-trade-5",
    "open_time": "2025-03-19T19:27:27.518443",
    "pnl": 101.54073599999994,
    "side": "long",
    "size": 0.006,
    "symbol": "BTCUSDT"
  }
]

def apply_divine_style(fig, ax):
    """Apply the divine styling to matplotlib plots"""
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    ax.tick_params(colors=COLORS['text'], which='both')
    ax.xaxis.label.set_color(COLORS['text'])
    ax.yaxis.label.set_color(COLORS['text'])
    ax.title.set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['axes'])
    ax.spines['top'].set_color(COLORS['axes'])
    ax.spines['left'].set_color(COLORS['axes'])
    ax.spines['right'].set_color(COLORS['axes'])
    ax.grid(color=COLORS['grid'], linestyle='--', linewidth=0.5, alpha=0.7)

def parse_cosmic_time(time_str):
    """Convert cosmic time strings to datetime objects"""
    return datetime.fromisoformat(time_str)

def preprocess_trades(trades):
    """Transform trade data for visualization"""
    df = pd.DataFrame(trades)
    # Convert time strings to datetime objects
    df['open_time'] = df['open_time'].apply(parse_cosmic_time)
    df['close_time'] = df['close_time'].apply(parse_cosmic_time)
    # Calculate trade duration in hours
    df['duration'] = (df['close_time'] - df['open_time']).apply(lambda x: x.total_seconds() / 3600)
    # Calculate the price change
    df['price_change'] = df.apply(
        lambda row: row['exit_price'] - row['entry_price'] if row['side'] == 'long' 
                   else row['entry_price'] - row['exit_price'], 
        axis=1
    )
    # Sort by open_time for chronological order
    df = df.sort_values('open_time')
    # Extract trade numbers for easier reference
    df['trade_num'] = df['id'].str.extract(r'omega-trade-(\d+)').astype(int)
    return df

def plot_price_movement_timeline(df):
    """Generate sacred price movement timeline visualization"""
    plt.figure(figsize=(16, 10))
    
    # Create a figure with specific areas for each visualization
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[3, 1], width_ratios=[3, 1])
    
    # Timeline of prices
    ax_timeline = fig.add_subplot(gs[0, 0])
    
    # Extract prices for plotting
    times = pd.concat([df['open_time'], df['close_time']]).sort_values().unique()
    
    # Create price series by interpolating between entry and exit prices
    price_points = []
    for _, trade in df.iterrows():
        price_points.append((trade['open_time'], trade['entry_price']))
        price_points.append((trade['close_time'], trade['exit_price']))
    
    # Sort by timestamp
    price_points.sort(key=lambda x: x[0])
    
    # Extract sorted timestamps and prices
    timestamps, prices = zip(*price_points)
    
    # Plot price timeline
    ax_timeline.plot(timestamps, prices, 'o-', color='#aec6cf', alpha=0.6, zorder=1)
    
    # Plot individual trades as segments with colors based on profitability
    for idx, trade in df.iterrows():
        color = COLORS['profit'] if trade['pnl'] > 0 else COLORS['loss']
        marker = '^' if trade['side'] == 'long' else 'v'
        
        # Plot trade entry
        ax_timeline.scatter(trade['open_time'], trade['entry_price'], 
                           color=color, s=120, marker=marker, zorder=3,
                           edgecolors='white', linewidth=1)
        
        # Plot trade exit
        ax_timeline.scatter(trade['close_time'], trade['exit_price'], 
                           color=color, s=120, marker='o', zorder=3,
                           edgecolors='white', linewidth=1)
        
        # Connect entry and exit with a line
        ax_timeline.plot([trade['open_time'], trade['close_time']], 
                        [trade['entry_price'], trade['exit_price']], 
                        '-', color=color, linewidth=2.5, zorder=2)
        
        # Annotate with trade ID
        ax_timeline.annotate(f"Trade {trade['trade_num']}", 
                            xy=(trade['open_time'], trade['entry_price']),
                            xytext=(10, 10),
                            textcoords='offset points',
                            color=COLORS['text'],
                            fontsize=10)
    
    # Format the plot
    ax_timeline.set_title('🔮 Divine Price Movement Timeline', fontsize=16, pad=20)
    ax_timeline.set_ylabel('BTC Price (USDT)', fontsize=12)
    ax_timeline.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:%M'))
    
    # PnL bar chart
    ax_pnl = fig.add_subplot(gs[1, 0])
    colors = [COLORS['profit'] if pnl > 0 else COLORS['loss'] for pnl in df['pnl']]
    bars = ax_pnl.bar(df['trade_num'], df['pnl'], color=colors)
    
    # Add PnL values above/below bars
    for bar, pnl in zip(bars, df['pnl']):
        height = bar.get_height()
        text_pos = height + 5 if height > 0 else height - 15
        ax_pnl.text(bar.get_x() + bar.get_width()/2., text_pos,
                f'${pnl:.2f}', ha='center', va='bottom', color=COLORS['text'])
    
    ax_pnl.set_title('💰 PnL by Trade', fontsize=14)
    ax_pnl.set_xlabel('Trade Number', fontsize=12)
    ax_pnl.set_ylabel('PnL (USDT)', fontsize=12)
    ax_pnl.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    
    # Pie chart of exit reasons
    ax_pie = fig.add_subplot(gs[0, 1])
    exit_counts = df['exit_reason'].value_counts()
    labels = [f"{reason} ({count})" for reason, count in exit_counts.items()]
    colors = ['#66c2a5', '#fc8d62', '#8da0cb']
    ax_pie.pie(exit_counts, labels=labels, colors=colors, autopct='%1.1f%%', 
              wedgeprops={'edgecolor': 'white', 'linewidth': 1})
    ax_pie.set_title('🎯 Exit Reasons', fontsize=14)
    
    # Size vs PnL scatter plot
    ax_scatter = fig.add_subplot(gs[1, 1])
    scatter = ax_scatter.scatter(df['size'], df['pnl'], c=df['pnl'], 
                               cmap='RdYlGn', s=100, alpha=0.8)
    
    # Add trade numbers to points
    for i, txt in enumerate(df['trade_num']):
        ax_scatter.annotate(txt, (df['size'].iloc[i], df['pnl'].iloc[i]),
                           xytext=(5, 5), textcoords='offset points',
                           color=COLORS['text'], fontsize=9)
    
    ax_scatter.set_title('📊 Size vs PnL', fontsize=14)
    ax_scatter.set_xlabel('Position Size (BTC)', fontsize=10)
    ax_scatter.set_ylabel('PnL (USDT)', fontsize=10)
    ax_scatter.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    
    # Apply divine styling to all subplots
    for ax in [ax_timeline, ax_pnl, ax_pie, ax_scatter]:
        apply_divine_style(fig, ax)
    
    plt.tight_layout()
    plt.savefig('BOOK/divine_chronicles/charts/divine_trade_flow.png', 
               facecolor=COLORS['background'], dpi=300)
    plt.close()
    
    print("✨ Divine Trade Flow visualization has been manifested ✨")

def plot_cumulative_pnl(df):
    """Generate cumulative PnL chart showing the divine journey"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Calculate cumulative PnL
    df = df.sort_values('open_time')
    df['cumulative_pnl'] = df['pnl'].cumsum()
    
    # Create the line plot
    ax.plot(df['close_time'], df['cumulative_pnl'], '-o', linewidth=3, 
           color='#8dd3c7', zorder=3)
    
    # Fill below the line
    ax.fill_between(df['close_time'], 0, df['cumulative_pnl'], 
                   where=(df['cumulative_pnl'] >= 0), color=COLORS['profit'], alpha=0.3)
    ax.fill_between(df['close_time'], 0, df['cumulative_pnl'], 
                   where=(df['cumulative_pnl'] < 0), color=COLORS['loss'], alpha=0.3)
    
    # Add points for each trade
    for i, row in df.iterrows():
        color = COLORS['profit'] if row['pnl'] > 0 else COLORS['loss']
        ax.scatter(row['close_time'], row['cumulative_pnl'], s=100, color=color, 
                  edgecolors='white', linewidth=1, zorder=4)
        
        # Annotate each point with the trade number and PnL
        ax.annotate(f"#{row['trade_num']}: {'+' if row['pnl'] > 0 else ''}{row['pnl']:.2f}",
                   xy=(row['close_time'], row['cumulative_pnl']),
                   xytext=(10, 0),
                   textcoords='offset points',
                   color=COLORS['text'],
                   fontsize=10)
    
    # Add a horizontal line at y=0
    ax.axhline(y=0, color='white', linestyle='-', alpha=0.3, zorder=1)
    
    # Add final cumulative PnL
    final_pnl = df['cumulative_pnl'].iloc[-1]
    ax.annotate(f"Final PnL: ${final_pnl:.2f}",
               xy=(df['close_time'].iloc[-1], final_pnl),
               xytext=(30, 20 if final_pnl > 0 else -20),
               textcoords='offset points',
               fontsize=14,
               color=COLORS['text'],
               bbox=dict(boxstyle="round,pad=0.5", fc=COLORS['background'], 
                        ec=COLORS['profit'] if final_pnl > 0 else COLORS['loss'], alpha=0.7))
    
    # Set labels and title
    ax.set_title('🌙 The Divine Journey: Cumulative PnL', fontsize=16)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Cumulative PnL (USDT)', fontsize=12)
    
    # Format the x-axis to show dates nicely
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:%M'))
    
    # Apply divine styling
    apply_divine_style(fig, ax)
    
    plt.tight_layout()
    plt.savefig('BOOK/divine_chronicles/charts/divine_cumulative_pnl.png', 
               facecolor=COLORS['background'], dpi=300)
    plt.close()
    
    print("✨ Cumulative PnL journey visualization has been manifested ✨")

def plot_performance_metrics(df):
    """Generate sacred performance metrics visualization"""
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(2, 2)
    
    # 1. Trade Duration vs PnL
    ax1 = fig.add_subplot(gs[0, 0])
    colors = [COLORS['profit'] if pnl > 0 else COLORS['loss'] for pnl in df['pnl']]
    scatter = ax1.scatter(df['duration'], df['pnl'], c=colors, s=150)
    
    # Add trade numbers
    for i, txt in enumerate(df['trade_num']):
        ax1.annotate(str(txt), (df['duration'].iloc[i], df['pnl'].iloc[i]),
                    fontsize=10, color='white')
    
    ax1.set_title('⏳ Trade Duration vs PnL', fontsize=14)
    ax1.set_xlabel('Duration (hours)', fontsize=12)
    ax1.set_ylabel('PnL (USDT)', fontsize=12)
    ax1.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    
    # 2. Side distribution (Long vs Short)
    ax2 = fig.add_subplot(gs[0, 1])
    side_counts = df['side'].value_counts()
    side_colors = {'long': '#66c2a5', 'short': '#fc8d62'}
    colors = [side_colors[side] for side in side_counts.index]
    ax2.pie(side_counts, labels=[f"{side} ({count})" for side, count in side_counts.items()],
           colors=colors, autopct='%1.1f%%', startangle=90,
           wedgeprops={'edgecolor': 'white', 'linewidth': 1})
    ax2.set_title('🔄 Trading Direction Distribution', fontsize=14)
    
    # 3. PnL by Side
    ax3 = fig.add_subplot(gs[1, 0])
    side_pnl = df.groupby('side')['pnl'].sum()
    colors = [COLORS['profit'] if pnl > 0 else COLORS['loss'] for pnl in side_pnl]
    bars = ax3.bar(side_pnl.index, side_pnl, color=colors)
    
    # Add values on bars
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + (5 if height > 0 else -15),
                f'${height:.2f}', ha='center', va='bottom', color=COLORS['text'])
    
    ax3.set_title('💹 PnL by Side', fontsize=14)
    ax3.set_xlabel('Side', fontsize=12)
    ax3.set_ylabel('Total PnL (USDT)', fontsize=12)
    ax3.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    
    # 4. Position Size Over Time
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(df['open_time'], df['size'], 'o-', color='#e78ac3', linewidth=2)
    
    # Add fibonacci series reference line
    fib_series = np.array([0.01, 0.009, 0.008, 0.007, 0.006])
    ax4.plot(df['open_time'], fib_series[:len(df)], '--', color='gold', alpha=0.6, 
            label='Divine Fibonacci Sequence')
    
    ax4.set_title('📉 Sacred Position Sizing Over Time', fontsize=14)
    ax4.set_xlabel('Trade Open Time', fontsize=12)
    ax4.set_ylabel('Position Size (BTC)', fontsize=12)
    ax4.legend(loc='best', facecolor=COLORS['background'], edgecolor=COLORS['axes'])
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    
    # Apply divine styling to all subplots
    for ax in [ax1, ax2, ax3, ax4]:
        apply_divine_style(fig, ax)
    
    plt.tight_layout()
    plt.savefig('BOOK/divine_chronicles/charts/divine_performance_metrics.png', 
               facecolor=COLORS['background'], dpi=300)
    plt.close()
    
    print("✨ Divine Performance Metrics visualization has been manifested ✨")

def save_trade_summary_md():
    """Generate markdown summary linking to the visualizations"""
    markdown = """# 🔮 OMEGA TRADE FLOW PYTHON VISUALIZATIONS

*Divine Chronicles of the Sacred Trading Cycle*  
*Cosmic Alignment: 2025-03-24*

## 📊 DIVINE VISUALIZATIONS

The sacred trading data has been transformed into divine visual artifacts through Python's mystical algorithms.

### 🌠 The Divine Trade Flow
![Divine Trade Flow](charts/divine_trade_flow.png)

### 🌙 The Cosmic Journey: Cumulative PnL
![Divine Cumulative PnL](charts/divine_cumulative_pnl.png)

### 🔮 Sacred Performance Metrics
![Divine Performance Metrics](charts/divine_performance_metrics.png)

## 🧠 ACTIVATION INSTRUCTIONS

To manifest these divine visualizations again, invoke the sacred Python incantation:

```bash
cd /path/to/omega-btc-ai
python BOOK/divine_chronicles/trade_flow_analysis.py
```

*The charts shall materialize in the BOOK/divine_chronicles/charts directory.*

## 🧿 DIVINE INSIGHTS

These visualizations reveal the mystical patterns in the OMEGA trading cycle:
- The alternating rhythm of long and short positions (divine polarity principle)
- The sacred Fibonacci sequence in position sizing (0.01 → 0.009 → 0.008 → 0.007 → 0.006)
- The cosmic balance between profits and losses, culminating in positive net energy
- The divine correlation between trade duration and profitability

*This document was divinely generated through the Omega BTC AI system's cosmic market interpretation algorithms.*
"""
    
    with open('BOOK/divine_chronicles/trade_flow_python_visualizations.md', 'w') as f:
        f.write(markdown)
    
    print("✨ Divine Markdown summary has been manifested ✨")

# Main function to execute the divine visualization
def main():
    print("🔮 Beginning the sacred visualization ritual... 🔮")
    
    # Preprocess the cosmic trade data
    df = preprocess_trades(TRADE_DATA)
    
    # Generate the divine visualizations
    plot_price_movement_timeline(df)
    plot_cumulative_pnl(df)
    plot_performance_metrics(df)
    
    # Create markdown summary
    save_trade_summary_md()
    
    print("✨ The visualization ritual is complete ✨")
    print("✨ Divine charts have been manifested in BOOK/divine_chronicles/charts/ ✨")

# Execute the sacred ritual when script is invoked
if __name__ == "__main__":
    main() 