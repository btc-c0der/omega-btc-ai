#!/usr/bin/env python3

"""
Base trader profile class for OmegaBTC AI

This module provides the foundation for all trader profiles in the system.
"""

from typing import Dict, List, Tuple, Optional
from omega_ai.utils.redis_manager import RedisManager
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
    
    def __init__(self, initial_capital: float = 10000.0, name: str = "", redis_manager: Optional[RedisManager] = None):
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.name = name or self.__class__.__name__
        self.redis = redis_manager or RedisManager()
        self.state = TraderState()
        self.analyzer = TradingAnalyzer()
        
        # Initialize trader state in Redis
        self._initialize_state()
        
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if we should enter a trade based on market context."""
        raise NotImplementedError("Subclasses must implement should_enter_trade")
        
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on risk appetite and capital."""
        raise NotImplementedError("Subclasses must implement determine_position_size")
        
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Set stop loss level based on risk management rules."""
        raise NotImplementedError("Subclasses must implement set_stop_loss")
        
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set take profit targets based on risk/reward ratio."""
        raise NotImplementedError("Subclasses must implement set_take_profit")
        
    def process_trade_result(self, result: float, trade_duration: float) -> None:
        """Process the result of a completed trade."""
        # Update capital
        self.capital += result
        
        # Update state
        if result > 0:
            self.state.consecutive_wins += 1
            self.state.consecutive_losses = 0
            self.state.winning_trades += 1
        else:
            self.state.consecutive_losses += 1
            self.state.consecutive_wins = 0
            self.state.losing_trades += 1
            
        self.state.total_trades += 1
        self.state.total_pnl += result
        
        # Calculate drawdown
        drawdown = (self.initial_capital - self.capital) / self.initial_capital
        self.state.drawdown = max(self.state.drawdown, drawdown)
        
        # Update emotional state
        self.state.update_emotional_state(result, self.analyzer.random)
        
        # Update Redis state
        self._update_redis_state()
        
    def print_status(self) -> None:
        """Print current trader status with color formatting."""
        win_rate = (self.state.winning_trades / self.state.total_trades * 100 
                   if self.state.total_trades > 0 else 0)
                   
        pnl_color = GREEN if self.state.total_pnl >= 0 else RED
        state_color = self._get_state_color()
        risk_color = self._format_risk_level(self.state.risk_appetite)
        confidence_color = self._format_confidence_level(self.state.confidence)
        
        print(f"\n{BOLD}{WHITE}Trader Profile: {self.name}{RESET}")
        print(f"Capital: ${self.capital:,.2f}")
        print(f"PnL: {pnl_color}${self.state.total_pnl:,.2f}{RESET}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Total Trades: {self.state.total_trades}")
        print(f"Consecutive Wins: {self.state.consecutive_wins}")
        print(f"Consecutive Losses: {self.state.consecutive_losses}")
        print(f"Max Drawdown: {self.state.drawdown*100:.1f}%")
        print(f"Emotional State: {state_color}{self.state.emotional_state}{RESET}")
        print(f"Risk Level: {risk_color}")
        print(f"Confidence: {confidence_color}\n")
        
    def _get_state_color(self) -> str:
        """Get color code for emotional state."""
        state_colors = {
            "neutral": WHITE,
            "greedy": RED,
            "fearful": YELLOW,
            "excited": GREEN,
            "cautious": CYAN
        }
        return state_colors.get(self.state.emotional_state, WHITE)
        
    def _format_risk_level(self, risk: float) -> str:
        """Format risk level with color coding."""
        if risk < 0.3:
            return f"{BLUE}Low Risk ({risk:.2f}){RESET}"
        elif risk < 0.7:
            return f"{YELLOW}Medium Risk ({risk:.2f}){RESET}"
        else:
            return f"{RED}High Risk ({risk:.2f}){RESET}"
            
    def _format_confidence_level(self, confidence: float) -> str:
        """Format confidence level with color coding."""
        if confidence < 0.3:
            return f"{RED}Low Confidence ({confidence:.2f}){RESET}"
        elif confidence < 0.7:
            return f"{YELLOW}Medium Confidence ({confidence:.2f}){RESET}"
        else:
            return f"{GREEN}High Confidence ({confidence:.2f}){RESET}"
            
    def _initialize_analyzer(self):
        """Initialize trading analyzer component."""
        self.analyzer = TradingAnalyzer()
        
    def _initialize_state(self):
        """Initialize trader state in Redis."""
        state_data = {
            "name": self.name,
            "capital": self.capital,
            "pnl": self.state.total_pnl,
            "win_rate": (self.state.winning_trades / self.state.total_trades * 100 
                        if self.state.total_trades > 0 else 0),
            "trades": self.state.total_trades,
            "emotional_state": self.state.emotional_state,
            "confidence": self.state.confidence,
            "risk_level": self.state.risk_appetite
        }
        
        self.redis.set_with_validation(f"omega:live_trader:{self.name}", state_data)
        
    def _update_redis_state(self):
        """Update trader state in Redis."""
        self._initialize_state()  # Reuse initialization logic for updates

BaseTrader = TraderProfile  # Create alias for backward compatibility