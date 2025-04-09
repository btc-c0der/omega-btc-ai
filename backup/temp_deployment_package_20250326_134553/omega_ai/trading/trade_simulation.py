"""
Advanced trade simulation for OmegaBTC Trader Profiles

This module provides realistic price movement and position management simulation,
including partial closures, time-based exits, trailing stops, and market condition exits.
"""

import random
import time
import numpy as np
from typing import Dict, List, Tuple, Optional

# Terminal colors (copied from trader_profiles.py)
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"

# Background colors
RED_BG = "\033[41m"
GREEN_BG = "\033[42m"
YELLOW_BG = "\033[43m"
BLUE_BG = "\033[44m"
MAGENTA_BG = "\033[45m"
CYAN_BG = "\033[46m"
WHITE_BG = "\033[47m"

class TradeSimulator:
    """Advanced trade simulator that models realistic price movements and advanced exit strategies."""
    
    def __init__(self, 
                max_bars: int = 100,
                volatility_base: float = 0.002,
                trend_strength: float = 0.6,
                debug_mode: bool = False):
        """Initialize the trade simulator.
        
        Args:
            max_bars: Maximum number of price bars to simulate
            volatility_base: Base volatility per bar (as percentage)
            trend_strength: How strongly price follows the defined trend (0-1)
            debug_mode: Whether to print detailed simulation information
        """
        self.max_bars = max_bars
        self.volatility_base = volatility_base
        self.trend_strength = trend_strength
        self.debug_mode = debug_mode
    
    def simulate_aggressive_trade(self, 
                                direction: str,
                                entry_price: float,
                                position_size: float,
                                stop_loss: float,
                                take_profits: List[Dict],
                                leverage: float,
                                emotional_state: str) -> Tuple[float, List[Dict], int, float]:
        """Simulate an aggressive trader's position with advanced exit strategies.
        
        Returns:
            Tuple of (total PnL, list of exit details, number of bars, final price)
        """
        # Aggressive traders' settings
        trailing_stop_pct = 0.005  # 0.5% trailing stop
        max_trade_duration = 50    # Max bars to hold a trade
        quick_reaction = True      # React quickly to market changes
        
        # Adjust based on emotional state
        if emotional_state == "greedy":
            trailing_stop_pct = 0.003  # Tighter trailing stops when greedy
            max_trade_duration += 10   # Hold longer when greedy
        elif emotional_state == "fearful":
            trailing_stop_pct = 0.007  # Wider trailing stops when fearful
            max_trade_duration -= 10   # Exit earlier when fearful
        
        # Random bias: aggressive trades have ~40% chance of going against direction initially
        initial_bias = 1.0 if direction == "LONG" else -1.0
        if random.random() < 0.4:
            initial_bias *= -0.7  # Strong initial move against position
        
        # Higher volatility for aggressive trades
        volatility_multiplier = 1.3
        
        return self._simulate_trade(
            direction=direction,
            entry_price=entry_price,
            position_size=position_size,
            stop_loss=stop_loss,
            take_profits=take_profits,
            leverage=leverage,
            trailing_stop_pct=trailing_stop_pct,
            max_trade_duration=max_trade_duration,
            market_condition_exit=quick_reaction,
            initial_bias=initial_bias,
            volatility_multiplier=volatility_multiplier
        )
    
    def simulate_strategic_trade(self, 
                                direction: str,
                                entry_price: float,
                                position_size: float,
                                stop_loss: float,
                                take_profits: List[Dict],
                                leverage: float,
                                emotional_state: str,
                                patience_score: float) -> Tuple[float, List[Dict], int, float]:
        """Simulate a strategic trader's position with advanced exit strategies.
        
        Returns:
            Tuple of (total PnL, list of exit details, number of bars, final price)
        """
        # Strategic traders' settings
        trailing_stop_pct = 0.01   # 1% trailing stop (wider than aggressive)
        max_trade_duration = 80    # Longer max hold time
        quick_reaction = False     # More patient with market changes
        
        # Adjust based on emotional state (less impact than aggressive)
        if emotional_state == "greedy":
            trailing_stop_pct = 0.008  # Slightly tighter stops when greedy
            max_trade_duration += 5    # Hold slightly longer when greedy
        elif emotional_state == "fearful":
            trailing_stop_pct = 0.012  # Slightly wider stops when fearful
            max_trade_duration -= 5    # Exit slightly earlier when fearful
            
        # Adjust based on patience score
        trailing_stop_pct = trailing_stop_pct * (1.2 - patience_score * 0.4)  # More patient = tighter trailing stop
        max_trade_duration = int(max_trade_duration * (0.8 + patience_score * 0.4))  # More patient = longer max duration
        
        # Random bias: strategic trades have ~25% chance of going against direction initially
        initial_bias = 1.0 if direction == "LONG" else -1.0
        if random.random() < 0.25:
            initial_bias *= -0.5  # Moderate initial move against position
        
        # Normal volatility for strategic trades
        volatility_multiplier = 1.0
        
        return self._simulate_trade(
            direction=direction,
            entry_price=entry_price,
            position_size=position_size,
            stop_loss=stop_loss,
            take_profits=take_profits,
            leverage=leverage,
            trailing_stop_pct=trailing_stop_pct,
            max_trade_duration=max_trade_duration,
            market_condition_exit=quick_reaction,
            initial_bias=initial_bias,
            volatility_multiplier=volatility_multiplier
        )

    def _simulate_trade(self, 
                        direction: str,
                        entry_price: float,
                        position_size: float,
                        stop_loss: float,
                        take_profits: List[Dict],
                        leverage: float,
                        trailing_stop_pct: float,
                        max_trade_duration: int,
                        market_condition_exit: bool,
                        initial_bias: float,
                        volatility_multiplier: float) -> Tuple[float, List[Dict], int, float]:
        """Core trade simulation with price movement over time.
        
        Returns:
            Tuple of (total PnL, list of exit details, number of bars, final price)
        """
        if self.debug_mode:
            print(f"\n{CYAN}Simulating price movement for {direction} trade at ${entry_price:.2f}{RESET}")
            print(f"Stop loss: ${stop_loss:.2f} | Leverage: {leverage}x | Max duration: {max_trade_duration} bars")
            
        # Initialize simulation
        current_price = entry_price
        current_stop = stop_loss
        remaining_position = position_size
        position_value = position_size * entry_price * leverage
        total_pnl = 0.0
        exits = []
        
        # Deep copy take-profits to avoid modifying the original
        take_profits = [tp.copy() for tp in take_profits]
        
        # For trailing stop tracking
        highest_price = entry_price if direction == "LONG" else float('inf')  # For LONG
        lowest_price = float('inf') if direction == "LONG" else entry_price   # For SHORT
        
        # Generate random price series
        price_series = self._generate_price_series(
            entry_price, 
            stop_loss, 
            take_profits, 
            direction,
            initial_bias,
            volatility_multiplier
        )
        
        # Simulate bar by bar
        for bar_idx, price in enumerate(price_series):
            if bar_idx >= max_trade_duration:
                # Time-based exit
                exit_pct_change = (price - entry_price) / entry_price if direction == "LONG" else (entry_price - price) / entry_price
                exit_pnl = position_value * exit_pct_change * (remaining_position / position_size)
                
                exits.append({
                    "type": "time_based_exit",
                    "price": price,
                    "pnl": exit_pnl,
                    "position_closed": remaining_position,
                    "bar": bar_idx
                })
                
                total_pnl += exit_pnl
                
                if self.debug_mode:
                    print(f"{YELLOW}Time-based exit at ${price:.2f} after {bar_idx} bars: ${exit_pnl:.2f}{RESET}")
                
                return total_pnl, exits, bar_idx, price
            
            # Check for partial take profit hits
            for tp_idx, tp in enumerate(take_profits):
                if tp.get("hit", False):
                    continue  # Skip already hit take profits
                
                tp_price = tp["price"]
                tp_hit = False
                
                # Check if this TP was hit
                if (direction == "LONG" and price >= tp_price) or \
                   (direction == "SHORT" and price <= tp_price):
                    tp_hit = True
                    
                if tp_hit:
                    # Calculate portion size and PnL
                    portion = remaining_position * tp["percentage"]
                    pct_change = (tp_price - entry_price) / entry_price if direction == "LONG" else (entry_price - tp_price) / entry_price
                    portion_pnl = position_value * pct_change * (portion / position_size)
                    
                    # Update remaining position
                    remaining_position -= portion
                    
                    # Record exit
                    exits.append({
                        "type": "take_profit",
                        "level": tp_idx + 1,
                        "price": tp_price,
                        "pnl": portion_pnl,
                        "position_closed": portion,
                        "bar": bar_idx
                    })
                    
                    total_pnl += portion_pnl
                    tp["hit"] = True
                    
                    if self.debug_mode:
                        print(f"{GREEN}Take profit {tp_idx+1} hit at ${tp_price:.2f} on bar {bar_idx}: ${portion_pnl:.2f} ({tp['percentage']*100:.0f}% of position){RESET}")
                    
                    # If all take profits hit or no position remaining, exit
                    if remaining_position <= 0.0001:
                        if self.debug_mode:
                            print(f"{GREEN}All position closed at take profits{RESET}")
                        return total_pnl, exits, bar_idx, price
            
            # Update trailing stop logic
            if direction == "LONG" and price > highest_price:
                highest_price = price
                # Calculate new trailing stop
                new_stop = highest_price * (1 - trailing_stop_pct)
                
                # Only move stop up, never down
                if new_stop > current_stop:
                    current_stop = new_stop
                    if self.debug_mode and bar_idx % 5 == 0:  # Only log occasionally to reduce output
                        print(f"{BLUE}Updated trailing stop: ${current_stop:.2f}{RESET}")
                    
            elif direction == "SHORT" and price < lowest_price:
                lowest_price = price
                # Calculate new trailing stop
                new_stop = lowest_price * (1 + trailing_stop_pct)
                
                # Only move stop down, never up
                if new_stop < current_stop:
                    current_stop = new_stop
                    if self.debug_mode and bar_idx % 5 == 0:  # Only log occasionally
                        print(f"{BLUE}Updated trailing stop: ${current_stop:.2f}{RESET}")
            
            # Check for stop loss hit
            stop_hit = False
            if direction == "LONG" and price <= current_stop:
                stop_hit = True
            elif direction == "SHORT" and price >= current_stop:
                stop_hit = True
                
            if stop_hit and remaining_position > 0:
                # Calculate pnl
                pct_change = (current_stop - entry_price) / entry_price if direction == "LONG" else (entry_price - current_stop) / entry_price
                exit_pnl = position_value * pct_change * (remaining_position / position_size)
                
                # Record exit
                exits.append({
                    "type": "stop_loss",
                    "price": current_stop,
                    "pnl": exit_pnl,
                    "position_closed": remaining_position,
                    "bar": bar_idx
                })
                
                total_pnl += exit_pnl
                
                if self.debug_mode:
                    stop_type = "Trailing stop" if current_stop != stop_loss else "Initial stop"
                    print(f"{RED}{stop_type} hit at ${current_stop:.2f} on bar {bar_idx}: ${exit_pnl:.2f}{RESET}")
                
                return total_pnl, exits, bar_idx, price
            
            # Check for market condition exit
            if market_condition_exit and bar_idx > 10:
                # Simplified market condition change detection
                # In reality, this would check actual market indicators
                recent_prices = price_series[max(0, bar_idx-10):bar_idx+1]
                price_velocity = self._calculate_price_velocity(recent_prices)
                
                # If price velocity against our position exceeds threshold
                velocity_threshold = 0.015  # 1.5% adverse move in recent bars
                
                condition_exit = False
                if (direction == "LONG" and price_velocity < -velocity_threshold) or \
                   (direction == "SHORT" and price_velocity > velocity_threshold):
                   condition_exit = True
                
                if condition_exit and remaining_position > 0:
                    # Calculate pnl
                    pct_change = (price - entry_price) / entry_price if direction == "LONG" else (entry_price - price) / entry_price
                    exit_pnl = position_value * pct_change * (remaining_position / position_size)
                    
                    # Record exit
                    exits.append({
                        "type": "market_condition_exit",
                        "price": price,
                        "pnl": exit_pnl,
                        "position_closed": remaining_position,
                        "bar": bar_idx
                    })
                    
                    total_pnl += exit_pnl
                    
                    if self.debug_mode:
                        print(f"{YELLOW}Market condition exit at ${price:.2f} on bar {bar_idx}: ${exit_pnl:.2f}{RESET}")
                    
                    return total_pnl, exits, bar_idx, price
        
        # If we reach the end with position remaining, close at final price
        if remaining_position > 0:
            final_price = price_series[-1]
            pct_change = (final_price - entry_price) / entry_price if direction == "LONG" else (entry_price - final_price) / entry_price
            exit_pnl = position_value * pct_change * (remaining_position / position_size)
            
            exits.append({
                "type": "simulation_end",
                "price": final_price,
                "pnl": exit_pnl,
                "position_closed": remaining_position,
                "bar": len(price_series) - 1
            })
            
            total_pnl += exit_pnl
            
            if self.debug_mode:
                print(f"{BLUE}End of simulation with remaining position. Closed at ${final_price:.2f}: ${exit_pnl:.2f}{RESET}")
        
        return total_pnl, exits, len(price_series) - 1, price_series[-1]
            
    def _generate_price_series(self, 
                              entry_price: float, 
                              stop_loss: float, 
                              take_profits: List[Dict], 
                              direction: str,
                              initial_bias: float,
                              volatility_multiplier: float) -> List[float]:
        """Generate a realistic price series for trade simulation."""
        # Determine price movement range
        tp_prices = [tp["price"] for tp in take_profits]
        
        if direction == "LONG":
            price_low = min(stop_loss, entry_price * 0.95)  # Stop + some buffer
            price_high = max(tp_prices) * 1.1  # Beyond highest TP
            target_trend = 1.0  # Positive trend
        else:  # SHORT
            price_low = min(tp_prices) * 0.9  # Beyond lowest TP
            price_high = max(stop_loss, entry_price * 1.05)  # Stop + buffer
            target_trend = -1.0  # Negative trend
        
        # Base volatility with multiplier
        volatility = self.volatility_base * volatility_multiplier
        
        # Create price series
        prices = [entry_price]
        
        # Initial phase (first ~20% of bars) - follow initial bias
        initial_phase = int(self.max_bars * 0.2)
        for _ in range(initial_phase):
            last_price = prices[-1]
            # Random move with bias
            price_change = last_price * volatility * (initial_bias + random.uniform(-1, 1))
            new_price = last_price + price_change
            prices.append(new_price)
        
        # Main phase - follow target trend with noise
        for i in range(self.max_bars - initial_phase):
            last_price = prices[-1]
            
            # Slightly increasing volatility over time
            current_volatility = volatility * (1 + i / (self.max_bars * 2))
            
            # Create mean-reverting random walk with trend
            drift = self.trend_strength * target_trend * current_volatility
            noise = random.normalvariate(0, 1) * current_volatility
            price_change = last_price * (drift + noise)
            
            new_price = last_price + price_change
            
            # Ensure price stays within reasonable bounds
            new_price = max(price_low, min(price_high, new_price))
            prices.append(new_price)
        
        return prices
    
    def _calculate_price_velocity(self, prices: List[float]) -> float:
        """Calculate the recent price velocity as a percentage change."""
        if len(prices) < 2:
            return 0.0
        
        return (prices[-1] - prices[0]) / prices[0]


# Now update the simulate_trade_outcome functions in trader_profiles.py to use this new simulator

def simulate_trade_outcome(direction: str, entry_price: float, position_size: float, 
                         stop_loss: float, take_profits: List[Dict], leverage: float,
                         emotional_state: str) -> float:
    """Simulate an aggressive trader's position with realistic price movements."""
    simulator = TradeSimulator(debug_mode=False)
    
    total_pnl, exits, duration, final_price = simulator.simulate_aggressive_trade(
        direction=direction,
        entry_price=entry_price,
        position_size=position_size,
        stop_loss=stop_loss,
        take_profits=take_profits,
        leverage=leverage,
        emotional_state=emotional_state
    )
    
    # Summarize exits
    for exit_info in exits:
        exit_type = exit_info["type"]
        price = exit_info["price"]
        pnl = exit_info["pnl"]
        bar = exit_info["bar"]
        
        if exit_type == "take_profit":
            level = exit_info["level"]
            print(f"{GREEN}Take profit {level} hit at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
        elif exit_type == "stop_loss":
            print(f"{RED}Stop loss hit at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
        elif exit_type == "time_based_exit":
            print(f"{YELLOW}Time-based exit at ${price:.2f} after {bar} bars: ${pnl:.2f}{RESET}")
        elif exit_type == "market_condition_exit":
            print(f"{YELLOW}Market condition exit at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
    
    # Print overall result
    pnl_color = GREEN if total_pnl > 0 else RED
    print(f"{pnl_color}Total P&L: ${total_pnl:.2f} (trade duration: {duration} bars){RESET}")
    
    return total_pnl


def simulate_strategic_trade_outcome(direction: str, entry_price: float, position_size: float,
                                   stop_loss: float, take_profits: List[Dict], leverage: float,
                                   emotional_state: str, patience_score: float) -> float:
    """Simulate a strategic trader's position with realistic price movements."""
    simulator = TradeSimulator(debug_mode=False)
    
    total_pnl, exits, duration, final_price = simulator.simulate_strategic_trade(
        direction=direction,
        entry_price=entry_price,
        position_size=position_size,
        stop_loss=stop_loss,
        take_profits=take_profits,
        leverage=leverage,
        emotional_state=emotional_state,
        patience_score=patience_score
    )
    
    # Summarize exits
    for exit_info in exits:
        exit_type = exit_info["type"]
        price = exit_info["price"]
        pnl = exit_info["pnl"]
        bar = exit_info["bar"]
        
        if exit_type == "take_profit":
            level = exit_info["level"]
            print(f"{GREEN}Strategic TP {level} hit at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
        elif exit_type == "stop_loss":
            print(f"{RED}Strategic SL hit at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
        elif exit_type == "time_based_exit":
            print(f"{YELLOW}Strategic time exit at ${price:.2f} after {bar} bars: ${pnl:.2f}{RESET}")
        elif exit_type == "market_condition_exit":
            print(f"{YELLOW}Strategic condition exit at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
    
    # Print overall result
    pnl_color = GREEN if total_pnl > 0 else RED
    print(f"{pnl_color}Strategic total P&L: ${total_pnl:.2f} (duration: {duration} bars){RESET}")
    
    return total_pnl


def simulate_newbie_trade_outcome(direction: str, entry_price: float, position_size: float,
                                 stop_loss: float, take_profits: List[Dict], leverage: float,
                                 emotional_state: str) -> float:
    """Simulate the outcome of a newbie trader's position (high volatility and randomness)."""
    simulator = TradeSimulator(
        max_bars=150,               # Can hold trades longer (sometimes forgets about them)
        volatility_base=0.004,      # 2x normal volatility (newbies pick volatile assets)
        trend_strength=0.3,         # Less trend following (more random)
        debug_mode=False
    )
    
    # Newbie traders have higher probabilities of both stop losses and extreme moves
    # Simulate using the same engine but with more extreme parameters
    if emotional_state == "fomo":
        # FOMO trades often end badly
        initial_bias = -1.5 if direction == "LONG" else 1.5  # Strong move against position
        volatility_multiplier = 2.0  # Extreme volatility
    elif emotional_state == "revenge":
        # Revenge trades are erratic
        initial_bias = random.uniform(-2.0, 2.0)  # Completely random
        volatility_multiplier = 2.5  # Very extreme volatility
    elif emotional_state == "euphoric":
        # Sometimes euphoria is rewarded by lucky moves
        initial_bias = 1.5 if direction == "LONG" else -1.5  # Strong move in favor
        volatility_multiplier = 1.8  # High volatility
    else:
        # Default behavior
        initial_bias = random.uniform(-1.0, 1.0)  # Random
        volatility_multiplier = 1.5  # Higher than normal volatility
    
    # With extremely high leverage, small moves against can cause liquidation
    liquidation_threshold = 1 / leverage
    
    # Simulate the trade with custom parameters
    total_pnl, exits, duration, final_price = simulator._simulate_trade(
        direction=direction,
        entry_price=entry_price,
        position_size=position_size,
        stop_loss=stop_loss,
        take_profits=take_profits,
        leverage=leverage,
        trailing_stop_pct=0.02,  # Usually doesn't use trailing stops effectively
        max_trade_duration=random.randint(5, 150),  # Very inconsistent holding periods
        market_condition_exit=random.random() < 0.2,  # Usually ignores changing conditions
        initial_bias=initial_bias,
        volatility_multiplier=volatility_multiplier
    )
    
    # Check for liquidation events (much more common with newbie traders)
    if direction == "LONG":
        liquidation_price = entry_price * (1 - liquidation_threshold)
        if min([exit["price"] for exit in exits] + [final_price]) <= liquidation_price:
            # Account liquidated
            liquidation_pnl = -position_size * entry_price  # Total loss
            print(f"{RED_BG}{WHITE} 💥 LIQUIDATION! Account blown at ${liquidation_price:.2f} 💥 {RESET}")
            return liquidation_pnl
    else:  # SHORT
        liquidation_price = entry_price * (1 + liquidation_threshold)
        if max([exit["price"] for exit in exits] + [final_price]) >= liquidation_price:
            # Account liquidated
            liquidation_pnl = -position_size * entry_price  # Total loss
            print(f"{RED_BG}{WHITE} 💥 LIQUIDATION! Account blown at ${liquidation_price:.2f} 💥 {RESET}")
            return liquidation_pnl
    
    # Print normal exits for non-liquidation scenarios
    for exit_info in exits:
        exit_type = exit_info["type"]
        price = exit_info["price"]
        pnl = exit_info["pnl"]
        bar = exit_info["bar"]
        
        if exit_type == "take_profit":
            level = exit_info["level"]
            print(f"{GREEN}Newbie hit take profit {level} at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
        elif exit_type == "stop_loss":
            print(f"{RED}Newbie stop loss at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
        elif exit_type == "time_based_exit":
            print(f"{YELLOW}Newbie closed at ${price:.2f} after {bar} bars: ${pnl:.2f}{RESET}")
        elif exit_type == "market_condition_exit":
            print(f"{YELLOW}Newbie panic exit at ${price:.2f} (bar {bar}): ${pnl:.2f}{RESET}")
    
    # Print overall result
    pnl_color = GREEN if total_pnl > 0 else RED
    print(f"{pnl_color}Newbie P&L: ${total_pnl:.2f} (trade duration: {duration} bars){RESET}")
    
    return total_pnl