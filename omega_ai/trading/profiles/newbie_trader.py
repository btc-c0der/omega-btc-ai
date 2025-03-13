#!/usr/bin/env python3

"""
NewbieTrader Profile for OmegaBTC AI

This module simulates an inexperienced trader who follows social media hype,
uses excessive leverage, and exhibits classic novice trading behaviors.
"""

import random
from typing import Dict, List, Tuple, Optional

from omega_ai.trading.trader_base import (
    TraderProfile, 
    RESET, GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, WHITE, BOLD, RED_BG
)

class NewbieTrader(TraderProfile):
    """A newbie BTC futures trader using excessive leverage and driven by social media hype."""
    
    def __init__(self, initial_capital: float = 10000.0):
        super().__init__(initial_capital, name="YOLO Crypto Influencer Follower")
        self.base_leverage = 50        # Base leverage (will scale up to 100x)
        self.min_risk_per_trade = 0.20  # 20% of capital at risk per trade
        self.max_risk_per_trade = 0.50  # Up to 50% of capital at risk
        
        # Social media and hype parameters
        self.hype_threshold = 0.3     # Threshold for entering based on "hype"
        self.fud_threshold = 0.4      # Threshold for entering based on "FUD"
        self.influencer_trust = 0.8   # High trust in social media influencers
        
        # Psychological traits
        self.state.risk_appetite = 0.9    # Extremely high risk appetite
        self.state.confidence = 0.9       # Overconfident despite inexperience
        self.state.emotional_state = "euphoric"  # Starts overly optimistic
        
        # Performance tracking
        self.fomo_trades = 0
        self.panic_sells = 0
        self.liquidation_events = 0
        self.near_liquidations = 0
        self.max_consecutive_losses = 0
        
        # Additional emotional states beyond the base trader
        self.emotional_states = ["euphoric", "fomo", "panic", "revenge", "fud", "hype", "neutral"]
        
        print(f"{RED}Initialized {self.name} with ${initial_capital:.2f} 🚀🌕{RESET}")
    
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if the trader should enter a trade based on social media hype and emotions."""
        price = market_context.get("price", 0)
        if price <= 0:
            return False, "No price data", "", 0
        
        # Simulate social media sentiment (random generation)
        social_sentiment = random.random()  # 0-1 score
        btc_trending = random.random() > 0.5  # Is BTC trending on social media?
        recent_price_direction = market_context.get("recent_change", 0)
        
        # Calculate current leverage based on emotional state (extremely high)
        current_leverage = self._calculate_current_leverage()
        
        # Signal variables
        entry_signal = False
        direction = ""
        reason = ""
        
        # Newbies tend to buy when price is already going up (FOMO)
        if recent_price_direction > 0 and social_sentiment > self.hype_threshold:
            entry_signal = True
            direction = "LONG"
            reason = f"🚀 PRICE GO UP! Social media bullish ({social_sentiment:.2f})"
            self.fomo_trades += 1
        
        # Or they might short when there's extreme FUD
        elif recent_price_direction < 0 and social_sentiment < self.fud_threshold:
            entry_signal = True
            direction = "SHORT"
            reason = f"💩 PRICE DUMPING! Social media bearish ({social_sentiment:.2f})"
        
        # Random "influencer tip" entries
        elif random.random() < self.influencer_trust * 0.3:  # 30% chance of following random tips
            entry_signal = True
            direction = "LONG" if random.random() > 0.4 else "SHORT"  # Slight bias toward long
            influencer = random.choice(["CryptoGuru", "BTCWhale", "MoonboyCapital", "LaserEyes2021"])
            reason = f"💯 FOLLOWING {influencer}'s *guaranteed* trade signal!"
        
        # Revenge trading after losses
        if self.state.consecutive_losses >= 2 and random.random() < 0.8:
            entry_signal = True
            # Often doubles down on the same direction that lost
            direction = "LONG" if self.state.emotional_state == "revenge" and random.random() > 0.3 else "SHORT"
            reason = f"😤 REVENGE TRADE to recover {self.state.consecutive_losses} losses!"
            self.state.emotional_state = "revenge"
        
        # FOMO on market volatility
        if market_context.get("recent_volatility", 0) > 500 and random.random() < 0.7:
            entry_signal = True
            direction = "LONG" if recent_price_direction > 0 else "SHORT"
            reason = f"⚡ HIGH VOLATILITY OPPORTUNITY! Can't miss this move!"
            self.state.emotional_state = "fomo"
        
        return entry_signal, direction, reason, current_leverage
    
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on emotional state (typically way too large)."""
        # Base risk percentage varies with emotional state
        if self.state.emotional_state in ["fomo", "euphoric", "revenge"]:
            risk_pct = self.max_risk_per_trade  # Maximum risk when FOMO or revenge trading
        elif self.state.emotional_state == "panic":
            risk_pct = self.min_risk_per_trade * 0.5  # Reduced size when panicking
        else:
            risk_pct = self.min_risk_per_trade
        
        # Impulsively increase position size after wins (dangerous behavior)
        if self.state.consecutive_wins > 0:
            # Dramatically size up after any win
            risk_pct *= (1 + self.state.consecutive_wins * 0.2)
        
        # Nearly always uses full account leverage
        leverage = self._calculate_current_leverage()
        
        # Calculate position size in BTC - often ignores proper risk calculation
        position_size = (self.capital * risk_pct) / entry_price
        
        # Apply full leverage
        position_size *= leverage
        
        # Don't account properly for potential drawdown (typically exceeds safe levels)
        liquidation_risk = self._calculate_liquidation_risk(direction, entry_price, position_size, leverage)
        if liquidation_risk > 0.7 and random.random() < 0.3:
            # Sometimes reduces size if liquidation risk is extreme (but not always)
            position_size *= 0.7
            print(f"{YELLOW}Reduced size due to extreme liquidation risk ({liquidation_risk:.2f}){RESET}")
        
        return position_size
    
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Determine stop-loss level (typically very loose or non-existent)."""
        # 30% chance of setting no real stop (will cause liquidation instead)
        if random.random() < 0.3:
            # Set stop at liquidation level (effectively no stop)
            liquidation_pct = 1 / self._calculate_current_leverage()
            if direction == "LONG":
                return entry_price * (1 - liquidation_pct * 0.95)  # Just above liquidation
            else:
                return entry_price * (1 + liquidation_pct * 0.95)  # Just above liquidation
        
        # Otherwise set a very loose stop
        stop_pct = random.uniform(0.05, 0.15)  # 5-15% stop (extremely wide)
        
        if direction == "LONG":
            stop_price = entry_price * (1 - stop_pct)
        else:  # SHORT
            stop_price = entry_price * (1 + stop_pct)
        
        return stop_price
    
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set unrealistic take-profit targets."""
        # Calculate risk in dollars
        risk = abs(entry_price - stop_loss)
        
        # Often sets unrealistic profit targets (10x, 25x, 100x)
        # Newbies love to dream about 10x, 100x returns
        if direction == "LONG":
            tp1_price = entry_price * 1.10  # +10%
            tp2_price = entry_price * 1.25  # +25%
            tp3_price = entry_price * 2.0   # +100%
        else:  # SHORT
            tp1_price = entry_price * 0.90  # -10%
            tp2_price = entry_price * 0.75  # -25%
            tp3_price = entry_price * 0.5   # -50%
        
        # Unrealistic distribution - mostly focused on the huge wins
        take_profits = [
            {"price": tp1_price, "percentage": 0.2, "hit": False},
            {"price": tp2_price, "percentage": 0.3, "hit": False},
            {"price": tp3_price, "percentage": 0.5, "hit": False}  # 50% of position at the 100% gain target
        ]
        
        return take_profits
    
    def process_trade_result(self, result: float, trade_duration: float) -> None:
        """Process the outcome with extreme emotional responses to wins/losses."""
        # Check for liquidation event
        if abs(result) >= self.capital * 0.9:  # Lost >90% of capital
            self.liquidation_events += 1
            print(f"{RED_BG}{WHITE}⚠️ ACCOUNT LIQUIDATION #{self.liquidation_events}! Lost ${abs(result):.2f}{RESET}")
        elif abs(result) >= self.capital * 0.7:  # Lost >70% of capital
            self.near_liquidations += 1
            print(f"{RED}⚠️ NEAR LIQUIDATION! Lost ${abs(result):.2f}{RESET}")
        
        # Update base metrics
        super().process_trade_result(result, trade_duration)
        
        # Extreme emotional state changes
        if result > 0:
            # After wins, newbies often become euphoric or overconfident
            if random.random() < 0.7:
                self.state.emotional_state = "euphoric"
                self.state.confidence = 1.0  # Maximum confidence after any win
                self.state.risk_appetite += 0.2  # Increase risk appetite significantly
        else:
            # After losses, either panic or revenge trading
            if self.state.consecutive_losses > self.max_consecutive_losses:
                self.max_consecutive_losses = self.state.consecutive_losses
            
            if random.random() < 0.5:
                self.state.emotional_state = "panic"
                self.panic_sells += 1
            else:
                self.state.emotional_state = "revenge"
                
            # But confidence remains unreasonably high despite losses
            self.state.confidence = max(0.4, self.state.confidence - 0.1)
    
    def print_status(self) -> None:
        """Print current trader status with added liquidation metrics."""
        # Call the parent class method to print standard metrics
        super().print_status()
        
        # Add newbie trader specific metrics
        liquidation_risk = self._calculate_overall_liquidation_risk()
        
        print(f"\n{RED}High-Risk Trading Metrics:{RESET}")
        print(f"FOMO Trades: {self.fomo_trades}")
        print(f"Panic Sells: {self.panic_sells}")
        print(f"Liquidation Events: {self.liquidation_events}")
        print(f"Near Liquidations: {self.near_liquidations}")
        print(f"Max Consecutive Losses: {self.max_consecutive_losses}")
        print(f"Current Liquidation Risk: {self._format_liquidation_risk(liquidation_risk)}")
        
        # Portfolio health assessment
        health_score = self._calculate_portfolio_health()
        print(f"Portfolio Health: {self._format_health_score(health_score)}/100")
    
    def _calculate_current_leverage(self) -> int:
        """Calculate current leverage based on emotional state (extremely high)."""
        # Base leverage is already high (50x)
        leverage = self.base_leverage
        
        # Adjust based on emotional state
        if self.state.emotional_state == "euphoric":
            leverage = 100  # Maximum leverage when euphoric
        elif self.state.emotional_state == "fomo":
            leverage = 80   # Very high leverage during FOMO
        elif self.state.emotional_state == "revenge":
            leverage = 75   # High leverage for revenge trades
        elif self.state.emotional_state == "panic":
            leverage = 30   # Lower leverage when panicking
        
        # Newbie traders don't properly adjust leverage based on market conditions
        # Instead they often increase leverage after wins
        if self.state.consecutive_wins > 0:
            leverage = min(100, leverage + self.state.consecutive_wins * 5)
        
        return int(leverage)
    
    def _calculate_liquidation_risk(self, direction: str, entry_price: float, position_size: float, leverage: float) -> float:
        """Calculate risk of liquidation for a specific trade."""
        # Higher leverage = less price movement needed for liquidation
        liquidation_threshold = 1 / leverage
        
        # The closer to liquidation threshold, the higher the risk
        risk_factor = min(0.95, position_size * entry_price * leverage / self.capital)
        
        # Scale to 0-1 probability
        liquidation_probability = risk_factor * 0.8 + (leverage / 100) * 0.2
        
        return min(1.0, liquidation_probability)
    
    def _calculate_overall_liquidation_risk(self) -> float:
        """Calculate overall account liquidation risk based on trading history and behavior."""
        # Start with base risk based on leverage preference
        base_risk = self.base_leverage / 100
        
        # Increase risk based on emotional state
        emotion_factor = {
            "euphoric": 0.2,
            "fomo": 0.25,
            "revenge": 0.3,
            "panic": 0.15,
            "fud": 0.1,
            "neutral": 0.05
        }.get(self.state.emotional_state, 0.1)
        
        # Increase risk based on trading history
        history_factor = (
            (self.liquidation_events * 0.1) +  # Each liquidation increases future risk
            (self.near_liquidations * 0.05) +  # Near liquidations also increase risk
            (min(self.state.consecutive_losses, 5) * 0.05) +  # Recent losing streak
            (self.fomo_trades / max(1, self.state.total_trades) * 0.2)  # FOMO trading rate
        )
        
        # Calculate final risk score
        liquidation_risk = base_risk + emotion_factor + history_factor
        
        return min(1.0, liquidation_risk)
    
    def _calculate_portfolio_health(self) -> int:
        """Calculate a portfolio health score (0-100)."""
        # Start with 100 and deduct for risk factors
        health = 100
        
        # Poor leverage practices
        health -= (self._calculate_current_leverage() - 20) * 0.5  # -0.5 points per leverage unit above 20
        
        # Deduct for liquidation events
        health -= self.liquidation_events * 15
        health -= self.near_liquidations * 5
        
        # Deduct for emotional trading
        health -= self.fomo_trades * 2
        health -= self.panic_sells * 2
        
        # Deduct for consecutive losses
        health -= self.state.consecutive_losses * 3
        
        # Capital loss
        if self.capital < self.initial_capital:
            loss_pct = (self.initial_capital - self.capital) / self.initial_capital
            health -= loss_pct * 50  # Lose up to 50 points for losing all capital
        
        return max(0, int(health))
    
    def _format_liquidation_risk(self, risk: float) -> str:
        """Format liquidation risk with color coding."""
        if risk < 0.3:
            return f"{BLUE}Low ({risk:.2f}){RESET}"
        elif risk < 0.6:
            return f"{YELLOW}Medium ({risk:.2f}){RESET}"
        else:
            return f"{RED}HIGH ({risk:.2f}){RESET}"
    
    def _format_health_score(self, score: int) -> str:
        """Format health score with color coding."""
        if score > 70:
            return f"{GREEN}{score}{RESET}"
        elif score > 40:
            return f"{YELLOW}{score}{RESET}"
        else:
            return f"{RED}{score}{RESET}"