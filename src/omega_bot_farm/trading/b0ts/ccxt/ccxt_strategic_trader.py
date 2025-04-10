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
Strategic Trader Bot with CCXT Exchange Integration

This module implements a strategic trader that connects to cryptocurrency exchanges
via CCXT for live trading in the containerized bot farm environment.
"""

import logging
import asyncio
import random
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any, Tuple
import datetime
import time

from src.omega_bot_farm.trading.core.trader_base_b0t import TraderProfile
from src.omega_bot_farm.trading.bots.trading_analyser.trading_analyzer_b0t import TradingAnalyzerB0t
from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t
from src.omega_bot_farm.utils.redis_client import RedisClient
from src.omega_bot_farm.utils.cosmic_factor_service import (
    CosmicFactorService, 
    MoonPhase, 
    SchumannFrequency, 
    MarketLiquidity, 
    GlobalSentiment
)

# Try to load environment variables from the root .env file
try:
    # First try loading from the project root
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    env_path = os.path.join(root_dir, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logging.info(f"Loaded environment variables from {env_path}")
    else:
        logging.warning(f"No .env file found at {env_path}")
except Exception as e:
    logging.warning(f"Failed to load environment variables: {e}")

logger = logging.getLogger("ccxt_strategic_trader")

class CCXTStrategicTraderB0t(TraderProfile):
    """
    CCXT-powered strategic trader with exchange connectivity.
    
    This trader combines the strategic trading approach with live exchange
    connectivity through CCXT for real trading operations.
    """
    
    def __init__(self, 
                 initial_capital: float = None, 
                 name: str = "CCXT_Strategic_B0t",
                 redis_client: Optional[RedisClient] = None,
                 exchange_id: str = "bitget",
                 symbol: str = None,
                 max_position_size: float = None,
                 cosmic_config_path: Optional[str] = None):
        """
        Initialize the CCXT strategic trader bot.
        
        Args:
            initial_capital: Starting capital in USD (default from env)
            name: Bot name for identification
            redis_client: Redis client for communication
            exchange_id: CCXT exchange ID (default bitget)
            symbol: Trading symbol (default from env)
            max_position_size: Maximum position size (default from env)
            cosmic_config_path: Path to cosmic factor configuration file
        """
        # Get initial capital from environment if not provided
        if initial_capital is None:
            initial_capital = float(os.environ.get("INITIAL_CAPITAL", 24.0))
            
        super().__init__(initial_capital, name, redis_client)
        
        # Initialize trading analyzer
        self.analyzer = TradingAnalyzerB0t()
        
        # Get symbol from environment if not provided
        self.symbol = symbol or os.environ.get("SYMBOL", "BTCUSDT")
        self.trading_symbol = os.environ.get("TRADING_SYMBOL", "BTCUSDT_UMCBL")
        
        # Get position size from environment if not provided
        position_size_percent = float(os.environ.get("POSITION_SIZE_PERCENT", 1.0))
        self.max_position_size = max_position_size or (self.initial_capital * position_size_percent / 100)
        
        # Get leverage and risk parameters from environment
        self.leverage = int(os.environ.get("MAX_LEVERAGE", 20))
        self.stop_loss_percent = float(os.environ.get("STOP_LOSS_PERCENT", 1.0))
        self.take_profit_multiplier = float(os.environ.get("TAKE_PROFIT_MULTIPLIER", 2.0))
        
        # Initialize exchange client
        self.exchange = ExchangeClientB0t(
            exchange_id=exchange_id,
            symbol=self.symbol
        )
        
        # Trading state variables
        self.active_position = False
        self.position_side = None
        self.position_entry_price = 0.0
        self.position_size = 0.0
        
        # Strategic trader specific attributes
        self.patience_score = 0.8  # High patience (0.0-1.0)
        self.avg_trade_duration = 16.0  # Hours
        self.position_sizing_factor = 0.02  # Conservative position sizing
        self.min_trend_confirmation = 0.65  # Require strong trend confirmation
        self.risk_reward_target = 3.0  # Seek 3:1 reward:risk ratio
        
        # Initialize cosmic factor service
        if cosmic_config_path is None:
            # Try to get default config path
            default_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                "config", 
                "cosmic_factors.yaml"
            )
            if os.path.exists(default_path):
                cosmic_config_path = default_path
                
        self.cosmic_service = CosmicFactorService(config_path=cosmic_config_path)
        logger.info(f"Cosmic Factor Service initialized. Enabled: {self.cosmic_service.is_enabled()}")
        
        logger.info(f"CCXT Strategic Trader Bot '{name}' initialized with ${initial_capital:,.2f}")
        logger.info(f"Trading {self.symbol} with max position size: {self.max_position_size}")
        
    async def initialize(self):
        """Initialize the trader and connect to exchange."""
        try:
            # Initialize exchange connection
            await self.exchange.initialize()
            
            # Set leverage
            await self.exchange.set_leverage(self.symbol, self.leverage)
            
            # Update Redis with initial state
            self._update_redis_state()
            
            logger.info(f"CCXT Strategic Trader successfully initialized for {self.symbol}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize CCXT Strategic Trader: {e}")
            return False
            
    async def shutdown(self):
        """Shut down the trader and close exchange connection."""
        try:
            # Close any open positions
            if self.active_position:
                await self.close_position()
                
            # Close exchange connection
            await self.exchange.close()
            
            logger.info("CCXT Strategic Trader successfully shut down")
            return True
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            return False
            
    async def update_market_data(self) -> Dict[str, Any]:
        """
        Update market data from exchange.
        
        Returns:
            Dict containing market context
        """
        try:
            # Fetch current ticker
            ticker = await self.exchange.fetch_ticker(self.symbol)
            
            # Fetch recent candles
            candles = await self.exchange.fetch_ohlcv(
                symbol=self.symbol,
                timeframe="1h",
                limit=30
            )
            
            # Extract price history from candles
            price_history = [candle[4] for candle in candles]  # Close prices
            
            # Detect market trend
            trend = self.analyzer.analyze_trend(price_history)
            
            # Calculate volatility
            volatility = self.analyzer.calculate_volatility(price_history)
            
            # Detect support/resistance
            support, resistance = self.analyzer.detect_support_resistance(price_history)
            
            # Get current date and time for cosmic factors
            now = datetime.datetime.now()
            
            # Create market context
            market_context = {
                "symbol": self.symbol,
                "price": ticker.get("last", 0.0),
                "bid": ticker.get("bid", 0.0),
                "ask": ticker.get("ask", 0.0),
                "price_history": price_history,
                "trend": trend,
                "recent_volatility": volatility,
                "support": support,
                "resistance": resistance,
                "regime": self.analyzer.analyze_market_regime(price_history),
                "risk_factor": self.analyzer.calculate_risk_factor({
                    "trend": trend,
                    "recent_volatility": volatility,
                    "price": ticker.get("last", 0.0)
                }),
                # Add cosmic conditions
                "moon_phase": MoonPhase.FULL_MOON,  # In production, calculate from date
                "schumann_frequency": SchumannFrequency.BASELINE,  # In production, get from external source
                "market_liquidity": MarketLiquidity.NORMAL,  # In production, calculate from volume
                "global_sentiment": GlobalSentiment.NEUTRAL,  # In production, get from sentiment analysis
                "mercury_retrograde": False,  # In production, calculate from date
                "trader_latitude": float(os.environ.get("TRADER_LATITUDE", 40.0)),
                "trader_longitude": float(os.environ.get("TRADER_LONGITUDE", -74.0)),
                "day_of_week": now.weekday(),  # 0=Monday, 6=Sunday
                "hour_of_day": now.hour
            }
            
            return market_context
            
        except Exception as e:
            logger.error(f"Error updating market data: {e}")
            return {
                "error": str(e),
                "symbol": self.symbol,
                "price": 0.0,
                "trend": "unknown",
                "price_history": []
            }
            
    async def update_position_status(self) -> None:
        """Update current position status from exchange."""
        try:
            positions = await self.exchange.fetch_positions(self.symbol)
            
            # Reset position flags
            self.active_position = False
            self.position_side = None
            self.position_size = 0.0
            
            for position in positions:
                # Skip positions with zero size
                size = float(position.get("contracts", 0))
                if size == 0:
                    continue
                    
                # We have an active position
                self.active_position = True
                self.position_side = position.get("side", "").lower()
                self.position_size = size
                self.position_entry_price = float(position.get("entryPrice", 0.0))
                
                logger.info(
                    f"Active position: {self.position_side} {self.position_size} contracts "
                    f"at {self.position_entry_price:.2f}"
                )
                break
                
        except Exception as e:
            logger.error(f"Error updating position status: {e}")
            
    def _get_current_cosmic_conditions(self, market_context: Dict) -> Dict:
        """Extract cosmic conditions from market context."""
        # Extract conditions from market context if available
        # Or set some defaults based on current market state
        conditions = {
            "moon_phase": market_context.get("moon_phase", MoonPhase.FULL_MOON),
            "schumann_frequency": market_context.get("schumann_frequency", SchumannFrequency.BASELINE),
            "market_liquidity": market_context.get("market_liquidity", MarketLiquidity.NORMAL),
            "global_sentiment": market_context.get("global_sentiment", GlobalSentiment.NEUTRAL),
            "mercury_retrograde": market_context.get("mercury_retrograde", False),
            "trader_latitude": market_context.get("trader_latitude", 40.0),
            "trader_longitude": market_context.get("trader_longitude", -74.0),
            "day_of_week": market_context.get("day_of_week", 0),
            "hour_of_day": market_context.get("hour_of_day", 12),
        }
        return conditions
            
    async def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """
        Determine if we should enter a trade based on market context.
        
        Returns tuple of (should_enter, direction, reason, leverage)
        """
        # Check if we already have an active position
        if self.active_position:
            return False, "none", "Already have an active position", 1.0
            
        # Extract relevant market data
        price = market_context.get("price", 0.0)
        trend = market_context.get("trend", "sideways")
        regime = market_context.get("regime", "neutral")
        
        # Get price history for analysis
        price_history = market_context.get("price_history", [])
        if not price_history and price > 0:
            price_history = [price]  # Fallback
            
        # Strategic traders require more data and confirmation
        if len(price_history) < 10:
            return False, "none", "Insufficient historical data", 1.0
            
        # Analyze trend strength
        detected_trend = self.analyzer.analyze_trend(price_history)
        
        # Confirm trend with more sophisticated analysis
        trend_match = (trend == detected_trend)
        regime_supports_trend = False
        
        # Check if market regime supports the trend
        if (regime in ["bullish", "bullish_volatile"] and detected_trend == "uptrend") or \
           (regime in ["bearish", "bearish_volatile"] and detected_trend == "downtrend"):
            regime_supports_trend = True
            
        # Strategic traders need multiple confirmations
        confirmation_score = 0.0
        if trend_match:
            confirmation_score += 0.4
        if regime_supports_trend:
            confirmation_score += 0.3
            
        # Additional patterns recognition
        if len(price_history) >= 20:
            # Simple pattern: consecutive higher lows for uptrend
            if detected_trend == "uptrend":
                min_price_recent = min(price_history[-10:])
                min_price_older = min(price_history[-20:-10])
                if min_price_recent > min_price_older:
                    confirmation_score += 0.2
            # Simple pattern: consecutive lower highs for downtrend
            elif detected_trend == "downtrend":
                max_price_recent = max(price_history[-10:])
                max_price_older = max(price_history[-20:-10])
                if max_price_recent < max_price_older:
                    confirmation_score += 0.2
                    
        # Create a decision object that can be modified by cosmic factors
        decision = {
            "entry_threshold": self.min_trend_confirmation,
            "confidence": confirmation_score
        }
        
        # Get cosmic conditions from market context
        cosmic_conditions = self._get_current_cosmic_conditions(market_context)
        
        # Calculate cosmic influences
        cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
        
        # Apply cosmic influences to decision
        modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
        
        # Get modified confirmation score and entry threshold
        confirmation_score = modified_decision.get("confidence", confirmation_score)
        entry_threshold = modified_decision.get("entry_threshold", self.min_trend_confirmation)
        
        # Strategic traders only enter with sufficient confirmation
        if confirmation_score < entry_threshold:
            return False, "none", "Insufficient trend confirmation", 1.0
            
        # Determine direction based on trend
        if detected_trend == "uptrend":
            direction = "long"
            reason = f"Confirmed uptrend with {confirmation_score:.2f} confidence"
        elif detected_trend == "downtrend":
            direction = "short"
            reason = f"Confirmed downtrend with {confirmation_score:.2f} confidence"
        else:
            return False, "none", "No clear trend direction", 1.0
            
        # Set leverage based on confirmation level
        leverage = 1.0 + (confirmation_score - 0.5) * 2
        leverage = min(leverage, self.leverage)
            
        return True, direction, reason, leverage
        
    async def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on risk management and cosmic influences."""
        # Base position size calculation
        max_amount = self.max_position_size / entry_price  # Convert to crypto amount
        
        # Adjust based on market context and risk
        base_amount = max_amount * self.position_sizing_factor
        
        # Create a decision object for cosmic factor service
        decision = {
            "position_size": base_amount,
            "entry_price": entry_price,
            "direction": direction
        }
        
        # Get current cosmic conditions
        # This would normally come from market context
        # but we'll use default values for simplicity
        cosmic_conditions = {
            "moon_phase": MoonPhase.FULL_MOON,
            "schumann_frequency": SchumannFrequency.BASELINE,
            "market_liquidity": MarketLiquidity.NORMAL,
            "global_sentiment": GlobalSentiment.NEUTRAL,
            "mercury_retrograde": False,
            "trader_latitude": 40.0,
            "trader_longitude": -74.0,
            "day_of_week": 0,
            "hour_of_day": 12,
        }
        
        # Calculate cosmic influences
        cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
        
        # Apply cosmic influences to position size
        modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
        
        # Get modified position size
        base_amount = modified_decision.get("position_size", base_amount)
        
        # Ensure we don't exceed maximum position size
        final_amount = min(base_amount, max_amount)
        
        logger.info(f"Position size: {final_amount:.4f} {self.symbol} at {entry_price:.2f}")
        
        return final_amount
        
    async def enter_trade(self, direction: str, amount: float) -> Dict[str, Any]:
        """
        Enter a trade on the exchange.
        
        Args:
            direction: Trade direction ("long" or "short")
            amount: Position size in BTC
            
        Returns:
            Dict containing order result
        """
        try:
            # Convert direction to side
            side = "buy" if direction == "long" else "sell"
            
            # Create market order
            order_result = await self.exchange.create_market_order(
                symbol=self.symbol,
                side=side,
                amount=amount
            )
            
            # Check for errors
            if "error" in order_result:
                logger.error(f"Failed to enter trade: {order_result['error']}")
                return order_result
                
            # Mark position as active
            self.active_position = True
            self.position_side = direction
            self.position_size = amount
            
            # Update position details from exchange
            await self.update_position_status()
            
            # Update trader state in Redis
            self._update_redis_state()
            
            logger.info(f"Entered {direction} position of {amount} BTC")
            return order_result
            
        except Exception as e:
            logger.error(f"Error entering trade: {e}")
            return {"error": str(e)}
            
    async def close_position(self) -> Dict[str, Any]:
        """
        Close the current position.
        
        Returns:
            Dict containing order result
        """
        if not self.active_position:
            logger.warning("No active position to close")
            return {"error": "No active position"}
            
        try:
            result = await self.exchange.close_position(self.symbol)
            
            # Reset position flags
            self.active_position = False
            self.position_side = None
            self.position_size = 0.0
            
            # Update trader state in Redis
            self._update_redis_state()
            
            logger.info(f"Closed position: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return {"error": str(e)}
    
    async def check_exit_conditions(self, market_context: Dict) -> Tuple[bool, str]:
        """
        Check exit conditions for current position.
        
        Returns:
            Tuple of (should_exit, reason)
        """
        # If no active position, nothing to exit
        if not self.active_position:
            return False, "No active position"
            
        # Extract relevant market data
        price = market_context.get("price", 0.0)
        trend = market_context.get("trend", "sideways")
        
        # If price data is missing, don't exit
        if price <= 0:
            return False, "Invalid price data"
            
        # Create a decision object for cosmic factor service
        decision = {
            "exit_impulse": 0.0,
            "exit_threshold": 0.5
        }
        
        # Trend reversal check
        if (self.position_side == "long" and trend == "downtrend") or \
           (self.position_side == "short" and trend == "uptrend"):
            decision["exit_impulse"] += 0.4
            
        # Price movement against position
        pct_change = 0.0
        if self.position_side == "long":
            pct_change = (price - self.position_entry_price) / self.position_entry_price
            if pct_change < -0.01:  # 1% against position
                decision["exit_impulse"] += 0.3
        else:  # short
            pct_change = (self.position_entry_price - price) / self.position_entry_price
            if pct_change < -0.01:  # 1% against position
                decision["exit_impulse"] += 0.3
                
        # Get cosmic conditions from market context
        cosmic_conditions = self._get_current_cosmic_conditions(market_context)
        
        # Calculate cosmic influences
        cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
        
        # Apply cosmic influences to exit decision
        modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
        
        # Get modified exit impulse and threshold
        exit_impulse = modified_decision.get("exit_impulse", decision["exit_impulse"])
        exit_threshold = modified_decision.get("exit_threshold", decision["exit_threshold"])
        
        # Check if exit impulse exceeds threshold
        if exit_impulse > exit_threshold:
            return True, f"Exit signal confirmed: {exit_impulse:.2f} > {exit_threshold:.2f}"
        
        return False, "No exit signal"
            
    async def run_trading_cycle(self):
        """Run one complete trading cycle."""
        try:
            # Update market data
            market_context = await self.update_market_data()
            if "error" in market_context:
                logger.error(f"Failed to update market data: {market_context['error']}")
                return
                
            # Update position status
            await self.update_position_status()
            
            # If we have an active position, check exit conditions
            if self.active_position:
                should_exit, reason = await self.check_exit_conditions(market_context)
                
                if should_exit:
                    logger.info(f"Exit signal: {reason}")
                    result = await self.close_position()
                    
                    if "error" not in result:
                        logger.info(f"Successfully closed position: {reason}")
                    else:
                        logger.error(f"Failed to close position: {result['error']}")
            else:
                # Check entry conditions
                should_enter, direction, reason, leverage = await self.should_enter_trade(market_context)
                
                if should_enter:
                    logger.info(f"Entry signal: {direction}, Reason: {reason}")
                    
                    # Calculate position size
                    amount = await self.determine_position_size(
                        direction, 
                        market_context.get("price", 0.0)
                    )
                    
                    # Enter trade
                    result = await self.enter_trade(direction, amount)
                    
                    if "error" not in result:
                        logger.info(f"Successfully entered {direction} trade with {amount} BTC")
                    else:
                        logger.error(f"Failed to enter trade: {result['error']}")
                else:
                    logger.info(f"No entry signal: {reason}")
                    
            # Update Redis with current state
            self._update_redis_state()
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")
            
    async def start_trading(self, interval_seconds: int = 60):
        """
        Start the trading loop.
        
        Args:
            interval_seconds: Seconds between trading cycles
        """
        logger.info(f"Starting trading loop with {interval_seconds}s interval")
        
        # Initialize exchange connection
        await self.initialize()
        
        try:
            while True:
                await self.run_trading_cycle()
                await asyncio.sleep(interval_seconds)
        except asyncio.CancelledError:
            logger.info("Trading loop cancelled")
            await self.shutdown()
        except Exception as e:
            logger.error(f"Error in trading loop: {e}")
            await self.shutdown()
            
    def get_status_dict(self) -> Dict:
        """
        Get a status dictionary with current bot state.
        
        Returns:
            Dict with current bot state
        """
        status = {
            "name": self.name,
            "exchange": self.exchange.exchange_id,
            "symbol": self.symbol,
            "active_position": self.active_position,
            "position_side": self.position_side,
            "position_size": self.position_size,
            "entry_price": self.position_entry_price,
            "capital": self.capital,
            "profit_loss": self.profit_loss,
            "win_rate": self.win_rate,
            "trade_count": self.trade_count,
            "cosmic_service_enabled": self.cosmic_service.is_enabled(),
            "timestamp": int(time.time())
        }
        
        return status 