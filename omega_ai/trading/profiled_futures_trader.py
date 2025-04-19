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
from datetime import datetime, timezone
from omega_ai.trading.btc_futures_trader import BtcFuturesTrader, TradeHistory, Position
from omega_ai.trading.profiles import AggressiveTrader, NewbieTrader, ScalperTrader, StrategicTrader
from typing import Dict, List, Optional, Tuple, Union
from omega_ai.utils.redis_connection import RedisConnectionManager
from collections import deque
import uuid

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

# Initialize Redis connection
redis_manager = RedisConnectionManager()

logger = logging.getLogger(__name__)

@dataclass
class Position:
    """Trading position data model."""
    id: str
    direction: str  # "LONG" or "SHORT"
    entry_price: float
    size: float  # In BTC
    leverage: int
    entry_time: datetime
    entry_reason: str
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    exit_reason: Optional[str] = None
    take_profits: List[Dict[str, float]] = field(default_factory=list)
    stop_loss: Optional[float] = None
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0  # Add unrealized PnL field
    status: str = "OPEN"  # OPEN, CLOSED, LIQUIDATED

    def calculate_unrealized_pnl(self, current_price: float) -> Tuple[float, float]:
        """Calculate unrealized profit/loss in USD and percentage."""
        if self.direction == "LONG":
            pnl_pct = (current_price - self.entry_price) / self.entry_price * 100 * self.leverage
            pnl_usd = (current_price - self.entry_price) * self.size * self.leverage
        else:  # SHORT
            pnl_pct = (self.entry_price - current_price) / self.entry_price * 100 * self.leverage
            pnl_usd = (self.entry_price - current_price) * self.size * self.leverage
        
        return pnl_usd, pnl_pct

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        result = {
            "id": self.id,
            "direction": self.direction,
            "entry_price": self.entry_price,
            "size": self.size,
            "leverage": self.leverage,
            "entry_time": self.entry_time.isoformat(),
            "entry_reason": self.entry_reason,
            "exit_price": self.exit_price,
            "exit_time": self.exit_time.isoformat() if self.exit_time else None,
            "exit_reason": self.exit_reason,
            "take_profits": self.take_profits,
            "stop_loss": self.stop_loss,
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": self.unrealized_pnl,
            "status": self.status
        }
        return result

class ProfiledFuturesTrader(BtcFuturesTrader):
    """BTC Futures Trader that behaves according to a specific trader profile."""
    
    def __init__(self, 
                 profile_type: str = "strategic", 
                 initial_capital: float = 10000.0,
                 **kwargs):
        """Initialize trader with a specific psychological profile."""
        self._current_price = kwargs.get('btc_last_price', 1.0) if kwargs.get('btc_last_price', 1.0) > 0 else 1.0
        super().__init__(initial_capital=initial_capital, **kwargs)
        self.profile_type = profile_type
        self.positions: List[Position] = []
        self._last_valid_price = self._current_price
        self._price_update_time = None
        self._max_price_age = 60  # Maximum age of price data in seconds
        
        # Trading metrics
        self.total_trades: int = 0
        self.winning_trades: int = 0
        self.losing_trades: int = 0
        self.win_rate: float = 0.0
        
        self.state = {
            "emotional_state": "neutral",  # neutral, greedy, fearful
            "confidence": 0.5,  # 0.0 to 1.0
            "stress_level": 0.0,  # 0.0 to 1.0
            "consecutive_losses": 0,
            "consecutive_wins": 0
        }
        
        # Initialize profile and set risk parameters
        self._initialize_profile(profile_type, initial_capital)
        
        self.trade_history = []
        self.price_history = deque(maxlen=100)  # Keep last 100 prices
        self.current_position: Optional[Position] = None
        self.emotional_state = {
            "confidence": 0.5,
            "fear": 0.3,
            "greed": 0.3
        }
        
    def _initialize_profile(self, profile_type: str, initial_capital: float) -> None:
        """Initialize the trader profile with proper risk parameters."""
        # Set risk_per_trade based on profile type - JAH BLESSED VALUES
        if profile_type == "aggressive":
            self.risk_per_trade = 0.4  # 40% risk - RASTA FIRE
            self.max_leverage = 20    # High leverage
            self.patience = 0.3       # Low patience
            self.fomo_factor = 0.8    # High FOMO
            self.trend_follow_threshold = 0.5  # Responsive to short-term trends
            self.profile = AggressiveTrader(initial_capital)
            
        elif profile_type == "strategic":
            self.risk_per_trade = 0.2  # 20% risk - BALANCED DIVINE ENERGY
            self.max_leverage = 5     # Moderate leverage
            self.patience = 0.8       # High patience
            self.fomo_factor = 0.2    # Low FOMO
            self.trend_follow_threshold = 0.8  # Requires stronger trend confirmation
            self.profile = StrategicTrader(initial_capital)
            
        elif profile_type == "newbie":
            self.risk_per_trade = 0.3  # 30% risk - LEARNING THE PATH
            self.max_leverage = 50    # Excessive leverage
            self.patience = 0.2       # Very low patience
            self.fomo_factor = 0.9    # Extreme FOMO
            self.trend_follow_threshold = 0.3  # Easily affected by short-term movements
            self.profile = NewbieTrader(initial_capital)
            
        elif profile_type == "scalper":
            self.risk_per_trade = 0.2  # 20% risk - CALCULATED PRECISION
            self.max_leverage = 15    # Higher leverage for small moves
            self.patience = 0.1       # Ultra-low patience (scalpers exit quickly)
            self.fomo_factor = 0.4    # Moderate FOMO
            self.trend_follow_threshold = 0.1  # Doesn't care much about trends
            self.profile = ScalperTrader(initial_capital)
            
        else:
            self.risk_per_trade = 0.2  # Default values
            self.max_leverage = 5
            self.patience = 0.5
            self.fomo_factor = 0.5
            self.trend_follow_threshold = 0.5
            self.profile = StrategicTrader(initial_capital)
            
        # Ensure profile uses our risk parameters
        self.profile.risk_per_trade = self.risk_per_trade
        print(f"Initialized {self.profile_type.capitalize()} BTC Futures Trader with ${initial_capital:.2f}")
        
    @property
    def current_price(self) -> float:
        """Get the current price with validation."""
        if self._current_price <= 0:
            if self._last_valid_price > 0:
                return self._last_valid_price
            raise ValueError("No valid price available")
        
        # Check if price is too old
        if self._price_update_time:
            age = (datetime.now() - self._price_update_time).total_seconds()
            if age > self._max_price_age:
                if self._last_valid_price > 0:
                    return self._last_valid_price
                raise ValueError(f"Price data is too old ({age:.1f} seconds)")
        
        return self._current_price
    
    @current_price.setter
    def current_price(self, value: float) -> None:
        """Set the current price with validation."""
        if value <= 0:
            raise ValueError(f"Invalid price value: {value}")
        
        self._last_valid_price = self._current_price if self._current_price > 0 else value
        self._current_price = value
        self._price_update_time = datetime.now()
        
        # Update profile's price as well
        if hasattr(self, 'profile'):
            self.profile.update_price(value)
            
    def update_current_price(self) -> float:
        """Get latest BTC price from Redis with validation."""
        try:
            price_str = redis_manager.get("last_btc_price")
            if not price_str:
                raise ValueError("No price data in Redis")
                
            price = float(price_str)
            if price <= 0:
                raise ValueError(f"Invalid price from Redis: {price}")
                
            # Update both our price and profile's price
            self.current_price = price
            return price
            
        except Exception as e:
            print(f"{RED}❌ Error getting current price: {e}{RESET}")
            # Return last valid price if available, otherwise raise
            if self._last_valid_price > 0:
                return self._last_valid_price
            raise ValueError("No valid price available")
    
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
            pnl_usd, _ = pos.calculate_unrealized_pnl(price)
            if pnl_usd > 0:
                print(f"{GREEN}Position {pos.direction} showing profit: ${pnl_usd:.2f}{RESET}")
            elif pnl_usd < 0:
                print(f"{RED}Position {pos.direction} showing loss: ${pnl_usd:.2f}{RESET}")
    
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

    def open_position(self, direction: str, reason: str, leverage: int = 1, stop_loss_pct: float = None) -> Optional[Position]:
        """Open a new trading position."""
        if direction not in ["LONG", "SHORT"]:
            logger.error(f"Invalid position direction: {direction}")
            return None
            
        # Validate leverage
        if leverage <= 0 or leverage > self.max_leverage:
            raise ValueError(f"Invalid leverage value: {leverage}. Must be between 1 and {self.max_leverage}")

        try:
            # Calculate stop loss using provided percentage or default calculation
            if stop_loss_pct is not None:
                stop_loss = self.current_price * (1 - stop_loss_pct) if direction == "LONG" else self.current_price * (1 + stop_loss_pct)
            else:
                stop_loss = self._calculate_stop_loss(direction, self.current_price)

            # Create position
            position = Position(
                id=str(uuid.uuid4()),
                direction=direction,
                entry_price=self.current_price,
                size=self.capital * self.risk_per_trade,
                leverage=leverage,
                entry_time=datetime.now(timezone.utc),
                entry_reason=reason,
                stop_loss=stop_loss,
                take_profits=self._calculate_take_profit_levels(direction, self.current_price)
            )

            # Store position data
            self._store_position_in_redis(position)
            self.positions.append(position)
            
            # Log the trade
            logger.info(f"Opened {direction} position with {leverage}x leverage")
            logger.info(f"Entry Price: ${self.current_price:,.2f}")
            logger.info(f"Position Size: ${position.size:,.2f}")
            logger.info(f"Stop Loss: ${stop_loss:,.2f}")
            logger.info(f"Reason: {reason}")
            
            # Update state
            self._update_psychological_state()
            
            return position

        except Exception as e:
            logger.error(f"Error opening position: {e}")
            return None

    def _calculate_stop_loss(self, direction: str, entry_price: float) -> float:
        """Calculate appropriate stop-loss based on trader profile."""
        # Different profiles have different stop-loss strategies
        volatility_factor = 0.02  # Default 2% volatility assumption
        
        try:
            # Try to calculate volatility from recent price history
            if hasattr(self, 'price_history') and len(self.price_history) > 0:
                # Calculate simple volatility as standard deviation of returns
                prices = list(self.price_history)[-20:]  # Use last 20 prices
                returns = [(prices[i] - prices[i-1])/prices[i-1] for i in range(1, len(prices))]
                if returns:
                    std_dev = (sum((r - sum(returns)/len(returns))**2 for r in returns) / len(returns))**0.5
                    volatility_factor = max(0.005, min(0.05, std_dev))  # Cap between 0.5% and 5%
        except Exception as e:
            logger.warning(f"Error calculating volatility: {e}. Using default value.")
        
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

    def _store_position_in_redis(self, position: Position) -> None:
        """Store position data in Redis for analysis."""
        try:
            # Convert position to serializable dictionary
            position_data = position.to_dict()
            position_data["trader_profile"] = self.profile_type
            
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

    def _update_position_pnl(self, position: Position) -> None:
        """Update position's PnL."""
        if not self.current_price:
            return

        # Calculate unrealized PnL
        pnl_usd, pnl_pct = position.calculate_unrealized_pnl(self.current_price)
        position.unrealized_pnl = pnl_usd  # Update the position's unrealized PnL

        # Add divine PnL status with cosmic colors
        if pnl_usd > 0:
            print(f"{GREEN}Position {position.direction} showing profit: ${pnl_usd:.2f}{RESET}")
        elif pnl_usd < 0:
            print(f"{RED}Position {position.direction} showing loss: ${pnl_usd:.2f}{RESET}")

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
        if not position.take_profits:
            return False
            
        for tp in position.take_profits:
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

    def _close_position(self, position: Position, reason: str) -> None:
        """Close a position and update PnL."""
        position.exit_price = self.current_price
        position.exit_time = datetime.now(timezone.utc)  # Use timezone-aware datetime
        position.exit_reason = reason
        position.status = "CLOSED"
        
        # Calculate PnL
        price_diff = position.exit_price - position.entry_price if position.direction == "LONG" else position.entry_price - position.exit_price
        pnl = price_diff * position.size * position.leverage
        roi_pct = (pnl / (position.size * position.entry_price)) * 100
        
        # Update position PnL
        position.realized_pnl = pnl
        
        # Update trader's capital
        self.capital += pnl
        
        # Print position summary with color coding
        color = '\x1b[92m' if pnl >= 0 else '\x1b[91m'  # Green for profit, Red for loss
        print(f"\n{color}🔒 CLOSED {position.direction} POSITION with {position.leverage}x leverage")
        print(f"Entry Price: ${position.entry_price:,.2f}")
        print(f"Exit Price: ${position.exit_price:,.2f}")
        print(f"P&L: ${pnl:,.2f} ({roi_pct:+.2f}%)")
        print(f"Reason: {reason}\x1b[0m")
        
        # Print position lifetime
        lifetime_minutes = (position.exit_time - position.entry_time).total_seconds() / 60
        print(f"Position Lifetime: {lifetime_minutes:.1f} minutes")
        
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
            print(f"{GREEN}Win rate updated: {self.win_rate:.2%}{RESET}")
        
        # Store trade result in trade history
        trade_result = {
            "direction": position.direction,
            "entry_price": position.entry_price,
            "exit_price": position.exit_price,
            "entry_time": position.entry_time,
            "exit_time": position.exit_time,
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
            
            # Add to local trade history
            if not hasattr(self, 'trade_history'):
                self.trade_history = []
            self.trade_history.append(trade_data)
            
        except Exception as e:
            # Don't let Redis errors disrupt trading
            print(f"{YELLOW}Redis error storing trade result: {e}{RESET}")

    def calculate_sharpe_ratio(self) -> float:
        """Calculate the Sharpe ratio for the trader's performance."""
        if not hasattr(self, 'trade_history') or not self.trade_history:
            return 0.0
            
        # Get returns from trade history
        returns = []
        if isinstance(self.trade_history, list):
            returns = [trade.get("pnl", 0.0) / trade.get("entry_value", 1.0) * 100 for trade in self.trade_history]
        else:
            # Handle TradeHistory object
            for trade in self.trade_history.trades:
                if hasattr(trade, 'realized_pnl') and hasattr(trade, 'entry_price') and hasattr(trade, 'size'):
                    entry_value = trade.entry_price * trade.size
                    returns.append((trade.realized_pnl / entry_value) * 100)
            
        if not returns:
            return 0.0
            
        # Calculate average return and standard deviation
        avg_return = sum(returns) / len(returns)
        std_dev = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
        
        # Risk-free rate assumed to be 0% for simplicity
        risk_free_rate = 0.0
        
        # Calculate Sharpe ratio
        if std_dev == 0:
            return 0.0
            
        sharpe = (avg_return - risk_free_rate) / std_dev
        return sharpe

    def calculate_max_drawdown(self) -> float:
        """Calculate the maximum drawdown from peak capital."""
        if not hasattr(self, 'trade_history') or not self.trade_history:
            return 0.0
            
        # Track peak capital and current drawdown
        peak_capital = self.initial_capital
        max_drawdown = 0.0
        current_capital = self.initial_capital
        
        # Get trades from trade history
        trades = []
        if isinstance(self.trade_history, list):
            trades = self.trade_history
        else:
            # Handle TradeHistory object
            trades = self.trade_history.trades
            
        for trade in trades:
            if isinstance(trade, dict):
                pnl = trade.get("pnl", 0.0)
            else:
                # Get PnL from trade object
                pnl = trade.realized_pnl if hasattr(trade, 'realized_pnl') else 0.0
                
            current_capital += pnl
            peak_capital = max(peak_capital, current_capital)
            drawdown = (peak_capital - current_capital) / peak_capital
            max_drawdown = max(max_drawdown, drawdown)
            
        return max_drawdown

    @property
    def total_pnl(self) -> float:
        """Calculate total profit/loss from all trades."""
        if not hasattr(self, 'trade_history') or not self.trade_history:
            return 0.0
            
        # Get trades from trade history
        trades = []
        if isinstance(self.trade_history, list):
            trades = self.trade_history
        else:
            # Handle TradeHistory object
            trades = self.trade_history.trades
            
        total = 0.0
        for trade in trades:
            if isinstance(trade, dict):
                total += trade.get("pnl", 0.0)
            else:
                # Get PnL from trade object
                total += trade.realized_pnl if hasattr(trade, 'realized_pnl') else 0.0
                
        return total