#!/usr/bin/env python3

"""
Base trader profile class for OmegaBTC AI

This module provides the foundation for all trader profiles in the system.
"""

import redis
from typing import Dict, List, Tuple, Optional

from omega_ai.trading.trading_analyzer import TradingAnalyzer

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
RED_BG = "\033[41m"

class TraderState:
    """Tracks the psychological and performance state of a trader."""
    def __init__(self):
        self.emotional_state = "neutral"  # excited, fearful, greedy, neutral, etc.
        self.confidence = 0.5             # 0.0-1.0 scale
        self.risk_appetite = 0.5          # 0.0-1.0 scale
        self.consecutive_losses = 0
        self.consecutive_wins = 0
        self.drawdown = 0.0
        
        # Performance metrics
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0
    
    def update_emotional_state(self, trade_result: float, random_module) -> None:
        """Update emotional state based on recent trade results."""
        prev_state = self.emotional_state
        
        # Adjust confidence based on result
        if (trade_result > 0):
            # Winning trade increases confidence
            self.confidence = min(1.0, self.confidence + 0.1)
            
            # After consecutive wins, may become overconfident/greedy
            if (self.consecutive_wins >= 3):
                greed_prob = 0.3 + (self.consecutive_wins - 3) * 0.1
                if (random_module.random() < greed_prob):
                    self.emotional_state = "greedy"
                    self.risk_appetite = min(1.0, self.risk_appetite + 0.15)
                    return
            
            # Normal state transition after win
            if (prev_state == "fearful"):
                self.emotional_state = "neutral"  # Fear -> Neutral
                self.risk_appetite += 0.1
            elif (prev_state == "neutral"):
                # Small chance to become greedy after a win
                if (random_module.random() < 0.2):
                    self.emotional_state = "greedy" 
                    self.risk_appetite += 0.15
        else:
            # Losing trade decreases confidence
            self.confidence = max(0.1, self.confidence - 0.15)
            
            # After consecutive losses, likely to become fearful
            if (self.consecutive_losses >= 2):
                fear_prob = 0.3 + (self.consecutive_losses - 2) * 0.15
                if (random_module.random() < fear_prob):
                    self.emotional_state = "fearful"
                    self.risk_appetite = max(0.1, self.risk_appetite - 0.2)
                    return
            
            # Normal state transition after loss
            if prev_state == "greedy":
                self.emotional_state = "neutral"  # Greed -> Neutral
                self.risk_appetite -= 0.1
            elif prev_state == "neutral":
                # Chance to become fearful after a loss
                if random_module.random() < 0.3:
                    self.emotional_state = "fearful"
                    self.risk_appetite -= 0.15
        
        # Constrain risk appetite
        self.risk_appetite = max(0.1, min(1.0, self.risk_appetite))


class TraderProfile:
    """Base class for trader profile simulations."""
    
    def __init__(self, initial_capital: float = 10000.0, name: str = ""):
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.name = name or self.__class__.__name__
        self.type = self.__class__.__name__.lower().replace("trader", "")
        
        # Common attributes
        self.base_leverage = 5.0
        self.base_stop_pct = 0.03  # 3% base stop loss
        self.min_retest_waiting_period = 3600  # 1 hour in seconds
        
        # Initialize Redis connection
        self.redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        
        # Key Fibonacci levels
        self.key_fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618]
        
        # Discipline metrics tracking
        self.discipline_metrics = {
            "rules_followed": 0,
            "rules_broken": 0,
            "entries_skipped": 0,
            "targets_reached": 0,
            "early_exits": 0
        }
        
        # Initialize analyzer and state
        self.analyzer = self._initialize_analyzer()
        self.state = self._initialize_state()
        
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if the trader should enter a trade."""
        raise NotImplementedError("Subclasses must implement this")
        
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on risk parameters and emotional state."""
        raise NotImplementedError("Subclasses must implement this")
    
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Determine stop-loss level based on trading style."""
        raise NotImplementedError("Subclasses must implement this")
    
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Determine take-profit levels based on trading style."""
        raise NotImplementedError("Subclasses must implement this")
    
    def process_trade_result(self, result: float, trade_duration: float) -> None:
        """Process the outcome of a trade and update the trader state."""
        # Update capital
        self.capital += result
        
        # Update trade statistics
        self.state.total_trades += 1
        if result > 0:
            self.state.winning_trades += 1
            self.state.consecutive_wins += 1
            self.state.consecutive_losses = 0
        else:
            self.state.losing_trades += 1
            self.state.consecutive_losses += 1
            self.state.consecutive_wins = 0
        
        # Update emotional state
        self.state.total_pnl += result
        import random
        self.state.update_emotional_state(result, random)
        
        # Calculate drawdown
        high_watermark = max(self.initial_capital, self.capital)
        current_drawdown = (high_watermark - self.capital) / high_watermark * 100
        self.state.drawdown = max(self.state.drawdown, current_drawdown)
        
    def print_status(self) -> None:
        """Print current trader status and performance metrics."""
        profit = self.capital - self.initial_capital
        profit_pct = (profit / self.initial_capital) * 100
        
        if profit >= 0:
            profit_text = f"{GREEN}+${profit:.2f} ({profit_pct:.1f}%){RESET}"
        else:
            profit_text = f"{RED}-${abs(profit):.2f} ({profit_pct:.1f}%){RESET}"
        
        win_rate = self.state.winning_trades / max(1, self.state.total_trades) * 100
        
        # Emotional state color coding
        state_colors = {
            "neutral": WHITE,
            "greedy": YELLOW,
            "fearful": RED,
            "excited": GREEN,
            "euphoric": MAGENTA,
            "fomo": YELLOW,
            "panic": RED,
            "revenge": RED,
            "fud": YELLOW,
            "hype": GREEN
        }
        emotion_color = state_colors.get(self.state.emotional_state, WHITE)
        
        print(f"\n{MAGENTA}══════════════════════════════════════{RESET}")
        print(f"{CYAN}{BOLD}{self.name} Status Report{RESET}")
        print(f"{MAGENTA}══════════════════════════════════════{RESET}")
        print(f"Capital: ${self.capital:.2f} | P&L: {profit_text}")
        print(f"Trades: {self.state.total_trades} | Win Rate: {win_rate:.1f}%")
        print(f"Emotional State: {emotion_color}{self.state.emotional_state}{RESET}")
        print(f"Risk Appetite: {self._format_risk_level(self.state.risk_appetite)}")
        print(f"Confidence: {self._format_confidence_level(self.state.confidence)}")
        print(f"Max Drawdown: {RED}{self.state.drawdown:.1f}%{RESET}")
        
    def _format_risk_level(self, risk: float) -> str:
        """Format risk level with color coding."""
        if risk < 0.3:
            return f"{BLUE}Conservative ({risk:.1f}){RESET}"
        elif risk < 0.7:
            return f"{WHITE}Moderate ({risk:.1f}){RESET}"
        else:
            return f"{RED}Aggressive ({risk:.1f}){RESET}"
    
    def _format_confidence_level(self, confidence: float) -> str:
        """Format confidence level with color coding."""
        if confidence < 0.3:
            return f"{RED}Low ({confidence:.1f}){RESET}"
        elif confidence < 0.7:
            return f"{WHITE}Moderate ({confidence:.1f}){RESET}"
        else:
            return f"{GREEN}High ({confidence:.1f}){RESET}"

    def _initialize_analyzer(self):
        """Initialize market analyzer for this trader."""
        from omega_ai.trading.trading_analyzer import TradingAnalyzer
        return TradingAnalyzer()

    def _initialize_state(self):
        """Initialize trader state object."""
        return TraderState()  # Just return an instance of the existing class

BaseTrader = TraderProfile  # Create alias for backward compatibility