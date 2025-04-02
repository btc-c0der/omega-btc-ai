#!/usr/bin/env python3
"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

OMEGA MAX DUMP SIMULATION: Quantum Price Analysis
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter

# Create output directory if it doesn't exist
os.makedirs('data/omega_max_dump', exist_ok=True)

def simulate_omega_max_dump(days=180, volatility=0.03, dump_factor=0.5, recovery_factor=0.3, end_date=None, dump_time=None):
    """
    Simulate OMEGA MAX DUMP price action with a significant drop and recovery pattern.
    
    Args:
        days: Number of days to simulate
        volatility: Daily price volatility
        dump_factor: How severe the dump is (0-1)
        recovery_factor: How strong the recovery is (0-1)
        end_date: Optional specific end date (datetime object)
        dump_time: Optional specific time for the dump to occur (timedelta)
    
    Returns:
        DataFrame with price data
    """
    # Start with a price of $84,428 (cosmic number)
    start_price = 84428
    
    # Create date range
    if end_date is None:
        # Default to April 2, 2025 at 00:00:00
        end_date = datetime(2025, 4, 2)
    start_date = end_date - timedelta(days=days)
    
    # Create hourly date range for more granular simulation
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Generate random price movements with drift
    np.random.seed(42)  # Set seed for reproducibility
    returns = np.random.normal(0.0005, volatility/24, size=len(date_range))  # Scale volatility for hourly data
    
    # Determine dump start time (if specified use dump_time, otherwise 70% through the time period)
    if dump_time is None:
        dump_start_idx = int(len(date_range) * 0.7)
    else:
        # Find the index that corresponds to dump_time after simulation start
        hours_from_start = int(dump_time.total_seconds() / 3600)
        dump_start_idx = min(hours_from_start, len(date_range) - 50)  # Ensure some time left for recovery
    
    # 4:20 special marker - ensure dump happens at 4:20
    # Find the nearest index that has hour=4 and minute=20
    target_hour = 4
    target_minute = 20
    
    # Find all 4:20 timestamps in the simulation
    dump_candidates = []
    for i, timestamp in enumerate(date_range):
        if timestamp.hour == target_hour and timestamp.minute == target_minute:
            dump_candidates.append(i)
    
    # Use the first 4:20 occurrence if available
    if dump_candidates:
        dump_start_idx = dump_candidates[0]
    
    dump_duration = int(len(date_range) * 0.01)  # 1% of total hours - make it sudden
    recovery_start_idx = dump_start_idx + dump_duration
    
    # Apply dump pattern - make it more severe for 4:20
    for i in range(dump_start_idx, recovery_start_idx):
        # More severe sudden drop at 4:20
        if i == dump_start_idx:
            returns[i] = -0.3 * dump_factor  # Major sudden drop
        else:
            # Tapering drop for remaining dump period
            returns[i] = -0.07 * dump_factor * (1 - (i - dump_start_idx) / dump_duration)
    
    # Apply recovery pattern
    recovery_duration = int(len(date_range) * 0.1)  # 10% of hours
    for i in range(recovery_start_idx, min(recovery_start_idx + recovery_duration, len(returns))):
        # Tapering recovery pattern
        phase = (i - recovery_start_idx) / recovery_duration
        returns[i] = 0.05 * recovery_factor * (1 - phase)
    
    # Calculate price series
    price_series = start_price * (1 + returns).cumprod()
    
    # Add some quantum noise to the price
    quantum_noise = np.random.normal(0, 0.005, size=len(price_series))
    price_series = price_series * (1 + quantum_noise)
    
    # Create DataFrame with date and price
    df = pd.DataFrame({'date': date_range, 'price': price_series})
    
    # Add volume data (higher during dump and recovery)
    base_volume = 10000
    volumes = np.random.normal(base_volume, base_volume * 0.2, size=len(date_range))
    
    # Increase volume during dump (panic selling)
    for i in range(dump_start_idx, recovery_start_idx):
        # Extremely high volume at 4:20
        if i == dump_start_idx:
            volumes[i] = volumes[i] * (8 + random.random() * 4)  # 8-12x volume
        else:
            volumes[i] = volumes[i] * (3 + random.random() * 2)  # 3-5x volume
    
    # Increase volume during early recovery (accumulation)
    for i in range(recovery_start_idx, min(recovery_start_idx + recovery_duration // 2, len(volumes))):
        volumes[i] = volumes[i] * (2 + random.random() * 1.5)  # 2-3.5x volume
    
    df['volume'] = volumes
    
    # Calculate moving averages - use hourly intervals but equivalent to daily MA
    df['ma_21'] = df['price'].rolling(window=21*24).mean()
    df['ma_50'] = df['price'].rolling(window=50*24).mean()
    df['ma_200'] = df['price'].rolling(window=200*24).mean()
    
    # Add trading signals based on quantum blockchain patterns
    df['quantum_signal'] = 0  # Neutral
    
    # Generate signals based on price patterns and moving averages
    for i in range(50*24, len(df)):  # Start after we have some moving average data
        # Death cross (21 MA crosses below 50 MA)
        if df['ma_21'].iloc[i-1] >= df['ma_50'].iloc[i-1] and df['ma_21'].iloc[i] < df['ma_50'].iloc[i]:
            df.loc[df.index[i], 'quantum_signal'] = -2  # Strong sell
        
        # Golden cross (21 MA crosses above 50 MA)
        elif df['ma_21'].iloc[i-1] <= df['ma_50'].iloc[i-1] and df['ma_21'].iloc[i] > df['ma_50'].iloc[i]:
            df.loc[df.index[i], 'quantum_signal'] = 2  # Strong buy
        
        # Price below both MAs and increasing
        elif df['price'].iloc[i] < df['ma_50'].iloc[i] and df['price'].iloc[i-5:i].is_monotonic_increasing:
            df.loc[df.index[i], 'quantum_signal'] = 1  # Buy
        
        # Price above both MAs and decreasing
        elif df['price'].iloc[i] > df['ma_50'].iloc[i] and df['price'].iloc[i-5:i].is_monotonic_decreasing:
            df.loc[df.index[i], 'quantum_signal'] = -1  # Sell
    
    # Mark the OMEGA MAX DUMP event - specifically at 4:20
    df.loc[df.index[dump_start_idx], 'event'] = 'OMEGA MAX DUMP DETECTED AT 4:20'
    
    # Just before recovery
    recovery_idx = recovery_start_idx - 1
    df.loc[df.index[recovery_idx], 'event'] = 'QUANTUM ACCUMULATION'
    
    # Mid recovery
    mid_recovery_idx = recovery_start_idx + recovery_duration // 2
    if mid_recovery_idx < len(df):
        df.loc[df.index[mid_recovery_idx], 'event'] = 'MATRIX REVERSAL PATTERN'
    
    # Revert to daily data for easier visualization (aggregate by day)
    df_daily = df.resample('D', on='date').agg({
        'price': 'last', 
        'volume': 'sum',
        'ma_21': 'last',
        'ma_50': 'last',
        'ma_200': 'last'
    }).reset_index()
    
    # Keep track of events in the daily data
    events_df = df[df['event'].notna()]
    for _, event_row in events_df.iterrows():
        # Find closest day in daily DataFrame
        event_date = event_row['date'].date()
        matching_rows = df_daily[df_daily['date'].dt.date == event_date]
        if not matching_rows.empty:
            idx = matching_rows.index[0]
            df_daily.loc[idx, 'event'] = event_row['event']
    
    # Fill missing signal values
    df_daily['quantum_signal'] = 0
    for _, event_row in df[df['quantum_signal'] != 0].iterrows():
        event_date = event_row['date'].date()
        matching_rows = df_daily[df_daily['date'].dt.date == event_date]
        if not matching_rows.empty:
            idx = matching_rows.index[0]
            current_signal = df_daily.loc[idx, 'quantum_signal']
            event_signal = event_row['quantum_signal']
            # Use manual comparison instead of abs()
            if (event_signal > 0 and event_signal > current_signal) or (event_signal < 0 and event_signal < current_signal):
                df_daily.loc[idx, 'quantum_signal'] = event_signal
    
    # Add special 4:20 info to metadata
    dump_timestamp = df.loc[dump_start_idx, 'date']
    # Ensure dump_timestamp is a datetime object
    if isinstance(dump_timestamp, pd.Timestamp):
        dump_timestamp_str = dump_timestamp.strftime('%Y-%m-%d %H:%M')
        is_420_dump = dump_timestamp.hour == 4 and dump_timestamp.minute == 20
    else:
        # Handle case where it might be another type
        dump_timestamp_str = str(dump_timestamp)
        is_420_dump = False
    
    df_daily.attrs['dump_timestamp'] = dump_timestamp_str
    df_daily.attrs['is_420_dump'] = is_420_dump
    
    return df_daily

def money_formatter(x, pos):
    """Format y axis labels as money values."""
    if x >= 1000000:
        return f'${x/1000000:.1f}M'
    elif x >= 1000:
        return f'${x/1000:.0f}K'
    else:
        return f'${x:.0f}'

def plot_omega_max_dump(df):
    """
    Create a visualization of the OMEGA MAX DUMP simulation.
    
    Args:
        df: DataFrame with price and volume data
    
    Returns:
        Path to saved plot image
    """
    # Extract any metadata
    is_420_dump = df.attrs.get('is_420_dump', False)
    dump_timestamp = df.attrs.get('dump_timestamp', None)
    
    # Set up plot style
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
    fig.patch.set_facecolor('#0f0f23')
    
    # Main title - add 4:20 reference if applicable
    title = '🔱 OMEGA MAX DUMP SIMULATION 🔱'
    if is_420_dump:
        title += ' - 4:20 CRASH EDITION'
    fig.suptitle(title, fontsize=22, color='gold', y=0.98, fontweight='bold')
    
    # Format date axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    
    # Plot price with golden color
    ax1.plot(df['date'], df['price'], color='#ffd700', linewidth=2, label='BTC Price')
    
    # Add moving averages
    ax1.plot(df['date'], df['ma_21'], color='#ff3333', linewidth=1, alpha=0.8, label='21-Day MA')
    ax1.plot(df['date'], df['ma_50'], color='#33ccff', linewidth=1, alpha=0.8, label='50-Day MA')
    ax1.plot(df['date'], df['ma_200'], color='#00ff00', linewidth=1, alpha=0.8, label='200-Day MA')
    
    # Format y-axis as money
    ax1.yaxis.set_major_formatter(FuncFormatter(money_formatter))
    
    # Highlight dump and recovery periods
    dump_start_idx = df[df['event'].str.contains('OMEGA MAX DUMP', na=False)].index[0] if not df[df['event'].str.contains('OMEGA MAX DUMP', na=False)].empty else None
    
    if dump_start_idx is not None:
        dump_start_date = df.loc[dump_start_idx, 'date']
        
        # Find recovery start as the lowest price after dump
        post_dump_df = df.loc[dump_start_idx:]
        recovery_start_idx = post_dump_df['price'].idxmin()
        recovery_start_date = df.loc[recovery_start_idx, 'date']
        
        # Find end date
        end_date = df['date'].iloc[-1]
        
        # Highlight dump period
        dump_color = '#ff3333'
        recovery_color = '#33cc33'
        ax1.axvspan(dump_start_date, recovery_start_date, alpha=0.2, color=dump_color)
        ax1.axvspan(recovery_start_date, end_date, alpha=0.2, color=recovery_color)
        
        # Add event markers
        events = df[df['event'].notna()]
        for idx, row in events.iterrows():
            marker_y = row['price']
            event_text = row['event']
            
            if 'OMEGA MAX DUMP' in event_text:
                marker_color = '#ff0000'  # Bright red for 4:20 crash
                y_offset = marker_y * 0.1
                arrow = dict(arrowstyle='->', color=marker_color)
                
                # Add special 4:20 formatting if applicable
                if is_420_dump:
                    event_text = event_text + f"\n{dump_timestamp}"
                    arrow['width'] = 2
                    
                ax1.annotate(event_text, xy=(row['date'], marker_y), 
                            xytext=(row['date'] - timedelta(days=15), marker_y + y_offset),
                            color=marker_color, fontweight='bold', fontsize=10,
                            arrowprops=arrow)
            
            elif event_text == 'QUANTUM ACCUMULATION':
                marker_color = 'white'
                y_offset = marker_y * 0.05
                arrow = dict(arrowstyle='->', color=marker_color)
                ax1.annotate(event_text, xy=(row['date'], marker_y), 
                            xytext=(row['date'] - timedelta(days=5), marker_y - y_offset),
                            color=marker_color, fontweight='bold', fontsize=10,
                            arrowprops=arrow)
            
            elif event_text == 'MATRIX REVERSAL PATTERN':
                marker_color = recovery_color
                y_offset = marker_y * 0.1
                arrow = dict(arrowstyle='->', color=marker_color)
                ax1.annotate(event_text, xy=(row['date'], marker_y), 
                            xytext=(row['date'] - timedelta(days=5), marker_y + y_offset),
                            color=marker_color, fontweight='bold', fontsize=10,
                            arrowprops=arrow)
    
    # Plot quantum signals
    for i, row in df.iterrows():
        if row['quantum_signal'] == 2:  # Strong buy
            ax1.scatter(row['date'], row['price'] * 0.98, marker='^', color='lime', s=100, alpha=0.8)
        elif row['quantum_signal'] == -2:  # Strong sell
            ax1.scatter(row['date'], row['price'] * 1.02, marker='v', color='red', s=100, alpha=0.8)
        elif row['quantum_signal'] == 1:  # Buy
            ax1.scatter(row['date'], row['price'] * 0.99, marker='^', color='lime', s=50, alpha=0.6)
        elif row['quantum_signal'] == -1:  # Sell
            ax1.scatter(row['date'], row['price'] * 1.01, marker='v', color='red', s=50, alpha=0.6)
    
    # Plot volume data in the second subplot
    volume_colors = []
    prev_price = df['price'].iloc[0]
    for current_price in df['price']:
        if current_price >= prev_price:
            volume_colors.append('#33cc33')  # Green for price increase
        else:
            volume_colors.append('#ff3333')  # Red for price decrease
        prev_price = current_price
    
    ax2.bar(df['date'], df['volume'], color=volume_colors, alpha=0.7, width=1)
    ax2.set_ylabel('Volume', color='white')
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x < 1000000 else f'{x/1000000:.1f}M'))
    
    # Set background and grid
    for ax in [ax1, ax2]:
        ax.set_facecolor('#0f0f23')
        ax.grid(alpha=0.2, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#333333')
        ax.spines['left'].set_color('#333333')
        ax.tick_params(colors='white')
    
    # Set labels
    ax1.set_ylabel('BTC Price (USD)', color='white')
    title_text = 'Bitcoin Price during OMEGA MAX DUMP Event'
    if is_420_dump:
        title_text += ' - 4:20 Crash Edition'
    ax1.set_title(title_text, color='white', fontsize=14)
    ax1.legend(loc='upper left', facecolor='#0f0f23', framealpha=0.7)
    
    # Add explanatory text
    if dump_start_idx is not None:
        dump_pct = ((df['price'].min() - df['price'].iloc[dump_start_idx]) / df['price'].iloc[dump_start_idx]) * 100
        recovery_pct = ((df['price'].iloc[-1] - df['price'].min()) / df['price'].min()) * 100
        
        explanation = (
            f"OMEGA MAX DUMP Analysis:\n"
            f"• Total Dump: {dump_pct:.1f}%\n"
            f"• Recovery: {recovery_pct:.1f}%\n"
        )
        
        if is_420_dump:
            explanation += f"• Crash Time: {dump_timestamp}\n"
        
        explanation += "• Quantum Matrix Pattern: ACTIVE"
        
        # Place text box in bottom right
        props = dict(boxstyle='round,pad=0.5', facecolor='#333355', alpha=0.8)
        ax1.text(0.98, 0.02, explanation, transform=ax1.transAxes, fontsize=10,
                verticalalignment='bottom', horizontalalignment='right', color='white',
                bbox=props)
    
    # Rotate date labels
    fig.autofmt_xdate()
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    
    # Save the figure
    output_path = 'data/omega_max_dump/omega_max_dump_simulation_chart.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    return output_path

def display_image(image_path):
    """
    Display the saved image.
    
    Args:
        image_path: Path to the image file
    """
    img = plt.imread(image_path)
    plt.figure(figsize=(16, 10))
    plt.imshow(img)
    plt.axis('off')  # Hide axes
    plt.title("🔱 OMEGA MAX DUMP SIMULATION 🔱", fontsize=16, color='gold')
    plt.show()

def main():
    """
    Main function to run the OMEGA MAX DUMP simulation.
    """
    print("🔱 OMEGA MAX DUMP SIMULATION 🔱")
    print("Generating price data and visualization...")
    
    # Set end date to April 2, 2025
    end_date = datetime(2025, 4, 2)
    
    # Set the dump to occur at 4:20
    dump_time = timedelta(hours=4, minutes=20)
    
    # Simulate price data with specific crash time
    dump_data = simulate_omega_max_dump(
        days=180, 
        volatility=0.03, 
        dump_factor=0.8,  # More severe dump 
        recovery_factor=0.4,
        end_date=end_date,
        dump_time=dump_time
    )
    
    # Create visualization
    output_path = plot_omega_max_dump(dump_data)
    
    print(f"Simulation complete!")
    print(f"Visualization saved to: {output_path}")
    
    # Display 4:20 dump info if available
    if dump_data.attrs.get('is_420_dump', False):
        print(f"\n*** 4:20 CRASH DETECTED at {dump_data.attrs.get('dump_timestamp')} ***")
    
    print("\nTo view the visualization, run:")
    print("python -c \"import matplotlib.pyplot as plt; import matplotlib.image as mpimg; img = mpimg.imread('data/omega_max_dump/omega_max_dump_simulation_chart.png'); plt.figure(figsize=(16, 10)); plt.imshow(img); plt.axis('off'); plt.title('🔱 OMEGA MAX DUMP SIMULATION 🔱', fontsize=16, color='gold'); plt.show()\"")
    
    # Write simulation data to CSV
    dump_data.to_csv('data/omega_max_dump/omega_max_dump_data.csv', index=False)
    
    return output_path

if __name__ == "__main__":
    main() 