#!/usr/bin/env python3

"""
Base Trader Profile for OmegaBTC AI

This module provides the base class and common functionality for all trader profiles.
It implements the core interfaces and shared behavior that all trader profiles must follow.
"""

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from abc import ABC, abstractmethod

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

@dataclass
class PsychologicalState:
    """Represents the current psychological state of a trader."""
    emotional_state: str = "neutral"  # neutral, greedy, fearful
    confidence_level: float = 0.5  # 0.0 to 1.0
    stress_level: float = 0.5  # 0.0 to 1.0
    risk_appetite: float = 0.5  # 0.0 to 1.0
    consecutive_wins: int = 0
    consecutive_losses: int = 0
    recent_trades: List[Dict] = field(default_factory=list)  # List of recent trade results
    
    def __post_init__(self):
        if self.recent_trades is None:
            self.recent_trades = []

@dataclass
class RiskParameters:
    """Risk management parameters for a trader profile."""
    max_risk_per_trade: float  # Maximum risk per trade as percentage of capital
    base_leverage: float      # Base leverage to use
    max_leverage: float       # Maximum allowed leverage
    min_risk_reward_ratio: float  # Minimum risk:reward ratio required
    position_sizing_volatility_factor: float  # Factor to adjust position size based on volatility
    stop_loss_multiplier: float  # Multiplier for stop loss distance
    take_profit_multiplier: float  # Multiplier for take profit distance

class TraderProfile(ABC):
    """Base class for all trader profiles."""
    
    def __init__(self, initial_capital: float = 10000.0, btc_last_price: float = 0.0):
        """Initialize the trader profile with common attributes."""
        self.name = "Base Trader"  # Default name, should be overridden by subclasses
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.positions: List[Dict] = []
        self.trade_history: List[Dict] = []
        self.state = PsychologicalState()
        self.risk_params = self._get_risk_parameters()
        
        # Risk management
        self._risk_per_trade: float = 0.02  # Default 2% risk per trade
        
        # Performance tracking
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.win_rate = 0.0
        self.avg_trade_duration = 0.0
        self.max_drawdown = 0.0
        self.current_drawdown = 0.0
        
        # Market analysis state
        self.last_analysis_time = None
        self.market_regime = "neutral"
        self.trend_strength = 0.0
        self.volatility = 0.0
        
        # Initialize current price with a valid value
        self._current_price = btc_last_price if btc_last_price > 0 else 1.0
        self._last_valid_price = self._current_price
        self._price_update_time = None
        self._max_price_age = 300  # Max age in seconds for a price to be considered valid
    
    @property
    def risk_per_trade(self) -> float:
        """Get the risk per trade percentage."""
        return self._risk_per_trade
        
    @risk_per_trade.setter
    def risk_per_trade(self, value: float) -> None:
        """Set the risk per trade percentage with validation."""
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Risk per trade must be between 0 and 1, got {value}")
        self._risk_per_trade = value
    
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
            if self._last_valid_price > 0:
                self._current_price = self._last_valid_price
                return
            raise ValueError(f"Invalid price value: {value}")
        
        self._last_valid_price = self._current_price if self._current_price > 0 else value
        self._current_price = value
        self._price_update_time = datetime.now()
    
    def update_price(self, price: float) -> None:
        """Update the current price with validation."""
        try:
            self.current_price = price  # This will use the setter with validation
            self._update_positions_pnl()  # Update PnL for all positions
        except ValueError as e:
            print(f"{RED}❌ Price update failed: {e}{RESET}")
            
    def _update_positions_pnl(self) -> None:
        """Update unrealized PnL for all positions."""
        try:
            price = self.current_price  # This will use the getter with validation
            for position in self.positions:
                if "entry_price" not in position or position["entry_price"] <= 0:
                    continue
                    
                price_diff = price - position["entry_price"]
                if position["direction"] == "SHORT":
                    price_diff = -price_diff
                    
                position["unrealized_pnl"] = (price_diff / position["entry_price"]) * position["size"] * position.get("leverage", 1.0)
        except ValueError as e:
            print(f"{YELLOW}⚠️ Could not update positions PnL: {e}{RESET}")
    
    @abstractmethod
    def _get_risk_parameters(self) -> RiskParameters:
        """Get risk parameters specific to this profile."""
        pass
    
    @abstractmethod
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if a trade should be entered based on market context."""
        pass
    
    @abstractmethod
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on risk parameters and market conditions."""
        pass
    
    @abstractmethod
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Set stop loss level based on profile's risk management rules."""
        pass
    
    @abstractmethod
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set take profit levels based on profile's profit-taking strategy."""
        pass
    
    def process_trade_result(self, result: float, trade_duration: float) -> None:
        """Process the result of a completed trade."""
        self.total_trades += 1
        self.avg_trade_duration = (self.avg_trade_duration * (self.total_trades - 1) + trade_duration) / self.total_trades
        
        # Update trade history
        self.state.recent_trades.append({
            "result": result,
            "duration": trade_duration,
            "price": self.current_price
        })
        
        # Keep only last 10 trades
        if len(self.state.recent_trades) > 10:
            self.state.recent_trades.pop(0)
        
        # Update capital and track performance
        self.capital += result
        if result > 0:
            self.winning_trades += 1
            self.state.consecutive_wins += 1
            self.state.consecutive_losses = 0
            self.state.confidence_level = min(1.0, self.state.confidence_level + 0.1)
            self.state.stress_level = max(0.0, self.state.stress_level - 0.1)
            self._update_psychological_state(True)
        else:
            self.losing_trades += 1
            self.state.consecutive_losses += 1
            self.state.consecutive_wins = 0
            self.state.confidence_level = max(0.0, self.state.confidence_level - 0.1)
            self.state.stress_level = min(1.0, self.state.stress_level + 0.1)
            self._update_psychological_state(False)
        
        # Update win rate
        self.win_rate = self.winning_trades / self.total_trades if self.total_trades > 0 else 0.0
        
        # Update drawdown
        self._update_drawdown()
    
    def _update_psychological_state(self, is_win: bool) -> None:
        """Update psychological state based on trade outcome."""
        if is_win:
            if self.state.consecutive_wins >= 3:
                self.state.emotional_state = "greedy"
        else:
            if self.state.consecutive_losses >= 2:
                self.state.emotional_state = "fearful"
        
        # Return to neutral state if no strong emotions
        if self.state.consecutive_wins < 3 and self.state.consecutive_losses < 3:
            self.state.emotional_state = "neutral"
    
    def _update_drawdown(self) -> None:
        """Update drawdown calculations."""
        if self.capital > self.initial_capital:
            self.initial_capital = self.capital
            self.current_drawdown = 0.0
        else:
            self.current_drawdown = (self.initial_capital - self.capital) / self.initial_capital
            self.max_drawdown = max(self.max_drawdown, self.current_drawdown)
    
    def print_status(self) -> None:
        """Print current status of the trader profile."""
        print(f"\n{CYAN}=== {self.name} Status ==={RESET}")
        print(f"Capital: ${self.capital:,.2f}")
        print(f"Win Rate: {self.win_rate:.2%}")
        print(f"Total Trades: {self.total_trades}")
        print(f"Current Drawdown: {self.current_drawdown:.2%}")
        print(f"Max Drawdown: {self.max_drawdown:.2%}")
        print(f"Average Trade Duration: {self.avg_trade_duration:.1f} minutes")
        
        # Print psychological state
        print(f"\n{GREEN}Psychological State:{RESET}")
        print(f"Emotional State: {self.state.emotional_state}")
        print(f"Confidence: {self.state.confidence_level:.2f}")
        print(f"Stress Level: {self.state.stress_level:.2f}")
        
        # Print risk parameters
        print(f"\n{YELLOW}Risk Parameters:{RESET}")
        print(f"Max Risk per Trade: {self.risk_params.max_risk_per_trade:.2%}")
        print(f"Base Leverage: {self.risk_params.base_leverage:.1f}x")
        print(f"Max Leverage: {self.risk_params.max_leverage:.1f}x")
        print(f"Min Risk:Reward: {self.risk_params.min_risk_reward_ratio:.1f}") 