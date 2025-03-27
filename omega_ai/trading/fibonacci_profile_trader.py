#!/usr/bin/env python3
"""
OMEGA BTC AI - Fibonacci Profile Trader
=======================================

This module implements a Fibonacci trading strategy that adapts its behavior
based on trader profile personality traits. It integrates with the BitGet
exchange and incorporates market condition analysis for optimal entry/exit points.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from omega_ai.exchange.bitget_client import BitGetClient
from omega_ai.utils.fibonacci import validate_pattern, calculate_fibonacci_levels
from omega_ai.utils.risk import calculate_position_size, calculate_risk_ratio
from omega_ai.trading.market_condition_analyzer import MarketConditionAnalyzer
from omega_ai.trading.profiles.strategic_trader import StrategicTrader
from omega_ai.trading.profiles.aggressive_trader import AggressiveTrader
from omega_ai.trading.profiles.scalper_trader import ScalperTrader
from omega_ai.trading.profiles.newbie_trader import NewbieTrader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TradingSignal:
    """Trading signal with entry, stop loss, and take profit levels."""
    symbol: str
    side: str  # "long" or "short"
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_percent: float
    confidence: float
    pattern_type: str
    leverage: float = 1.0
    position_size: float = 0.0
    take_profit_levels: List[Dict] = None

class FibonacciProfileTrader:
    """
    Fibonacci trading strategy that adapts to different trader profiles.
    
    This class implements Fibonacci pattern detection and trading logic with
    behavior that changes based on the selected trader profile. It connects
    to BitGet exchange and manages positions automatically.
    """
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        passphrase: str,
        symbol: str = "BTCUSDT",
        profile_type: str = "strategic",
        initial_capital: float = 10000.0,
        leverage: float = 5.0,
        base_risk_percent: float = 1.0,
        enable_trailing_stop: bool = True
    ):
        """
        Initialize the Fibonacci Profile Trader.
        
        Args:
            api_key: BitGet API key
            api_secret: BitGet API secret
            passphrase: BitGet API passphrase
            symbol: Trading pair symbol (default: BTCUSDT)
            profile_type: Type of trader profile (default: strategic)
            initial_capital: Initial capital amount (default: 10000.0)
            leverage: Trading leverage (default: 5.0)
            base_risk_percent: Base risk per trade as percentage (default: 1.0)
            enable_trailing_stop: Whether to enable trailing stop loss (default: True)
        """
        # Trading parameters
        self.symbol = symbol
        self.profile_type = profile_type.lower()
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.leverage = leverage
        self.base_risk_percent = base_risk_percent
        self.enable_trailing_stop = enable_trailing_stop
        
        # Exchange client
        self.client = BitGetClient(api_key, api_secret, passphrase)
        
        # Trading state
        self.running = False
        self.pattern_points = []
        self.active_signals = []
        self.positions = {}
        self.open_orders = {}
        self.last_price = 0.0
        
        # Market analyzer
        self.market_analyzer = None
        
        # Initialize profile
        self._init_profile()
    
    def _init_profile(self):
        """Initialize the trader profile based on profile_type."""
        if self.profile_type == "strategic":
            self.profile = StrategicTrader(self.initial_capital)
        elif self.profile_type == "aggressive":
            self.profile = AggressiveTrader(self.initial_capital)
        elif self.profile_type == "scalper":
            self.profile = ScalperTrader(self.initial_capital)
        elif self.profile_type == "newbie":
            self.profile = NewbieTrader(self.initial_capital)
        else:
            # Default to strategic
            logger.warning(f"Unknown profile type: {self.profile_type}, defaulting to strategic")
            self.profile = StrategicTrader(self.initial_capital)
            
        logger.info(f"Initialized {self.profile.name} profile for Fibonacci trading")
    
    async def initialize(self):
        """Initialize the trader and connect to exchange."""
        logger.info(f"Initializing Fibonacci trader for {self.symbol} with {self.profile_type} profile")
        
        # Initialize BitGet client
        await self.client.initialize()
        
        # Initialize market analyzer
        self.market_analyzer = MarketConditionAnalyzer(self.symbol)
        await self.market_analyzer.initialize()
        
        # Get account balance
        account_info = await self.client.get_account_balance()
        if account_info:
            # Update current capital
            for asset in account_info.get("assets", []):
                if asset.get("asset") == "USDT":
                    self.current_capital = float(asset.get("availableBalance", self.initial_capital))
                    break
        
        logger.info(f"Current capital: {self.current_capital} USDT")
        
        # Check for existing positions
        await self._check_existing_positions()
    
    async def _check_existing_positions(self):
        """Check for existing positions on startup and handle them."""
        try:
            positions = await self.client.get_positions(self.symbol)
            if not positions:
                logger.info(f"No existing positions found for {self.symbol}")
                return
            
            for position in positions:
                position_size = float(position.get('size', 0))
                if position_size <= 0:
                    continue
                
                position_side = position.get('side', '')
                entry_price = float(position.get('entryPrice', 0))
                leverage = float(position.get('leverage', self.leverage))
                
                logger.warning(
                    f"Found existing {position_side} position of {position_size} {self.symbol} "
                    f"at price {entry_price} with {leverage}x leverage"
                )
                
                # Save position to our tracking
                self.positions[self.symbol] = position
                
                # If the leverage doesn't match our target leverage, try to adjust it
                if abs(leverage - self.leverage) > 0.1:
                    try:
                        logger.info(f"Adjusting leverage from {leverage}x to {self.leverage}x")
                        await self.client.set_leverage(self.symbol, self.leverage)
                    except Exception as e:
                        logger.error(f"Failed to adjust leverage: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error checking existing positions: {str(e)}")
    
    async def run(self):
        """Start the trading loop."""
        if self.running:
            logger.warning("Trader is already running")
            return
        
        self.running = True
        logger.info(f"Starting Fibonacci trader with {self.profile.name} profile")
        
        try:
            while self.running:
                await self._trading_cycle()
                await asyncio.sleep(10)  # Check every 10 seconds
        
        except Exception as e:
            logger.error(f"Error in trading loop: {str(e)}")
            self.running = False
    
    async def stop(self):
        """Stop the trading loop."""
        self.running = False
        logger.info("Stopping Fibonacci trader")
    
    async def _trading_cycle(self):
        """Execute one complete trading cycle."""
        try:
            # Update market data
            ticker = await self.client.get_market_ticker(self.symbol)
            if not ticker:
                logger.warning("Failed to get market data")
                return
            
            # Update last price
            self.last_price = float(ticker.get('last', 0))
            
            # Update market analyzer
            await self.market_analyzer.update(self.last_price)
            
            # Update pattern points
            await self._update_pattern_points()
            
            # Check for new patterns
            patterns = await self._detect_patterns()
            
            # Generate signals
            for pattern in patterns:
                signal = await self._generate_signal(pattern)
                if signal and self._validate_signal(signal):
                    # Only add new signals that don't conflict with existing positions
                    if await self._can_add_signal(signal):
                        self.active_signals.append(signal)
                        logger.info(f"New trading signal: {signal.side} {signal.symbol} at {signal.entry_price}")
            
            # Execute signals
            for signal in self.active_signals[:]:  # Copy list for iteration
                await self._execute_signal(signal)
            
            # Manage positions
            await self._manage_positions()
        
        except Exception as e:
            logger.error(f"Error in trading cycle: {str(e)}")
    
    async def _update_pattern_points(self):
        """Update pattern points with new price data."""
        # Add latest price if it's significantly different
        if self.pattern_points and abs(self.last_price - self.pattern_points[-1]) / self.pattern_points[-1] < 0.0005:
            # Change is less than 0.05%, don't add
            return
        
        self.pattern_points.append(self.last_price)
        
        # Keep a reasonable history
        if len(self.pattern_points) > 100:
            self.pattern_points = self.pattern_points[-100:]
    
    async def _detect_patterns(self) -> List[Dict]:
        """Detect Fibonacci patterns in the price data."""
        if len(self.pattern_points) < 5:
            return []
        
        patterns = []
        
        # Look for patterns in the last N points
        for i in range(5, min(20, len(self.pattern_points)) + 1):
            points_to_check = self.pattern_points[-i:]
            
            # Validate if these points form a pattern
            pattern = validate_pattern(points_to_check)
            if pattern and pattern.get('is_valid', False):
                patterns.append(pattern)
        
        return patterns
    
    async def _generate_signal(self, pattern: Dict) -> Optional[TradingSignal]:
        """Generate a trading signal from a detected pattern."""
        try:
            pattern_type = pattern.get('pattern_type', 'unknown')
            pattern_points = pattern.get('points', [])
            
            if not pattern_points or len(pattern_points) < 3:
                return None
            
            # Calculate Fibonacci levels
            fib_levels = calculate_fibonacci_levels(
                pattern_points, 
                pattern.get('pattern_type', 'retracement')
            )
            
            # Determine trade direction
            side = "long" if 'bullish' in pattern_type.lower() else "short"
            
            # Use profile to determine entry, stop loss, and take profit levels
            entry_price = self.profile.determine_entry_level(fib_levels, pattern_type)
            stop_loss = self.profile.determine_stop_loss(fib_levels, pattern_type, entry_price)
            take_profit = self.profile.determine_take_profit(fib_levels, pattern_type, entry_price)
            
            # Calculate risk and position size
            risk_levels = self.profile.calculate_risk_levels(
                entry_price, 
                self.base_risk_percent, 
                self.current_capital
            )
            
            # Apply leverage
            risk_ratio = calculate_risk_ratio(entry_price, stop_loss, take_profit)
            
            # Calculate take profit levels (multiple targets)
            tp_levels = self.profile.set_take_profit(side, entry_price, stop_loss)
            
            # Get leverage from profile with current market conditions
            market_context = await self.market_analyzer.get_market_context()
            leverage = self.profile._calculate_current_leverage(market_context)
            
            return TradingSignal(
                symbol=self.symbol,
                side=side,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                risk_percent=self.base_risk_percent,
                confidence=pattern.get('confidence', 0.5),
                pattern_type=pattern_type,
                leverage=leverage,
                position_size=risk_levels.get('position_size', 0.0),
                take_profit_levels=tp_levels
            )
        
        except Exception as e:
            logger.error(f"Error generating signal: {str(e)}")
            return None
    
    def _validate_signal(self, signal: TradingSignal) -> bool:
        """Validate a trading signal based on profile criteria."""
        try:
            # Use profile-specific validation
            return self.profile.validate_trade_signal(signal)
        except Exception as e:
            logger.error(f"Error validating signal: {str(e)}")
            return False
    
    async def _can_add_signal(self, signal: TradingSignal) -> bool:
        """Check if a new signal can be added based on existing positions."""
        # Check for existing positions
        position = self.positions.get(signal.symbol)
        if position:
            position_side = position.get('side', '')
            
            # If we have a position in the opposite direction, don't add a new signal
            if (position_side == 'long' and signal.side == 'short') or \
               (position_side == 'short' and signal.side == 'long'):
                logger.info(
                    f"Skipping {signal.side} signal due to existing {position_side} position. "
                    f"Close existing position first or wait for it to close."
                )
                return False
            
            # If we already have a position in the same direction
            if position_side == signal.side:
                # Don't add another signal if it's too close to our entry
                entry_price = float(position.get('entryPrice', 0))
                price_diff = abs(entry_price - signal.entry_price) / entry_price
                
                if price_diff < 0.02:  # Within 2% of existing entry
                    logger.info(
                        f"Skipping {signal.side} signal as it's too close to existing position entry at {entry_price}"
                    )
                    return False
        
        # Check for similar active signals
        for existing_signal in self.active_signals:
            if existing_signal.symbol == signal.symbol and existing_signal.side == signal.side:
                # Similar signal already exists
                price_diff = abs(existing_signal.entry_price - signal.entry_price) / existing_signal.entry_price
                
                if price_diff < 0.02:  # Within 2% of existing signal
                    logger.info(f"Similar {signal.side} signal already exists")
                    return False
        
        return True
    
    async def _execute_signal(self, signal: TradingSignal):
        """Execute a trading signal if conditions are right."""
        try:
            # Check if price is near entry level
            price_diff = abs(self.last_price - signal.entry_price) / signal.entry_price
            
            # Only execute if price is within 0.5% of entry price
            if price_diff > 0.005:
                return
            
            # Remove from active signals
            if signal in self.active_signals:
                self.active_signals.remove(signal)
            
            # Set leverage
            await self.client.set_leverage(signal.symbol, signal.leverage)
            
            # Calculate final position size
            position_size = signal.position_size * signal.leverage
            
            # Create the order
            order_result = await self.client.create_order(
                symbol=signal.symbol,
                side="buy" if signal.side == "long" else "sell",
                order_type="market",
                quantity=position_size,
                leverage=signal.leverage
            )
            
            if not order_result:
                logger.error(f"Failed to create order for {signal.side} {signal.symbol}")
                return
            
            order_id = order_result.get('orderId', '')
            logger.info(f"Created {signal.side} order {order_id} for {position_size} {signal.symbol}")
            
            # Set stop loss and take profit orders
            await self._set_risk_management_orders(signal)
            
            # Add to positions tracking
            await self._update_positions()
        
        except Exception as e:
            logger.error(f"Error executing signal: {str(e)}")
    
    async def _set_risk_management_orders(self, signal: TradingSignal):
        """Set stop loss and take profit orders for a position."""
        try:
            # Set stop loss order
            sl_result = await self.client.create_order(
                symbol=signal.symbol,
                side="sell" if signal.side == "long" else "buy",
                order_type="stop_market",
                quantity=signal.position_size,
                stop_price=signal.stop_loss,
                reduce_only=True
            )
            
            if not sl_result:
                logger.error(f"Failed to set stop loss for {signal.side} {signal.symbol}")
            else:
                logger.info(f"Set stop loss at {signal.stop_loss} for {signal.side} {signal.symbol}")
            
            # Set take profit orders (multiple levels)
            for i, tp_level in enumerate(signal.take_profit_levels or []):
                tp_price = tp_level.get('price', 0)
                tp_quantity = signal.position_size * tp_level.get('percentage', 1.0)
                
                tp_result = await self.client.create_order(
                    symbol=signal.symbol,
                    side="sell" if signal.side == "long" else "buy",
                    order_type="limit",
                    quantity=tp_quantity,
                    price=tp_price,
                    reduce_only=True
                )
                
                if not tp_result:
                    logger.error(f"Failed to set take profit {i+1} at {tp_price} for {signal.side} {signal.symbol}")
                else:
                    logger.info(
                        f"Set take profit {i+1} at {tp_price} for {tp_quantity} units of {signal.side} {signal.symbol}"
                    )
        
        except Exception as e:
            logger.error(f"Error setting risk management orders: {str(e)}")
    
    async def _update_positions(self):
        """Update the positions dictionary with current positions."""
        try:
            positions = await self.client.get_positions(self.symbol)
            
            # Reset positions dictionary
            self.positions = {}
            
            if not positions:
                return
            
            for position in positions:
                symbol = position.get('symbol', '')
                size = float(position.get('size', 0))
                
                if size > 0:
                    self.positions[symbol] = position
                    logger.info(
                        f"Updated position tracking: {position.get('side', '')} {size} {symbol} "
                        f"at {position.get('entryPrice', 0)}"
                    )
        
        except Exception as e:
            logger.error(f"Error updating positions: {str(e)}")
    
    async def _update_orders(self):
        """Update the open orders dictionary."""
        try:
            orders = await self.client.get_open_orders(self.symbol)
            
            # Reset orders dictionary
            self.open_orders = {}
            
            if not orders:
                return
            
            for order in orders:
                order_id = order.get('orderId', '')
                self.open_orders[order_id] = order
        
        except Exception as e:
            logger.error(f"Error updating orders: {str(e)}")
    
    async def _manage_positions(self):
        """Manage existing positions (trailing stops, etc.)"""
        try:
            # First update positions
            await self._update_positions()
            
            # If no positions, nothing to do
            if not self.positions:
                return
            
            # Update orders
            await self._update_orders()
            
            # Check each position
            for symbol, position in self.positions.items():
                position_size = float(position.get('size', 0))
                if position_size <= 0:
                    continue
                
                position_side = position.get('side', '')
                entry_price = float(position.get('entryPrice', 0))
                unrealized_pnl = float(position.get('unrealizedPnl', 0))
                
                # Check if we need to update the trailing stop
                if self.enable_trailing_stop:
                    await self._update_trailing_stop(symbol, position, self.last_price)
        
        except Exception as e:
            logger.error(f"Error managing positions: {str(e)}")
    
    async def _update_trailing_stop(self, symbol: str, position: Dict, current_price: float):
        """Update trailing stop for a position."""
        try:
            # Use profile to calculate new trailing stop
            new_stop = self.profile.calculate_trailing_stop(position, current_price)
            
            if new_stop <= 0:
                return  # No trailing stop needed yet
            
            # Find existing stop loss orders
            sl_orders = []
            for order_id, order in self.open_orders.items():
                if order.get('symbol') != symbol:
                    continue
                
                if order.get('type', '').lower() in ['stop', 'stop_market']:
                    sl_orders.append(order)
            
            # If no stop loss orders found, create one
            if not sl_orders:
                side = "sell" if position.get('side', '') == "long" else "buy"
                
                sl_result = await self.client.create_order(
                    symbol=symbol,
                    side=side,
                    order_type="stop_market",
                    quantity=float(position.get('size', 0)),
                    stop_price=new_stop,
                    reduce_only=True
                )
                
                if sl_result:
                    logger.info(f"Created new trailing stop at {new_stop} for {position.get('side', '')} {symbol}")
                return
            
            # Check existing stop orders
            for sl_order in sl_orders:
                old_stop = float(sl_order.get('stopPrice', 0))
                
                # Only update if the new stop is better
                if position.get('side', '') == "long" and new_stop > old_stop:
                    # Cancel old order
                    await self.client.cancel_order(symbol, sl_order.get('orderId', ''))
                    
                    # Create new order
                    sl_result = await self.client.create_order(
                        symbol=symbol,
                        side="sell",
                        order_type="stop_market",
                        quantity=float(position.get('size', 0)),
                        stop_price=new_stop,
                        reduce_only=True
                    )
                    
                    if sl_result:
                        logger.info(
                            f"Updated trailing stop from {old_stop} to {new_stop} for long {symbol}"
                        )
                
                elif position.get('side', '') == "short" and new_stop < old_stop:
                    # Cancel old order
                    await self.client.cancel_order(symbol, sl_order.get('orderId', ''))
                    
                    # Create new order
                    sl_result = await self.client.create_order(
                        symbol=symbol,
                        side="buy",
                        order_type="stop_market",
                        quantity=float(position.get('size', 0)),
                        stop_price=new_stop,
                        reduce_only=True
                    )
                    
                    if sl_result:
                        logger.info(
                            f"Updated trailing stop from {old_stop} to {new_stop} for short {symbol}"
                        )
        
        except Exception as e:
            logger.error(f"Error updating trailing stop: {str(e)}")
    
    async def close_position(self, symbol: str = None):
        """
        Close a specific position or all positions.
        
        Args:
            symbol: Symbol to close position for, or None for all positions
        """
        try:
            if symbol:
                # Close specific position
                position = self.positions.get(symbol)
                if not position:
                    logger.warning(f"No position found for {symbol}")
                    return
                
                position_side = position.get('side', '')
                position_size = float(position.get('size', 0))
                
                if position_size <= 0:
                    logger.warning(f"Position size for {symbol} is 0")
                    return
                
                # Create close order
                close_result = await self.client.create_order(
                    symbol=symbol,
                    side="sell" if position_side == "long" else "buy",
                    order_type="market",
                    quantity=position_size,
                    reduce_only=True
                )
                
                if close_result:
                    logger.info(f"Closed {position_side} position for {position_size} {symbol}")
                else:
                    logger.error(f"Failed to close {position_side} position for {symbol}")
            
            else:
                # Close all positions
                for pos_symbol, position in self.positions.items():
                    position_side = position.get('side', '')
                    position_size = float(position.get('size', 0))
                    
                    if position_size <= 0:
                        continue
                    
                    # Create close order
                    close_result = await self.client.create_order(
                        symbol=pos_symbol,
                        side="sell" if position_side == "long" else "buy",
                        order_type="market",
                        quantity=position_size,
                        reduce_only=True
                    )
                    
                    if close_result:
                        logger.info(f"Closed {position_side} position for {position_size} {pos_symbol}")
                    else:
                        logger.error(f"Failed to close {position_side} position for {pos_symbol}")
        
        except Exception as e:
            logger.error(f"Error closing position: {str(e)}")
    
    async def adjust_position_leverage(self, symbol: str, new_leverage: float):
        """
        Adjust the leverage for an existing position.
        
        Args:
            symbol: Symbol to adjust leverage for
            new_leverage: New leverage value
        """
        try:
            # Check if we have a position
            position = self.positions.get(symbol)
            if not position:
                logger.warning(f"No position found for {symbol}")
                return
            
            current_leverage = float(position.get('leverage', 0))
            
            # If leverage is already correct, do nothing
            if abs(current_leverage - new_leverage) < 0.1:
                logger.info(f"Leverage for {symbol} is already set to {current_leverage}x")
                return
            
            # Set new leverage
            result = await self.client.set_leverage(symbol, new_leverage)
            
            if result:
                logger.info(f"Adjusted leverage for {symbol} from {current_leverage}x to {new_leverage}x")
            else:
                logger.error(f"Failed to adjust leverage for {symbol}")
        
        except Exception as e:
            logger.error(f"Error adjusting position leverage: {str(e)}")
    
    async def handle_existing_position(self, symbol: str, action: str = "keep"):
        """
        Handle an existing position with specified action.
        
        Args:
            symbol: Symbol of the position to handle
            action: Action to take (keep, close, or adjust)
        """
        try:
            position = self.positions.get(symbol)
            if not position:
                logger.warning(f"No position found for {symbol}")
                return
            
            if action == "close":
                # Close the position
                await self.close_position(symbol)
            
            elif action == "adjust":
                # Adjust to our current leverage setting
                await self.adjust_position_leverage(symbol, self.leverage)
            
            elif action == "keep":
                # Keep position but update our tracking
                logger.info(
                    f"Keeping existing {position.get('side', '')} position of {position.get('size', 0)} {symbol} "
                    f"at {position.get('entryPrice', 0)} with {position.get('leverage', 0)}x leverage"
                )
            
            # Update our position tracking
            await self._update_positions()
        
        except Exception as e:
            logger.error(f"Error handling existing position: {str(e)}") 