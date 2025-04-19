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
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""

"""
POSITION HARMONY EXAMPLE

This script demonstrates the use of the PositionHarmonyAdvisor class
to analyze and provide recommendations for trading positions based on
Fibonacci principles and Golden Ratio harmony.
"""

import sys
import json
from pprint import pprint
from datetime import datetime

# Add parent directory to path to allow imports
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.recommendations.position_harmony import PositionHarmonyAdvisor

def main():
    """Run the Position Harmony example"""
    print("=" * 80)
    print(" POSITION HARMONY ADVISOR - DIVINE SIZING RECOMMENDATIONS")
    print("=" * 80)
    
    # Create sample account data
    account_balance = 10000.0  # $10,000 account
    leverage = 1.0  # No leverage
    
    # Create sample positions
    # These are structured similar to what would come from BitGet API
    sample_positions = [
        {
            "symbol": "BTCUSDT",
            "side": "long", 
            "notional": 3000.0,  # $3000 position
            "leverage": 1.0,
            "entry_price": 45000.0,
            "mark_price": 46000.0,
            "unrealized_pnl": 66.67
        },
        {
            "symbol": "ETHUSDT",
            "side": "long",
            "notional": 1000.0,  # $1000 position
            "leverage": 1.0,
            "entry_price": 2500.0,
            "mark_price": 2550.0,
            "unrealized_pnl": 20.0
        },
        {
            "symbol": "LTCUSDT",
            "side": "short",
            "notional": 500.0,  # $500 position
            "leverage": 1.0,
            "entry_price": 80.0,
            "mark_price": 78.0,
            "unrealized_pnl": 12.5
        }
    ]
    
    # Create the PositionHarmonyAdvisor
    advisor = PositionHarmonyAdvisor(
        max_account_risk=0.0618,  # 6.18% max account risk
        position_phi_targets=True, 
        long_short_balance=True
    )
    
    # Analyze the positions
    analysis = advisor.analyze_positions(
        positions=sample_positions,
        account_balance=account_balance,
        leverage=leverage
    )
    
    # Print summary of analysis
    print(f"\n📊 POSITION HARMONY ANALYSIS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Account Balance: ${account_balance:,.2f}")
    print(f"Total Positions: {analysis['position_metrics']['position_count']}")
    print(f"Total Exposure: ${analysis['position_metrics']['total_exposure']:,.2f} " +
          f"({analysis['position_metrics']['total_exposure_pct']*100:.2f}% of account)")
    
    print(f"\n🌟 HARMONY STATE: {analysis['harmony_state']}")
    print(f"Harmony Score: {analysis['harmony_score']:.3f}")
    
    print(f"\n✨ DIVINE ADVICE:")
    print(f"  {analysis['divine_advice']}")
    
    # Print recommendations
    if analysis['recommendations']:
        print("\n📝 RECOMMENDATIONS:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"  {i}. {rec['description']}")
            if rec['type'] == 'position_size':
                print(f"     Symbol: {rec['position_symbol']}")
                print(f"     Current: {rec['current_size_pct']*100:.2f}% " +
                      f"(${rec['current_size_pct']*account_balance:,.2f})")
                print(f"     Target:  {rec['target_size_pct']*100:.2f}% " +
                      f"(${rec['target_size']:,.2f})")
            elif rec['type'] == 'long_short_balance':
                print(f"     Current Ratio: {rec['current_ratio']:.3f}")
                print(f"     Target Ratio:  {rec['target_ratio']:.3f}")
    else:
        print("\n📝 RECOMMENDATIONS: None (Position harmony achieved)")
    
    # Print ideal position sizes
    print("\n🎯 IDEAL POSITION SIZES (FIBONACCI-BASED):")
    for size in analysis['ideal_position_sizes'][:5]:  # Show top 5 position sizes
        print(f"  • {size['size_name']} - ${size['absolute_size']:,.2f} " +
              f"({size['risk_category']} risk)")
    
    print("\n" + "=" * 80)
    
    # Example of unbalanced portfolio
    print("\n\nUNBALANCED PORTFOLIO EXAMPLE")
    print("-" * 40)
    
    # Create unbalanced positions (heavy on longs)
    unbalanced_positions = [
        {
            "symbol": "BTCUSDT",
            "side": "long", 
            "notional": 5000.0,
            "leverage": 1.0,
            "entry_price": 45000.0,
            "mark_price": 46000.0,
            "unrealized_pnl": 111.11
        },
        {
            "symbol": "ETHUSDT",
            "side": "long",
            "notional": 2500.0,
            "leverage": 1.0,
            "entry_price": 2500.0,
            "mark_price": 2550.0,
            "unrealized_pnl": 50.0
        },
        {
            "symbol": "LTCUSDT",
            "side": "short",
            "notional": 500.0,
            "leverage": 1.0,
            "entry_price": 80.0,
            "mark_price": 78.0,
            "unrealized_pnl": 12.5
        }
    ]
    
    # Analyze the unbalanced positions
    unbalanced_analysis = advisor.analyze_positions(
        positions=unbalanced_positions,
        account_balance=account_balance,
        leverage=leverage
    )
    
    # Print summary
    print(f"\n📊 UNBALANCED PORTFOLIO ANALYSIS")
    print(f"Harmony Score: {unbalanced_analysis['harmony_score']:.3f}")
    print(f"Harmony State: {unbalanced_analysis['harmony_state']}")
    print(f"Long/Short Ratio: {unbalanced_analysis['position_metrics']['long_short_ratio']:.2f}")
    
    print(f"\n✨ DIVINE ADVICE:")
    print(f"  {unbalanced_analysis['divine_advice']}")
    
    # Print recommendations for unbalanced portfolio
    if unbalanced_analysis['recommendations']:
        print("\n📝 RECOMMENDATIONS:")
        for i, rec in enumerate(unbalanced_analysis['recommendations'], 1):
            print(f"  {i}. {rec['description']}")
    
    print("\n" + "=" * 80)
    
    # Show harmony trend after multiple analyses
    # Simulate a few more position states to build history
    for _ in range(3):
        # Adjust position sizes slightly for simulation
        for pos in sample_positions:
            # Randomly adjust position by small amount
            import random
            adjustment = 1.0 + (random.random() - 0.5) * 0.1  # ±5%
            pos['notional'] *= adjustment
        
        # Run analysis again to build history
        advisor.analyze_positions(sample_positions, account_balance, leverage)
    
    # Get harmony trend
    trend = advisor.get_harmony_trend()
    
    print("\nHARMONY TREND ANALYSIS")
    print("-" * 40)
    print(f"Trend Direction: {trend['trend'].upper()}")
    print(f"Recent Change: {trend['change']*100:.2f}%")
    print(f"Latest Score: {trend['latest_score']:.3f}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main() 