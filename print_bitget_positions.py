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
BitGet Position Fibonacci Analysis
Queries and displays current BitGet positions with Fibonacci analysis metrics
"""

import os
import sys
import json
import math
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Attempt to import the BitGet trader module
try:
    from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
except ImportError as e:
    logger.error(f"Failed to import BitGet trader module: {e}")
    logger.info("Make sure PYTHONPATH includes the root directory of the project")
    sys.exit(1)

# Define Fibonacci constants
PHI = 1.618033988749895  # Golden Ratio
FIBONACCI_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618, 4.236]

def calculate_phi_resonance(long_positions, short_positions):
    """Calculate Phi Resonance based on position distribution"""
    # Default to 0.5 if no positions
    if not long_positions and not short_positions:
        return 0.5
        
    total_long_size = sum(float(pos.get('contracts', 0)) for pos in long_positions)
    total_short_size = sum(float(pos.get('contracts', 0)) for pos in short_positions)
    
    # If only one side has positions
    if total_long_size == 0 or total_short_size == 0:
        return 0.618  # Golden ratio as the baseline
        
    # Calculate ratio between long and short positions
    long_short_ratio = total_long_size / total_short_size
    
    # Calculate how close the ratio is to PHI (1.618) or its inverse (0.618)
    phi_alignment = min(
        abs(long_short_ratio - PHI) / PHI,
        abs(long_short_ratio - (1/PHI)) / (1/PHI)
    )
    
    # Normalize to a 0-1 scale where 1 is perfect alignment
    phi_resonance = max(0, 1 - phi_alignment)
    
    return round(phi_resonance, 3)

def generate_fibonacci_levels(entry_price, is_long=True):
    """Generate Fibonacci retracement and extension levels"""
    fib_levels = {}
    
    # Set range for calculations
    if is_long:
        range_high = entry_price * 1.1  # 10% above entry
        range_low = entry_price * 0.9   # 10% below entry
    else:
        range_high = entry_price * 1.1  # 10% above entry
        range_low = entry_price * 0.9   # 10% below entry
    
    # Calculate levels
    for level in FIBONACCI_LEVELS:
        if level <= 0.5:
            # Levels below entry (retracement for longs, extension for shorts)
            fib_levels[str(level)] = entry_price - ((entry_price - range_low) * level / 0.5)
        else:
            # Levels above entry (extension for longs, retracement for shorts)
            normalized_level = (level - 0.5) / 0.5  # Normalize to 0-1 range
            fib_levels[str(level)] = entry_price + ((range_high - entry_price) * normalized_level)
    
    return fib_levels

def analyze_position(position):
    """Analyze a position with Fibonacci metrics"""
    if not position:
        return {}
    
    # Extract basic position details
    side = position.get('side', '')
    entry_price = position.get('entryPrice', 0)
    mark_price = position.get('markPrice', 0)
    contracts = position.get('contracts', 0)
    notional = position.get('notional', 0)
    unrealized_pnl = position.get('unrealizedPnl', 0)
    percentage = position.get('percentage', 0)
    
    # Generate Fibonacci levels
    is_long = side.lower() == 'long'
    fib_levels = generate_fibonacci_levels(entry_price, is_long)
    
    # Determine closest Fibonacci level to current price
    closest_level = None
    min_distance = float('inf')
    for level, price in fib_levels.items():
        distance = abs(mark_price - price)
        if distance < min_distance:
            min_distance = distance
            closest_level = level
    
    # Calculate price move percentage from entry
    price_move_percent = ((mark_price - entry_price) / entry_price) * 100
    if not is_long:
        price_move_percent = -price_move_percent
    
    # Calculate entry harmony (how well entry aligns with Fibonacci levels)
    # This is a simplified version - in reality would analyze market structure
    entry_harmony = 0.5  # Default value
    
    analysis = {
        'side': side,
        'contracts': contracts,
        'notional_value': notional,
        'entry_price': entry_price,
        'mark_price': mark_price,
        'price_move_percent': round(price_move_percent, 2),
        'unrealized_pnl': unrealized_pnl,
        'percentage_return': percentage,
        'fibonacci_levels': fib_levels,
        'closest_fibonacci_level': closest_level,
        'entry_harmony': entry_harmony,
    }
    
    return analysis

def display_position_analysis(position, analysis):
    """Display position analysis in a readable format"""
    if not position or not analysis:
        return
    
    print("\n" + "="*80)
    print(f"POSITION ANALYSIS: {position.get('symbol')} {analysis.get('side').upper()}")
    print("="*80)
    
    # Basic position details
    print(f"\n📊 POSITION DETAILS:")
    print(f"  Symbol:          {position.get('symbol')}")
    print(f"  Side:            {analysis.get('side').upper()}")
    print(f"  Size:            {analysis.get('contracts')} contracts (${analysis.get('notional_value'):.2f})")
    print(f"  Entry Price:     ${analysis.get('entry_price'):.2f}")
    print(f"  Current Price:   ${analysis.get('mark_price'):.2f}")
    print(f"  Price Movement:  {analysis.get('price_move_percent')}%")
    print(f"  Unrealized PnL:  ${analysis.get('unrealized_pnl'):.2f} ({analysis.get('percentage_return')}%)")
    
    # Leverage and risk metrics
    print(f"\n⚠️ RISK METRICS:")
    print(f"  Leverage:        {position.get('leverage')}x")
    print(f"  Liquidation:     ${position.get('liquidationPrice'):.2f}")
    if position.get('entryPrice') and position.get('liquidationPrice'):
        liq_distance = abs(position.get('liquidationPrice') - position.get('entryPrice'))
        liq_percent = (liq_distance / position.get('entryPrice')) * 100
        print(f"  Liq. Distance:   {liq_percent:.2f}% from entry")
    
    # Fibonacci Analysis
    print(f"\n🔱 FIBONACCI ANALYSIS:")
    print(f"  Closest Fib Level: {analysis.get('closest_fibonacci_level')}")
    
    # Print key Fibonacci levels
    print(f"\n  Key Fibonacci Levels:")
    key_levels = ['0', '0.236', '0.382', '0.5', '0.618', '1.0', '1.618']
    for level in key_levels:
        if level in analysis.get('fibonacci_levels', {}):
            price = analysis.get('fibonacci_levels', {}).get(level)
            if price:
                current = "◀️ CURRENT" if abs(price - analysis.get('mark_price')) < 100 else ""
                print(f"    {level.ljust(5)} : ${price:.2f} {current}")
    
    print("\n" + "-"*80)

def main():
    """Main function to retrieve and analyze BitGet positions"""
    logger.info("Initializing BitGet position analysis...")
    
    try:
        # Get API credentials from environment variables
        api_key = os.getenv("BITGET_API_KEY", "")
        secret_key = os.getenv("BITGET_SECRET_KEY", "")
        passphrase = os.getenv("BITGET_PASSPHRASE", "")
        
        # Verify API credentials
        if not api_key or not secret_key or not passphrase:
            logger.error("Missing BitGet API credentials in environment variables")
            print("\n⚠️ ERROR: Missing BitGet API credentials. Please set BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE environment variables.")
            return
            
        # Create BitGet trader instance (using mainnet)
        trader = BitGetLiveTraders(
            use_testnet=False,  # Use mainnet
            api_key=api_key,
            secret_key=secret_key,
            passphrase=passphrase,
            strategic_only=True  # Only use strategic trader
        )
        logger.info("Successfully connected to BitGet")
        
        # Get strategic trader and update positions
        strategic_trader = trader.traders.get("strategic")
        if not strategic_trader:
            logger.error("Strategic trader not initialized")
            print("\n⚠️ ERROR: Strategic trader not initialized")
            return
            
        # Fetch positions
        strategic_trader.update_positions()
        positions = strategic_trader.current_positions
        
        if not positions:
            logger.info("No active positions found")
            print("\n🔍 NO ACTIVE POSITIONS FOUND")
            return
        
        # Separate positions by side
        long_positions = [p for p in positions if p.get('side') == 'long']
        short_positions = [p for p in positions if p.get('side') == 'short']
        
        # Calculate Phi Resonance
        phi_resonance = calculate_phi_resonance(long_positions, short_positions)
        
        # Print overall portfolio metrics
        total_long_notional = sum(float(p.get('notional', 0)) for p in long_positions)
        total_short_notional = sum(float(p.get('notional', 0)) for p in short_positions)
        
        print("\n" + "="*80)
        print("BITGET PORTFOLIO FIBONACCI ANALYSIS")
        print("="*80)
        
        # Display position counts
        print(f"\n📈 PORTFOLIO OVERVIEW:")
        print(f"  Long Positions:  {len(long_positions)} (${total_long_notional:.2f})")
        print(f"  Short Positions: {len(short_positions)} (${total_short_notional:.2f})")
        
        # Display Long:Short ratio if both exist
        if total_long_notional > 0 and total_short_notional > 0:
            long_short_ratio = total_long_notional / total_short_notional
            print(f"  Long:Short Ratio: {long_short_ratio:.3f}")
            is_golden = 0.6 < long_short_ratio < 0.64 or 1.6 < long_short_ratio < 1.64
            if is_golden:
                print(f"  ✨ GOLDEN RATIO ALIGNMENT DETECTED!")
        
        # Display Phi Resonance
        print(f"\n🔱 PHI RESONANCE: {phi_resonance}")
        if phi_resonance > 0.8:
            print(f"  ✨ STRONG FIBONACCI ALIGNMENT")
        elif phi_resonance > 0.5:
            print(f"  ✓ Moderate Fibonacci alignment")
        else:
            print(f"  ⚠️ Weak Fibonacci alignment")
            
        # Analyze each position
        for position in positions:
            analysis = analyze_position(position)
            display_position_analysis(position, analysis)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return
    
if __name__ == "__main__":
    main() 