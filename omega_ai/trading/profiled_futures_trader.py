#!/usr/bin/env python3

"""
Profiled BTC Futures Trader

This module integrates the sophisticated market analysis capabilities of BtcFuturesTrader
with the diverse behavioral patterns of trader profiles to create realistic trading
simulations that account for both technical analysis and trader psychology.

MIT License

Copyright (c) 2025 OMEGA-BTC-AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import logging
import random
import redis
from dataclasses import dataclass, field
from datetime import datetime
from omega_ai.trading.btc_futures_trader import BtcFuturesTrader
from omega_ai.trading.profiles import AggressiveTrader, NewbieTrader, ScalperTrader, StrategicTrader
from typing import Dict, List, Optional, Tuple

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
            "emotional_state": "neutral",  # neutral, greedy, fearful
            "confidence": 0.5,  # 0.0 to 1.0
            "stress_level": 0.0,  # 0.0 to 1.0
            "consecutive_losses": 0,
            "consecutive_wins": 0
        }
        
        # Set risk_per_trade based on profile type - JAH BLESSED VALUES
        if profile_type == "aggressive":
            # Aggressive traders take higher risks - living on the edge
            self.risk_per_trade = 0.4  # 40% risk - RASTA FIRE
            self.max_leverage = 20    # High leverage
            self.patience = 0.3       # Low patience
            self.fomo_factor = 0.8    # High FOMO
            self.trend_follow_threshold = 0.5  # Responsive to short-term trends
            
        elif profile_type == "strategic":
            # Strategic traders take calculated risks - wisdom of JAH
            self.risk_per_trade = 0.2  # 20% risk - BALANCED DIVINE ENERGY
            self.max_leverage = 5     # Moderate leverage
            self.patience = 0.8       # High patience
            self.fomo_factor = 0.2    # Low FOMO
            self.trend_follow_threshold = 0.8  # Requires stronger trend confirmation
            
        elif profile_type == "newbie":
            # Newbies take random risks - seeking knowledge
            self.risk_per_trade = 0.3  # 30% risk - LEARNING THE PATH
            self.max_leverage = 50    # Excessive leverage
            self.patience = 0.2       # Very low patience
            self.fomo_factor = 0.9    # Extreme FOMO
            self.trend_follow_threshold = 0.3  # Easily affected by short-term movements
        
        elif profile_type == "scalper":
            # Scalpers take precise, calculated risks - swift divine action
            self.risk_per_trade = 0.2  # 20% risk - CALCULATED PRECISION
            self.max_leverage = 15    # Higher leverage for small moves
            self.patience = 0.1       # Ultra-low patience (scalpers exit quickly)
            self.fomo_factor = 0.4    # Moderate FOMO
            self.trend_follow_threshold = 0.1  # Doesn't care much about trends
        
        # Set reasonable defaults if profile_type is unknown
        else:
            self.risk_per_trade = 0.2
            self.max_leverage = 5
            self.patience = 0.5
            self.fomo_factor = 0.5
            self.trend_follow_threshold = 0.5
        
        # Track psychological state
        self.win_rate = 0.0
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
    
        # For profile-specific logic
        if profile_type == "aggressive":
            self.profile = AggressiveTrader(initial_capital)
            # Force risk alignment between trader and profile
            self.profile.risk_per_trade = self.risk_per_trade
        elif profile_type == "strategic":
            self.profile = StrategicTrader(initial_capital)
            self.profile.risk_per_trade = self.risk_per_trade
        elif profile_type == "newbie":
            self.profile = NewbieTrader(initial_capital)
            # Ensure the NewbieTrader profile uses our desired risk level
            self.profile.risk_per_trade = self.risk_per_trade
        elif profile_type == "scalper":
            self.profile = ScalperTrader(initial_capital)
            self.profile.risk_per_trade = self.risk_per_trade
        else:
            self.profile = StrategicTrader(initial_capital)  # Default to strategic
            self.profile.risk_per_trade = self.risk_per_trade
            
        print(f"Initialized {self.profile_type.capitalize()} BTC Futures Trader with ${initial_capital:.2f}")
    
    @property
    def risk_per_trade(self):
        """Get the risk per trade with divine profile alignment."""
        if hasattr(self, '_risk_per_trade'):
            return self._risk_per_trade
        
        # Return default values based on profile if not set
        if self.profile_type == "aggressive":
            return 0.4
        elif self.profile_type == "newbie":
            return 0.3
        elif self.profile_type == "strategic" or self.profile_type == "scalper":
            return 0.2
        return 0.2  # Default
    
    @risk_per_trade.setter
    def risk_per_trade(self, value):
        """Set the risk per trade with JAH BLESSING."""
        self._risk_per_trade = value
    
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
        # DIVINE FIX: Allow even mechanical scalpers to become fearful after many losses
        if self.state["consecutive_losses"] >= 5:
            # Even the most mechanical trader cannot resist fear after 5 consecutive losses
            self.state["emotional_state"] = "fearful"
            self.state["confidence"] = max(0.1, self.state["confidence"] - 0.2)
            self.state["stress_level"] = min(1.0, self.state["stress_level"] + 0.3)
        # Regular threshold for most profiles
        elif self.state["consecutive_losses"] > 3 and self.profile_type != "scalper":
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
        
        # Scalpers are mechanical but not emotionless when extremely stressed
        if self.profile_type == "scalper" and self.state["consecutive_losses"] < 5:
            self.state["emotional_state"] = "neutral"
        
        # Over time, tendency to return to neutral - but not during extreme loss streaks
        if random.random() < 0.1 and self.state["consecutive_losses"] < 3:
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

    def open_position(self, direction: str, reason: str, leverage: float = 1.0, stop_loss_pct: float = None) -> None:
        """
        Open a new trading position with JAH BLESS energy.
        
        Args:
            direction: "LONG" or "SHORT"
            reason: Why this position was opened
            leverage: Leverage multiplier (1-100)
            stop_loss_pct: Optional custom stop loss percentage (decimal, e.g., 0.02 for 2%)
        """
        if not direction in ["LONG", "SHORT"]:
            print(f"{RED}Invalid position direction: {direction}. Must be 'LONG' or 'SHORT'.{RESET}")
            return
        
        # Apply profile-specific risk management
        position_size = self.capital * self.risk_per_trade
        
        # Adjust leverage based on trader profile
        if self.profile_type == "newbie" and random.random() < 0.3:
            # Newbies sometimes use excessive leverage
            leverage = min(leverage * 2, self.max_leverage)
        elif self.profile_type == "aggressive" and random.random() < 0.4:
            # Aggressive traders often increase leverage
            leverage = min(leverage * 1.5, self.max_leverage)
        
        # Cap leverage at the max allowed
        leverage = min(leverage, self.max_leverage)
        
        # DIVINE FIX: Calculate stop loss based on provided percentage or default
        stop_loss = None
        if stop_loss_pct is not None:
            if direction == "LONG":
                stop_loss = self.current_price * (1 - stop_loss_pct)  # Stop below entry for longs
            else:
                stop_loss = self.current_price * (1 + stop_loss_pct)  # Stop above entry for shorts
            print(f"{YELLOW}Using custom stop loss at ${stop_loss:.2f} ({stop_loss_pct*100:.1f}%){RESET}")
        else:
            stop_loss = self._calculate_stop_loss(direction, self.current_price)
        
        # Create the position with divine Rastafarian energy
        position = TradingPosition(
            direction=direction,
            entry_price=self.current_price,
            size=position_size,
            leverage=leverage,
            entry_time=datetime.now(),
            stop_loss=stop_loss,
            take_profit=self._calculate_take_profit_levels(direction, self.current_price)
        )
        
        # Add to positions list with JAH BLESSING
        self.positions.append(position)
        
        # Apply psychological effects
        if self.state["emotional_state"] == "greedy":
            # When greedy, traders often skip proper position sizing
            print(f"{YELLOW}⚠️ Greed affected position sizing! Using higher risk.{RESET}")
        
        # Log the trade with divine color
        direction_color = GREEN if direction == "LONG" else RED
        print(f"\n{direction_color}📊 OPENED {direction} POSITION with {leverage}x leverage{RESET}")
        print(f"Entry Price: ${self.current_price:,.2f}")
        print(f"Position Size: ${position_size:,.2f}")
        print(f"Reason: {reason}")
        
        # Update state
        self._update_psychological_state()
        
        # Check if we should update Redis with position data
        try:
            self._store_position_in_redis(position)
        except Exception as e:
            print(f"{YELLOW}Cannot store position in Redis: {e}{RESET}")

    def _calculate_stop_loss(self, direction: str, entry_price: float) -> float:
        """Calculate appropriate stop-loss based on trader profile."""
        # Different profiles have different stop-loss strategies
        volatility_factor = 0.02  # Default 2% volatility assumption
        
        try:
            # Try to get actual recent volatility
            volatility = self.analyzer.get_recent_volatility() / entry_price
            volatility_factor = max(0.005, min(0.05, volatility))  # Cap between 0.5% and 5%
        except:
            pass
        
        # Profile-specific stop-loss multipliers
        stop_multipliers = {
            "strategic": 2.0,    # Wide stops based on market structure
            "aggressive": 1.0,   # Tighter stops to enable higher leverage
            "newbie": 0.5,       # Too tight stops that often get hit
            "scalper": 0.7       # Tight but reasonable for short timeframes
        }
        
        multiplier = stop_multipliers.get(self.profile_type, 1.5)
        stop_distance = entry_price * volatility_factor * multiplier
        
        if direction == "LONG":
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance

    def _calculate_take_profit_levels(self, direction: str, entry_price: float) -> List[Dict]:
        """Calculate multiple take-profit levels based on trader profile."""
        # Different profiles use different take-profit strategies
        take_profits = []
        
        # Base profit target as percentage of entry price
        base_target = 0.02  # 2% default target
        
        # Profile-specific take-profit configurations
        if self.profile_type == "strategic":
            # Strategic traders use multiple take-profit levels at key levels
            targets = [
                {"percentage": 0.5, "price_pct": base_target * 1.5},
                {"percentage": 0.3, "price_pct": base_target * 2.5},
                {"percentage": 0.2, "price_pct": base_target * 4.0}
            ]
        elif self.profile_type == "aggressive":
            # Aggressive traders use bigger targets but often exit too early
            targets = [
                {"percentage": 0.7, "price_pct": base_target * 3},
                {"percentage": 0.3, "price_pct": base_target * 5}
            ]
        elif self.profile_type == "newbie":
            # Newbies often use unrealistic profit targets
            if random.random() < 0.5:
                # Sometimes they exit too early
                targets = [{"percentage": 1.0, "price_pct": base_target * 0.7}]
            else:
                # Sometimes they wait for unrealistic targets
                targets = [{"percentage": 1.0, "price_pct": base_target * 10}]
        elif self.profile_type == "scalper":
            # Scalpers use small, quick targets
            targets = [{"percentage": 1.0, "price_pct": base_target * 0.8}]
        else:
            # Default - single take profit level
            targets = [{"percentage": 1.0, "price_pct": base_target * 2.0}]
        
        # Calculate actual price levels based on direction
        for target in targets:
            price_change = entry_price * target["price_pct"]
            
            if direction == "LONG":
                price = entry_price + price_change
            else:
                price = entry_price - price_change
                
            take_profits.append({
                "percentage": target["percentage"],
                "price": price
            })
        
        return take_profits

    def _store_position_in_redis(self, position: TradingPosition) -> None:
        """Store position data in Redis for analysis."""
        try:
            # Convert position to serializable dictionary
            position_data = {
                "direction": position.direction,
                "entry_price": position.entry_price,
                "size": position.size,
                "leverage": position.leverage,
                "entry_time": position.entry_time.isoformat(),
                "stop_loss": position.stop_loss,
                "trader_profile": self.profile_type
            }
            
            # Store in Redis
            redis_key = f"trader:positions:{self.profile_type}:{datetime.now().timestamp()}"
            redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
            redis_conn.set(redis_key, json.dumps(position_data))
            
            # Also store in a list of positions
            redis_conn.lpush(f"trader:positions:{self.profile_type}", json.dumps(position_data))
            
            # Trim the list to a reasonable size
            redis_conn.ltrim(f"trader:positions:{self.profile_type}", 0, 99)
            
        except Exception as e:
            # Don't let Redis errors stop the trading
            print(f"{YELLOW}Redis storage error: {e}{RESET}")

    def manage_open_positions(self):
        """
        Manage all open positions with divine RASTA wisdom.
        - Update unrealized profit/loss
        - Check stop loss and take profit conditions
        - Close positions if conditions are met
        """
        if not self.positions:
            return
            
        # Update each position's unrealized P&L first
        for position in self.positions:
            self._update_position_pnl(position)
        
        # Positions to close (can't modify list while iterating)
        positions_to_close = []
        
        # Check each position for stop loss / take profit
        for position in self.positions:
            # Check stop loss
            if self._check_stop_loss_hit(position):
                reason = f"🛑 Stop loss triggered at ${self.current_price:,.2f}"
                positions_to_close.append((position, reason))
                continue
                
            # Check take profit
            if self._check_take_profit_hit(position):
                reason = f"✅ Take profit triggered at ${self.current_price:,.2f}" 
                positions_to_close.append((position, reason))
                continue
                
        # Close positions that hit stop/take profit
        for position, reason in positions_to_close:
            self._close_position(position, reason)

    def _update_position_pnl(self, position):
        """Calculate unrealized profit/loss for a position with divine precision."""
        # Skip if no current price
        if not self.current_price or position.entry_price == 0:
            return
            
        # Calculate price difference
        price_diff = self.current_price - position.entry_price
        
        # P&L calculation depends on direction
        if position.direction == "LONG":
            # For long positions, profit when price goes up
            position.unrealized_pnl = (price_diff / position.entry_price) * position.size * position.leverage
        else:
            # For short positions, profit when price goes down
            position.unrealized_pnl = (-price_diff / position.entry_price) * position.size * position.leverage
        
        # Add divine PnL status with cosmic colors
        if position.unrealized_pnl > 0:
            print(f"{GREEN}Position {position.direction} showing profit: ${position.unrealized_pnl:.2f}{RESET}")
        elif position.unrealized_pnl < 0:
            print(f"{RED}Position {position.direction} showing loss: ${position.unrealized_pnl:.2f}{RESET}")

    def _check_stop_loss_hit(self, position):
        """Check if a position's stop loss has been triggered with divine protection."""
        if position.stop_loss is None:
            return False
            
        if position.direction == "LONG":
            # Long positions: stop loss is below entry
            return self.current_price <= position.stop_loss
        else:
            # Short positions: stop loss is above entry
            return self.current_price >= position.stop_loss

    def _check_take_profit_hit(self, position):
        """Check if any take profit level has been hit with divine blessing."""
        if not position.take_profit:
            return False
            
        for tp in position.take_profit:
            price_level = tp.get("price")
            if price_level is None:
                continue
                
            if position.direction == "LONG":
                # Long positions: take profit is above entry
                if self.current_price >= price_level:
                    return True
            else:
                # Short positions: take profit is below entry
                if self.current_price <= price_level:
                    return True
                    
        return False

    def _close_position(self, position, reason=""):
        """Close a position with JAH BLESSING and record results."""
        # Calculate realized profit/loss
        price_diff = self.current_price - position.entry_price
        
        if position.direction == "SHORT":
            # For shorts, profit is inverse
            price_diff = -price_diff
            
        # Calculate P&L with leverage
        pnl = (price_diff / position.entry_price) * position.size * position.leverage
        
        # Update trader capital with realized profit/loss
        self.capital += pnl
        
        # Get divine color for P&L
        color = GREEN if pnl > 0 else RED if pnl < 0 else YELLOW
        
        # Calculate ROI percentage
        roi_pct = (pnl / position.size) * 100
        
        # Print spiritual closing message
        print(f"\n{color}🔒 CLOSED {position.direction} POSITION with {position.leverage}x leverage{RESET}")
        print(f"Entry Price: ${position.entry_price:,.2f}")
        print(f"Exit Price: ${self.current_price:,.2f}")
        print(f"P&L: {color}${pnl:,.2f} ({roi_pct:+.2f}%){RESET}")
        print(f"Reason: {reason}")
        print(f"Position Lifetime: {(datetime.now() - position.entry_time).total_seconds()/60:.1f} minutes")
        
        # Update trader state based on outcome
        if pnl > 0:
            self.state["consecutive_wins"] += 1
            self.state["consecutive_losses"] = 0
            self.winning_trades += 1
            
            # Boost confidence with wins
            self.state["confidence"] = min(1.0, self.state["confidence"] + 0.1)
            
            # Update emotional state
            if roi_pct > 15:
                self.state["emotional_state"] = "greedy"
            else:
                self.state["emotional_state"] = "neutral"
                
        else:
            self.state["consecutive_losses"] += 1
            self.state["consecutive_wins"] = 0
            self.losing_trades += 1
            
            # Reduced confidence with losses
            self.state["confidence"] = max(0.1, self.state["confidence"] - 0.15)
            
            # Update emotional state
            if roi_pct < -10:
                self.state["emotional_state"] = "fearful"
            # DIVINE RASTA FIX: Check consecutive losses threshold regardless of ROI
            elif self.state["consecutive_losses"] > 3:
                self.state["emotional_state"] = "fearful"
            else:
                self.state["emotional_state"] = "neutral"
        
        # DIVINE RASTA FIX: Apply psychological update after trade
        self._update_psychological_state()
        
        # Update total trades counter
        self.total_trades += 1
        
        # Calculate win rate
        if self.total_trades > 0:
            self.win_rate = self.winning_trades / self.total_trades
        
        # Store trade result in trade history
        trade_result = {
            "direction": position.direction,
            "entry_price": position.entry_price,
            "exit_price": self.current_price,
            "entry_time": position.entry_time,
            "exit_time": datetime.now(),
            "size": position.size,
            "leverage": position.leverage,
            "pnl": pnl,
            "pnl_percent": roi_pct,
            "reason": reason
        }
        
        # Try to store in Redis if available
        try:
            self._store_trade_result(trade_result)
        except Exception as e:
            print(f"{YELLOW}Redis error storing trade result: {e}{RESET}")
        
        # Remove position from active positions list
        self.positions.remove(position)
        
        return pnl
    
    def _store_trade_result(self, trade_result):
        """Store trade result in Redis for divine analysis."""
        try:
            # Convert datetime objects to ISO format strings
            trade_data = dict(trade_result)
            if "entry_time" in trade_data and isinstance(trade_data["entry_time"], datetime):
                trade_data["entry_time"] = trade_data["entry_time"].isoformat()
            if "exit_time" in trade_data and isinstance(trade_data["exit_time"], datetime):
                trade_data["exit_time"] = trade_data["exit_time"].isoformat()
            
            # Add trader profile type
            trade_data["profile_type"] = self.profile_type
            
            # Convert to JSON
            trade_json = json.dumps(trade_data)
            
            # Store in Redis
            redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
            
            # Add to trade history list
            redis_conn.lpush(f"trader:trades:{self.profile_type}", trade_json)
            
            # Keep trade history to reasonable size
            redis_conn.ltrim(f"trader:trades:{self.profile_type}", 0, 99)
            
            # Also store latest performance metrics
            metrics = {
                "win_rate": self.win_rate,
                "total_trades": self.total_trades,
                "capital": self.capital,
                "timestamp": datetime.now().isoformat(),
                "emotional_state": self.state["emotional_state"],
                "confidence": self.state["confidence"]
            }
            
            redis_conn.hset(f"trader:metrics:{self.profile_type}", mapping=metrics)
            
        except Exception as e:
            # Don't let Redis errors disrupt trading
            print(f"{YELLOW}Redis error storing trade result: {e}{RESET}")