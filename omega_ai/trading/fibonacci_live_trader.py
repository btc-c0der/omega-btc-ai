#!/usr/bin/env python3
"""
OMEGA BTC AI - Fibonacci Live Trader
==================================

This module implements a live trading strategy based on Fibonacci patterns
with dynamic adjustments based on market conditions. It integrates with
the BitGet exchange and includes:

1. Pattern Detection: Identifies Fibonacci patterns in real-time
2. Risk Management: Dynamic position sizing and stop-loss placement
3. Position Management: Manages entries and exits using Fibonacci levels
4. Market Adaptation: Adjusts parameters based on volatility and trend

Features:
- Real-time pattern detection
- Dynamic risk management
- Automated position management
- Market condition integration
"""

import os
import sys
import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone
from dataclasses import dataclass

# Local imports
from omega_ai.trading.market_conditions import MarketConditionAnalyzer, MarketState
from omega_ai.utils.fibonacci import calculate_fibonacci_levels, validate_pattern
from omega_ai.utils.risk import calculate_position_size
from omega_ai.exchange.bitget_client import BitGetClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TradingSignal:
    """Trading signal with Fibonacci levels and risk parameters."""
    pattern_type: str
    entry_price: float
    stop_loss: float
    take_profit: float
    confidence: float
    timeframe: str
    fibonacci_levels: Dict[str, float]
    risk_percent: float
    position_size: float
    timestamp: datetime

class FibonacciLiveTrader:
    """Live trading implementation using Fibonacci patterns."""
    
    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 passphrase: str,
                 symbol: str = "BTCUSDT",
                 timeframe: str = "1h",
                 base_risk_percent: float = 1.0,
                 leverage: int = 1):
        """Initialize the Fibonacci trader."""
        try:
            # Initialize BitGet client
            self.client = BitGetClient(
                api_key=api_key,
                api_secret=api_secret,
                passphrase=passphrase
            )
            
            # Trading parameters
            self.symbol = symbol
            self.timeframe = timeframe
            self.base_risk_percent = base_risk_percent
            self.leverage = leverage
            
            # Initialize market analyzer
            self.market_analyzer = MarketConditionAnalyzer(
                symbol=symbol,
                timeframe=timeframe
            )
            
            # State management
            self.active_positions: Dict[str, Dict] = {}
            self.pattern_points: List[Dict] = []
            self.last_signal: Optional[TradingSignal] = None
            
            logger.info(f"Initialized Fibonacci trader for {symbol}")
            
        except Exception as e:
            logger.error(f"Error initializing Fibonacci trader: {str(e)}")
            raise
    
    async def update_pattern_points(self, price_data: List[Dict]) -> None:
        """Update pattern points with new price data."""
        try:
            # Update market analyzer
            await self.market_analyzer.update_market_conditions(
                price_data[-1]['price']
            )
            
            # Update pattern points
            self.pattern_points.extend(price_data)
            
            # Keep only recent points
            max_points = 100  # Adjust based on pattern requirements
            if len(self.pattern_points) > max_points:
                self.pattern_points = self.pattern_points[-max_points:]
            
            logger.debug(f"Updated pattern points: {len(self.pattern_points)} points")
            
        except Exception as e:
            logger.error(f"Error updating pattern points: {str(e)}")
    
    def detect_patterns(self) -> List[Dict]:
        """Detect Fibonacci patterns in current price data."""
        try:
            if len(self.pattern_points) < 5:  # Minimum points for pattern
                return []
            
            patterns = []
            prices = [p['price'] for p in self.pattern_points]
            
            # Get market adjustments
            market_adjustments = self.market_analyzer.get_market_adjustments(
                self.base_risk_percent
            )
            
            # Detect patterns with adjusted parameters
            for i in range(len(prices) - 4):
                pattern = validate_pattern(
                    prices[i:i+5],
                    tolerance=0.1 * market_adjustments['fibonacci_adjustments']['extension_multiplier']
                )
                
                if pattern:
                    patterns.append({
                        'type': pattern['type'],
                        'points': pattern['points'],
                        'confidence': pattern['confidence'],
                        'timestamp': self.pattern_points[i+4]['timestamp']
                    })
            
            logger.debug(f"Detected {len(patterns)} patterns")
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting patterns: {str(e)}")
            return []
    
    def generate_trading_signal(self, pattern: Dict) -> Optional[TradingSignal]:
        """Generate trading signal from detected pattern."""
        try:
            # Get market adjustments
            market_adjustments = self.market_analyzer.get_market_adjustments(
                self.base_risk_percent
            )
            
            # Calculate Fibonacci levels
            fib_levels = calculate_fibonacci_levels(
                pattern['points'],
                pattern['type'],
                market_adjustments['fibonacci_adjustments']
            )
            
            # Determine entry, stop loss, and take profit
            entry_price = fib_levels['0.618']  # Common entry level
            stop_loss = fib_levels['0.786']    # Stop below 78.6% retracement
            take_profit = fib_levels['1.618']  # Take profit at 161.8% extension
            
            # Calculate position size
            risk_params = market_adjustments['risk_adjustments']
            position_size = calculate_position_size(
                entry_price=entry_price,
                stop_loss=stop_loss,
                risk_percent=risk_params['risk_percent'],
                account_size=self.get_account_size(),
                leverage=self.leverage
            )
            
            signal = TradingSignal(
                pattern_type=pattern['type'],
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                confidence=pattern['confidence'],
                timeframe=self.timeframe,
                fibonacci_levels=fib_levels,
                risk_percent=risk_params['risk_percent'],
                position_size=position_size,
                timestamp=datetime.now(timezone.utc)
            )
            
            logger.info(f"Generated trading signal: {signal}")
            return signal
            
        except Exception as e:
            logger.error(f"Error generating trading signal: {str(e)}")
            return None
    
    async def execute_trade(self, signal: TradingSignal) -> bool:
        """Execute trade based on trading signal."""
        try:
            # Validate signal
            if not self.validate_signal(signal):
                logger.warning("Invalid trading signal")
                return False
            
            # Place entry order
            entry_order = await self.client.create_order(
                symbol=self.symbol,
                side="buy" if signal.pattern_type.endswith("bullish") else "sell",
                order_type="limit",
                price=signal.entry_price,
                quantity=signal.position_size,
                time_in_force="GTC"
            )
            
            if not entry_order:
                logger.error("Failed to place entry order")
                return False
            
            # Place stop loss
            stop_order = await self.client.create_order(
                symbol=self.symbol,
                side="sell" if signal.pattern_type.endswith("bullish") else "buy",
                order_type="stop_market",
                stop_price=signal.stop_loss,
                quantity=signal.position_size,
                time_in_force="GTC"
            )
            
            if not stop_order:
                # Cancel entry if stop loss fails
                await self.client.cancel_order(
                    symbol=self.symbol,
                    order_id=entry_order['orderId']
                )
                logger.error("Failed to place stop loss order")
                return False
            
            # Place take profit
            take_profit_order = await self.client.create_order(
                symbol=self.symbol,
                side="sell" if signal.pattern_type.endswith("bullish") else "buy",
                order_type="limit",
                price=signal.take_profit,
                quantity=signal.position_size,
                time_in_force="GTC"
            )
            
            if not take_profit_order:
                # Cancel other orders if take profit fails
                await self.client.cancel_order(
                    symbol=self.symbol,
                    order_id=entry_order['orderId']
                )
                await self.client.cancel_order(
                    symbol=self.symbol,
                    order_id=stop_order['orderId']
                )
                logger.error("Failed to place take profit order")
                return False
            
            # Store position details
            position_id = f"{self.symbol}_{int(signal.timestamp.timestamp())}"
            self.active_positions[position_id] = {
                'signal': signal,
                'entry_order': entry_order,
                'stop_order': stop_order,
                'take_profit_order': take_profit_order,
                'status': 'pending'
            }
            
            self.last_signal = signal
            logger.info(f"Successfully placed orders for position {position_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing trade: {str(e)}")
            return False
    
    def validate_signal(self, signal: TradingSignal) -> bool:
        """Validate trading signal before execution."""
        try:
            # Basic validation
            if not all([signal.entry_price, signal.stop_loss, signal.take_profit]):
                return False
            
            # Validate price levels
            if signal.pattern_type.endswith("bullish"):
                if not (signal.entry_price > signal.stop_loss and 
                        signal.take_profit > signal.entry_price):
                    return False
            else:
                if not (signal.entry_price < signal.stop_loss and 
                        signal.take_profit < signal.entry_price):
                    return False
            
            # Validate risk parameters
            max_risk_percent = 2.0  # Maximum risk per trade
            if signal.risk_percent > max_risk_percent:
                return False
            
            # Validate position size
            min_position_size = 0.001  # Minimum position size
            if signal.position_size < min_position_size:
                return False
            
            # Validate signal age
            max_age_seconds = 300  # 5 minutes
            age = (datetime.now(timezone.utc) - signal.timestamp).total_seconds()
            if age > max_age_seconds:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating signal: {str(e)}")
            return False
    
    async def manage_positions(self) -> None:
        """Manage open positions and update orders."""
        try:
            for position_id, position in list(self.active_positions.items()):
                # Get position status
                entry_status = await self.client.get_order_status(
                    symbol=self.symbol,
                    order_id=position['entry_order']['orderId']
                )
                
                if entry_status == 'filled':
                    # Update position status
                    if position['status'] == 'pending':
                        position['status'] = 'active'
                        logger.info(f"Position {position_id} activated")
                    
                    # Check if take profit or stop loss hit
                    tp_status = await self.client.get_order_status(
                        symbol=self.symbol,
                        order_id=position['take_profit_order']['orderId']
                    )
                    
                    sl_status = await self.client.get_order_status(
                        symbol=self.symbol,
                        order_id=position['stop_order']['orderId']
                    )
                    
                    if tp_status == 'filled' or sl_status == 'filled':
                        # Position closed
                        del self.active_positions[position_id]
                        logger.info(f"Position {position_id} closed")
                        continue
                    
                    # Update trailing stop if needed
                    await self.update_trailing_stop(position_id, position)
                
                elif entry_status == 'canceled':
                    # Cancel other orders
                    await self.client.cancel_order(
                        symbol=self.symbol,
                        order_id=position['stop_order']['orderId']
                    )
                    await self.client.cancel_order(
                        symbol=self.symbol,
                        order_id=position['take_profit_order']['orderId']
                    )
                    del self.active_positions[position_id]
                    logger.info(f"Position {position_id} cancelled")
            
        except Exception as e:
            logger.error(f"Error managing positions: {str(e)}")
    
    async def update_trailing_stop(self, position_id: str, position: Dict) -> None:
        """Update trailing stop loss based on price movement."""
        try:
            signal = position['signal']
            current_price = float(await self.client.get_current_price(self.symbol))
            
            # Calculate new stop loss level
            if signal.pattern_type.endswith("bullish"):
                if current_price > signal.entry_price:
                    # Move stop loss to break even after 1:1 R:R
                    risk = signal.entry_price - signal.stop_loss
                    if current_price >= signal.entry_price + risk:
                        new_stop = signal.entry_price
                    else:
                        return
                else:
                    return
            else:
                if current_price < signal.entry_price:
                    # Move stop loss to break even after 1:1 R:R
                    risk = signal.stop_loss - signal.entry_price
                    if current_price <= signal.entry_price - risk:
                        new_stop = signal.entry_price
                    else:
                        return
                else:
                    return
            
            # Update stop loss order
            old_stop = position['stop_order']
            if float(old_stop['stopPrice']) != new_stop:
                # Cancel old stop loss
                await self.client.cancel_order(
                    symbol=self.symbol,
                    order_id=old_stop['orderId']
                )
                
                # Place new stop loss
                new_stop_order = await self.client.create_order(
                    symbol=self.symbol,
                    side="sell" if signal.pattern_type.endswith("bullish") else "buy",
                    order_type="stop_market",
                    stop_price=new_stop,
                    quantity=signal.position_size,
                    time_in_force="GTC"
                )
                
                if new_stop_order:
                    position['stop_order'] = new_stop_order
                    logger.info(f"Updated trailing stop for position {position_id}")
            
        except Exception as e:
            logger.error(f"Error updating trailing stop: {str(e)}")
    
    def get_account_size(self) -> float:
        """Get current account size for position sizing."""
        try:
            # Get account balance
            balance = self.client.get_account_balance()
            return float(balance['total'])
            
        except Exception as e:
            logger.error(f"Error getting account size: {str(e)}")
            return 0.0
    
    async def run(self) -> None:
        """Main trading loop."""
        try:
            logger.info("Starting Fibonacci trader...")
            
            while True:
                # Get current price data
                price_data = await self.client.get_klines(
                    symbol=self.symbol,
                    interval=self.timeframe,
                    limit=100
                )
                
                # Update patterns
                await self.update_pattern_points(price_data)
                
                # Detect patterns
                patterns = self.detect_patterns()
                
                # Generate and execute signals
                for pattern in patterns:
                    signal = self.generate_trading_signal(pattern)
                    if signal and self.validate_signal(signal):
                        await self.execute_trade(signal)
                
                # Manage positions
                await self.manage_positions()
                
                # Sleep
                await asyncio.sleep(60)  # 1-minute update interval
                
        except Exception as e:
            logger.error(f"Error in trading loop: {str(e)}")
            raise
    
    async def stop(self) -> None:
        """Stop the trader and clean up."""
        try:
            logger.info("Stopping Fibonacci trader...")
            
            # Cancel all active orders
            for position in self.active_positions.values():
                for order_type in ['entry_order', 'stop_order', 'take_profit_order']:
                    if order := position.get(order_type):
                        await self.client.cancel_order(
                            symbol=self.symbol,
                            order_id=order['orderId']
                        )
            
            self.active_positions.clear()
            logger.info("Fibonacci trader stopped")
        except Exception as e:
            logger.error(f"Error stopping trader: {str(e)}")
            raise 