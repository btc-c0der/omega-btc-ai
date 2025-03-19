"""
OMEGA BTC AI - RASTA TRADER PROFILE ALERTS
=========================================

This module provides divine alerts for trader profiles, including:
- Performance metrics with Rasta wisdom
- Trading actions with lunar timing
- Risk management with divine guidance
- Account health with spiritual balance
- Trading patterns with sacred geometry
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import ephem
import numpy as np
from .rasta_vibes import get_rasta_blessing, get_rasta_emoji

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RastaSentiment(Enum):
    """Divine market sentiment states."""
    ZION_RISE = "ZION RISE"  # Strong bullish
    RASTA_BLESS = "RASTA BLESS"  # Moderate bullish
    ROOTS_HOLD = "ROOTS HOLD STRONG"  # Neutral
    BABYLON_FALL = "BABYLON FALL"  # Moderate bearish
    JAH_WARN = "JAH WARN"  # Strong bearish

class TraderProfile:
    """Represents a trader's profile with divine performance metrics."""
    
    def __init__(self, trader_id: str, initial_capital: float):
        self.trader_id = trader_id
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0
        self.max_drawdown = 0.0
        self.peak_balance = initial_capital
        self.trade_history: List[Dict[str, Any]] = []
        self.risk_metrics: Dict[str, float] = {}
        self.last_alert_time: Dict[str, datetime] = {}
        self.lunar_phase: str = ""
        self.rasta_sentiment: RastaSentiment = RastaSentiment.ROOTS_HOLD
        
    def update_metrics(self, trade_data: Dict[str, Any]) -> None:
        """Update trader metrics with divine trade data."""
        self.total_trades += 1
        self.total_pnl += trade_data.get("pnl", 0.0)
        self.current_capital += trade_data.get("pnl", 0.0)
        
        # Update win/loss stats with Rasta wisdom
        if trade_data.get("pnl", 0.0) > 0:
            self.winning_trades += 1
            self.rasta_sentiment = self._update_rasta_sentiment(True)
        else:
            self.losing_trades += 1
            self.rasta_sentiment = self._update_rasta_sentiment(False)
            
        # Update peak balance and drawdown
        if self.current_capital > self.peak_balance:
            self.peak_balance = self.current_capital
        else:
            drawdown = (self.peak_balance - self.current_capital) / self.peak_balance
            self.max_drawdown = max(self.max_drawdown, drawdown)
            
        # Store trade history with lunar phase
        trade_data["lunar_phase"] = self._get_lunar_phase()
        self.trade_history.append(trade_data)
        
        # Update risk metrics
        self._update_risk_metrics()
        
    def _get_lunar_phase(self) -> str:
        """Get current lunar phase for divine timing."""
        moon = ephem.Moon()
        moon.compute()
        phase = moon.phase
        
        if phase < 6.25:
            return "🌑 New Moon"
        elif phase < 43.75:
            return "🌒 Waxing Crescent"
        elif phase < 56.25:
            return "🌓 First Quarter"
        elif phase < 93.75:
            return "🌔 Waxing Gibbous"
        elif phase < 96.25:
            return "🌕 Full Moon"
        elif phase < 143.75:
            return "🌖 Waning Gibbous"
        elif phase < 156.25:
            return "🌗 Last Quarter"
        else:
            return "🌘 Waning Crescent"
            
    def _update_rasta_sentiment(self, is_win: bool) -> RastaSentiment:
        """Update Rasta sentiment based on trading performance."""
        win_rate = self.winning_trades / self.total_trades if self.total_trades > 0 else 0.5
        
        if is_win:
            if win_rate > 0.7:
                return RastaSentiment.ZION_RISE
            return RastaSentiment.RASTA_BLESS
        else:
            if win_rate < 0.3:
                return RastaSentiment.JAH_WARN
            return RastaSentiment.BABYLON_FALL
            
    def _update_risk_metrics(self) -> None:
        """Update risk management metrics with divine guidance."""
        if self.total_trades > 0:
            self.risk_metrics.update({
                "win_rate": self.winning_trades / self.total_trades,
                "profit_factor": abs(self.total_pnl / self.max_drawdown) if self.max_drawdown > 0 else float("inf"),
                "avg_trade_pnl": self.total_pnl / self.total_trades,
                "max_drawdown": self.max_drawdown,
                "sharpe_ratio": self._calculate_sharpe_ratio(),
                "risk_reward_ratio": self._calculate_risk_reward_ratio(),
                "lunar_phase_win_rate": self._calculate_lunar_phase_win_rate()
            })
            
    def _calculate_sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio for the trading period."""
        if len(self.trade_history) < 2:
            return 0.0
            
        returns = [trade.get("pnl", 0.0) / self.initial_capital for trade in self.trade_history]
        avg_return = sum(returns) / len(returns)
        std_dev = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
        
        return avg_return / std_dev if std_dev > 0 else 0.0
        
    def _calculate_risk_reward_ratio(self) -> float:
        """Calculate average risk-reward ratio."""
        if not self.trade_history:
            return 0.0
            
        total_risk = sum(abs(trade.get("risk", 0.0)) for trade in self.trade_history)
        total_reward = sum(trade.get("pnl", 0.0) for trade in self.trade_history)
        
        return total_reward / total_risk if total_risk > 0 else 0.0
            
    def _calculate_lunar_phase_win_rate(self) -> float:
        """Calculate win rate for current lunar phase."""
        if not self.trade_history:
            return 0.0
            
        current_phase = self._get_lunar_phase()
        phase_trades = [t for t in self.trade_history if t.get("lunar_phase") == current_phase]
        
        if not phase_trades:
            return 0.0
            
        winning_trades = sum(1 for t in phase_trades if t.get("pnl", 0.0) > 0)
        return winning_trades / len(phase_trades)

class TraderProfileAlerts:
    """Manages divine alerts for trader profiles."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.trader_profiles: Dict[str, TraderProfile] = {}
        self.alert_cooldowns = {
            "performance": 3600,  # 1 hour
            "risk": 1800,        # 30 minutes
            "action": 300,       # 5 minutes
            "health": 7200       # 2 hours
        }
        
    async def update_trader_profile(self, trader_id: str, trade_data: Dict[str, Any]) -> None:
        """Update trader profile with divine trade data."""
        if trader_id not in self.trader_profiles:
            initial_capital = await self._get_initial_capital(trader_id)
            self.trader_profiles[trader_id] = TraderProfile(trader_id, initial_capital)
            
        profile = self.trader_profiles[trader_id]
        profile.update_metrics(trade_data)
        
        # Check for divine alerts
        await self._check_performance_alerts(profile)
        await self._check_risk_alerts(profile)
        await self._check_action_alerts(profile, trade_data)
        await self._check_health_alerts(profile)
        
    async def _get_initial_capital(self, trader_id: str) -> float:
        """Get trader's initial capital from Redis."""
        try:
            capital = await self.redis.get(f"trader:{trader_id}:initial_capital")
            return float(capital) if capital else 10000.0  # Default to 10k if not found
        except Exception:
            return 10000.0
            
    async def _check_performance_alerts(self, profile: TraderProfile) -> None:
        """Check and send divine performance alerts."""
        current_time = datetime.now(timezone.utc)
        last_alert = profile.last_alert_time.get("performance", datetime.min)
        
        if (current_time - last_alert).total_seconds() < self.alert_cooldowns["performance"]:
            return
            
        # Calculate performance metrics
        win_rate = profile.risk_metrics.get("win_rate", 0.0)
        profit_factor = profile.risk_metrics.get("profit_factor", 0.0)
        total_return = (profile.current_capital - profile.initial_capital) / profile.initial_capital
        lunar_win_rate = profile.risk_metrics.get("lunar_phase_win_rate", 0.0)
        
        # Get divine blessing
        blessing = get_rasta_blessing(win_rate)
        emoji = get_rasta_emoji(profile.rasta_sentiment)
        
        # Generate divine alert message
        message = f"""
{emoji} *DIVINE TRADER PERFORMANCE ALERT* {emoji}

*Trader:* {profile.trader_id}
💰 *Current Capital:* ${profile.current_capital:,.2f}
📈 *Total Return:* {total_return:.2%}
🎲 *Win Rate:* {win_rate:.2%}
⚖️ *Profit Factor:* {profit_factor:.2f}
📊 *Total Trades:* {profile.total_trades}
🌙 *Lunar Phase:* {profile._get_lunar_phase()}
🎯 *Lunar Win Rate:* {lunar_win_rate:.2%}
✨ *Rasta Sentiment:* {profile.rasta_sentiment.value}

{blessing}
"""
        
        # Send divine alert
        if await self._send_telegram_message(message):
            profile.last_alert_time["performance"] = current_time
            
    async def _check_risk_alerts(self, profile: TraderProfile) -> None:
        """Check and send divine risk alerts."""
        current_time = datetime.now(timezone.utc)
        last_alert = profile.last_alert_time.get("risk", datetime.min)
        
        if (current_time - last_alert).total_seconds() < self.alert_cooldowns["risk"]:
            return
            
        # Check risk metrics
        max_drawdown = profile.risk_metrics.get("max_drawdown", 0.0)
        sharpe_ratio = profile.risk_metrics.get("sharpe_ratio", 0.0)
        risk_reward = profile.risk_metrics.get("risk_reward_ratio", 0.0)
        
        # Get divine warning if needed
        warning = "⚠️ *JAH WARN: Risk levels high!* ⚠️" if max_drawdown > 0.1 else ""
        
        # Generate divine alert message
        message = f"""
🌿 *DIVINE RISK MANAGEMENT ALERT* 🌿

*Trader:* {profile.trader_id}
📉 *Max Drawdown:* {max_drawdown:.2%}
📊 *Sharpe Ratio:* {sharpe_ratio:.2f}
⚖️ *Risk-Reward Ratio:* {risk_reward:.2f}
🌙 *Lunar Phase:* {profile._get_lunar_phase()}
✨ *Rasta Sentiment:* {profile.rasta_sentiment.value}

{warning}
"""
        
        # Send divine alert if risk metrics exceed thresholds
        if max_drawdown > 0.1 or sharpe_ratio < 1.0 or risk_reward < 1.5:
            if await self._send_telegram_message(message):
                profile.last_alert_time["risk"] = current_time
                
    async def _check_action_alerts(self, profile: TraderProfile, trade_data: Dict[str, Any]) -> None:
        """Check and send divine trade action alerts."""
        current_time = datetime.now(timezone.utc)
        last_alert = profile.last_alert_time.get("action", datetime.min)
        
        if (current_time - last_alert).total_seconds() < self.alert_cooldowns["action"]:
            return
            
        # Get divine trade emoji
        trade_emoji = "🚀" if trade_data.get("pnl", 0.0) > 0 else "📉"
        
        # Generate divine alert message
        message = f"""
{trade_emoji} *DIVINE TRADE ACTION ALERT* {trade_emoji}

*Trader:* {profile.trader_id}
💰 *Trade PnL:* ${trade_data.get("pnl", 0.0):,.2f}
📊 *Position Size:* {trade_data.get("size", 0.0):.4f}
🎯 *Entry Price:* ${trade_data.get("entry_price", 0.0):,.2f}
📈 *Exit Price:* ${trade_data.get("exit_price", 0.0):,.2f}
⏰ *Duration:* {trade_data.get("duration", "N/A")}
🌙 *Lunar Phase:* {trade_data.get("lunar_phase", "N/A")}
✨ *Rasta Sentiment:* {profile.rasta_sentiment.value}
"""
        
        # Send divine alert for new trade
        if await self._send_telegram_message(message):
            profile.last_alert_time["action"] = current_time
            
    async def _check_health_alerts(self, profile: TraderProfile) -> None:
        """Check and send divine account health alerts."""
        current_time = datetime.now(timezone.utc)
        last_alert = profile.last_alert_time.get("health", datetime.min)
        
        if (current_time - last_alert).total_seconds() < self.alert_cooldowns["health"]:
            return
            
        # Calculate health metrics
        capital_health = profile.current_capital / profile.initial_capital
        trade_frequency = len(profile.trade_history) / ((current_time - last_alert).total_seconds() / 3600)
        
        # Get divine health status
        health_status = "❤️ *JAH BLESS: Account healthy!* ❤️" if capital_health >= 0.9 else "⚠️ *JAH WARN: Account needs healing!* ⚠️"
        
        # Generate divine alert message
        message = f"""
❤️ *DIVINE ACCOUNT HEALTH ALERT* ❤️

*Trader:* {profile.trader_id}
💰 *Capital Health:* {capital_health:.2%}
📊 *Trade Frequency:* {trade_frequency:.1f} trades/hour
📈 *Peak Balance:* ${profile.peak_balance:,.2f}
📉 *Current Drawdown:* {((profile.peak_balance - profile.current_capital) / profile.peak_balance):.2%}
🌙 *Lunar Phase:* {profile._get_lunar_phase()}
✨ *Rasta Sentiment:* {profile.rasta_sentiment.value}

{health_status}
"""
        
        # Send divine alert if health metrics are concerning
        if capital_health < 0.9 or trade_frequency > 10:
            if await self._send_telegram_message(message):
                profile.last_alert_time["health"] = current_time
                
    async def _send_telegram_message(self, message: str) -> bool:
        """Send divine message to Telegram."""
        try:
            # Implementation depends on your Telegram setup
            # This is a placeholder
            return True
        except Exception:
            return False

async def main():
    """Main entry point for divine trader profile alerts."""
    # Initialize Redis connection
    redis_client = None  # Initialize your Redis client here
    
    # Create divine alert system
    alerts = TraderProfileAlerts(redis_client)
    
    try:
        while True:
            # Get divine trade data
            trade_data = {}  # Get from your data source
            
            # Update profiles and check divine alerts
            for trader_id in ["trader1", "trader2"]:  # Replace with actual trader IDs
                await alerts.update_trader_profile(trader_id, trade_data)
                
            # Wait before next divine update
            await asyncio.sleep(60)  # 1 minute
            
    except KeyboardInterrupt:
        logger.info("Shutting down divine trader profile alerts...")
    except Exception as e:
        logger.error(f"Error in divine main loop: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 