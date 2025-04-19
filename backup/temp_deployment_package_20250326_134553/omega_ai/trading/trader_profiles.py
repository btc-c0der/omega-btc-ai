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
Trader Profile Simulator for OmegaBTC AI

This module simulates different trader personalities with unique behaviors, risk tolerances, 
and psychological patterns to analyze how different trading styles perform in various market conditions.
"""

import datetime
import time
import random
import numpy as np
import redis
from typing import Dict, List, Tuple, Optional

# Import trader profiles from the profiles package
from omega_ai.trading.profiles import AggressiveTrader, StrategicTrader, NewbieTrader, ScalperTrader
from omega_ai.trading.trade_simulation import (
    simulate_trade_outcome, 
    simulate_strategic_trade_outcome, 
    simulate_newbie_trade_outcome
)
from omega_ai.trading.trading_analyzer import safe_float_convert

# Terminal colors for visual output
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BLUE = "\033[94m"
WHITE = "\033[97m"
BOLD = "\033[1m"

def simulate_trader_performance():
    """Run a simulation comparing different trader profiles."""
    print(f"{MAGENTA}{BOLD}╔════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}{BOLD}║        TRADER PROFILE SIMULATOR            ║{RESET}")
    print(f"{MAGENTA}{BOLD}║          OMEGA BTC AI RESEARCH             ║{RESET}")
    print(f"{MAGENTA}{BOLD}╚════════════════════════════════════════════╝{RESET}")
    
    # Initialize traders with different profiles
    aggressive_trader = AggressiveTrader(initial_capital=10000.0)
    strategic_trader = StrategicTrader(initial_capital=10000.0)
    newbie_trader = NewbieTrader(initial_capital=10000.0)
    scalper_trader = ScalperTrader(initial_capital=10000.0)
    
    # Initialize market simulation variables
    current_price = 83000.0  # Starting BTC price
    price_history = [current_price]
    market_trend_duration = 0
    current_trend = "sideways"
    market_regime = "neutral"
    volatility_base = 200.0
    
    # Add this function to generate simulated orderbook
    def generate_simulated_orderbook(price):
        """Generate a simulated order book around the current price."""
        spread = price * 0.0005  # 0.05% spread
        bid = price - spread/2
        ask = price + spread/2
        
        # Generate bids and asks with decreasing volume
        bids = []
        asks = []
        
        # Generate 10 levels on each side
        for i in range(10):
            # Bids
            bid_price = bid - i * spread
            bid_volume = random.uniform(0.5, 5.0) * (10-i)/10
            bids.append({"price": bid_price, "volume": bid_volume})
            
            # Asks
            ask_price = ask + i * spread
            ask_volume = random.uniform(0.5, 5.0) * (10-i)/10
            asks.append({"price": ask_price, "volume": ask_volume})
        
        return {
            "bids": bids,
            "asks": asks,
            "spread": spread,
            "mid_price": (bid + ask) / 2
        }
    
    # Run simulation
    try:
        # Main simulation loop
        iteration = 0
        while True:
            iteration += 1
            print(f"\n{BLUE}Simulation Iteration {iteration}{RESET}")
            
            # Simulate price movement
            price_change_pct = random.normalvariate(0, 0.005)  # 0.5% standard deviation
            current_price = current_price * (1 + price_change_pct)
            price_history.append(current_price)
            
            # Update market trend & regime
            market_trend_duration += 1
            if market_trend_duration > 20 or random.random() < 0.1:
                # Change trend occasionally
                market_trend_duration = 0
                current_trend = random.choice(["uptrend", "downtrend", "sideways"])
                
            # Update market regime with 5% chance of change
            if random.random() < 0.05:
                market_regime = random.choice(["bullish", "bearish", "neutral"])
            
            # Calculate volatility based on recent price movements
            if len(price_history) > 10:
                recent_prices = price_history[-10:]
                volatility_value = np.std(recent_prices)
            else:
                volatility_value = volatility_base
                
            # Update market context (use a single context for all traders)
            market_context = {
                "price": current_price,
                "timestamp": datetime.datetime.now().timestamp(),
                "trend": current_trend,  # Use the variable we defined above
                "regime": market_regime, # Use the variable we defined above
                "recent_volatility": safe_float_convert(volatility_value),
                "orderbook": generate_simulated_orderbook(current_price),
                "price_history": price_history[-20:],  # Last 20 prices
                "volume": random.uniform(100, 1000)  # Random trading volume
            }
            
            # Simulate aggressive trader
            should_enter, direction, reason, leverage = aggressive_trader.should_enter_trade(market_context)
            
            if should_enter:
                print(f"{YELLOW}[{aggressive_trader.name}] Opening {direction} position: {reason} ({leverage}x){RESET}")
                
                # Mock trade execution and result
                entry_price = market_context["price"]
                position_size = aggressive_trader.determine_position_size(direction, entry_price)
                stop_loss = aggressive_trader.set_stop_loss(direction, entry_price)
                take_profits = aggressive_trader.set_take_profit(direction, entry_price, stop_loss)
                
                # Simulate trade outcome
                trade_result = simulate_trade_outcome(
                    direction, 
                    entry_price, 
                    position_size, 
                    stop_loss, 
                    take_profits, 
                    leverage,
                    aggressive_trader.state.emotional_state
                )
                
                # Process the trade result
                aggressive_trader.process_trade_result(trade_result, random.uniform(0.5, 12.0))
            
            # Simulate strategic trader
            should_enter, direction, reason, leverage = strategic_trader.should_enter_trade(market_context)
            
            if should_enter:
                print(f"{CYAN}[{strategic_trader.name}] Opening {direction} position: {reason} ({leverage:.1f}x){RESET}")
                
                # Mock trade execution and result
                entry_price = market_context["price"]
                position_size = strategic_trader.determine_position_size(direction, entry_price)
                stop_loss = strategic_trader.set_stop_loss(direction, entry_price)
                take_profits = strategic_trader.set_take_profit(direction, entry_price, stop_loss)
                
                # Simulate trade outcome - strategic traders tend to hold longer
                trade_result = simulate_strategic_trade_outcome(
                    direction, 
                    entry_price, 
                    position_size, 
                    stop_loss, 
                    take_profits, 
                    leverage,
                    strategic_trader.state.emotional_state,
                    strategic_trader.patience_score
                )
                
                # Process the trade result - strategic trades last 1-24 hours
                strategic_trader.process_trade_result(trade_result, random.uniform(1.0, 24.0))
            
            # Simulate newbie trader (trades most frequently)
            should_enter, direction, reason, leverage = newbie_trader.should_enter_trade(market_context)
            
            if should_enter:
                print(f"{RED}[{newbie_trader.name}] Opening {direction} position: {reason} ({leverage}x){RESET}")
                
                # Mock trade execution and result
                entry_price = market_context["price"]
                position_size = newbie_trader.determine_position_size(direction, entry_price)
                stop_loss = newbie_trader.set_stop_loss(direction, entry_price)
                take_profits = newbie_trader.set_take_profit(direction, entry_price, stop_loss)
                
                # Simulate trade outcome - newbies often exit randomly
                # Use a special parameter for newbie traders (higher volatility and randomness)
                trade_result = simulate_newbie_trade_outcome(
                    direction, 
                    entry_price, 
                    position_size, 
                    stop_loss, 
                    take_profits, 
                    leverage,
                    newbie_trader.state.emotional_state
                )
                
                # Newbies have completely random trade durations
                newbie_trader.process_trade_result(trade_result, random.uniform(0.1, 48.0))
            
            # Simulate scalper trader
            should_enter, direction, reason, leverage = scalper_trader.should_enter_trade(market_context)
            
            if should_enter:
                print(f"{BLUE}[{scalper_trader.name}] Opening {direction} position: {reason} ({leverage:.1f}x){RESET}")
                
                # Mock trade execution and result
                entry_price = market_context["price"]
                position_size = scalper_trader.calculate_position_size(entry_price, 
                                 entry_price * (0.99 if direction == "LONG" else 1.01))
                stop_loss = entry_price * (0.99 if direction == "LONG" else 1.01)
                take_profits = [{"price": entry_price * (1.01 if direction == "LONG" else 0.99), "percentage": 1.0}]
                
                # Simulate trade outcome - scalpers have very short timeframes
                trade_result = simulate_trade_outcome(
                    direction, 
                    entry_price, 
                    position_size, 
                    stop_loss, 
                    take_profits, 
                    leverage,
                    "neutral" # Scalpers tend to be more mechanical
                )
                
                # Process the trade result - scalper trades last minutes to hours
                scalper_trader.process_trade_result(trade_result, random.uniform(0.1, 2.0))
            
            # Print trader status every 5 iterations
            if iteration % 5 == 0:
                print(f"\n{MAGENTA}═════ TRADER PERFORMANCE COMPARISON ═════{RESET}")
                aggressive_trader.print_status()
                strategic_trader.print_status()
                newbie_trader.print_status()
                scalper_trader.print_status()
            
            time.sleep(5)  # Pause between iterations
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Simulation stopped by user{RESET}")
        print(f"\n{MAGENTA}═════ FINAL PERFORMANCE COMPARISON ═════{RESET}")
        aggressive_trader.print_status()
        strategic_trader.print_status()
        newbie_trader.print_status()
        scalper_trader.print_status()
        print(f"\n{MAGENTA}End of simulation{RESET}")

if __name__ == "__main__":
    simulate_trader_performance()