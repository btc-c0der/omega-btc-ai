import json
import graphviz
from collections import defaultdict
import os
from datetime import datetime, timedelta
from omega_ai.utils.redis_manager import RedisManager
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from matplotlib.dates import date2num, DateFormatter
import matplotlib.dates as mdates
import redis
import pandas as pd
import mplfinance as mpf
from matplotlib.gridspec import GridSpec

# Define output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'omega_king_runs')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class FeeTrackingSystem:
    """Track position fees for 10XFE3 strategy"""
    def __init__(self):
        self.initial_fee = 0.0
        self.current_fee = 0.0
        self.fee_history = []
        self.fee_multiplier = 10.0
        self.position_size = 1.0  # Default position size
        self.maker_rate = 0.0002  # 0.02% maker fee
        self.taker_rate = 0.0004  # 0.04% taker fee
        self.funding_rate = 0.0001  # 0.01% funding rate
        self.slippage_rate = 0.0001  # 0.01% slippage
        
    def calculate_position_fee(self, holding_time):
        """Calculate current position fee including all components"""
        maker_fee = self.position_size * self.maker_rate * holding_time
        taker_fee = self.position_size * self.taker_rate * 2  # Entry + Exit
        funding_fee = self.position_size * self.funding_rate * holding_time
        slippage_cost = self.position_size * self.slippage_rate
        
        total_fee = maker_fee + taker_fee + funding_fee + slippage_cost
        return total_fee
    
    def check_fee_threshold(self, holding_time):
        """Check if current fee exceeds threshold"""
        self.current_fee = self.calculate_position_fee(holding_time)
        return self.current_fee >= (self.initial_fee * self.fee_multiplier)

def load_redis_data(hours=10):
    """Load the last N hours of BTC data from Redis"""
    redis_manager = RedisManager()
    
    # Get price movement history
    history = redis_manager.lrange("btc_movement_history", 0, -1)
    if not history:
        raise ValueError("No BTC movement history found in Redis")
    
    # Get current time and calculate cutoff
    now = datetime.now()
    cutoff = now - timedelta(hours=hours)
    
    # Process price data
    price_data = []
    for entry in history:
        try:
            if "," in entry:
                price_str, volume_str = entry.split(",")
                price = float(price_str)
                volume = float(volume_str)
                
                # Validate price and volume
                if price <= 0 or volume < 0:
                    print(f"⚠️ Invalid data point: Price={price}, Volume={volume}")
                    continue
                    
                # Check for extreme price movements (more than 10% from previous)
                if price_data and abs(price - price_data[-1]['price']) / price_data[-1]['price'] > 0.10:
                    print(f"⚠️ Large price movement detected: {price_data[-1]['price']} -> {price}")
                
                price_data.append({
                    'price': price,
                    'volume': volume,
                    'timestamp': now.isoformat()  # Store timestamp as ISO format
                })
                now = now - timedelta(minutes=1)  # Assuming 1-minute intervals
        except Exception as e:
            print(f"Error processing entry {entry}: {e}")
    
    # Sort by timestamp to ensure correct order
    price_data.sort(key=lambda x: x['timestamp'])
    
    # Filter for last N hours
    recent_data = [d for d in price_data if datetime.fromisoformat(d['timestamp']) > cutoff]
    
    # Print data summary
    print(f"\n📊 Data Summary:")
    print(f"Total data points: {len(recent_data)}")
    print(f"Time range: {recent_data[0]['timestamp']} to {recent_data[-1]['timestamp']}")
    print(f"Price range: ${min(d['price'] for d in recent_data):,.2f} - ${max(d['price'] for d in recent_data):,.2f}")
    print(f"Volume range: {min(d['volume'] for d in recent_data):.2f} - {max(d['volume'] for d in recent_data):.2f}")
    
    return recent_data

def analyze_price_states(price_data):
    """Analyze price movements and determine states"""
    states = []
    state_details = []
    current_state = "ANALYZING"
    current_position = None
    entry_price = None
    position_start_time = None
    fee_multiplier = 1.0
    best_pnl = 0.0
    
    # Configuration
    TREND_THRESHOLD = 0.001  # 0.1%
    ENTRY_THRESHOLD = 0.002  # 0.2%
    REVERSAL_THRESHOLD = 0.003  # 0.3%
    VOLUME_THRESHOLD = 0.01  # 1.0%
    STAGNATION_PERIODS = 5
    MAX_FEE_MULTIPLIER = 1.05  # 5% max fee
    
    # Calculate volatility for position sizing
    def calculate_volatility(data, window=10):
        if len(data) < window:
            return 0.01  # Default volatility
        prices = [float(d['price']) for d in data[-window:]]
        returns = [np.log(prices[i] / prices[i-1]) for i in range(1, len(prices))]
        return np.std(returns) * np.sqrt(252)  # Annualized volatility
    
    for i in range(1, len(price_data)):
        timestamp = price_data[i]['timestamp']
        current_time = datetime.fromisoformat(timestamp)
        price = float(price_data[i]['price'])
        volume = float(price_data[i]['volume'])
        
        # Calculate volatility and adjust position size
        volatility = calculate_volatility(price_data[:i+1])
        target_position_size = 1.0 / (volatility * 10)  # Inverse volatility sizing
        position_size = max(0.1, min(2.0, target_position_size))  # Cap between 0.1 and 2.0
        
        # Calculate price changes and PnL
        if i > 0:
            start_price = float(price_data[i-1]['price'])
            price_change = (price - start_price) / start_price
            volume_sum = sum(float(p['volume']) for p in price_data[max(0, i-5):i+1])
            pnl = 0.0
            if current_position and entry_price:
                if current_position == "OPEN_LONG":
                    pnl = (price - entry_price) / entry_price * 100 * position_size
                elif current_position == "OPEN_SHORT":
                    pnl = (entry_price - price) / entry_price * 100 * position_size
                
                # Update best PnL and check trailing stop
                if pnl > best_pnl:
                    best_pnl = pnl
                elif best_pnl > 0 and (best_pnl - pnl) > (best_pnl * 0.3):
                    print(f"🔄 Closing {current_position} position due to trailing stop")
                    current_position = None
                    position_start_time = None
                    entry_price = None
                    fee_multiplier = 1.0
                    best_pnl = 0.0
                    current_state = "CLOSE_LONG" if current_position == "OPEN_LONG" else "CLOSE_SHORT"
        else:
            start_price = price
            price_change = 0
            volume_sum = volume
            pnl = 0.0
            
        print(f"\n🔍 Position Analysis at {timestamp}:")
        print(f"Current State: {current_state}")
        print(f"Current Position: {current_position}")
        print(f"Position Size: {position_size:.2f}x")
        
        if current_position and position_start_time is not None:
            holding_time = (current_time - position_start_time).total_seconds() / 3600
            fee_multiplier = 1.0 + (holding_time * 0.3)  # 30% fee increase per hour
            print(f"Position Holding Time: {holding_time:.2f} hours")
            print(f"Current Fee Multiplier: {fee_multiplier:.2f}x")
            print(f"Current PnL: {pnl:.2f}%")
            print(f"Best PnL: {best_pnl:.2f}%")
            
            # Check for position reversal
            if current_position == "OPEN_LONG" and price_change < -REVERSAL_THRESHOLD:
                print(f"🔄 Closing {current_position} position due to reversal")
                current_position = None
                position_start_time = None
                entry_price = None
                fee_multiplier = 1.0
                best_pnl = 0.0
                current_state = "CLOSE_LONG"
            elif current_position == "OPEN_SHORT" and price_change > REVERSAL_THRESHOLD:
                print(f"🔄 Closing {current_position} position due to reversal")
                current_position = None
                position_start_time = None
                entry_price = None
                fee_multiplier = 1.0
                best_pnl = 0.0
                current_state = "CLOSE_SHORT"
            
            # Check for price stagnation
            if abs(price_change) < 0.0001:  # Less than 0.01% change
                stagnation_count = 1
                if stagnation_count >= STAGNATION_PERIODS:
                    print(f"🔄 Closing {current_position} position due to price stagnation")
                    current_position = None
                    position_start_time = None
                    entry_price = None
                    fee_multiplier = 1.0
                    best_pnl = 0.0
                    current_state = "CLOSE_LONG" if current_position == "OPEN_LONG" else "CLOSE_SHORT"
            else:
                stagnation_count = 0
                
            # Check for fee threshold
            if fee_multiplier >= MAX_FEE_MULTIPLIER:
                print(f"🔄 Closing {current_position} position due to fee threshold")
                current_position = None
                position_start_time = None
                entry_price = None
                fee_multiplier = 1.0
                best_pnl = 0.0
                current_state = "CLOSE_LONG" if current_position == "OPEN_LONG" else "CLOSE_SHORT"
            
            # Update fee multiplier
            fee_multiplier += 0.01  # 1% increase per period
        
        print(f"\n🔍 Price Movement Analysis:")
        print(f"Start Price: ${start_price:.2f}")
        print(f"End Price: ${price:.2f}")
        print(f"Price Change: {price_change:.2%}")
        print(f"Volume Sum: {volume_sum:.2f}")
        print(f"Volatility: {volatility:.2%}")
        
        # State transition logic
        if current_state == "ANALYZING":
            if price_change > ENTRY_THRESHOLD and volume_sum > VOLUME_THRESHOLD:
                current_state = "OPEN_LONG"
                current_position = "OPEN_LONG"
                entry_price = price
                position_start_time = current_time
                fee_multiplier = 1.0
                best_pnl = 0.0
                print(f"🔰 Opening new position: OPEN_LONG")
            elif price_change < -ENTRY_THRESHOLD and volume_sum > VOLUME_THRESHOLD:
                current_state = "OPEN_SHORT"
                current_position = "OPEN_SHORT"
                entry_price = price
                position_start_time = current_time
                fee_multiplier = 1.0
                best_pnl = 0.0
                print(f"🔰 Opening new position: OPEN_SHORT")
        
        states.append({
            'timestamp': timestamp,
            'state': current_state,
            'position': current_position,
            'price': price,
            'volume': volume,
            'price_change': price_change,
            'volume_sum': volume_sum,
            'fee_multiplier': fee_multiplier,
            'entry_price': entry_price,
            'pnl': pnl,
            'position_size': position_size,
            'volatility': volatility
        })
        
    return states

def create_state_visualization(state_counts, total_transitions):
    # Create a new directed graph
    dot = graphviz.Digraph('btc_states')
    dot.attr(rankdir='LR')
    
    # Color scheme for states
    state_colors = {
        'ANALYZING': '#FFD700',  # Gold
        'TRAP_DETECTION': '#FF6B6B',  # Red
        'OPEN_LONG': '#4CAF50',  # Green
        'OPEN_SHORT': '#2196F3',  # Blue
        'CLOSE_LONG': '#E91E63',  # Pink
        'CLOSE_SHORT': '#E91E63',  # Pink
    }
    
    # Add nodes with state counts
    for state, count in state_counts.items():
        if count > 0:  # Only show states that were visited
            percentage = (count / total_transitions) * 100
            label = f"{state}\n{count} visits\n({percentage:.1f}%)"
            dot.node(state, label, 
                    style='filled', 
                    fillcolor=state_colors.get(state, '#CCCCCC'),
                    fontcolor='black')
    
    # Add edges between states that can transition
    valid_transitions = {
        'ANALYZING': ['OPEN_LONG', 'OPEN_SHORT'],
        'OPEN_LONG': ['CLOSE_LONG'],
        'OPEN_SHORT': ['CLOSE_SHORT'],
        'CLOSE_LONG': ['ANALYZING'],
        'CLOSE_SHORT': ['ANALYZING'],
    }
    
    # Add edges with transition probabilities
    for source, targets in valid_transitions.items():
        if state_counts.get(source, 0) > 0:  # Only process states that were visited
            for target in targets:
                if state_counts.get(target, 0) > 0:  # Only connect to states that were visited
                    # Calculate edge thickness based on state counts
                    weight = 1 + (min(state_counts[source], state_counts[target]) / total_transitions) * 5
                    dot.edge(source, target, penwidth=str(weight))
    
    return dot

def aggregate_to_candles(price_data, interval_minutes=15):
    """Aggregate price data into OHLCV candles"""
    # Convert to pandas DataFrame
    df = pd.DataFrame([{
        'timestamp': datetime.fromisoformat(d['timestamp']),
        'price': d['price'],
        'volume': d['volume']
    } for d in price_data])
    
    # Set timestamp as index
    df.set_index('timestamp', inplace=True)
    
    # Resample to 15-minute candles
    ohlc = df.resample(f'{interval_minutes}T').agg({
        'price': ['first', 'max', 'min', 'last'],
        'volume': 'sum'
    })
    
    # Flatten column names
    ohlc.columns = ['open', 'high', 'low', 'close', 'volume']
    
    return ohlc

def create_price_chart(price_data, state_details):
    """Create a price chart with position events and PnL tracking"""
    # Create figure with three subplots in specific layout
    fig = plt.figure(figsize=(15, 10))
    
    # Define grid layout
    gs = GridSpec(2, 2, height_ratios=[2, 1])
    
    # Create subplots
    ax1 = fig.add_subplot(gs[0, :])  # Top full width
    ax2 = fig.add_subplot(gs[1, 0])  # Bottom left
    ax3 = fig.add_subplot(gs[1, 1])  # Bottom right
    
    # Convert timestamps to matplotlib dates
    dates = [date2num(datetime.fromisoformat(d['timestamp'])) for d in price_data]
    prices = [d['price'] for d in price_data]
    
    # Plot main price chart
    ax1.plot(dates, prices, 'white', linewidth=1)
    ax1.set_title('🔮 OMEGA KING Sacred Price Movement', color='white', fontsize=12)
    ax1.grid(True, alpha=0.2)
    ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    # Add entry and liquidation lines
    entry_price = price_data[0]['price']
    liq_price = entry_price * 0.93  # 7% below entry
    ax1.axhline(y=entry_price, color='green', linestyle='--', alpha=0.5, label=f'Entry: ${entry_price:,.2f}')
    ax1.axhline(y=liq_price, color='red', linestyle='--', alpha=0.5, label=f'Liquidation: ${liq_price:,.2f}')
    
    # Track PnL and position size
    pnl_data = []
    current_pnl = 0
    entry_price = None
    position_type = None
    
    # Create a dictionary to map timestamps to state details
    state_details_map = {d['timestamp']: d for d in state_details}
    
    # Process each price point and plot position markers
    for i, d in enumerate(price_data):
        price = d['price']
        
        # Get state detail for this timestamp
        detail = state_details_map.get(d['timestamp'])
        
        if detail and detail['position']:
            # Update PnL based on position
            if detail['position'] in ['OPEN_LONG', 'OPEN_SHORT']:
                # New position entry
                entry_price = price
                position_type = detail['position']
                current_pnl = 0
                
                # Plot entry markers
                marker = '^' if detail['position'] == 'OPEN_LONG' else 'v'
                color = '#4CAF50' if detail['position'] == 'OPEN_LONG' else '#2196F3'
                ax1.scatter(dates[i], price * 0.998, color=color, marker=marker, s=100)
                
            elif detail['position'] in ['CLOSE_LONG', 'CLOSE_SHORT'] and entry_price is not None:
                # Position exit
                if position_type == 'OPEN_LONG':
                    current_pnl = (price - entry_price) / entry_price * 100
                else:  # OPEN_SHORT
                    current_pnl = (entry_price - price) / entry_price * 100
                entry_price = None
                position_type = None
                
                # Plot exit markers
                ax1.scatter(dates[i], price * 1.002, color='#E91E63', marker='x', s=100)
        
        pnl_data.append(current_pnl)
    
    # Plot PnL chart
    ax2.plot(dates, pnl_data, 'cyan', linewidth=1)
    ax2.fill_between(dates, pnl_data, 0, alpha=0.2, color='cyan')
    ax2.set_title('📈 Profit/Loss Over Time', color='white', fontsize=10)
    ax2.grid(True, alpha=0.2)
    ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    # Add state tree text
    tree_text = "🔮 OMEGA KING SIMULATION: {\n"
    tree_text += "  'INITIAL SETUP': {\n"
    tree_text += f"    'Entry': '${price_data[0]['price']:,.2f}',\n"
    tree_text += f"    'Size': '1.0 BTC',\n"
    tree_text += f"    'Liquidation': '${liq_price:,.2f}'\n"
    tree_text += "  },\n"
    tree_text += "  'MARKET FLOW': {\n"
    tree_text += f"    'Start': '${price_data[0]['price']:,.2f}',\n"
    tree_text += f"    'High': '${max(d['price'] for d in price_data):,.2f}',\n"
    tree_text += f"    'Low': '${min(d['price'] for d in price_data):,.2f}',\n"
    tree_text += f"    'End': '${price_data[-1]['price']:,.2f}',\n"
    tree_text += f"    'Change': '{((price_data[-1]['price'] - price_data[0]['price']) / price_data[0]['price'] * 100):+.2f}%'\n"
    tree_text += "  },\n"
    tree_text += "  'BATTLE STATS': {\n"
    tree_text += f"    'Max Gain': '${max(pnl_data):.2f}%',\n"
    tree_text += f"    'Max Loss': '${min(pnl_data):.2f}%',\n"
    tree_text += f"    'Final PnL': '${pnl_data[-1]:.2f}%'\n"
    tree_text += "  },\n"
    tree_text += "  'STATE FLOW': {\n"
    tree_text += "    '🔍 Transitions',\n"
    tree_text += "    '📊 PnL Tracking',\n"
    tree_text += f"    '⚡ {len(state_details)} transitions'\n"
    tree_text += "  }\n"
    tree_text += "}"
    
    ax3.text(0, 1, tree_text, fontfamily='monospace', color='white', 
             transform=ax3.transAxes, fontsize=8, verticalalignment='top')
    ax3.axis('off')
    
    # Style the plots
    for ax in [ax1, ax2]:
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
    
    fig.set_facecolor('black')
    plt.tight_layout()
    
    return fig

def main():
    try:
        # Load Redis data
        print("📊 Loading BTC price data from Redis...")
        price_data = load_redis_data(hours=10)
        
        if not price_data:
            print("❌ No price data found in Redis")
            return
        
        print(f"✅ Loaded {len(price_data)} price points")
        
        # Analyze states
        print("\n🔍 Analyzing price movements and states...")
        states = analyze_price_states(price_data)
        
        # Create state transition visualization
        print("\n📈 Generating state transition visualization...")
        state_counts = defaultdict(int)
        for state in states:
            state_counts[state['state']] += 1
        dot = create_state_visualization(state_counts, len(states))
        
        # Create price chart with position events and PnL
        print("\n📊 Generating price chart with position events and PnL...")
        price_chart = create_price_chart(price_data, states)
        
        # Save visualizations
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save state transition visualization
        output_file = os.path.join(OUTPUT_DIR, f'btc_states_{timestamp}')
        dot.render(output_file, format='png', cleanup=True)
        
        # Save price chart
        price_chart_file = os.path.join(OUTPUT_DIR, f'btc_price_chart_{timestamp}.png')
        price_chart.savefig(price_chart_file)
        
        # Calculate PnL statistics
        pnl_data = [d['pnl'] for d in states if d['position']]
        total_pnl = sum(pnl_data)
        max_pnl = max(pnl_data)
        min_pnl = min(pnl_data)
        
        # Save state transitions to JSON
        json_output = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_transitions': len(states),
                'total_price_points': len(price_data),
                'analysis_window_size': 5,  # minutes
                'strategy': '10XFE3_TRADER'
            },
            'price_summary': {
                'start_price': price_data[0]['price'],
                'end_price': price_data[-1]['price'],
                'price_change_pct': ((price_data[-1]['price'] - price_data[0]['price']) / price_data[0]['price']) * 100
            },
            'pnl_summary': {
                'total_pnl': total_pnl,
                'max_pnl': max_pnl,
                'min_pnl': min_pnl,
                'average_pnl': total_pnl / len(pnl_data)
            },
            'state_counts': dict(state_counts),
            'state_details': states
        }
        
        json_file = os.path.join(OUTPUT_DIR, f'btc_states_{timestamp}.json')
        with open(json_file, 'w') as f:
            json.dump(json_output, f, indent=2)
        
        # Print statistics
        print(f"\n✅ Generated visualization of {len(states)} state transitions")
        print(f"📝 State transition visualization saved to: {output_file}.png")
        print(f"📝 Price chart saved to: {price_chart_file}")
        print(f"📝 State details saved to: {json_file}")
        
        # Print state statistics
        print("\n📊 State Statistics:")
        total_visits = sum(state_counts.values())
        for state, count in sorted(state_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_visits) * 100
            print(f"{state}: {count} visits ({percentage:.1f}%)")
        
        # Print price summary
        first_price = price_data[0]['price']
        last_price = price_data[-1]['price']
        price_change = ((last_price - first_price) / first_price) * 100
        print(f"\n💰 Price Summary:")
        print(f"Start: ${first_price:,.2f}")
        print(f"End: ${last_price:,.2f}")
        print(f"Change: {price_change:+.2f}%")
        
        # Print PnL summary
        print(f"\n📈 PnL Summary:")
        print(f"Total PnL: {total_pnl:.2f}%")
        print(f"Max PnL: {max_pnl:.2f}%")
        print(f"Min PnL: {min_pnl:.2f}%")
        print(f"Average PnL: {(total_pnl / len(pnl_data)):.2f}%")
        
        # Print position statistics
        positions = [d['position'] for d in states if d['position']]
        if positions:
            print("\n🎯 Position Statistics:")
            position_counts = defaultdict(int)
            for pos in positions:
                position_counts[pos] += 1
            for pos, count in position_counts.items():
                percentage = (count / len(positions)) * 100
                print(f"{pos}: {count} occurrences ({percentage:.1f}%)")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()