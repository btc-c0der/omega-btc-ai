#!/usr/bin/env python3

"""
Profiled BTC Futures Trader

This module integrates the sophisticated market analysis capabilities of BtcFuturesTrader
with the diverse behavioral patterns of trader profiles to create realistic trading
simulations that account for both technical analysis and trader psychology.
"""

import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from omega_ai.trading.btc_futures_trader import BtcFuturesTrader
from omega_ai.trading.profiles import AggressiveTrader, StrategicTrader, NewbieTrader, ScalperTrader

# Terminal colors for output formatting
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"

# Background colors (if needed)
RED_BG = "\033[41m"
GREEN_BG = "\033[42m"
YELLOW_BG = "\033[43m"
BLUE_BG = "\033[44m"
MAGENTA_BG = "\033[45m"
CYAN_BG = "\033[46m"
WHITE_BG = "\033[47m"

@dataclass
class TradingPosition:
    direction: str
    entry_price: float
    size: float
    leverage: float
    entry_time: datetime
    stop_loss: Optional[float] = None
    take_profit: List[Dict] = field(default_factory=list)
    unrealized_pnl: float = 0.0

class ProfiledFuturesTrader(BtcFuturesTrader):
    """BTC Futures Trader that behaves according to a specific trader profile."""
    
    def __init__(self, 
                 profile_type: str = "strategic", 
                 initial_capital: float = 10000.0,
                 **kwargs):
        """Initialize trader with a specific psychological profile.
        
        Args:
            profile_type: The type of trader profile to use ("aggressive", 
                         "strategic", "newbie", "scalper")
            initial_capital: Starting capital
            **kwargs: Additional arguments for BtcFuturesTrader
        """
        super().__init__(initial_capital=initial_capital, **kwargs)
        self.profile_type = profile_type
        self.positions: List[TradingPosition] = []
        self.current_price: float = 0.0
        self.state = {
            "emotional_state": "neutral",
            "confidence": 0.5
        }
        self.win_rate = 0.0
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.risk_per_trade = 0.02  # 2% risk per trade
        
        # Create profile instance for accessing its attributes
        if profile_type == "aggressive":
            self.profile = AggressiveTrader(initial_capital)
            self.risk_per_trade = 0.05  # Higher risk
            self.max_leverage = 10
            self.patience = 0.3  # Low patience
            self.fomo_factor = 0.7  # High FOMO
            self.trend_follow_threshold = 0.4  # More likely to follow trends
        
        elif profile_type == "strategic":
            self.profile = StrategicTrader(initial_capital)
            self.risk_per_trade = 0.02  # Moderate risk
            self.max_leverage = 5
            self.patience = 0.8  # High patience
            self.fomo_factor = 0.2  # Low FOMO
            self.trend_follow_threshold = 0.7  # Only follows strong trends
        
        elif profile_type == "newbie":
            self.profile = NewbieTrader(initial_capital)
            self.risk_per_trade = random.uniform(0.01, 0.1)  # Inconsistent risk
            self.max_leverage = 20  # Dangerously high max leverage
            self.patience = 0.2  # Very low patience
            self.fomo_factor = 0.9  # Extreme FOMO
            self.trend_follow_threshold = 0.3  # Easily affected by short-term movements
        
        elif profile_type == "scalper":
            self.profile = ScalperTrader(initial_capital)
            self.risk_per_trade = 0.01  # Lower risk per trade due to higher frequency
            self.max_leverage = 15  # Higher leverage for small moves
            self.patience = 0.1  # Ultra-low patience (scalpers exit quickly)
            self.fomo_factor = 0.4  # Moderate FOMO
            self.trend_follow_threshold = 0.1  # Doesn't care much about trends
        
        # Track psychological state
        self.state = {
            "emotional_state": "neutral",  # neutral, greedy, fearful
            "confidence": 0.5,  # 0.0 to 1.0
            "stress_level": 0.0,  # 0.0 to 1.0
            "consecutive_losses": 0,
            "consecutive_wins": 0
        }
        
        print(f"Initialized {self.profile_type.capitalize()} BTC Futures Trader with ${initial_capital:.2f}")
    
    def should_open_position(self) -> Tuple[bool, str, float]:
        """Override to incorporate trader profile behavior."""
        # Get base analysis from BtcFuturesTrader's analyzer
        should_trade, reason, leverage = self.analyzer.analyze_trading_opportunity()
        
        # Apply profile-specific modifications to the decision
        if self.profile_type == "aggressive":
            # Aggressive traders are more likely to enter and use higher leverage
            leverage = min(leverage * 1.5, self.max_leverage)
            
            # Sometimes enter due to FOMO even against signals
            if not should_trade and random.random() < self.fomo_factor and "bearish" not in reason.lower():
                should_trade = True
                reason += " (FOMO override)"
                
        elif self.profile_type == "strategic":
            # Strategic traders wait for confirmation and use moderate leverage
            if should_trade:
                # Check if the signal is strong enough
                fib_levels = self.get_fibonacci_entry_zones()
                if not fib_levels or len(fib_levels) < 3:
                    # Not enough Fibonacci confirmation
                    if random.random() > 0.3:  # 70% chance to skip without confirmation
                        should_trade = False
                        reason = "Waiting for better Fibonacci alignment"
            
            # Calculate optimal leverage based on volatility and confidence
            leverage = max(1, min(leverage * 0.8, self.max_leverage))
            
        elif self.profile_type == "newbie":
            # Newbies make random decisions and use inappropriate leverage
            if random.random() < 0.3:
                # 30% chance to completely override analysis
                should_trade = random.random() < 0.5
                if should_trade:
                    reason = random.choice([
                        "Feeling lucky!",
                        "Saw a bullish tweet",
                        "Chart pattern looks good",
                        "Friend said it's going up"
                    ])
                    
            # Newbies often use excessive leverage
            if should_trade and random.random() < 0.4:
                leverage = random.randint(10, self.max_leverage)
                
        elif self.profile_type == "scalper":
            # Scalpers focus on orderbook imbalances and short timeframes
            # They ignore longer-term signals and focus on quick in-and-out
            
            # Only enter if there's sufficient volatility for scalping
            try:
                volatility = self.analyzer.get_recent_volatility()
                if volatility < 150:  # Low volatility is bad for scalpers
                    should_trade = False
                    reason = "Insufficient volatility for scalping"
            except:
                pass
                
            # Scalpers use higher leverage but have tight stops
            leverage = min(leverage * 1.3, self.max_leverage)
            
            # Override reason with orderbook-focused explanation
            if should_trade:
                reason = "Order book imbalance detected" if "long" in reason.lower() else "Order flow showing selling pressure"
        
        # Update psychological state based on market conditions
        self._update_psychological_state()
        
        # Final decision might be affected by current emotional state
        if self.state["emotional_state"] == "fearful" and random.random() < 0.7:
            should_trade = False
            reason = f"Skipping trade due to {self.state['emotional_state']} state"
        elif self.state["emotional_state"] == "greedy" and random.random() < 0.5:
            should_trade = True
            leverage = min(leverage * 1.2, self.max_leverage)
            reason += f" (Enhanced by {self.state['emotional_state']} state)"
        
        return should_trade, reason, leverage
    
    def _update_psychological_state(self):
        """Update the trader's psychological state based on recent performance."""
        # Update based on consecutive wins/losses
        if self.state["consecutive_losses"] > 3:
            self.state["emotional_state"] = "fearful"
            self.state["confidence"] = max(0.1, self.state["confidence"] - 0.2)
            self.state["stress_level"] = min(1.0, self.state["stress_level"] + 0.3)
        elif self.state["consecutive_wins"] > 3:
            self.state["emotional_state"] = "greedy"
            self.state["confidence"] = min(0.9, self.state["confidence"] + 0.2)
            
        # Profile-specific psychological adjustments
        if self.profile_type == "newbie":
            # Newbies are highly affected by recent results
            if self.state["consecutive_losses"] > 1:
                self.state["emotional_state"] = "fearful"
            elif self.state["consecutive_wins"] > 1:
                self.state["emotional_state"] = "greedy"
        
        # Over time, tendency to return to neutral
        if random.random() < 0.1:
            self.state["emotional_state"] = "neutral"
            self.state["confidence"] = 0.5
            self.state["stress_level"] = max(0.0, self.state["stress_level"] - 0.1)
    
    def close_position(self, position, reason: str, percentage: float = 1.0) -> None:
        """Override to incorporate trader profile behavior in exit decisions."""
        # Call parent method first to handle the actual closing
        super().close_position(position, reason, percentage)
        
        # Update psychological state based on trade outcome
        if position.realized_pnl > 0:
            self.state["consecutive_wins"] += 1
            self.state["consecutive_losses"] = 0
            
            # Update confidence level
            self.state["confidence"] = min(1.0, self.state["confidence"] + 0.1)
        else:
            self.state["consecutive_losses"] += 1
            self.state["consecutive_wins"] = 0
            
            # Update confidence level
            self.state["confidence"] = max(0.1, self.state["confidence"] - 0.15)
            
            # Update stress level
            self.state["stress_level"] = min(1.0, self.state["stress_level"] + 0.2)
    
    def print_position_status(self) -> None:
        """Override to add psychological state information."""
        super().print_position_status()
        
        # Add profile-specific information
        print(f"\n{CYAN}Trader Profile: {self.profile_type.capitalize()}{RESET}")
        
        # Format emotional state with color
        emotional_color = {
            "neutral": WHITE,
            "greedy": GREEN,
            "fearful": RED
        }.get(self.state["emotional_state"], WHITE)
        
        print(f"Emotional State: {emotional_color}{self.state['emotional_state'].capitalize()}{RESET}")
        print(f"Confidence: {self.state['confidence']:.2f} | Stress Level: {self.state['stress_level']:.2f}")
        
        if self.state["consecutive_wins"] > 0:
            print(f"{GREEN}Consecutive Wins: {self.state['consecutive_wins']}{RESET}")
        if self.state["consecutive_losses"] > 0:
            print(f"{RED}Consecutive Losses: {self.state['consecutive_losses']}{RESET}")
    
    def update_price(self, price: float):
        """Update current price and positions"""
        self.current_price = price
        # Update unrealized PnL for open positions
        for pos in self.positions:
            price_diff = self.current_price - pos.entry_price
            multiplier = 1 if pos.direction == "LONG" else -1
            pos.unrealized_pnl = price_diff * pos.size * pos.leverage * multiplier
    
    def execute_trading_logic(self):
        """Execute trading logic based on profile type"""
        try:
            if self.profile_type == "strategic":
                self._execute_strategic_logic()
            elif self.profile_type == "aggressive":
                self._execute_aggressive_logic()
            elif self.profile_type == "newbie":
                self._execute_newbie_logic()
            elif self.profile_type == "scalper":
                self._execute_scalper_logic()
        except Exception as e:
            logging.error(f"Error in trading logic for {self.profile_type}: {e}")
    
    def _execute_strategic_logic(self):
        # Implement strategic trading logic
        pass
    
    def _execute_aggressive_logic(self):
        # Implement aggressive trading logic
        pass
    
    def _execute_newbie_logic(self):
        # Implement newbie trading logic
        pass
    
    def _execute_scalper_logic(self):
        # Implement scalper trading logic
        pass