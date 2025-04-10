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
Base trader profile class for OmegaBTC AI Bot Farm

This module provides the foundation for all trader profiles in the containerized bot system.
"""

from typing import Dict, List, Tuple, Optional
import logging
from src.omega_bot_farm.utils.redis_client import RedisClient

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

# Configure logging
logger = logging.getLogger("trader_base_b0t")

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
    """Base class for trader profile in containerized environment."""
    
    def __init__(self, initial_capital: float = 10000.0, name: str = "", redis_client: Optional[RedisClient] = None):
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.name = name or self.__class__.__name__
        self.redis = redis_client or RedisClient()
        self.state = TraderState()
        
        # Placeholder for trading analyzer - will be imported properly in subclasses
        self.analyzer = None
        
        # Logger for containerized environment
        self.logger = logging.getLogger(f"trader.{self.name}")
        
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
        
        # Log the trade result for the containerized environment
        self.logger.info(f"Trade completed: {result:.2f} USD, duration: {trade_duration:.2f} hours")
        
    def get_status_dict(self) -> Dict:
        """Get trader status as a dictionary for API and Discord integration."""
        win_rate = (self.state.winning_trades / self.state.total_trades * 100 
                   if self.state.total_trades > 0 else 0)
                   
        return {
            "name": self.name,
            "capital": self.capital,
            "initial_capital": self.initial_capital,
            "pnl": self.state.total_pnl,
            "win_rate": win_rate,
            "total_trades": self.state.total_trades,
            "winning_trades": self.state.winning_trades,
            "losing_trades": self.state.losing_trades,
            "consecutive_wins": self.state.consecutive_wins,
            "consecutive_losses": self.state.consecutive_losses,
            "max_drawdown": self.state.drawdown * 100,
            "emotional_state": self.state.emotional_state,
            "risk_appetite": self.state.risk_appetite,
            "confidence": self.state.confidence
        }
        
    def print_status(self) -> None:
        """Print current trader status with color formatting."""
        win_rate = (self.state.winning_trades / self.state.total_trades * 100 
                   if self.state.total_trades > 0 else 0)
                   
        pnl_color = GREEN if self.state.total_pnl >= 0 else RED
        state_color = self._get_state_color()
        risk_color = self._format_risk_level(self.state.risk_appetite)
        confidence_color = self._format_confidence_level(self.state.confidence)
        
        self.logger.info(f"Trader Status: {self.name}")
        self.logger.info(f"Capital: ${self.capital:,.2f}")
        self.logger.info(f"PnL: ${self.state.total_pnl:,.2f}")
        self.logger.info(f"Win Rate: {win_rate:.1f}%")
        self.logger.info(f"Emotional State: {self.state.emotional_state}")
        
        # Also print to console for debugging/development
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
        # This will be implemented in subclasses that import the specific analyzer
        pass
        
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
        
        self.redis.set(f"omega:bot:{self.name}", state_data)
        
    def _update_redis_state(self):
        """Update trader state in Redis."""
        self._initialize_state()  # Reuse initialization logic for updates

# Aliases for backward compatibility
BaseTrader = TraderProfile
BaseBotTrader = TraderProfile 