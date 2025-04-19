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
OMEGA BTC AI - Trading History Analysis
=======================================

Emotional Trading Journey Analysis for BitGet trading history
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import os

# Set up styling for plots
plt.style.use('dark_background')
COLORS = {
    'profit': '#00b894',
    'loss': '#d63031',
    'neutral': '#0984e3',
    'text': '#dfe6e9',
    'grid': '#2d3436',
    'background': '#1e272e'
}

def load_trading_data(csv_file):
    """Load trading data from CSV file"""
    df = pd.read_csv(csv_file)
    
    # Convert date strings to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Convert numeric columns to float
    numeric_cols = ['Transaction amount', 'Average Price', 'Realized P/L', 'NetProfits', 'Fee']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Sort by date
    df = df.sort_values('Date')
    
    return df

def analyze_trading_journey(df):
    """Analyze trading journey and derive key metrics"""
    # Calculate daily PnL
    df['day'] = df['Date'].dt.date
    daily_pnl = df.groupby('day')['Realized P/L'].sum().reset_index()
    daily_pnl['cumulative_pnl'] = daily_pnl['Realized P/L'].cumsum()
    
    # Calculate win/loss stats
    win_trades = df[df['Realized P/L'] > 0]
    loss_trades = df[df['Realized P/L'] < 0]
    
    win_rate = len(win_trades) / len(df) if len(df) > 0 else 0
    avg_win = win_trades['Realized P/L'].mean() if len(win_trades) > 0 else 0
    avg_loss = loss_trades['Realized P/L'].mean() if len(loss_trades) > 0 else 0
    
    # Calculate volume stats by day
    daily_volume = df.groupby('day')['Transaction amount'].sum().reset_index()
    
    # Average position size over time
    df['week'] = df['Date'].dt.isocalendar().week
    weekly_size = df.groupby('week')['Transaction amount'].mean().reset_index()
    
    # Calculate long vs short stats
    direction_counts = df['Direction'].value_counts()
    
    return {
        'daily_pnl': daily_pnl,
        'daily_volume': daily_volume,
        'weekly_size': weekly_size,
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'direction_counts': direction_counts,
        'total_trades': len(df),
        'total_pnl': df['Realized P/L'].sum(),
        'total_fees': df['Fee'].sum(),
        'max_win': df['Realized P/L'].max(),
        'max_loss': df['Realized P/L'].min(),
        'avg_trade_pnl': df['Realized P/L'].mean(),
    }

def create_emotional_journey_chart(metrics, output_dir='charts'):
    """Create emotional journey chart based on daily PnL"""
    os.makedirs(output_dir, exist_ok=True)
    
    daily_pnl = metrics['daily_pnl']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1]})
    
    # Cumulative PnL chart (emotional journey)
    ax1.plot(daily_pnl['day'], daily_pnl['cumulative_pnl'], 
             color=COLORS['neutral'], linewidth=3, marker='o')
    
    # Fill area
    ax1.fill_between(daily_pnl['day'], 0, daily_pnl['cumulative_pnl'],
                    where=(daily_pnl['cumulative_pnl'] >= 0),
                    color=COLORS['profit'], alpha=0.3)
    ax1.fill_between(daily_pnl['day'], 0, daily_pnl['cumulative_pnl'],
                    where=(daily_pnl['cumulative_pnl'] < 0),
                    color=COLORS['loss'], alpha=0.3)
    
    # Annotate key points in the journey
    max_pnl_idx = daily_pnl['cumulative_pnl'].idxmax()
    min_pnl_idx = daily_pnl['cumulative_pnl'].idxmin()
    
    ax1.annotate(f"Peak: ${daily_pnl['cumulative_pnl'].max():.2f}",
                xy=(daily_pnl['day'].iloc[max_pnl_idx], daily_pnl['cumulative_pnl'].max()),
                xytext=(0, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'),
                color=COLORS['text'])
    
    ax1.annotate(f"Bottom: ${daily_pnl['cumulative_pnl'].min():.2f}",
                xy=(daily_pnl['day'].iloc[min_pnl_idx], daily_pnl['cumulative_pnl'].min()),
                xytext=(0, -30), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'),
                color=COLORS['text'])
    
    # Style cumulative chart
    ax1.set_title('Your Emotional Trading Journey', fontsize=20, color=COLORS['text'])
    ax1.set_ylabel('Cumulative Profit/Loss (USDT)', fontsize=14, color=COLORS['text'])
    ax1.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    ax1.grid(color=COLORS['grid'], linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Daily PnL chart
    bars = ax2.bar(daily_pnl['day'], daily_pnl['Realized P/L'], 
                  color=[COLORS['profit'] if x >= 0 else COLORS['loss'] for x in daily_pnl['Realized P/L']])
    
    # Style daily chart
    ax2.set_title('Daily P/L', fontsize=16, color=COLORS['text'])
    ax2.set_ylabel('Daily P/L (USDT)', fontsize=14, color=COLORS['text'])
    ax2.set_xlabel('Date', fontsize=14, color=COLORS['text'])
    ax2.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    ax2.grid(color=COLORS['grid'], linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Format dates
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        ax.tick_params(colors=COLORS['text'])
    
    # Add summary stats in text box
    textstr = '\n'.join((
        f"Total P/L: ${metrics['total_pnl']:.2f}",
        f"Win Rate: {metrics['win_rate']*100:.1f}%",
        f"Avg Win: ${metrics['avg_win']:.2f}",
        f"Avg Loss: ${metrics['avg_loss']:.2f}",
        f"Total Trades: {metrics['total_trades']}",
        f"Total Fees: ${abs(metrics['total_fees']):.2f}"
    ))
    
    props = dict(boxstyle='round', facecolor='black', alpha=0.5)
    ax1.text(0.02, 0.05, textstr, transform=ax1.transAxes, fontsize=12,
            verticalalignment='bottom', bbox=props, color=COLORS['text'])
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/emotional_journey.png", dpi=300, 
               facecolor=COLORS['background'])
    plt.close()

def create_trading_insights_chart(metrics, output_dir='charts'):
    """Create additional insights chart with multiple visualizations"""
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(16, 14))
    fig.patch.set_facecolor(COLORS['background'])
    
    gs = fig.add_gridspec(3, 2)
    
    # 1. Daily Trading Volume
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.bar(metrics['daily_volume']['day'], metrics['daily_volume']['Transaction amount'],
           color=COLORS['neutral'], alpha=0.7)
    ax1.set_title('Daily Trading Volume', fontsize=16, color=COLORS['text'])
    ax1.set_ylabel('Volume (BTC)', fontsize=12, color=COLORS['text'])
    ax1.tick_params(colors=COLORS['text'])
    
    # 2. Win/Loss Distribution
    ax2 = fig.add_subplot(gs[0, 1])
    win_loss_data = [
        len([x for x in metrics['daily_pnl']['Realized P/L'] if x > 0]),
        len([x for x in metrics['daily_pnl']['Realized P/L'] if x < 0]),
        len([x for x in metrics['daily_pnl']['Realized P/L'] if x == 0])
    ]
    ax2.pie(win_loss_data, 
           labels=['Winning Days', 'Losing Days', 'Breakeven Days'],
           colors=[COLORS['profit'], COLORS['loss'], COLORS['neutral']],
           autopct='%1.1f%%', 
           startangle=90,
           wedgeprops={'edgecolor': 'white', 'linewidth': 1})
    ax2.set_title('Win/Loss Distribution', fontsize=16, color=COLORS['text'])
    
    # 3. Long vs Short Trades
    ax3 = fig.add_subplot(gs[1, 0])
    if not metrics['direction_counts'].empty:
        direction_data = metrics['direction_counts']
        ax3.bar(direction_data.index, direction_data.values, color=COLORS['neutral'])
        ax3.set_title('Long vs Short Trades', fontsize=16, color=COLORS['text'])
        ax3.set_ylabel('Number of Trades', fontsize=12, color=COLORS['text'])
        ax3.tick_params(colors=COLORS['text'])
    
    # 4. PnL Distribution
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.hist(metrics['daily_pnl']['Realized P/L'], bins=20, 
            color=COLORS['neutral'], edgecolor='white', alpha=0.7)
    ax4.axvline(x=0, color='white', linestyle='--', alpha=0.5)
    ax4.set_title('P/L Distribution', fontsize=16, color=COLORS['text'])
    ax4.set_xlabel('Daily P/L (USDT)', fontsize=12, color=COLORS['text'])
    ax4.set_ylabel('Frequency', fontsize=12, color=COLORS['text'])
    ax4.tick_params(colors=COLORS['text'])
    
    # 5. Weekly average position size
    ax5 = fig.add_subplot(gs[2, :])
    ax5.plot(metrics['weekly_size']['week'], metrics['weekly_size']['Transaction amount'],
            marker='o', linewidth=2, color=COLORS['neutral'])
    ax5.set_title('Average Position Size by Week', fontsize=16, color=COLORS['text'])
    ax5.set_xlabel('Week Number', fontsize=12, color=COLORS['text'])
    ax5.set_ylabel('Average Position Size (BTC)', fontsize=12, color=COLORS['text'])
    ax5.tick_params(colors=COLORS['text'])
    ax5.grid(color=COLORS['grid'], linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Add emotional insights text box
    if metrics['total_pnl'] > 0:
        emotion = "Your trading shows resilience and discipline."
        key_insight = f"Strongest performance: ${metrics['max_win']:.2f} profit"
    else:
        emotion = "Your trading shows determination through challenges."
        key_insight = f"Most challenging trade: ${metrics['max_loss']:.2f} loss"
        
    win_loss_ratio = abs(metrics['avg_win'] / metrics['avg_loss']) if metrics['avg_loss'] != 0 else 0
    
    textstr = '\n'.join((
        "EMOTIONAL TRADING INSIGHTS",
        f"➤ {emotion}",
        f"➤ Win/Loss Ratio: {win_loss_ratio:.2f}",
        f"➤ {key_insight}",
        f"➤ Your trading fees total ${abs(metrics['total_fees']):.2f}",
        f"➤ Overall P/L stands at ${metrics['total_pnl']:.2f}"
    ))
    
    props = dict(boxstyle='round', facecolor='black', alpha=0.5)
    ax5.text(0.02, 0.95, textstr, transform=ax5.transAxes, fontsize=12,
            verticalalignment='top', bbox=props, color=COLORS['text'])
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/trading_insights.png", dpi=300, 
               facecolor=COLORS['background'])
    plt.close()

def generate_trading_journey_report(metrics, output_dir='charts'):
    """Generate a markdown report with trading journey insights"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate additional metrics
    win_loss_ratio = abs(metrics['avg_win'] / metrics['avg_loss']) if metrics['avg_loss'] != 0 else 0
    profit_factor = abs(sum([p for p in metrics['daily_pnl']['Realized P/L'] if p > 0]) / 
                      sum([abs(p) for p in metrics['daily_pnl']['Realized P/L'] if p < 0])) if sum([abs(p) for p in metrics['daily_pnl']['Realized P/L'] if p < 0]) != 0 else 0
    
    # Generate emotional insight based on metrics
    if metrics['win_rate'] > 0.5:
        emotional_insight = "Your trading shows a disciplined approach with more winning trades than losing ones."
    elif metrics['total_pnl'] > 0 and metrics['win_rate'] <= 0.5:
        emotional_insight = "Despite having fewer winning trades, your profitable trades are significant enough to outweigh the losses - a sign of good risk management."
    elif metrics['total_pnl'] < 0 and metrics['avg_loss'] > abs(metrics['avg_win']):
        emotional_insight = "Your trading shows a pattern of holding onto losing positions too long while cutting winners short. This emotional pattern is common and can be addressed with more disciplined exit strategies."
    else:
        emotional_insight = "Your trading journey shows determination to navigate through market volatility."
    
    # Format report
    report = f"""# 🌊 YOUR EMOTIONAL TRADING JOURNEY

## 🧠 TRADING PSYCHOLOGY ANALYSIS

*"The market is a device for transferring money from the impatient to the patient." - Warren Buffett*

### 📊 KEY METRICS

| Metric | Value |
|--------|-------|
| Total Trades | {metrics['total_trades']} |
| Win Rate | {metrics['win_rate']*100:.1f}% |
| Total P/L | ${metrics['total_pnl']:.2f} |
| Average Win | ${metrics['avg_win']:.2f} |
| Average Loss | ${metrics['avg_loss']:.2f} |
| Win/Loss Ratio | {win_loss_ratio:.2f} |
| Profit Factor | {profit_factor:.2f} |
| Maximum Win | ${metrics['max_win']:.2f} |
| Maximum Loss | ${metrics['max_loss']:.2f} |
| Total Fees Paid | ${abs(metrics['total_fees']):.2f} |

### 💫 EMOTIONAL INSIGHTS

{emotional_insight}

## 🧿 YOUR TRADING JOURNEY VISUALIZED

### The Emotional Rollercoaster
![Emotional Journey](emotional_journey.png)

### Trading Patterns & Insights
![Trading Insights](trading_insights.png)

## 🧘‍♂️ RECOMMENDATIONS FOR EMOTIONAL RESILIENCE

1. **Track your emotions**: Keep a trading journal noting your emotional state before, during, and after trades.

2. **Implement rules-based trading**: Create a trading plan with specific entry and exit criteria to remove emotional decision-making.

3. **Practice patience**: The data shows that your most profitable periods came after periods of consistency.

4. **Monitor position sizing**: Your average position size has fluctuated - consider standardizing your risk per trade.

5. **Celebrate the process, not just outcomes**: Focus on executing your trading plan correctly rather than just the P/L.

*"The key to trading success is emotional discipline. Making money has nothing to do with intelligence - trust me on that." - Victor Sperandeo*

"""
    
    # Write report to file
    with open(f"{output_dir}/trading_journey_report.md", 'w') as f:
        f.write(report)

def main():
    """Main entry point for analysis"""
    # Load trading data
    print("🧠 Loading trading data...")
    df = load_trading_data('tmp_data/20250324064858.csv')
    
    # Analyze trading data
    print("📊 Analyzing your emotional trading journey...")
    metrics = analyze_trading_journey(df)
    
    # Create output directory
    os.makedirs('charts', exist_ok=True)
    
    # Generate visualizations
    print("🎨 Creating visualizations of your trading journey...")
    create_emotional_journey_chart(metrics)
    create_trading_insights_chart(metrics)
    
    # Generate report
    print("📝 Generating emotional trading journey report...")
    generate_trading_journey_report(metrics)
    
    print("✨ Analysis complete! Check the 'charts' directory for your emotional trading journey report and visualizations.")

if __name__ == "__main__":
    main() 