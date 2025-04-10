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
Basic Trading Analyzer Demo

This script demonstrates using the TradingAnalyzerB0t for market analysis.
"""

import random
import time
from omega_bots_bundle.analyzers.trading_analyzer import TradingAnalyzerB0t

def generate_sample_prices(start_price=10000.0, count=30, volatility=0.02):
    """Generate sample price data for demonstration."""
    prices = [start_price]
    price = start_price
    
    for _ in range(count - 1):
        # Random walk with slight upward bias
        change_percent = random.uniform(-volatility, volatility + 0.001)
        price = price * (1 + change_percent)
        prices.append(price)
    
    return prices

def demo_analyzer():
    """Demonstrate the trading analyzer with sample data."""
    # Create analyzer
    analyzer = TradingAnalyzerB0t()
    print(f"Initialized Trading Analyzer v{analyzer.get_version()}\n")
    
    # Generate sample prices
    print("Generating sample price data...")
    prices = generate_sample_prices()
    
    # Show sample data summary
    print(f"Starting price: ${prices[0]:.2f}")
    print(f"Ending price: ${prices[-1]:.2f}")
    price_change = (prices[-1] - prices[0]) / prices[0] * 100
    print(f"Price change: {price_change:.2f}%\n")
    
    # Analyze trend
    print("Analyzing market data...")
    trend = analyzer.analyze_trend(prices)
    volatility = analyzer.calculate_volatility(prices)
    support, resistance = analyzer.detect_support_resistance(prices)
    regime = analyzer.analyze_market_regime(prices)
    
    print("\nAnalysis Results:")
    print("----------------")
    print(f"Market trend: {trend}")
    print(f"Market regime: {regime}")
    print(f"Price volatility: {volatility:.2f}")
    print(f"Support level: ${support:.2f}")
    print(f"Resistance level: ${resistance:.2f}")
    
    # Calculate risk factor
    market_context = {
        "trend": trend,
        "recent_volatility": volatility,
        "price": prices[-1]
    }
    risk_factor = analyzer.calculate_risk_factor(market_context)
    print(f"Risk factor: {risk_factor:.2f}\n")
    
    # Determine if we should enter the market
    print("Trading Signal Analysis:")
    print("-----------------------")
    
    for emotional_state in ["neutral", "greedy", "fearful"]:
        trader_state = {"emotional_state": emotional_state}
        should_enter, direction, confidence = analyzer.should_enter_market(
            market_context, trader_state, risk_appetite=0.5
        )
        
        signal = "ENTER" if should_enter else "WAIT"
        emotion_display = emotional_state.upper()
        
        print(f"{emotion_display} trader signal: {signal}")
        if should_enter:
            print(f"  Direction: {direction.upper()}")
            print(f"  Confidence: {confidence:.2f}")

if __name__ == "__main__":
    demo_analyzer() 